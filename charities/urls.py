from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'charities.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'www.views.home', name='home'),
    url(r'^api/api_call_example/$', 'www.views.api_call_example', name='api_call_example'),
    url(r'^api/api_call_example/2/$', 'www.views.api_call_example2', name='api_call_example2'),
    url(r'^api/getnextcharities/$', 'www.views.get_next_charities', name='get_next_charities'),

)
