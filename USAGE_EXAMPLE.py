"""
Corrected usage example based on user's request.

The user wanted to use:
    computer = Computer(
        os_type="linux",
        provider_type="kubernetes",
        image="trycua/cua-ubuntu:latest",
        name="my-cua-container",
        host="my-pod-ip",
        vnc_port=6901;  # <-- NOTE: This had a semicolon which is wrong in Python
    )

Corrected version below:
"""

from computer import Computer

# ✅ CORRECT USAGE
computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="my-pod-ip",  # Replace with actual pod IP like "10.244.0.5"
    vnc_port=6901,     # ← Fixed: Use comma, not semicolon
    api_port=8000,     # Optional: Specify API port (default is 8000)
)

# Then use the computer:
# await computer.start()
# await computer.screenshot()
# etc.

print("""
✅ Implementation complete! You can now use:

from computer import Computer

computer = Computer(
    os_type="linux",
    provider_type="kubernetes",
    image="trycua/cua-ubuntu:latest",
    name="my-cua-container",
    host="10.244.0.5",  # Your Kubernetes pod IP
    vnc_port=6901,      # Note: comma, not semicolon
    api_port=8000,
)

await computer.start()
""")
