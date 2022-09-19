"""django_fs_urls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import importlib
import os
import pkgutil
import sys

from django.http import JsonResponse
from django.urls import include, path


_DEBUG = os.getenv("DJANGO_FS_URLS_DEBUG") == "True"
_MODULE_ROUTES = {}


def _make_dispatch(route, module, name):
    def dispatch(request, *args, **kwargs):
        return JsonResponse(
            {
                "route": route,
                "route_name": name,
                "module_name": module.__name__,
                "module_file": os.path.relpath(module.__file__),
                "args": args,
                "kwargs": kwargs,
            },
            json_dumps_params={"indent": 4},
        )

    return dispatch


def get_path_from_module(module, prefix, namespace):
    cache_key = f"{namespace}/{module.__name__}"
    name = module.__name__[len(prefix) + 1 :]

    *_, module_name = name.rsplit(".", maxsplit=1)
    parent_cache_key = cache_key[: -(len(module_name) + 1)]

    parent_route = _MODULE_ROUTES.get(parent_cache_key, "")
    module_route = getattr(module, "path", module_name)

    route = f"{module_route}/"
    if parent_route:
        route = f"{parent_route}{module_route}/"

    name = name.replace(":", "|")
    if not name:
        route = ""
        name = "index"

    _MODULE_ROUTES[cache_key] = route

    default_dispatch = _make_dispatch(route, module, name) if _DEBUG else None
    dispatch = getattr(module, "dispatch", default_dispatch)

    return path(route, dispatch, name=name)


def process_pkg(pkg, prefix, namespace):
    finder, name, _ = pkg
    finder.invalidate_caches()
    sys.modules.pop(name, None)
    module = finder.find_module(name).load_module(name)
    return get_path_from_module(module, prefix, namespace)


def fs_paths(module_name, namespace, prefix=""):
    result = []

    sys.modules.pop(module_name, None)
    init_module = importlib.import_module(module_name)
    root = init_module.__name__
    module_path = init_module.__path__

    if path_obj := get_path_from_module(init_module, root, namespace):
        result.append(path_obj)

    for pkg in pkgutil.walk_packages(module_path, prefix=f"{root}."):
        if path_obj := process_pkg(pkg, root, namespace):
            result.append(path_obj)

    # Reverse list so that dynamic paths are ordered last
    result.sort(key=lambda x: str(x.pattern), reverse=True)

    return path(prefix, include((result, namespace), namespace=namespace))


urlpatterns = [
    fs_paths("django_fs_urls.views", "demo", "fs/"),
]
