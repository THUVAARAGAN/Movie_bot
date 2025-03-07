import subprocess
import sys

required_packages = [
    "openai==0.28",
    "pandas",
    "python-dotenv",
    "flask"
]

for package in required_packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

