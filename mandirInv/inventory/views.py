from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.shortcuts import render
from django.utils.datetime_safe import date
from datetime import date
from django.shortcuts import redirect
from authencation.models import Area
from .models import Item, Report, User
from .models import ReportTable as RT
# from mandirInv.mandirInv import UserManager
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateReport, CreateArea, CreateItem
from django.urls import reverse_lazy
from time import time

from itertools import islice
from django.http import HttpResponse, Http404, JsonResponse
from django.core import serializers
import json

CurrentUser = get_user_model()


# TODO: Create two more pages for the user side where can add and then admin can approve the item or delete it
# filter reports area wise and user side

class UserAreas(View, LoginRequiredMixin):
    template_name = "inventory/area_in_charge.html"

    def get(self, request, *args, **kwargs):
        arr = request.user.get_area_incharge()
        return render(request, self.template_name, {
            "areas": arr,
            "show": True,
            "page": 0
        })


class UserSettings(ListView):
    model = User
    context_object_name = "users"
    template_name = "inventory/settings.html"
    extra_context = {"show": True, "page": 4}


class AddArea(CreateView):
    template_name = "inventory/add_area.html"
    model = Area
    form_class = CreateArea
    extra_context = {"show": True, "page": 1}
    success_url = "/add-item/"

    def form_valid(self, form):
        if self.request.method == 'POST':
            name = self.request.POST["name"]
            location = self.request.POST["location"]
            name = name.strip()
            location = location.strip()
            form.instance.name = name
            form.instance.location = location
            return super(AddArea, self).form_valid(form)
        return super(AddArea, self).form_invalid(form)


class UserSettingsDetails(DetailView, UpdateView):
    model = User
    areas = Area.objects.all()
    fields = ["full_name"]
    extra_context = {"show": False, "areas": areas}
    template_name = "inventory/settings-details.html"
    pk_url_kwarg = "id"
    success_url = "/"

    def form_valid(self, form, *args, **kwargs):
        if self.request.method == 'POST':
            loc = self.request.POST["areas"].split(", ")
            # form.clean()
            # form.save()

            area = loc[0]
            mandir = loc[1]
            mandir = mandir.strip()
            area = area.strip()
            qarea = Area.objects.filter(name=area, location=mandir)[0]
            usr = User.objects.filter(email=self.object)[0]
            form.instance.area_incharge.add(qarea)
            form.instance.full_name = usr.full_name
            form.save()

            self.success_url = "/settings/" + str(form.instance.id)
            return super().form_valid(form)
        return super(UserSettingsDetails, self).form_invalid(form)

    def convert_to_area_string(self, json):
        output = ""
        count = 0
        for i in json:
            a = ", ".join(json[i])
            a += " | " + i
            if count != 0:
                output += " / " + a
            else:
                output += a
            count += 1
        return output


class ReportListView(View):
    template_name = "inventory/reportlist.html"
    areas = Area.objects.all()
    extra_context = {"show": True, "page": 3, "areas": areas}

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get(self, request):
        self.extra_context = {"show": True, "page": 3, "areas": self.areas}
        if self.is_ajax(request=request):
            text = request.GET.get("btn_txt")
            area_txt = text.strip()
            area_txt = area_txt.split(", ")
            a = Area.objects.filter(name=area_txt[0], location=area_txt[1])[0]
            print(a)
            data = RT.objects.filter(area=a)
            print(data)
            data_serial = serializers.serialize('json', data)
            # print(data_serial)
            # print(data_dates)
            # data_dates = serializers.serialize('json', data_dates)
            return JsonResponse(data_serial, safe=False)
        return render(request, "inventory/reportlist.html", self.extra_context)


class UserReportDetails(DetailView):
    model = Report
    extra_context = {"show": False}
    template_name = "inventory/user_report_detail.html"


class InventoryView(ListView, LoginRequiredMixin):
    model = Item
    context_object_name = "list"
    template_name = "inventory/inventory.html"
    paginate_by = 10


class InventoryDetail(DetailView, LoginRequiredMixin, UserPassesTestMixin,
                      UpdateView):
    model = Item
    fields = ['description', 'image', 'quantity', 'code', 'area']
    success_url = "/inventory"

    def form_valid(self, form):
        if self.request.user.is_admin:
            return super().form_valid(form)
        return super().form_invalid(form)

    def test_func(self):
        if self.request.user.is_admin:
            return True
        return False


