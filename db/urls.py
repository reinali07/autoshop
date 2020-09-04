"""db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sites.models import Site

admin.site.unregister(Site)

urlpatterns = [
    path('',include('landing_page.urls',namespace='landing_page')),
    path('admin/', admin.site.urls),
    path('contacts_db/', include('contacts_db.urls',namespace='contacts_db')),
    path('vehicles_db/', include('vehicles_db.urls',namespace='vehicles_db')),
    path('clientcars_db/', include('clientcars_db.urls',namespace='clientcars_db')),
    path('sup_invoices/', include('sup_invoices.urls',namespace='sup_invoices')),
    path('stock/', include('stock.urls',namespace='stock')),
    path('workorders/', include('workorders.urls',namespace='workorders')),
    #path("select2/", include("django_select2.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)