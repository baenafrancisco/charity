from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'charities.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'www.views.home', name='home'),
    url(r'^api/getnextcharities/$', 'www.views.get_next_charities', name='get_next_charities'),
    url(r'^api/donatetocharity/$', 'www.views.donate_to_charity', name='donate_to_charity'),
    url(r'^api/declinedonation/$', 'www.views.decline_donation', name='decline_donation'),
    url(r'^charity/(?P<charity_id>\d+)/$', 'www.views.display_charity_profile', name="display_charity_profile"),
    url(r'^user/(?P<user_id>\d+)/$', 'www.views.display_user_profile', name="display_user_profile"),
)
