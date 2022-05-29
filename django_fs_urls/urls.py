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
import pkgutil
import sys

from django.urls import path


_MODULE_ROUTES = {}


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

    url_name = f"{namespace}/{name}"
    if not name:
        route = ""
        url_name = namespace

    _MODULE_ROUTES[cache_key] = route

    if not hasattr(module, "dispatch"):
        return None
    return path(route, module.dispatch, name=url_name)


def process_pkg(pkg, prefix, namespace):
    finder, name, _ = pkg
    finder.invalidate_caches()
    sys.modules.pop(name, None)
    module = finder.find_module(name).load_module(name)
    return get_path_from_module(module, prefix, namespace)


def fs_paths(module_name, namespace):
    result = []

    sys.modules.pop(module_name, None)
    init_module = importlib.import_module(module_name)
    root = init_module.__name__
    module_path = init_module.__path__

    if path := get_path_from_module(init_module, root, namespace):
        result.append(path)

    for pkg in pkgutil.walk_packages(module_path, prefix=f"{root}."):
        if path := process_pkg(pkg, root, namespace):
            result.append(path)

    return result


urlpatterns = [
    *fs_paths("django_fs_urls.views", "django_fs_urls"),
]
