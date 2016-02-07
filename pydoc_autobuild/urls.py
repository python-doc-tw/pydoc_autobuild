"""auto_pydoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from os.path import join
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.static import serve
from doc_tasks import views


urlpatterns = [
    url(r'^_build/$', views.home, name='home'),
    url(r'^_build/update/$', views.run_task_update_one_source),
    url(r'^_build/task/(?P<id>\w+)$', views.view_task, name='view_task'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    pydoc_built_root = join(settings.PYDOC_ROOT, 'build', 'html')
    urlpatterns += [
        # serve /3/index.html
        url(r'^3/$', RedirectView.as_view(url='index.html'), name='doc_home'),
        # serve /3/*
        url(
            r'^3/(?P<path>.*)$',
            serve,
            kwargs={'document_root': pydoc_built_root},
            name='pydoc'
        ),
        # redirect /3.5/* to /3/*
        url(
            r'^3.5/(?P<path>.*)$',
            RedirectView.as_view(pattern_name="pydoc"),
            name="pydoc_redirect_35"
        ),
        # redirect / to /_build
        url(r'^$', RedirectView.as_view(pattern_name='home')),
    ]


