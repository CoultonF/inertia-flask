import os
import shutil
import subprocess
import threading
import time

from flask import Blueprint, Flask
from flask.cli import AppGroup


def get_package_manager(root_path):
    """Determine the package manager based on the presence of lock files."""
    if os.path.exists(os.path.join(root_path, "pnpm-lock.yaml")):
        return "pnpm"
    elif os.path.exists(os.path.join(root_path, "yarn.lock")):
        return "yarn"
    elif shutil.which("pnpm") is not None:
        return "pnpm"
    elif shutil.which("yarn") is not None:
        return "yarn"
    else:
        return "npm"


class InertiaCommands:
    def __init__(self, inertia_instance, app=None):
        self.inertia = inertia_instance
        self.app = app or inertia_instance.app

    def register_as_flask(self, app: Flask):
        """Register CLI commands with the Flask app"""
        # Create a command group
        vite_group = AppGroup("vite", help="Vite integration commands")

        # Add the build command
        @vite_group.command("build")
        def vite_build_command():
            """Build Vite assets for production"""
            self._vite_build()

        # Add the dev command
        @vite_group.command("dev")
        def vite_dev_command():
            """Run Flask and Vite dev servers together"""
            self._vite_dev()

        @vite_group.command("install")
        def vite_install_command():
            """Install Vite dependencies"""
            self._vite_install()

        # Add the command group to the app
        app.cli.add_command(vite_group)

    def register_as_blueprint(self, blueprint: Blueprint):
        """Register CLI commands with the Blueprint"""

        # Create a command group
        vite_group = AppGroup("vite", help="Vite integration commands")

        # Add the build command
        @vite_group.command("build")
        def vite_build_command():
            """Build Vite assets for production"""
            self._vite_build()

        # Add the dev command
        @vite_group.command("dev")
        def vite_dev_command():
            """Run Flask and Vite dev servers together"""
            self._vite_dev()

        @vite_group.command("install")
        def vite_install_command():
            """Install Vite dependencies"""
            self._vite_install()

        blueprint.cli.add_command(vite_group)

    def _run_vite_dev(self):
        """Run Vite dev server in a separate thread"""
        vite_dir = self.app.config.get("INERTIA_VITE_DIR")
        vite_dir_path = os.path.join(self.app.app.root_path, vite_dir)

        # Check if package.json exists
        if not os.path.exists(os.path.join(vite_dir_path, "package.json")):
            print(f"Error: No package.json found in {vite_dir_path}")
            return

        # Determine package manager (npm, yarn, pnpm)
        package_manager = get_package_manager(vite_dir_path)

        # Run Vite dev server
        os.chdir(vite_dir_path)
        with subprocess.Popen([package_manager, "run", "dev"]):
            print(f"Vite dev server started in {vite_dir_path}")

    def _vite_dev(self):
        """Run Flask and Vite dev servers together"""
        # Start Vite in a separate thread
        vite_thread = threading.Thread(target=self.run_vite_dev)
        vite_thread.daemon = True
        vite_thread.start()

        # Give Vite time to start
        time.sleep(2)

        # Flask server will continue running in the main thread
        print("Flask server running with Vite integration")

    def _vite_build(self):
        """Build Vite assets for production"""
        vite_dir = self.app.config.get("INERTIA_VITE_DIR", "react")
        vite_dir_path = os.path.join(self.app.root_path, vite_dir)

        # Determine package manager
        package_manager = get_package_manager(vite_dir_path)

        # Run build
        os.chdir(vite_dir_path)
        subprocess.run([package_manager, "run", "build"], check=True)
        print(f"Vite assets built successfully in {vite_dir_path}")

        # For backward compatibility and direct calling

    def _vite_install(self):
        """Install Vite dependencies"""
        vite_dir = self.app.config.get("INERTIA_VITE_DIR", "react")
        vite_dir_path = os.path.join(self.app.root_path, vite_dir)
        # Determine package manager
        package_manager = get_package_manager(vite_dir_path)

        # Run install
        os.chdir(vite_dir_path)
        subprocess.run([package_manager, "install"], check=True)
        print(f"Vite dependencies installed successfully in {vite_dir_path}")

    def vite_build(self):
        """Build Vite assets for production (for direct calling)"""
        return self._vite_build()

    def vite_dev(self):
        """Run Flask and Vite dev servers together (for direct calling)"""
        return self._vite_dev()

    def vite_install(self):
        """Install Vite dependencies (for direct calling)"""
        return self._vite_install()

    def run_vite_dev(self):
        """Run Vite dev server (for direct calling)"""
        return self._run_vite_dev()
