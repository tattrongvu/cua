# Kubernetes Provider - Quick Start Guide

## ✅ Implementation Complete

All necessary code changes have been implemented to support connecting to CUA containers running in Kubernetes.

## 📝 What Was Changed

### 1. **providers/kubernetes/__init__.py**
- Added proper exports for `KubernetesProvider` and `HAS_KUBERNETES`

### 2. **providers/factory.py**
- Added handling for `VMProviderType.KUBERNETES`
- Factory can now create `KubernetesProvider` instances

### 3. **computer/computer.py**
- Added `vnc_port` parameter as an alias for `noVNC_port` (for better compatibility)
- Updated docstrings to document Kubernetes support

### 4. **Existing Files**
- `providers/base.py` already had `KUBERNETES` enum value
- `providers/kubernetes/provider.py` already had the provider implementation
- `computer.py` already had Kubernetes initialization logic (lines ~410-425)

## 🚀 Usage

### Basic Example

```python
from computer import Computer

computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="10.244.0.5",  # Your pod IP
    vnc_port=6901,      # VNC interface port
    api_port=8000,      # Computer server API port
)

await computer.start()
```

### Parameters

- **os_type**: `"linux"` (required for Kubernetes)
- **provider_type**: `"kubernetes"` (required)
- **image**: Container image name (default: `"trycua/cua-ubuntu:latest"`)
- **name**: Name for the computer instance
- **host**: IP address of your Kubernetes pod (required)
- **vnc_port**: Port for VNC web interface (default: 6901)
- **api_port**: Port for computer-server API (default: 8000)
- **display**: Display resolution (default: "1024x768")
- **verbosity**: Logging level (0-4, default: 1)

## 🎯 How to Get Your Pod IP

```bash
# Method 1: Using kubectl
kubectl get pod my-cua-container -o jsonpath='{.status.podIP}'

# Method 2: Describe the pod
kubectl describe pod my-cua-container | grep IP:

# Method 3: Using kubectl with custom columns
kubectl get pods -o custom-columns=NAME:.metadata.name,IP:.status.podIP
```

## 📦 Kubernetes Deployment Example

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
      protocol: TCP
    - containerPort: 8000
      name: api
      protocol: TCP
    - containerPort: 5901
      name: vnc-server
      protocol: TCP
```

To deploy:
```bash
kubectl apply -f cua-pod.yaml
```

## 🧪 Verification

Run the verification script:
```bash
python verify_kubernetes_implementation.py
```

Expected output: `✅ SUCCESS! All code changes are in place.`

## 📖 Full Example

See `examples/kubernetes_example.py` for a complete working example.

## 🔍 Key Points

1. **No VM Creation**: The Kubernetes provider connects to existing pods, it doesn't create them
2. **Direct Connection**: Uses the pod IP directly without service discovery
3. **Port Requirements**: Your pod must expose ports 6901 (VNC) and 8000 (API)
4. **vnc_port vs noVNC_port**: Both work the same way, `vnc_port` is just an alias

## 🛠️ Troubleshooting

### Can't connect to pod
- Verify the pod IP is correct: `kubectl get pod <name> -o jsonpath='{.status.podIP}'`
- Check pod is running: `kubectl get pod <name>`
- Verify ports are exposed: `kubectl describe pod <name>`

### Connection timeout
- Check if computer-server is running inside the pod
- Verify network policies allow traffic to the pod
- Test with port-forward: `kubectl port-forward pod/<name> 8000:8000`

### Import errors during development
- The provider requires the full CUA environment to run
- For testing without full setup, use `verify_kubernetes_implementation.py`

## 📚 Additional Resources

- Full implementation details: `KUBERNETES_PROVIDER_IMPLEMENTATION.md`
- Working example: `examples/kubernetes_example.py`
- Verification script: `verify_kubernetes_implementation.py`
