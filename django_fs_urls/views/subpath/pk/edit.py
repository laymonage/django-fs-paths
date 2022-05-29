from django.http import HttpResponse


def dispatch(request, pk, *args, **kwargs):
    return HttpResponse(f"{__name__} with pk={pk}")
