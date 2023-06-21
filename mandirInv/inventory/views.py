from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.shortcuts import render
from django.utils.datetime_safe import date
from datetime import date
from authencation.models import Area
from .models import Item, Report, User, ReportTable
# from mandirInv.mandirInv import UserManager
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateReport, CreateArea
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404

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


class AddItem(CreateView):
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
            return super(AddItem, self).form_valid(form)
        return super(AddItem, self).form_invalid(form)





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


class ReportListView(ListView):
    model = Report
    context_object_name = "reports"
    template_name = "inventory/reportlist.html"
    areas = Area.objects.all()
    extra_context = {"show": True, "page": 3, "areas": areas}
    # paginate_by = 5

    def get_queryset(self):
        today = date.today()
        # return Report.objects.filter(user=usr)
        return Report.objects.all()


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
class ReportDetailView(CreateView):
    model = Item
    form_class = CreateReport
    template_name = "inventory/report_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        self.object = Item.objects.filter(slug=self.kwargs["slug"])[0]
        context["item"] = self.object
        return context

    def find_query_index(self, query, item):
        for i in range(len(query)):
            if query[i] == item:
                return i
        return -1

    def form_valid(self, form, *args, **kwargs):
        item = self.get_object()
        # self.success_url = "/report/" + str(item.slug)
        area = Area.objects.filter(name=item.area.name,
                                   location=item.area.location)[0]
        item_list = Item.objects.filter(area=area).order_by('id')
        index = self.find_query_index(item_list, item)
        vals = item_list.values()
        n = index + 1
        if n >= len(vals):
            self.success_url = "/report/" + item.area.name + "/" + item.area.location
        else:
            slugurl = vals[n]["slug"]
            self.success_url = "/report/" + str(slugurl)

        if self.request.method == 'POST':
            if 'perfect' in self.request.POST:
                form.instance.user = self.request.user
                form.instance.item = item
                form.instance.actual = item.quantity
                form.instance.expected = item.quantity
                print(date.today())
                # report_table = ReportTable(area=area, date=date.today(), reports=[])
                return super().form_valid(form)
            if 'doesnotexist' in self.request.POST:
                form.instance.user = self.request.user
                form.instance.item = item
                form.instance.expected = item.quantity
                form.instance.actual = 0
                return super().form_valid(form)
            if 'report' in self.request.POST:
                if form.instance.actual is None:
                    return super(ReportDetailView, self).form_invalid(form)
                form.instance.user = self.request.user
                form.instance.item = item
                form.instance.expected = item.quantity
                return super().form_valid(form)
        return super(ReportDetailView, self).form_invalid(form)


class TestView(View):

    def get(self, request):
        text = request.GET.get("button_text")
        print()
        print(text)
        print()
        return render(request, "inventory/test.html")