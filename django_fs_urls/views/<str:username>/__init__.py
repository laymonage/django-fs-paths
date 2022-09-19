from django.http import HttpResponse


def dispatch(request, username, *args, **kwargs):
    print(__file__)
    return HttpResponse(f"{__name__} with username={username}")
