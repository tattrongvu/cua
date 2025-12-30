"""
Direct module test to verify Kubernetes provider without going through __init__.py
"""

import sys
from pathlib import Path

# Add the libs/python/computer directory to sys.path
project_root = Path(__file__).parent
computer_lib = project_root / "libs" / "python" / "computer"
if str(computer_lib) not in sys.path:
    sys.path.insert(0, str(computer_lib))

def test_provider_type():
    """Test VMProviderType enum."""
    print("Testing VMProviderType enum...")
    # Import directly from the base module
    sys.path.insert(0, str(computer_lib / "computer" / "providers"))
    from base import VMProviderType
    
    assert hasattr(VMProviderType, 'KUBERNETES'), "KUBERNETES not in VMProviderType"
    assert VMProviderType.KUBERNETES == "kubernetes"
    print("✓ VMProviderType.KUBERNETES = 'kubernetes'")
    
    # List all provider types
    print("\nAvailable provider types:")
    for name in dir(VMProviderType):
        if not name.startswith('_'):
            value = getattr(VMProviderType, name)
            if isinstance(value, str):
                print(f"  - {name}: {value}")
    
    return True

def test_kubernetes_provider_class():
    """Test KubernetesProvider class."""
    print("\nTesting KubernetesProvider class...")
    sys.path.insert(0, str(computer_lib / "computer" / "providers" / "kubernetes"))
    from provider import KubernetesProvider
    
    # Create an instance
    provider = KubernetesProvider(
        host="10.0.0.100",
        image="trycua/cua-ubuntu:latest",
        vnc_port=6901,
        api_port=8000,
        verbose=True,
    )
    
    print("✓ KubernetesProvider instantiated")
    print(f"  - Provider type: {provider.provider_type}")
    print(f"  - Host: {provider.host}")
    print(f"  - VNC Port: {provider.vnc_port}")
    print(f"  - API Port: {provider.api_port}")
    print(f"  - Image: {provider.image}")
    
    return True

def test_factory_includes_kubernetes():
    """Test that factory.py includes Kubernetes handling."""
    print("\nChecking factory.py for Kubernetes support...")
    factory_path = computer_lib / "computer" / "providers" / "factory.py"
    
    with open(factory_path, 'r') as f:
        content = f.read()
    
    checks = [
        ("VMProviderType.KUBERNETES", "Kubernetes type check"),
        ("KubernetesProvider", "KubernetesProvider import/usage"),
        ("from .kubernetes import", "Kubernetes module import"),
    ]
    
    for check_str, description in checks:
        if check_str in content:
            print(f"✓ Found: {description}")
        else:
            print(f"✗ Missing: {description}")
            return False
    
    return True

def test_computer_py_includes_kubernetes():
    """Test that computer.py includes Kubernetes handling."""
    print("\nChecking computer.py for Kubernetes support...")
    computer_path = computer_lib / "computer" / "computer.py"
    
    with open(computer_path, 'r') as f:
        content = f.read()
    
    checks = [
        ("elif self.provider_type == VMProviderType.KUBERNETES:", "Kubernetes provider type handling"),
        ("vnc_port", "vnc_port parameter support"),
    ]
    
    for check_str, description in checks:
        if check_str in content:
            print(f"✓ Found: {description}")
        else:
            print(f"✗ Missing: {description}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 70)
    print("Kubernetes Provider Code Verification")
    print("=" * 70)
    
    tests = [
        ("VMProviderType enum", test_provider_type),
        ("KubernetesProvider class", test_kubernetes_provider_class),
        ("Factory includes Kubernetes", test_factory_includes_kubernetes),
        ("Computer.py includes Kubernetes", test_computer_py_includes_kubernetes),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 70)
        try:
            results.append(test_func())
        except Exception as e:
            print(f"✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 70)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 70)
    
    if all(results):
        print("\n✓ All verifications passed!")
        print("\n" + "=" * 70)
        print("Implementation Summary")
        print("=" * 70)
        print("""
The Kubernetes provider has been successfully implemented with:

1. VMProviderType.KUBERNETES enum value
2. KubernetesProvider class in providers/kubernetes/provider.py
3. Factory support in providers/factory.py
4. Computer class integration with vnc_port parameter

Usage Example:
--------------
from computer import Computer

computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="10.244.0.5",  # Your Kubernetes pod IP
    vnc_port=6901,      # VNC interface port
    api_port=8000,      # Computer server API port
)

await computer.start()

The Computer will connect to your pre-deployed Kubernetes pod at the
specified IP and ports.
""")
    else:
        print("\n✗ Some verifications failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
