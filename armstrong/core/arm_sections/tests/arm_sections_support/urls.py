from django.contrib import admin
from django.conf.urls.defaults import *

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
