"""mandirInv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from authencation.views import RegisterView, LoginView, costum_logout
from inventory.views import InventoryView, ReportTable, ReportDetailView, InventoryDetail, ReportListView, UserReport, UserAreas
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', costum_logout, name='logout'),
    path("inventory/", InventoryView.as_view(), name="inventory"),
    path("inventory/<int:pk>/", InventoryDetail.as_view(), name="inventory-update"),
    path("report/<str:area>", ReportTable.as_view(), name="report"),
    # path("reportlist/", ReportListView.as_view(), name="report-list"),
    # path("reportlist/<str:pk>/", UserReport.as_view(), name="reportuser-detail"),
    path('report/<str:msg>/<int:pk>/', ReportDetailView.as_view(), name="report-detail"),
    path('', include("main.urls")),
    path('areas/', UserAreas.as_view(), name='userareas')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
