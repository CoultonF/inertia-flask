[![Inertia.js](https://raw.githubusercontent.com/coultonf/inertia-flask/main/LOGO.png)](https://inertiajs.com/)

[![Inertia 2.0](https://img.shields.io/badge/Inertia-2.0-rgb(107%2C70%2C193).svg)](https://inertiajs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Inertia.js Flask Adapter

The Inertia.js Flask Adapter allows you to seamlessly integrate Inertia.js with your Flask applications. This adapter provides the necessary tools to build modern, single-page applications using Flask as the backend and Inertia.js for the frontend.

## Installation

ource## Using uv (recommended)

1. Install uv:
```bash
pip install uv
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. For development:
```bash
uv pip install -r requirements-dev.txt
```

5. For testing:
```bash
uv pip install -r requirements-test.txt

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

Inertia.js uses Axios as the requests library. You can modify axios to integrate Seasurf with Inertia.js in your .js entry file as follows:

```javascript
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "_csrf_token";
```
This ensures that Axios automatically includes the CSRF token in requests, aligning with Seasurf's protection mechanism.

## Use

###

## Examples

Ensure you have pnpm/npm installed and are on the latest version of node as Vite has dropped support for Node v21. If you are encountering issues around node and using Windows, try to sign out.

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

## Testing

### Running Tests

1. Install test dependencies:
```bash
uv pip install -r requirements-test.txt
```

2. Run tests using the test script:
```bash
./scripts/test.sh
```

### Test Options

- Run specific test file:
```bash
./scripts/test.sh tests/test_inertia.py
```

- Run tests with specific marker:
```bash
./scripts/test.sh -m "integration"
```

- Run tests with output:
```bash
./scripts/test.sh -v
```

### Coverage Report

The test script automatically generates a coverage report. To generate an HTML coverage report:

```bash
./scripts/test.sh --cov-report=html
```

The report will be available in the `htmlcov` directory.

## Thank you

Parts of this repo were inspired by: 

[Inertia-django](https://github.com/inertiajs/inertia-django?tab=readme-ov-file), MIT License, Copyright 2022 Bellawatt, Brandon Shar

[Flask-inertia](https://github.com/j0ack/flask-inertia), MIT License, Copyright 2021, TROUVERIE Joachim <jtrouverie@joakode.fr>

Maintained and sponsored by [IJACK Technologies](https://myijack.com/).

<a href="https://myijack.com/"> <img src="https://raw.githubusercontent.com/coultonf/inertia-flask/main/IJACK.png" alt="IJACK Technologies" width="120" /> </a> 
