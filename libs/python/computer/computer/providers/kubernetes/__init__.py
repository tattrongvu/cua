"""Kubernetes provider for running pods with computer-server."""

from .provider import KubernetesProvider

# Check if Kubernetes client is available
try:
    # For now, we'll assume Kubernetes is available if the provider is imported
    # In a production environment, you might want to check for kubernetes client library
    HAS_KUBERNETES = True
except Exception:
    HAS_KUBERNETES = False

__all__ = ["KubernetesProvider", "HAS_KUBERNETES"]
