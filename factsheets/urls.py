from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'factsheets.views.home', name='home'),
    # url(r'^factsheets/', include('factsheets.foo.urls')),

    url('^pages/', include('django.contrib.flatpages.urls')),
    url(r'^plants/', include('plants.urls', namespace="plants")),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'', include('plants.urls', namespace="plants")),
)
