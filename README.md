# django-fs-urls

Automatically generate URL paths based on your file structure.

Point a Python module/package and a `path()` will automatically be created for
each submodule that contains a `dispatch()` function.

## Example

Given the following directory structure:

```
myapp/views/
├── __init__.py
├── account.py
├── settings/
│  ├── __init__.py
│  ├── notifications/
│  │  ├── __init__.py
│  │  ├── filters.py
│  │  └── preferences.py
│  ├── privacy.py
│  └── security.py
└── username/
   ├── __init__.py
   └── media.py
```

And this `urls.py` file:

```py
urlpatterns = [
  # ...,
  *fs_paths("myapp.views", namespace="myapp"),
  # ...,
]
```

With each `.py` file in `myapp/views/` containing a `dispatch()` function, the
following URL paths will be generated:

```
/
/account/
/settings/
/settings/notifications/
/settings/notifications/filters/
/settings/notifications/preferences/
/settings/privacy/
/settings/security/
/username/
/username/media/
```

If the `.py` file contains a variable named `path`, the route fragment will use
that instead of the file name. This will be inherited by any descendant paths.
For example, with the following `myapp/views/username/__init__.py` file:

```py
path = "<str:username>"


def dispatch(request, username, *args, **kwargs):
    ...
```

And the following `myapp/views/username/media.py` file:

```py
def dispatch(request, username, *args, **kwargs):
    ...
```

Then, instead of the following URL paths:

```
/username/
/username/media/
```

the following URL paths will be generated:

```
/<str:username>/
/<str:username>/media/
```

You can also directly use path parameters (e.g. `<str:username>`) in your
file/directory name, but it is not recommended as it is non-standard and you
lose the ability to import that module normally.

## Motivation

### Marketing version

File-system based routing has been rising in popularity, especially in
JavaScript web frameworks, such as [Next.js][nextjs], [NuxtJS][nuxtjs],
[Gatsby][gatsby], and [SvelteKit][sveltekit]

With file-system based routing, the URL paths structure of your web application
is defined by the structure of the codebase. Each URL path corresponds to a
single view file under the same path in your codebase. This makes it easier to
find the view that handles a certain path, and vice versa.

### Honest version

I'm just curious to see how file-system based routing can be implemented in a
Django project, what it may look like, and how far it can go 🤷

## Room for improvements

### Request method handlers

Currently, `fs_paths()` only looks for a single `dispatch()` function in the
module. It would be nice if it can also detect functions that are named after
the request methods that they handle, e.g. `get()`, `post()`, etc. and make a
default `dispatch()` function, similar to how Django's [View][django-view] class
works.

### Actually turn this into a third-party package

I don't think I have the capacity to turn this into a real package and
maintain it. If you're interested in doing so, I'll be happy to hand over the
repository. Feel free to rename it to `django-fs-paths`, `django-file-urls`,
`django-why-would-you-need-this`, or whatever.

[nextjs]: https://nextjs.org/docs/routing/introduction
[nuxtjs]: https://nuxtjs.org/docs/features/file-system-routing/
[gatsby]: https://www.gatsbyjs.com/docs/reference/routing/file-system-route-api/
[sveltekit]: https://kit.svelte.dev/docs/routing
[nextjs-dynamic-routes]: https://nextjs.org/docs/routing/dynamic-routes
[django-view]: https://github.com/django/django/blob/f825536b5e09b3a047fec0c10aabd91bace0995c/django/views/generic/base.py#L132-L142
