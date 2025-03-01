#!/bin/bash

# Default options
PYTEST_ARGS="-v --cov=inertia_flask --cov-report=term-missing"

# If arguments are passed, append them to pytest args
if [ $# -gt 0 ]; then
    PYTEST_ARGS="$PYTEST_ARGS $@"
fi

# Run pytest with the assembled arguments
python -m pytest $PYTEST_ARGS