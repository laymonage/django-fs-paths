from django.http import HttpResponse


def dispatch(request, username, *args, **kwargs):
    return HttpResponse(f"{__name__} with username={username}")
