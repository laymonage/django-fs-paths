# django-fs-urls

Automatically generate URL paths based on your file structure.

Point a Python module/package and a `path()` will automatically be created for
each submodule that contains a `dispatch()` function.

## Example

Given the following directory structure:

```
myapp/views/
├── __init__.py
├── profile.py
└── settings/
   ├── __init__.py
   ├── notifications/
   │  ├── __init__.py
   │  ├── filters.py
   │  └── preferences.py
   ├── privacy.py
   └── security.py
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
/profile/
/settings/
/settings/notifications/
/settings/notifications/filters/
/settings/notifications/preferences/
/settings/privacy/
/settings/security/
```

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

### Path parameters

The real challenge of this project is to add support for path parameters. In JS
frameworks, this isn't a big deal as file/module names practically have no
restrictions. For example,
[Next.js allows dynamic routes using brackets, e.g. `[param].js`][nextjs-dynamic-routes].
In Python, module names must be valid identifiers, so we're limited to letters,
numbers, and underscores. Technically, it is possible to use an invalid
identifier as the module name, since we dynamically import the module at
runtime. However, this means that you won't be able to normally import the
module in your code.

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
