# /// script
# dependencies = []
# ///

import argparse
import os
import subprocess
from pathlib import Path

def is_docker() -> bool:
    """Detects if the script is running inside a Docker container."""
    cgroup = Path("/proc/1/cgroup")
    if cgroup.exists():
        with open(cgroup, "r") as f:
            return "docker" in f.read()
    
    # Alternative check for newer Docker/cgroup v2
    mountinfo = Path("/proc/self/mountinfo")
    if mountinfo.exists():
        with open(mountinfo, "r") as f:
            return "docker" in f.read()
            
    return False

def main() -> None:
    parser = argparse.ArgumentParser(description="Run jekyll serve and then launch the site")
    parser.add_index = False # Avoid argparse adding its own index
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Host to bind to.")
    parser.add_argument("-p", "--production", action="store_true", help="Run Jekyll in 'production' mode.")
    
    args = parser.parse_args()

    command = ["bundle", "exec", "jekyll", "s", "-l", "-H", args.host]
    
    env = os.environ.copy()
    if args.production:
        env["JEKYLL_ENV"] = "production"

    if is_docker():
        command.append("--force_polling")

    print(f"\n> {' '.join(command)}\n")
    
    try:
        subprocess.run(command, env=env, check=True)
    except KeyboardInterrupt:
        print("\nStopping Jekyll server...")
    except subprocess.CalledProcessError as e:
        print(f"\nError: Jekyll serve failed with exit code {e.returncode}")

if __name__ == "__main__":
    main()
