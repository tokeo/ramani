# pdoc template overrides

This folder overrides {{ app_name }}'s API documentation. It is listed before
```tokeo.templates.pdoc.html``` in ```config/{{ app_label }}/base.d/pdoc.yaml```,
so any file you drop here shadows the same-named file from tokeo while tokeo
supplies the rest.

## Quick branding — no files needed

Set these in ```config/{{ app_label }}/base.d/pdoc.yaml``` under ```pdoc:```

- ```favicon``` — path/URL of the favicon (default ```public/favicon.ico```)
- ```title```   — suffix in the page title (renders as "module dot Title")
- ```brand```   — sidebar label; leave null to use "rocket <app label>"

## Deeper customisation — drop a file here

Add any of these filenames to take full control of that piece:

- ```tokeo_head.html```    — head contents (custom CSS/JS, analytics, fonts)
- ```module.html.jinja2``` — the module page layout
- ```index.html.jinja2```  — the start page (root packages)

## Styling — two CSS files in `assets/` (build-free)

The pages link two stylesheets, both served from `assets/`:

- `tailwind.min.css` — the pre-built Tailwind framework (a broad set of utility
  classes). Inherited from tokeo; you normally don't touch it.
- `tokeo.theme.css` — plain, non-minified CSS with the brand colours (`:root`),
  fonts and component styles. This is where the look is defined.

To restyle {{ app_name }} **without any build step**, drop your own copy into
`{{ app_label }}/templates/pdoc/html/assets/tokeo.theme.css` and edit it — change
a `--color-brand-*` value, tweak a component, add plain CSS rules — then just
reload. Because this project's `assets/` is copied last, your file wins over
tokeo's. It fully replaces tokeo's `tokeo.theme.css`, so start from tokeo's copy
rather than an empty file. `tailwind.min.css` keeps coming from tokeo.

.. note::

    Only add what you want to change; everything else keeps coming from tokeo.
    See tokeo's ```CUSTOMIZE.md``` for details.
