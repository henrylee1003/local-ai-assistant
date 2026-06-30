print("Hello from inside a Docker container!")
import platform
print(f"Python version: {platform.python_version()}")
print(f"System: {platform.system()}")
print("這行是新加的，沒有重新 build")
