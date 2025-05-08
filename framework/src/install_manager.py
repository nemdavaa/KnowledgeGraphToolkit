# install_manager.py
import subprocess
import sys
import logging
import pkg_resources

logger = logging.getLogger(__name__)


class InstallManager:
    def __init__(self, requirements_file: str = "requirements.txt"):
        self.requirements_file = requirements_file

    def install_deps(self):
        """Install dependencies from the requirements file."""
        logger.info("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", self.requirements_file])
            logger.info("All dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Dependency installation failed: {e}")
            raise

    def check_deps(self) -> bool:
        """Check if all dependencies are already installed."""
        logger.info("Checking installed dependencies...")
        try:
            with open(self.requirements_file, 'r') as file:
                requirements = file.readlines()
            missing = []
            for req in requirements:
                req = req.strip()
                if req:
                    try:
                        pkg_resources.require(req)
                    except pkg_resources.DistributionNotFound:
                        missing.append(req)
                    except pkg_resources.VersionConflict:
                        missing.append(req)
            if missing:
                logger.warning(f"Missing or incompatible dependencies: {missing}")
                return False
            logger.info("All dependencies satisfied.")
            return True
        except Exception as e:
            logger.error(f"Dependency check failed: {e}")
            return False

    def resolve_deps(self):
        """Check and install dependencies if missing."""
        if not self.check_deps():
            self.install_deps()
        else:
            logger.info("No dependency installation needed.")

    def uninstall_deps(self):
        """Uninstall dependencies listed in the requirements file."""
        logger.info("Uninstalling dependencies...")
        try:
            with open(self.requirements_file, 'r') as file:
                requirements = [line.strip() for line in file if line.strip()]
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y"] + requirements)
            logger.info("Dependencies uninstalled.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Uninstallation failed: {e}")