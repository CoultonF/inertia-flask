import subprocess
from unittest.mock import patch

import pytest
from flask import Flask

from inertia_flask import Inertia
from inertia_flask.cli import InertiaCommands


class TestCLI:
    """Command line interface tests for inertia flask"""

    @pytest.fixture
    def app(self):
        """define an app and attach inertia commands"""
        app = Flask(__name__)
        app.config["INERTIA_VITE_DIR"] = "react"
        inertia = Inertia(app)
        commands = InertiaCommands(inertia)
        commands.register_as_flask(app)
        return app

    @pytest.fixture
    def commands(self):
        """define an app and attach inertia commands"""
        app = Flask(__name__)
        app.config["INERTIA_VITE_DIR"] = "react"
        inertia = Inertia(app)
        with app.app_context():
            commands = InertiaCommands(inertia)
            commands.register_as_flask(app)
            yield InertiaCommands(inertia)

    def test_vite_build_command(self, app, tmp_path):
        """Test to ensure `flask vite build` is implemented"""
        with patch("subprocess.run") as mock_run:
            # Create a runner and invoke the command
            vite_dir = tmp_path / "react"
            vite_dir.mkdir()
            app.config["INERTIA_VITE_DIR"] = str(vite_dir)
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "build"])

            # Check command executed successfully
            assert result.exit_code == 0

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(["pnpm", "run", "build"], check=True)

    def test_vite_install_command(self, app, tmp_path):
        """Test to ensure `flask vite install` is implemented"""
        with patch("subprocess.run") as mock_run:
            vite_dir = tmp_path / "react"
            vite_dir.mkdir()
            app.config["INERTIA_VITE_DIR"] = str(vite_dir)
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "install"])

            assert result.exit_code == 0
            mock_run.assert_called_once_with(["pnpm", "install"], check=True)

    def test_package_manager_detection(self, commands, tmp_path):
        """Test package manager detection logic"""
        vite_dir = tmp_path / "react"
        vite_dir.mkdir()

        # Test pnpm detection via lock file
        pnpm_lock = vite_dir / "pnpm-lock.yaml"
        pnpm_lock.touch()
        assert commands.get_package_manager(vite_dir) == "pnpm"
        pnpm_lock.unlink()

        # Test yarn detection via lock file
        yarn_lock = vite_dir / "yarn.lock"
        yarn_lock.touch()
        assert commands.get_package_manager(vite_dir) == "yarn"
        yarn_lock.unlink()

        # Test fallback to npm
        with patch("shutil.which", return_value=None):
            assert commands.get_package_manager(vite_dir) == "npm"

    def test_error_handling(self, app):
        """Ensure that is we have no vite dir set, we error"""
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, [])):
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "build"])
            assert result.exit_code != 0
