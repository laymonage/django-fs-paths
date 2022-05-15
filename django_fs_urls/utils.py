from django.http import HttpResponse


def make_dispatch(text):
    def dispatch(request):
        return HttpResponse(text)

    return dispatch
