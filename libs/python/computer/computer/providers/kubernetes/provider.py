"""
Docker VM provider implementation.

This provider uses Docker containers running the CUA Ubuntu image to create
Linux VMs with computer-server. It handles VM lifecycle operations through Docker
commands and container management.
"""

import asyncio
import json
import logging
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..base import BaseVMProvider, VMProviderType

# Setup logging
logger = logging.getLogger(__name__)

# Check if Docker is available
try:
    subprocess.run(["docker", "--version"], capture_output=True, check=True)
    HAS_DOCKER = True
except (subprocess.SubprocessError, FileNotFoundError):
    HAS_DOCKER = False


class KubernetesProvider(BaseVMProvider):
    """
    Kubernetes VM Provider implementation using Kubernetes clusters.

    This provider uses Kubernetes to run pods with the CUA Ubuntu image
    that includes computer-server for remote computer use.
    """

    def __init__(
        self,
        host: str = "localhost",
        storage: Optional[str] = None,
        shared_path: Optional[str] = None,
        image: str = "trycua/cua-ubuntu:latest",
        verbose: bool = False,
        ephemeral: bool = False,
        vnc_port: Optional[int] = 6901,
        api_port: Optional[int] = 8000,
    ):
        """Initialize the Docker VM Provider.

        Args:
            host: Hostname for the API server (default: localhost)
            storage: Path for persistent VM storage
            shared_path: Path for shared folder between host and container
            image: Docker image to use (default: "trycua/cua-ubuntu:latest")
                   Supported images:
                   - "trycua/cua-ubuntu:latest" (Kasm-based)
                   - "trycua/cua-xfce:latest" (vanilla XFCE)
            verbose: Enable verbose logging
            ephemeral: Use ephemeral (temporary) storage
            vnc_port: Port for VNC interface (default: 6901)
            api_port: Port for API server (default: 8000)
        """
        self.host = host
        self.api_port = api_port if api_port is not None else 8000
        self.vnc_port = vnc_port
        self.ephemeral = ephemeral

        self.shared_path = shared_path
        self.image = image
        self.verbose = verbose
        self._container_id = None
        self._running_containers = {}  # Track running containers by name

        # Detect image type and configure user directory accordingly
        self._detect_image_config()

        if ephemeral:
            self.storage = "ephemeral"  # Handle ephemeral storage (temporary directory)
        else:
            self.storage = storage

    def _detect_image_config(self):
        """Detect image type and configure paths accordingly."""
        # Detect if this is a XFCE, Kasm, or QEMU-based image
        if "xfce" in self.image.lower():
            self._home_dir = "/home/cua"
            self._image_type = "docker-xfce"
            logger.info(f"Detected docker-xfce image: using {self._home_dir}")
        else:
            # Default to Kasm configuration
            self._home_dir = "/home/kasm-user"
            self._image_type = "kasm"
            logger.info(f"Detected Kasm image: using {self._home_dir}")

    @property
    def provider_type(self) -> VMProviderType:
        """Return the provider type."""
        return VMProviderType.KUBERNETES

    async def get_vm(self, name: str, storage: Optional[str] = None) -> Dict[str, Any]:
        """Get VM information by name.

        Args:
            name: Name of the VM to get information for
            storage: Optional storage path override. If provided, this will be used
                    instead of the provider's default storage path.

        Returns:
            Dictionary with VM information including status, IP address, etc.
        """
        try:
            return {
                "name": name,
                "status": "running",
                "ip_address": self.host,  # Use localhost if no IP
                "ports": self.api_port,
                "image": self.image,
                "provider": "kubernetes",
                "container_id": "",  # Short ID
                "created": "",  # Creation timestamp
                "started": "",
            }

        except Exception as e:
            logger.error(f"Error getting VM info for {name}: {e}")
            import traceback

            traceback.print_exc()
            return {"name": name, "status": "error", "error": str(e), "provider": "docker"}

    async def list_vms(self) -> List[Dict[str, Any]]:
        """List all containers managed by this provider."""
        logger.info(f"List VMs method called for KubernetesProvider, but not implemented yet.")
        return []

    async def run_vm(
        self, image: str, name: str, run_opts: Dict[str, Any], storage: Optional[str] = None
    ) -> Dict[str, Any]:
        """Run a VM with the given options.

        Args:
            image: Name/tag of the Docker image to use
            name: Name of the container to run
            run_opts: Options for running the VM, including:
                - memory: Memory limit (e.g., "4GB", "2048MB")
                - cpu: CPU limit (e.g., 2 for 2 cores)
                - vnc_port: Specific port for VNC interface
                - api_port: Specific port for computer-server API

        Returns:
            Dictionary with VM status information
        """
        logger.info(f"Run VM method called for KubernetesProvider, but not implemented yet.")
        return {}


    async def stop_vm(self, name: str, storage: Optional[str] = None) -> Dict[str, Any]:
        """Stop a running VM by stopping the Docker container."""
        logger.info(f"Stop VM method called for KubernetesProvider, but not implemented yet.")
        return {}

    async def restart_vm(self, name: str, storage: Optional[str] = None) -> Dict[str, Any]:
        raise NotImplementedError("DockerProvider does not support restarting VMs.")

    async def update_vm(
        self, name: str, update_opts: Dict[str, Any], storage: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update VM configuration.

        Note: Docker containers cannot be updated while running.
        This method will return an error suggesting to recreate the container.
        """
        return {
            "name": name,
            "status": "error",
            "error": "Containers cannot be updated while running. Please stop and recreate the container with new options.",
            "provider": "kubernetes",
        }

    async def get_ip(self, name: str, storage: Optional[str] = None, retry_delay: int = 2) -> str:
        """Get the IP address of a VM, waiting indefinitely until it's available.

        Args:
            name: Name of the VM to get the IP for
            storage: Optional storage path override
            retry_delay: Delay between retries in seconds (default: 2)

        Returns:
            IP address of the VM when it becomes available
        """
        logger.info(f"Getting IP address for container {name}")

        return self.host

    async def __aenter__(self):
        """Async context manager entry."""
        logger.debug("Entering KubernetesProvider context")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit.

        This method handles cleanup of running containers if needed.
        """
        logger.debug(f"Exiting DockerProvider context, handling exceptions: {exc_type}")
        
