# GitHub Pages Deployment Learnings (Jekyll + Chirpy Theme)

This document summarizes the key findings and configurations required to fix the "pure HTML / broken scripts" issues when deploying a Jekyll site (specifically using the Chirpy theme) to GitHub Pages under a subdirectory (e.g., `/blog`) or a custom domain.

## 1. The `baseurl` and `url` Configuration
In `_config.yml`, ensure the following are correctly set:
- **`url`**: Should be the full domain (e.g., `https://bike-in-japan.de`). Do *not* include the trailing slash or the subdirectory.
- **`baseurl`**: Should be the path prefix (e.g., `/blog`). If the site is at the root of the domain, leave it empty (`""`).

## 2. GitHub Actions: Build Structure is Key
When deploying to a subdirectory like `/blog`, Jekyll generates links starting with `/blog/`. However, if you build into the root of `_site`, the physical files (like CSS/JS) won't be inside a `blog` folder.

**The Fix:** Build the site into a nested directory within `_site` that matches the `baseurl`.

```yaml
# In .github/workflows/pages-deploy.yml
- name: Build site
  run: bundle exec jekyll b -d "_site${{ steps.pages.outputs.base_path }}" --baseurl "${{ steps.pages.outputs.base_path }}"
```

By uploading the entire `_site` directory as an artifact, GitHub Pages will correctly serve `_site/blog/assets/...` at `https://domain.com/blog/assets/...`.

## 3. Don't Forget Submodules
The Chirpy theme often uses the `chirpy-static-assets` repository as a submodule for its core library files (in `assets/lib`). If these are missing, the site will fail to load scripts like `theme.min.js`.

**The Fix:** Enable submodule checkout in your workflow:
```yaml
- name: Checkout
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
    submodules: true # CRITICAL for Chirpy theme assets
```

## 4. Testing with `htmlproofer`
If you use `baseurl`, `htmlproofer` will fail to find internal links because it doesn't know how to map `/blog/assets/...` to your local file system.

**The Fix:** Use the `--swap-urls` flag to strip the prefix during testing:
```bash
bundle exec htmlproofer "_site/blog" --swap-urls "^/blog:"
```
*(Note: Swap `/blog` for an empty string, not `/`, to avoid double slashes like `//assets`.)*

## 5. PWA and "JSON.parse" Errors
If you see `Error: JSON.parse: unexpected character at line 1 column 1`, it usually means a script (like search or the service worker) tried to fetch a JSON file but received the `404.html` (or `index.html`) page instead. This is almost always caused by a `baseurl` mismatch in the path where the JSON file is expected.

## Summary Checklist
1. [ ] `url` in `_config.yml` matches the live domain.
2. [ ] `baseurl` in `_config.yml` matches the path prefix.
3. [ ] Workflow `Checkout` has `submodules: true`.
4. [ ] Workflow `Build` uses `-d "_site/baseurl"` and `--baseurl`.
5. [ ] Workflow `Test` uses `--swap-urls` matching the `baseurl`.
