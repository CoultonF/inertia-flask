[![Inertia.js](https://raw.githubusercontent.com/coultonf/inertia-flask/main/LOGO.png)](https://inertiajs.com/)

[![Inertia 2.0](https://img.shields.io/badge/Inertia-2.0-rgb(107%2C70%2C193).svg)](https://inertiajs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Inertia.js Flask Adapter

The Inertia.js Flask Adapter allows you to seamlessly integrate Inertia.js with your Flask applications. This adapter provides the necessary tools to build modern, single-page applications using Flask as the backend and Inertia.js for the frontend.

## Installation

To install the Flask Inertia adapter, use pip:

```bash
pip install inertia-flask
```

## Configuration
You can initialize inertia-flask like most other extensions in Flask.

``` python
from flask import Flask
from inertia_flask import Inertia

# Required configuration keys
SECRET_KEY = "secret!"
INERTIA_TEMPLATE = "base.html"  # Mandatory key

app = Flask(__name__)
app.config.from_object(__name__)

# Initialize Inertia
inertia = Inertia()
inertia.init_app(app)
# Alternatively, you can initialize it directly: inertia = Inertia(app)
```

### Initializing on a Blueprint

You can also initialize the Inertia extension on a specific Blueprint:


```python
from flask import Blueprint, Flask
from flask_inertia import Inertia

# Required configuration keys
SECRET_KEY = "secret!"
INERTIA_TEMPLATE = "base.html"  # Mandatory key

app = Flask(__name__)
app.config.from_object(__name__)

# Create a Blueprint
blueprint = Blueprint('inertia', __name__, template_folder='templates')

# Initialize Inertia on the Blueprint
inertia = Inertia(blueprint)
# Alternatively, you can initialize it directly: inertia = Inertia(blueprint)
```


## CSRF

Flask does not provide CSRF protection by default. To handle CSRF protection, you can use the [Flask Seasurf](https://github.com/maxcountryman/flask-seasurf) extension, which is a simple and effective solution for Flask applications.

To integrate Seasurf with Inertia.js, configure Axios in your .js entry file as follows:

```javascript
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "_csrf_token";
```
This ensures that Axios automatically includes the CSRF token in requests, aligning with Seasurf's protection mechanism.

## Examples

To run the example project, follow these steps:

#### Using `pnpm`

``` bash
cd demo/react
pnpm install  
pnpm run dev
```

#### Using `npm`

```bash
cd demo/react
npm install
npm run dev
```

In a separate terminal, start the Flask server:

``` bash
poetry install --with dev
poetry run demo
```

## Contributing

To contribute to the development of this extension, follow these steps:

1. Install the project dependencies with test support:
    ``` bash
    poetry install --with test
    ```

2. Run the unit tests using pytest:
    ``` bash
    poetry run pytest
    ```


## Thank you

Parts of this repo were inspired by: 

[Inertia-django](https://github.com/inertiajs/inertia-django?tab=readme-ov-file), MIT License, Copyright 2022 Bellawatt, Brandon Shar

[Flask-inertia](https://github.com/j0ack/flask-inertia), MIT License, Copyright 2021, TROUVERIE Joachim <jtrouverie@joakode.fr>

Maintained and sponsored by [IJACK Technologies](https://myijack.com/).

[![IJACK Technologies](https://raw.githubusercontent.com/coultonf/inertia-flask/main/IJACK.png)](https://myijack.com/)
