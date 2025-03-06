import subprocess
from unittest.mock import patch

import pytest
from flask import Flask
from flask.cli import ScriptInfo

from inertia_flask import Inertia
from inertia_flask.cli import InertiaCommands


class TestCLI:
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config["INERTIA_VITE_DIR"] = "react"
        inertia = Inertia(app)
        commands = InertiaCommands(inertia)
        commands.register_as_flask(app)
        return app

    @pytest.fixture
    def script_info(self, app):
        return ScriptInfo(create_app=lambda info: app)

    def test_vite_build_command(self, app, script_info):
        with patch("subprocess.run") as mock_run:
            # Create a runner and invoke the command
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "build"])

            # Check command executed successfully
            assert result.exit_code == 0

            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once_with(["npm", "run", "build"], check=True)

    def test_vite_dev_command(self, app, script_info):
        with (
            patch("threading.Thread") as mock_thread,
            patch("time.sleep") as mock_sleep,
        ):
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "dev"])

            assert result.exit_code == 0
            mock_thread.assert_called_once()
            mock_sleep.assert_called_once_with(2)

    def test_vite_install_command(self, app, script_info):
        with patch("subprocess.run") as mock_run:
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "install"])

            assert result.exit_code == 0
            mock_run.assert_called_once_with(["npm", "install"], check=True)

    def test_package_manager_detection(self, app, tmp_path):
        """Test package manager detection logic"""
        vite_dir = tmp_path / "react"
        vite_dir.mkdir()
        app.config["INERTIA_VITE_DIR"] = str(vite_dir)

        # Test pnpm detection via lock file
        pnpm_lock = vite_dir / "pnpm-lock.yaml"
        pnpm_lock.touch()
        assert InertiaCommands(Inertia(app)).get_package_manager() == "pnpm"
        pnpm_lock.unlink()

        # Test yarn detection via lock file
        yarn_lock = vite_dir / "yarn.lock"
        yarn_lock.touch()
        assert InertiaCommands(Inertia(app)).get_package_manager() == "yarn"
        yarn_lock.unlink()

        # Test fallback to npm
        with patch("shutil.which", return_value=None):
            assert InertiaCommands(Inertia(app)).get_package_manager() == "npm"

    def test_error_handling(self, script_info):
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, [])):
            runner = app.test_cli_runner()
            result = runner.invoke(args=["vite", "build"])
            assert result.exit_code != 0

    def test_missing_package_json(self, app, tmp_path):
        """Test behavior when package.json is missing"""
        vite_dir = tmp_path / "react"
        vite_dir.mkdir()
        app.config["INERTIA_VITE_DIR"] = str(vite_dir)

        runner = app.test_cli_runner()
        result = runner.invoke(args=["vite", "dev"])
        assert "No package.json found" in result.output
