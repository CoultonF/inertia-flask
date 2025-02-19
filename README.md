[![Inertia.js](https://raw.githubusercontent.com/coultonf/inertia-flask/main/LOGO.png)](https://inertiajs.com/)

# Inertia.js Flask Adapter

## Installation
------------

```bash
pip install flask-inertia
```

## Configuration
------------
You can initialize inertia-flask like most other extensions in Flask.

``` python
from flask import Flask
from inertia_flask import Inertia

SECRET_KEY = "secret!"
# mandatory key
INERTIA_TEMPLATE = "base.html"

app = Flask(__name__)
app.config.from_object(__name__)

inertia = Inertia()
inertia.init_app(app)
# or inertia = Inertia(app)
```

You can also initialize the extension on just a blueprint as well.

```python
from flask import Blueprint, Flask
from flask_inertia import Inertia

SECRET_KEY = "secret!"
# mandatory key
INERTIA_TEMPLATE = "base.html"

app = Flask(__name__)
app.config.from_object(__name__)

blueprint = Blueprint('inertia', __name__, template_folder='templates')

inertia = Inertia(blueprint)
# or inertia = Inertia(blueprint)
```


## CSRF
Flask doesn't provide a CSRF protection by default so you should implement CSRF using another flask extension.

Seasurf is a simple CSRF extension for Flask that will automatically handle CSRF on requests.
You should use Axios inside your Inertia JS entry fille and setup the defaults to handle Seasurf's CSRF protections.
```js
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "_csrf_token";
```