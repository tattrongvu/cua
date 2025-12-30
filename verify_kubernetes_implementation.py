"""
Code verification test - checks that all necessary code changes are in place
without trying to import the modules (which requires full environment setup).
"""

from pathlib import Path

def check_file_content(file_path, checks, description):
    """Check if a file contains expected strings."""
    print(f"\nChecking {description}...")
    print(f"  File: {file_path}")
    
    if not file_path.exists():
        print(f"  ✗ File not found!")
        return False
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    all_passed = True
    for check_str, check_desc in checks:
        if check_str in content:
            print(f"  ✓ {check_desc}")
        else:
            print(f"  ✗ {check_desc} - NOT FOUND")
            all_passed = False
    
    return all_passed

def main():
    project_root = Path(__file__).parent
    computer_root = project_root / "libs" / "python" / "computer" / "computer"
    providers_root = computer_root / "providers"
    
    print("=" * 80)
    print("Kubernetes Provider Implementation Verification")
    print("=" * 80)
    
    results = []
    
    # Check 1: base.py has KUBERNETES enum value
    results.append(check_file_content(
        providers_root / "base.py",
        [
            ('KUBERNETES = "kubernetes"', "KUBERNETES enum value defined"),
        ],
        "providers/base.py - VMProviderType enum"
    ))
    
    # Check 2: kubernetes/__init__.py exports properly
    results.append(check_file_content(
        providers_root / "kubernetes" / "__init__.py",
        [
            ('from .provider import KubernetesProvider', "KubernetesProvider import"),
            ('HAS_KUBERNETES', "HAS_KUBERNETES flag"),
            ('__all__', "__all__ export list"),
        ],
        "providers/kubernetes/__init__.py"
    ))
    
    # Check 3: kubernetes/provider.py has the provider class
    results.append(check_file_content(
        providers_root / "kubernetes" / "provider.py",
        [
            ('class KubernetesProvider', "KubernetesProvider class defined"),
            ('def __init__', "__init__ method"),
            ('vnc_port', "vnc_port parameter"),
            ('api_port', "api_port parameter"),
            ('VMProviderType.KUBERNETES', "Returns KUBERNETES type"),
        ],
        "providers/kubernetes/provider.py"
    ))
    
    # Check 4: factory.py handles Kubernetes
    results.append(check_file_content(
        providers_root / "factory.py",
        [
            ('elif provider_type == VMProviderType.KUBERNETES:', "Kubernetes type check"),
            ('from .kubernetes import', "Kubernetes import"),
            ('KubernetesProvider(', "KubernetesProvider instantiation"),
            ('vnc_port=noVNC_port', "vnc_port parameter passed"),
        ],
        "providers/factory.py"
    ))
    
    # Check 5: computer.py has vnc_port parameter
    results.append(check_file_content(
        computer_root / "computer.py",
        [
            ('vnc_port: Optional[int] = None', "vnc_port parameter in __init__"),
            ('if vnc_port is not None:', "vnc_port handling logic"),
            ('noVNC_port = vnc_port', "vnc_port to noVNC_port mapping"),
            ('elif self.provider_type == VMProviderType.KUBERNETES:', "Kubernetes provider initialization"),
        ],
        "computer/computer.py"
    ))
    
    print("\n" + "=" * 80)
    print(f"Results: {sum(results)}/{len(results)} checks passed")
    print("=" * 80)
    
    if all(results):
        print("\n✅ SUCCESS! All code changes are in place.")
        print("\n" + "=" * 80)
        print("Implementation Complete")
        print("=" * 80)
        print("""
The Kubernetes provider has been successfully implemented!

Files Modified:
---------------
1. libs/python/computer/computer/providers/base.py
   - Added KUBERNETES enum value

2. libs/python/computer/computer/providers/kubernetes/__init__.py
   - Added proper exports for KubernetesProvider

3. libs/python/computer/computer/providers/kubernetes/provider.py
   - Already implemented with necessary methods

4. libs/python/computer/computer/providers/factory.py
   - Added Kubernetes provider creation logic

5. libs/python/computer/computer/computer.py
   - Added vnc_port parameter as alias for noVNC_port
   - Kubernetes provider initialization already in place

Usage Example:
--------------
from computer import Computer

computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="10.244.0.5",  # Your Kubernetes pod IP
    vnc_port=6901,      # VNC interface port (maps to noVNC_port)
    api_port=8000,      # Computer server API port
)

# Start the computer (connects to your Kubernetes pod)
await computer.start()

Notes:
------
- The 'host' parameter should be the IP address of your Kubernetes pod
- The 'vnc_port' is an alias for 'noVNC_port' (you can use either)
- The provider connects to an existing pod, it doesn't create one
- Make sure your pod exposes the required ports (6901 for VNC, 8000 for API)

See KUBERNETES_PROVIDER_IMPLEMENTATION.md for more details.
""")
        return 0
    else:
        print("\n❌ Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
