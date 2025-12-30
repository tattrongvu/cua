"""
Example: Using Computer with Kubernetes Provider

This example demonstrates how to connect to a CUA container running in Kubernetes.

Prerequisites:
--------------
1. Deploy a CUA Ubuntu container in your Kubernetes cluster
2. Expose ports: 6901 (VNC), 8000 (API), 5901 (VNC server)
3. Get the pod IP address

Example Kubernetes Deployment:
-------------------------------
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
"""

import asyncio
from computer import Computer


async def main():
    # Replace with your actual pod IP
    POD_IP = "10.244.0.5"
    
    print(f"Connecting to Kubernetes pod at {POD_IP}...")
    
    # Create Computer instance pointing to your Kubernetes pod
    computer = Computer(
        os_type="linux",
        provider_type="kubernetes",
        image="trycua/cua-ubuntu:latest",
        name="my-cua-container",
        host=POD_IP,           # IP address of your Kubernetes pod
        vnc_port=6901,         # VNC interface port
        api_port=8000,         # Computer server API port
        display="1920x1080",   # Display resolution
        verbosity=2,           # Verbose logging
    )
    
    # Start the computer (connects to the pod)
    await computer.start()
    print("Connected to Kubernetes pod!")
    
    # Now you can use the computer as normal
    
    # Example: Take a screenshot
    print("\nTaking screenshot...")
    screenshot = await computer.screenshot()
    screenshot.save("kubernetes_computer_screenshot.png")
    print("Screenshot saved!")
    
    # Example: Execute a shell command
    print("\nExecuting command...")
    result = await computer.shell("echo 'Hello from Kubernetes!'")
    print(f"Command output: {result}")
    
    # Example: Click at a position
    print("\nMoving mouse...")
    await computer.mouse_click(100, 100)
    
    # Example: Type some text
    print("\nTyping text...")
    await computer.keyboard_type("Hello from the Computer API!")
    
    print("\nAll operations completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
