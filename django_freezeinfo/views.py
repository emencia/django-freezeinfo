from django_freezeinfo.info import FreezeInfo
from django_freezeinfo.errors import BuildoutError
from django.views.generic.base import TemplateView

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class FreezeInfoView(TemplateView):
    template_name = "django_freezeinfo/info_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['output'] = self.info_view()
        return context

    def info_view(self):
        try:
            instance = FreezeInfo()
            data = dict(instance.infos())
        except (BuildoutError, FileNotFoundError) as e:
            data = {'error': str(e)}
        return data
