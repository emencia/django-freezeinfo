from .views import FreezeInfoView, info_view


try:
    from django.urls import path

    urlpatterns = [
        path('admin/page-info/', FreezeInfoView.as_view(), name='page-info'),
        path('admin/page-info/requirements/', info_view, name='requirements'),
    ]
except ImportError:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^admin/page-info/$', FreezeInfoView.as_view(), name='page-info'),
        url(r'^admin/page-info/requirements/$', info_view, name='requirements'),
    ]
