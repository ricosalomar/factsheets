from django.conf.urls import patterns, url
from plants.views import *

urlpatterns = patterns('',
    url(r'^plant-list', PlantCatListView.as_view()),
    url(r'^category/(?P<cat>[-\w]+)/(?P<page>[\d]*)/$', CustomCatView.as_view()),
    url(r'^category/(?P<cat>[-\w]+)/$', CustomCatView.as_view()),
    url(r'^search/(?P<page>[\d]*)/$', CustomSearchView.as_view()),
    url(r'^search/$', CustomSearchView.as_view()),
    url(r'(?P<cat>[-\w]*)/(?P<slug>[-\w]+)/$', PlantDetailView.as_view()),
    url(r'^category/$', PlantCatListView.as_view()),
    url(r'^autocomplete/$', autocompleteModel),
    (r'^$', PlantCatListView.as_view())
)

