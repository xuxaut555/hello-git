from django.conf.urls import include, url
from django.contrib import admin
from mainsite.views import homepage, showpost

urlpatterns = [
    # Examples:
    # url(r'^$', 'mblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', homepage),
    url(r'^post/(\w+)$', showpost),
    url(r'^admin/', include(admin.site.urls)),
]
