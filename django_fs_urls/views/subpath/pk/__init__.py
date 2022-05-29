from django.http import HttpResponse


path = "<int:pk>"


def dispatch(request, pk, *args, **kwargs):
    return HttpResponse(f"{__name__} with pk={pk}")
