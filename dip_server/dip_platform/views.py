from django.http import HttpResponse

from dip_platform import models


def test(request):
    return HttpResponse(models.User.objects.get(id=0).username)