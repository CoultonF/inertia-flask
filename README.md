[![Inertia.js](https://raw.githubusercontent.com/coultonf/inertia-flask/main/LOGO.png)](https://inertiajs.com/)

# Inertia.js Flask Adapter

## Installation
------------

```bash
pip install flask-inertia
```

## Configuration
------------



Add the Inertia app to your `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
  # django apps,
  'inertia',
  # your project's apps,
]
```

Add the Inertia middleware to your `MIDDLEWARE` in `settings.py`

```python
MIDDLEWARE = [
  # django middleware,
  'inertia.middleware.InertiaMiddleware',
  # your project's middleware,
]
```

Finally, create a layout which exposes `{% block inertia %}{% endblock %}` in the body and set the path to this layout as `INERTIA_LAYOUT` in your `settings.py` file.

Now you're all set!
