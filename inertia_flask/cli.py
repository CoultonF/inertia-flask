import os
import shutil
import subprocess
import sys
import threading
import time

import click
from flask import Blueprint, Flask, current_app
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
    """
    Command line utilities to interface with Inertia

    Vite commands:

    - `flask vite build`: builds vite bundle to create static assets
    - `flask vite dev`: create a dev server to utilize HMR
    - `flask vite install`: install dependencies according to package manager

    The vite commands prefer pnpm, then yarn, then npm. pnpm is recommended.
    """

    def __init__(self, inertia_instance, app=None):
        self.inertia = inertia_instance

    def register_as_flask(self, app: Flask):
        """Register CLI commands with the Flask app"""
        # Create a command group
        vite_group = self.register_vite()
        inertia_group = self.register_inertia()

        # Add the command group to the app
        app.cli.add_command(vite_group)
        app.cli.add_command(inertia_group)

    def register_as_blueprint(self, blueprint: Blueprint):
        """Register CLI commands with the Blueprint"""

        vite_group = self.register_vite()
        inertia_group = self.register_inertia()
        blueprint.cli.add_command(vite_group)
        blueprint.cli.add_command(inertia_group)

    def register_inertia(self):
        """Register CLI commands with the Flask app"""
        # inertia_group = AppGroup("inertia", help="Inertia integration commands")

        @click.command(name="inertia")
        @click.option("--debug", is_flag=True, help="Enable debug mode")
        def inertia_group(debug):
            """Build Inertia assets for production"""
            if debug:
                current_app.config["DEBUG"] = True
                vite_process = self.vite_dev()
                vite_thread = threading.Thread(
                    target=self._stream_output, args=(vite_process, "vite")
                )
                vite_thread.daemon = True
                vite_thread.start()
                try:
                    # Keep the main thread running
                    while True:
                        if vite_process is not None and vite_process.poll() is not None:
                            print("Vite server stopped unexpectedly")
                            break
                        # if flask_process.poll() is not None:
                        #     print("Flask server stopped unexpectedly")
                        #     break
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nShutting down servers...")
                finally:
                    # Ensure both processes are terminated
                    if vite_process is not None:
                        vite_process.terminate()
                        # flask_process.terminate()
                        try:
                            vite_process.wait(timeout=5)
                            # flask_process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            vite_process.kill()
                        # flask_process.kill()
            else:
                current_app.config["DEBUG"] = False
                self._vite_build()

        return inertia_group

    def register_vite(self):
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

        return vite_group

    def _run_vite_dev(self):
        """Run Vite dev server in a separate thread"""
        vite_dir = current_app.config.get("INERTIA_VITE_DIR")
        vite_dir_path = os.path.join(current_app.root_path, vite_dir)

        # Check if package.json exists
        if not os.path.exists(os.path.join(vite_dir_path, "package.json")):
            print(f"Error: No package.json found in {vite_dir_path}")
            return

        # Determine package manager (npm, yarn, pnpm)
        package_manager = get_package_manager(vite_dir_path)

        # Run Vite dev server
        os.chdir(vite_dir_path)
        process = subprocess.Popen([package_manager, "run", "dev"])
        return process

    def _vite_dev(self):
        """Run Flask and Vite dev servers together"""
        # Start Vite in a separate thread
        app = current_app._get_current_object()

        def target():
            with app.app_context():
                self._run_vite_dev()

        vite_thread = threading.Thread(target=target)
        vite_thread.daemon = True
        vite_thread.start()
        try:
            # Keep the main thread running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down vite server...")

    def _vite_build(self):
        """Build Vite assets for production"""
        vite_dir = current_app.config.get("INERTIA_VITE_DIR", "react")
        vite_dir_path = os.path.join(current_app.root_path, vite_dir)

        # Determine package manager
        package_manager = get_package_manager(vite_dir_path)

        # Run build
        os.chdir(vite_dir_path)
        subprocess.run([package_manager, "run", "build"], check=True)
        print(f"Vite assets built successfully in {vite_dir_path}")

        # For backward compatibility and direct calling

    def _vite_install(self):
        """Install Vite dependencies"""
        vite_dir = current_app.config.get("INERTIA_VITE_DIR", "react")
        vite_dir_path = os.path.join(current_app.root_path, vite_dir)
        # Determine package manager
        package_manager = get_package_manager(vite_dir_path)

        # Run install
        os.chdir(vite_dir_path)
        subprocess.run([package_manager, "install"], check=True)
        print(f"Vite dependencies installed successfully in {vite_dir_path}")

    def _stream_output(self, process, prefix):
        while True:
            if process is not None:
                output = process.stdout.readline()
                if output:
                    print(f"[{prefix}] {output.strip()}")
                error = process.stderr.readline()
                if error:
                    print(f"[{prefix}] {error.strip()}", file=sys.stderr)
                if process.poll() is not None:
                    break
            else:
                break

    def vite_build(self):
        """Build Vite assets for production (for direct calling)"""
        return self._vite_build()

    def vite_dev(self):
        """Run Flask and Vite dev servers together (for direct calling)"""
        return self._vite_dev()

    def vite_install(self):
        """Install Vite dependencies (for direct calling)"""
        return self._vite_install()

    def get_package_manager(self, vite_dir_path=None):
        """Get the package manager used for the cli. Used for testing purposes."""
        vite_dir = current_app.config.get("INERTIA_VITE_DIR")
        vite_dir_path = vite_dir_path or os.path.join(current_app.root_path, vite_dir)
        return get_package_manager(vite_dir_path)
