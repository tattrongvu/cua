# Kubernetes Provider Implementation Summary

## Overview
This document summarizes the changes made to support the Kubernetes provider in the Computer class, allowing users to connect to pre-deployed Kubernetes pods running the CUA Ubuntu container.

## Changes Made

### 1. Updated `kubernetes/__init__.py`
- Added proper exports for `KubernetesProvider` and `HAS_KUBERNETES`
- Made the module importable from the factory

**File**: `libs/python/computer/computer/providers/kubernetes/__init__.py`

### 2. Updated `factory.py`
- Added handling for `VMProviderType.KUBERNETES` in the provider factory
- The factory now creates `KubernetesProvider` instances with the correct parameters
- Passes `host`, `vnc_port`, `api_port`, `image`, and other configuration to the provider

**File**: `libs/python/computer/computer/providers/factory.py`

### 3. Updated `computer.py`
- Added `vnc_port` parameter to the `Computer.__init__()` method as an alias for `noVNC_port`
- Added logic to use `vnc_port` if provided (for better compatibility with Docker/Kubernetes terminology)
- Updated docstring to document the new parameter and Kubernetes support
- The Computer class already had the infrastructure to handle Kubernetes provider (lines ~410-425)

**File**: `libs/python/computer/computer/computer.py`

### 4. Existing `KubernetesProvider` Implementation
The `KubernetesProvider` class was already partially implemented with:
- `get_vm()` - Returns VM info using the provided host IP
- `get_ip()` - Returns the host IP that was configured
- Proper provider type identification
- Context manager support

**File**: `libs/python/computer/computer/providers/kubernetes/provider.py`

## Usage

### Basic Example
```python
from computer import Computer

computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="10.244.0.5",  # Your pod IP
    vnc_port=6901,      # VNC web interface port
    api_port=8000,      # Computer server API port
)

# The computer instance will connect to your Kubernetes pod
await computer.start()
```

### With Custom Configuration
```python
from computer import Computer

computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="192.168.1.100",
    vnc_port=6901,
    api_port=8000,
    display="1920x1080",
    memory="4GB",
    cpu="2",
)

await computer.start()
```

## How It Works

1. **Provider Selection**: When `provider_type="kubernetes"` is specified, the factory creates a `KubernetesProvider` instance
2. **Host Configuration**: The `host` parameter is used as the pod IP address (no VM creation needed)
3. **Port Configuration**: 
   - `vnc_port` (or `noVNC_port`) specifies the VNC interface port (default: 6901)
   - `api_port` specifies the computer-server API port (default: 8000)
4. **Connection**: The Computer class connects directly to the specified host and ports

## Kubernetes Deployment Requirements

Your Kubernetes pod should:
1. Run the `trycua/cua-ubuntu:latest` image (or similar CUA container)
2. Expose port 6901 for the VNC web interface
3. Expose port 8000 for the computer-server API
4. Optionally expose port 5901 for the VNC server

### Example Kubernetes Deployment
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-cua-container
spec:
  containers:
  - name: cua
    image: trycua/cua-ubuntu:latest
    ports:
    - containerPort: 6901
      name: vnc-web
    - containerPort: 8000
      name: api
    - containerPort: 5901
      name: vnc-server
```

## Testing

Run the test script to verify the implementation:
```bash
cd /home/pv_rwm_models/workspace/trong/DEV/cua
python test_kubernetes_provider.py
```

## Key Design Decisions

1. **Minimal Changes**: The implementation reuses the existing Docker provider pattern
2. **No VM Management**: The Kubernetes provider doesn't create/destroy pods - it connects to existing ones
3. **Alias Parameter**: Added `vnc_port` as a more intuitive alias for `noVNC_port`
4. **Direct Connection**: Uses the provided host IP directly without additional discovery

## Future Enhancements

The following methods in `KubernetesProvider` are currently not implemented but could be added:
- `list_vms()` - List pods in the cluster
- `run_vm()` - Create new pods dynamically
- `stop_vm()` - Stop/delete pods
- `restart_vm()` - Restart pods

These can be implemented when needed using the Kubernetes Python client library.
