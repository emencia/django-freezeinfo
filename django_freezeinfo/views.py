from django.http import JsonResponse

from django_freezeinfo.info import FreezeInfo
from django_freezeinfo.errors import BuildoutError


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
