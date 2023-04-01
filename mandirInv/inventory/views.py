from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.shortcuts import render
from django.utils.datetime_safe import date

from .models import Item, Report, User, Area
# from mandirInv.mandirInv import UserManager
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateReport
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404

CurrentUser = get_user_model()


class UserAreas(View, LoginRequiredMixin):
    template_name = "inventory/area_in_charge.html"

    def get(self, request, *args, **kwargs):
        arr = request.user.get_area_incharge()
        return render(request, self.template_name, {"areas": arr})


class UserSettings(ListView):
    model = User
    context_object_name = "users"
    template_name = "inventory/settings.html"
    extra_context = {"show": True, "page": 4}


class UserSettingsDetails(DetailView, UpdateView):
    model = User
    tmp = Area.objects.all()
    fields = ["area_incharge"]
    extra_context = {"show": False, "areas": tmp}
    template_name = "inventory/settings-details.html"
    pk_url_kwarg = "id"


    def form_valid(self, form, *args, **kwargs):
        if self.request.method == 'POST':
            loc = self.request.POST["areas"].split(",")
            area = loc[0]
            mandir = loc[1]
            mandir = mandir.strip()
            print(mandir)
            print(area)

            usr = User.objects.filter(email=self.object)[0]
            areas = usr.get_area_incharge()
            print(areas)
            if mandir in areas:
                if area not in areas[mandir]:
                    areas[mandir].append(area)
            else:
                areas[mandir] = [area]
            a = self.convert_to_area_string(areas)
            form.instance.area_incharge = a
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
    extra_context = {"show": True, "page": 3}
    paginate_by = 5

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


class InventoryDetail(DetailView, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
    ordering = ['uid']
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        try:
            area = Area.objects.get(name=self.kwargs["area"])
            return Item.objects.filter(area=area)
        except:
            return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ReportTable, self).get_context_data(**kwargs)
        # print(self.get_queryset().values("uid"))
        result = ""
        for i in self.get_queryset().values("uid"):
            result += str(i["uid"]) + "_"

        result = result[:-1]
        context["result"] = result

        return context


# [Indivual item page]
class ReportDetailView(LoginRequiredMixin, DetailView, CreateView):
    model = Item
    form_class = CreateReport
    template_name = "inventory/report_detail.html"

    def __init__(self):
        super().__init__()
        # a = User.objects.all()
        # # for i in a:
        # #     print(i)

    def form_valid(self, form, *args, **kwargs):

        # Get the next item in the list
        msg = self.kwargs["msg"].split("_")
        pk = self.kwargs["pk"]
        msg = [int(i) for i in msg]
        a = msg.index(pk)
        msg = msg[a + 1:]
        if len(msg) <= 0:
            self.success_url = "/report/"
        else:
            msg = [str(i) for i in msg]
            s = '_'.join(msg)
            self.success_url = "/report/" + s + "/" + msg[0]

        # print("Hello World", self.kwargs)
        item = self.get_object()
        if self.request.method == 'POST' and 'report' in self.request.POST:
            if form.instance.actual is None:
                return super(ReportDetailView, self).form_invalid(form)
            form.instance.user = self.request.user
            form.instance.item = item
            form.instance.expected = item.quantity

            return super().form_valid(form)

        if self.request.method == 'POST' and 'perfect' in self.request.POST:
            form.instance.user = self.request.user
            form.instance.item = item
            form.instance.actual = item.quantity
            form.instance.expected = item.quantity
            return super().form_valid(form)

        if self.request.method == 'POST' and 'doesnotexist' in self.request.POST:
            form.instance.user = self.request.user
            form.instance.item = item
            form.instance.expected = item.quantity
            form.instance.actual = 0
            return super().form_valid(form)
