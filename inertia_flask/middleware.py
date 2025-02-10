from functools import wraps
from flask import request, session, redirect, make_response
from werkzeug.wrappers import Response
from .settings import settings

class InertiaMiddleware:
    def __init__(self, app):
        self.app = app
        self.init_app(app)

    def init_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def before_request(self):
        # Generate CSRF token if it doesn't exist
        if 'csrf_token' not in session:
            session['csrf_token'] = self.generate_csrf_token()

    def after_request(self, response):
        if not self.is_inertia_request():
            return response

        if self.is_non_post_redirect(response):
            response.status_code = 303

        if self.is_stale():
            return self.force_refresh()

        return response

    def is_non_post_redirect(self, response):
        return (self.is_redirect_request(response) and 
                request.method in ["PUT", "PATCH", "DELETE"])

    def is_inertia_request(self):
        return "X-Inertia" in request.headers

    def is_redirect_request(self, response):
        return response.status_code in [301, 302]

    def is_stale(self):
        return (
            request.headers.get("X-Inertia-Version", settings.INERTIA_VERSION)
            != settings.INERTIA_VERSION
        )

    def is_stale_inertia_get(self):
        return request.method == "GET" and self.is_stale()

    def force_refresh(self):
        # Store flash messages for the next request
        if 'messages' in session:
            session['_messages'] = session['messages']
            del session['messages']
            
        return Response(
            "",
            status=409,
            headers={"X-Inertia-Location": request.url}
        )

    def generate_csrf_token(self):
        # Generate a random token - in a real app you might want to use 
        # Flask-WTF or another CSRF library
        import secrets
        return secrets.token_hex(32)

def inertia_middleware(app):
    """
    Function to initialize the middleware
    """
    InertiaMiddleware(app)
    return app

# Example usage of flash messages helper
def add_message(category, message):
    """
    Helper function to add flash messages that persist across Inertia requests
    """
    if 'messages' not in session:
        session['messages'] = []
    session['messages'].append({
        'category': category,
        'message': message
    })