# Gemini Project Context: Bike in Japan Blog

This project is a personal blog built with [Jekyll](https://jekyllrb.com/) and the [Chirpy theme](https://github.com/cotes2020/jekyll-theme-chirpy). It tracks a bike tour through Japan, featuring interactive maps with GPX tracks and location markers.

## Project Overview

- **Core Technologies:** Jekyll, Ruby (Bundler), Liquid templates, SCSS, JavaScript.
- **Theme:** `jekyll-theme-chirpy` (v7.4+).
- **Key Features:** 
  - Automated post creation via GitHub Issues.
  - Interactive GPX track maps (using Leaflet/custom includes).
  - Geographic location markers stored in `_data/geopoints.yml`.
  - Multi-language support (defaulting to `de-DE`).

## Architecture & Structure

- `_posts/`: Blog posts in Markdown format. Naming convention: `YYYY-MM-DD-title.md`.
- `_data/`: Configuration data (contact info, geopoints, share settings, locales).
- `_includes/`: Reusable HTML snippets, including custom ones like `gpx-map.html`.
- `assets/gpx/`: Storage for `.gpx` track files used in posts.
- `_plugins/`: Custom Jekyll plugins (e.g., `posts-lastmod-hook.rb` for tracking last modified dates).
- `tools/`: Shell and Python scripts for automation and local development.
- `.github/workflows/`: GitHub Actions for CI/CD and automation (e.g., creating posts from issues).

## Building and Running

The project includes a `Makefile` for common tasks:

- **Install Dependencies:**
  ```bash
  make install
  ```
  *(Runs `bundle install`)*

- **Local Development:**
  ```bash
  make serve
  # OR
  make dev
  ```
  *(Runs `tools/run.sh`, starting Jekyll with live reload at `http://127.0.0.1:4000/blog/`)*

- **Build for Production:**
  ```bash
  make build
  ```
  *(Sets `JEKYLL_ENV=production` and runs `jekyll build`)*

- **Run Tests:**
  ```bash
  make test
  ```
  *(Builds the site and runs `html-proofer` via `tools/test.sh`)*

- **Clean Build Artifacts:**
  ```bash
  make clean
  ```

## Development Conventions

### Creating Posts
Posts can be created manually in `_posts/` or via the GitHub Issue automation described in `README.md`.
- **Front Matter:** Ensure `layout: post` is set (usually handled by defaults in `_config.yml`).
- **GPX Tracks:** To include a map, add `gpx: assets/gpx/filename.gpx` to the front matter.

### Adding Locations
Locations for the global map are stored in `_data/geopoints.yml`. These can be added via the `new-location` GitHub Issue label or by manually updating the YAML file.

### Coding Style
- Follow standard Jekyll and Chirpy theme conventions.
- Custom styles should be added to `assets/css/jekyll-theme-chirpy.scss`.
- Use `.editorconfig` for consistent formatting.

## Automation Tools
- `tools/create-post.sh`: Bash script to generate post files from templates.
- `tools/add-location.py`: Python script to process coordinates and update geographic data.
- `tools/run.sh`: Wrapper for `jekyll serve` with polling support for Docker/WSL.
