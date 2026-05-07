# /// script
# dependencies = [
#   "PyYAML",
#   "python-slugify",
# ]
# ///

import os
import re
import subprocess
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any
from slugify import slugify

def extract_meta(body: str, pattern: str) -> tuple[str | None, str]:
    """Extracts a metadata line from the body and returns (value, updated_body)."""
    match = re.search(pattern, body, re.IGNORECASE | re.MULTILINE)
    if match:
        value = match.group(1).strip()
        # Remove brackets if present
        value = re.sub(r'^\[(.*)\]$', r'\1', value).strip()
        # Remove the whole line from body
        updated_body = body[:match.start()] + body[match.end():]
        return value, updated_body.strip()
    return None, body

def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Runs a shell command and returns the result."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check)

def main() -> None:
    # Environment variables from GitHub Action
    title = os.environ.get("ISSUE_TITLE", "Untitled Post")
    body = os.environ.get("ISSUE_BODY", "")
    is_draft = os.environ.get("IS_DRAFT", "false").lower() == "true"

    # Extraction patterns
    tags, body = extract_meta(body, r'^(?:tag|tags):\s*(.*)$')
    categories, body = extract_meta(body, r'^(?:category|categories):\s*(.*)$')
    image_path, body = extract_meta(body, r'^image_path:\s*(.*)$')
    image_alt, body = extract_meta(body, r'^image_alt:\s*(.*)$')
    gpx_path_raw, body = extract_meta(body, r'^gpx:\s*(.*)$')

    # Process GPX
    if gpx_path_raw:
        gpx_path = Path(gpx_path_raw)
        if not gpx_path.exists():
            print(f"Error: GPX file '{gpx_path_raw}' not found.")
            exit(1)
        # Replace line with include (handled by extract_meta removing the line, now we prepend/append)
        body = f'{{% include gpx-map.html track="{gpx_path_raw}" %}}\n\n{body}'

    # Create Slug
    # python-slugify handles Umlaute by default if possible or we can use custom replaces
    slug = slugify(title)
    
    date_now = datetime.now()
    filename_date = date_now.strftime("%Y-%m-%d")
    post_date = date_now.strftime("%Y-%m-%d %H:%M:%S %z")
    if not post_date.endswith(" "): # Ensure timezone if empty
        post_date = date_now.strftime("%Y-%m-%d %H:%M:%S +0000")

    # Prepare Front Matter
    front_matter: dict[str, Any] = {
        "title": title,
        "date": post_date,
    }
    
    if categories:
        front_matter["categories"] = [c.strip() for c in categories.split(",")]
    if tags:
        front_matter["tags"] = [t.strip() for t in tags.split(",")]
    
    if image_path:
        front_matter["image"] = {"path": image_path}
        if image_alt:
            front_matter["image"]["alt"] = image_alt

    if is_draft:
        front_matter["published"] = False

    # Write Post
    posts_dir = Path("_posts")
    posts_dir.mkdir(exist_ok=True)
    post_file = posts_dir / f"{filename_date}-{slug}.md"
    
    with open(post_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(front_matter, f, allow_unicode=True, sort_keys=False)
        f.write("---\n\n")
        f.write(body)

    # Git Operations
    run_command(["git", "config", "--local", "user.email", "action@github.com"])
    run_command(["git", "config", "--local", "user.name", "GitHub Action"])
    run_command(["git", "add", str(post_file)])
    
    # Check for image assets
    asset_dir = Path(f"assets/img/posts/{slug}")
    if asset_dir.exists():
        run_command(["git", "add", str(asset_dir)])

    run_command(["git", "commit", "-m", f"Add new post: {title}"])
    run_command(["git", "push"])

    # Output post_url
    config_path = Path("_config.yml")
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            url = config.get("url", "").rstrip("/")
            baseurl = config.get("baseurl", "").strip("/")
            if baseurl:
                baseurl = f"/{baseurl}"
            post_url = f"{url}{baseurl}/posts/{slug}/"
            
            github_output = os.environ.get("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as go:
                    go.write(f"post_url={post_url}\n")

if __name__ == "__main__":
    main()
