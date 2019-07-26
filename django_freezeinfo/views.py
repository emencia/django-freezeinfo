from django.http import JsonResponse
from django_freezeinfo.info import FreezeInfo
from django_freezeinfo.errors import BuildoutError
from django.views.generic.base import TemplateView

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def info_view(request):
    path = request.GET.get('path')
    try: 
        if path:
            instance = FreezeInfo(path)
        else:
            instance = FreezeInfo()
        data = instance.infos()
    except (BuildoutError, FileNotFoundError) as e:
        data = {'error': str(e)}
    return JsonResponse(data)


class FreezeInfoView(TemplateView):
    template_name = "django_freezeinfo/info_form.html"
