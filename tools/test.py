# /// script
# dependencies = [
#   "PyYAML",
# ]
# ///

import argparse
import os
import subprocess
import shutil
import yaml
from pathlib import Path

def get_baseurl(config_files: list[str]) -> str:
    """Extracts the baseurl from the given config files (reverse order)."""
    baseurl = ""
    for config_file in reversed(config_files):
        path = Path(config_file)
        if path.exists():
            with open(path, "r") as f:
                config = yaml.safe_load(f)
                if config and "baseurl" in config:
                    # Clean up baseurl: ensure it starts with / and ends with nothing
                    val = str(config["baseurl"]).strip().strip("'").strip('"')
                    if val and not val.startswith("/"):
                        val = f"/{val}"
                    baseurl = val.rstrip("/")
                    break
    return baseurl

def run_command(cmd: list[str], env: dict[str, str] | None = None) -> None:
    """Runs a shell command and raises an exception on failure."""
    print(f"\n> {' '.join(cmd)}\n")
    subprocess.run(cmd, env=env, check=True)

def main() -> None:
    parser = argparse.ArgumentParser(description="Build and test the site content")
    parser.add_argument("-c", "--config", default="_config.yml", help="Specify config file(s), comma separated")
    
    args = parser.parse_args()
    config_list = args.config.split(",")
    
    site_dir = Path("_site")
    
    # 1. Clean up
    if site_dir.exists():
        shutil.rmtree(site_dir)
        
    # 2. Read baseurl
    baseurl = get_baseurl(config_list)
    
    # 3. Build
    build_cmd = ["bundle", "exec", "jekyll", "b", "-d", str(site_dir / baseurl.strip("/")), "-c", args.config]
    env = os.environ.copy()
    env["JEKYLL_ENV"] = "production"
    run_command(build_cmd, env=env)
    
    # 4. Test
    test_cmd = [
        "bundle", "exec", "htmlproofer", str(site_dir / baseurl.strip("/")),
        "--disable-external",
        "--ignore-urls", "/^http:\/\/127.0.0.1/,/^http:\/\/0.0.0.0/,/^http:\/\/localhost/",
        "--swap-urls", f"^{baseurl}:"
    ]
    run_command(test_cmd)

if __name__ == "__main__":
    main()
