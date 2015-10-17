"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from timetable import views

from django.contrib import admin
from django.views.generic import TemplateView

from registration.backends.simple.views import RegistrationView

admin.autodiscover()


# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/timetable/'

urlpatterns = [
    url(r'^$|^login/$', views.login, name='login'),
    url(r'^timetable/$', views.timetable, name='timetable'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    # ajax GET
    url(r'^class_search/$',views.class_search,name='class_search'),
    url(r'^class_add/$',views.class_add,name='class_add'),
    url(r'^class_remove/$',views.class_remove,name='class_remove'),
    url(r'^get_all_class/$',views.get_all_class,name='get_all_class'),
    url(r'^course_add/$',views.course_add,name='course_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)