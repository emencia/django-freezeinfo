from .views import FreezeInfoView

try:
    from django.urls import path

    urlpatterns = [
        path('admin/page-info/', FreezeInfoView.as_view(), name='page-info'),
    ]
except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^admin/page-info/$', FreezeInfoView.as_view(), name='page-info'),
    ]