class ReportTable(LoginRequiredMixin, ListView):
    # form_class = CreateReport
    model = Item
    template_name = "inventory/report.html"
    success_url = "/"
    ordering = ['id']
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        try:
            area = Area.objects.get(name=self.kwargs["area"],
                                    location=self.kwargs["location"])
            return Item.objects.filter(area=area)
        except:
            return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ReportTable, self).get_context_data(**kwargs)

        context["area"] = self.kwargs["area"]
        context["location"] = self.kwargs["location"]
        # print(context)

        return context


# [Indivual item page]

def user_report(request, slug):
    tmp_name = "inventory/report_detail.html"
    item = Item.objects.filter(slug=slug)[0]
    form = CreateReport()
    context = {
        "form": form,
        "item": item
    }

    def save_to_table(r):
        # r = Report.objects.latest("uid")
        table = RT.objects.filter(date=date.today(), area=item.area)
        if len(table) <= 0:
            t = RT(date=date.today(), area=item.area)
            t.save()
            t.reports.add(r)
            t.save()
        else:
            t = table[0]
            t.reports.add(r)
            t.save()

    def find_query_index(query, item):
        for i in range(len(query)):
            if query[i] == item:
                return i
        return -1

    def get_next_url():
        item_list = Item.objects.filter(area=item.area).order_by('id')
        index = find_query_index(item_list, item)
        vals = item_list.values()
        n = index + 1
        if n >= len(vals):
            success_url = "/report/" + item.area.name + "/" + item.area.location
        else:
            slugurl = vals[n]["slug"]
            success_url = "/report/" + str(slugurl)
        return success_url

    nurl = get_next_url()
    print(nurl)

    if request.method == 'POST':
        if 'perfect' in request.POST:
            form = CreateReport(request.POST or None)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.item = item
                form.instance.actual = item.quantity
                form.instance.expected = item.quantity
                form.save()
                r = Report.objects.latest("uid")
                save_to_table(r)
                return redirect(nurl)
        elif 'doesnotexist' in request.POST:
            form = CreateReport(request.POST or None)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.item = item
                form.instance.expected = item.quantity
                form.instance.actual = 0
                form.save()
                r = Report.objects.latest("uid")
                save_to_table(r)
                return redirect(nurl)
        elif 'report' in request.POST:
            form = CreateReport(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.item = item
                form.instance.expected = item.quantity
                form.save()
                r = Report.objects.latest("uid")
                save_to_table(r)
                return redirect(nurl)
    return render(request, tmp_name, context)


def report_table(request, slug):
    tmp_name = "inventory/report_table.html"
    a = slug.split("_")
    area = a[:-1]
    date = a[-1]

    res = list(islice(reversed(area), 0, 2))
    res.reverse()

    def remove_same(arr1, arr2):
        out = []
        for i in arr1:
            if i not in arr2:
                out.append(i)
        return out

    name = " ".join(remove_same(area, res))
    location = " ".join(res)
    a = Area.objects.filter(name=name, location=location)[0]
    table = RT.objects.filter(area=a, date=date)[0]
    # print(table.reports.all())
    context = {"table": table}

    if request.method == 'POST':
        table.viewed = True
        table.save()
        return redirect("/reportlist/")
    return render(request, tmp_name, context)


class TestView(View):

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get(self, request):
        if self.is_ajax(request=request):
            text = request.GET.get("button_text")
            data = RT.objects.all()
            if text == "Success":
                a = Area.objects.filter(id=6)[0]
                # data = RT.objects.filter(area=a)
            data_serial = serializers.serialize('json', data)
            # data_serial = json.loads(data_serial)
            # data_dates = {
            #     'dates': []
            # }
            # for data in data_serial:
            #     data_dates['dates'].append(data['fields']['date'])
            # print(data_dates)
            # data_dates = serializers.serialize('json', data_dates)
            return JsonResponse(data_serial, safe=False)
        return render(request, "inventory/test.html")


def add_item(request):
    tmp_name = "inventory/add_item.html"
    form = CreateItem()
    context = {
        "form": form,
        "show": True,
        "page": 2
    }

    if request.method == 'POST':
        form = CreateItem(request.POST or None)
        if form.is_valid():
            item = Item.objects.latest('uid')
            form.instance.uid = int(item.uid) + 1
            if request.user.is_admin:
                form.instance.approved = True
            form.save()

            item = Item.objects.latest('uid')
            actual = -1
            expected = -1
            report = Report(actual=actual, expected=expected, item=item, user=request.user)
            report.save()

            return redirect('/add-item/')

    return render(request, tmp_name, context)
