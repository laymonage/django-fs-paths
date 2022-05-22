from django.http import HttpResponse


def make_dispatch(text):
    """
    A helper function to create a dispatch function that returns an
    HttpResponse. Originally, I wanted to make it so that the text is
    automatically inferred from the module path, but it needs some `inspect`
    thing to work. So, just pass the __name__ as the text from the modules.

    This is just to make testing easier and is not necessary for
    django-fs-urls to work.
    """

    def dispatch(request):
        return HttpResponse(text)

    return dispatch
