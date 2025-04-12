[![Inertia.js](https://raw.githubusercontent.com/coultonf/inertia-flask/main/LOGO.png)](https://inertiajs.com/)
[![Inertia 2.0](https://img.shields.io/badge/Inertia-2.0-rgb(107%2C70%2C193).svg)](https://inertiajs.com/)
[![build](https://github.com/CoultonF/inertia-flask/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/CoultonF/inertia-flask/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/CoultonF/inertia-flask/badge.svg)](https://coveralls.io/github/CoultonF/inertia-flask)
[![Download](https://img.shields.io/pypi/dm/inertia-flask.svg)](https://pypi.org/project/inertia-flask/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Inertia.js Flask Adapter

The Inertia.js Flask Adapter allows you to seamlessly integrate Inertia.js with your Flask applications. This adapter provides the necessary tools to build modern, single-page applications using Flask as the backend and Inertia.js for the frontend.

## Development Installation

## Using uv (recommended)

1. Install uv:
```bash
pip install uv
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # Unix/macOS
```

3. Install dependencies:
```bash
uv pip install -e .
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

#### Important Note About Blueprints

When using Inertia with Flask, you must choose between initializing Inertia on either:
- The main Flask application
- A Blueprint

You cannot initialize Inertia on both simultaneously. This is because Inertia manages page state and routing, which can lead to conflicts if multiple instances are running.


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

## Command Line Interface (CLI)

- `flask vite build`: Builds Vite assets for production
- `flask vite dev`: Runs Flask and Vite dev servers together
- `flask vite install`: Installs Vite dependencies

## CSRF

Flask does not provide CSRF protection by default. To handle CSRF protection, you can use the [Flask Seasurf](https://github.com/maxcountryman/flask-seasurf) extension, which is a simple and effective solution for Flask applications.

Inertia.js uses Axios as the requests library. You can modify axios to integrate Seasurf with Inertia.js in your .js entry file as follows:

```javascript
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "_csrf_token";
```
This ensures that Axios automatically includes the CSRF token in requests, aligning with Seasurf's protection mechanism.

## Configuration Options

The following configuration options can be set in your Flask application's config:

### Core Settings

Use these settings for core Inertia functionality.

- `INERTIA_TEMPLATE` (required): The base template used for rendering Inertia pages
- `INERTIA_JSON_ENCODER`: Custom JSON encoder for serializing data (default: `InertiaJsonEncoder`)
- `INERTIA_ENCRYPT_HISTORY`: Enable encryption of Inertia history state (default: `False`)
- `INERTIA_STATIC_ENDPOINT`: Directory for static assets (default: `"static"`, blueprints: `"your_bp_name.static"`)

### Server-Side Rendering (SSR)

Use these settings to configure SSR support.

- `INERTIA_SSR_ENABLED`: Enable server-side rendering support (default: `False`)
- `INERTIA_SSR_URL`: URL where the SSR server is running (default: `"http://localhost:13714"`)

### Vite Integration

Use these settings to configure Vite.

- `INERTIA_VITE_DIR`: Directory containing your Vite/frontend project (default: `"inertia"`)
- `INERTIA_VITE_ORIGIN`: URL where Vite dev server runs (default: `"http://localhost:5173"`)
- `INERTIA_ROOT`: Root element ID for mounting the Inertia app (default: `"app"`)


    #### Manifest Files

    Use these settings to specify the manifest filenames.

    - `INERTIA_VITE_MANIFEST_PATH` (required): Client-side manifest file path
    - `INERTIA_VITE_SSR_MANIFEST_PATH`: Server-side manifest file path (default: `None`)

### Example Configuration

```python
app.config.update(
    INERTIA_TEMPLATE="base.html",
    INERTIA_SSR_ENABLED=True,
    INERTIA_VITE_DIR="frontend",
    INERTIA_ROOT="app",
    # Custom JSON encoder for special serialization needs
    INERTIA_JSON_ENCODER=MyCustomJsonEncoder
)
```

For blueprint-specific configuration, use prefixes:

```python
app.config.update(
    # Global settings
    INERTIA_TEMPLATE="base.html",
    # Blueprint-specific settings
    BP_INERTIA_TEMPLATE="blueprint.html",
    BP_INERTIA_VITE_DIR="bp_frontend"
)
```

## Examples

Ensure you have pnpm/npm installed and are on the latest version of node as Vite has dropped support for Node v21. If you are encountering issues around node and using Windows, try to sign out.

To run the example project, follow these steps:

``` bash
uv venv
source .venv/bin/activate  # Unix/macOS
uv pip install -e .
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
cd examples/react
flask vite install
flask vite dev
```

## Contributing

To contribute to the development of this extension, follow these steps:

1. Install the project dependencies with test support:
    ``` bash
    uv pip install -e .
    uv pip install -r requirements.txt
    uv pip install -r requirements-test.txt
    source .venv/bin/activate  # Unix/macOS
    ```

2. Run the unit tests using pytest:
    ``` bash
    python -m pytest
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
