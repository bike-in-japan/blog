# A blog using Jekyll and the Chirpy theme

Check out the [theme's docs](https://github.com/cotes2020/jekyll-theme-chirpy/wiki).

[![Gem Version](https://img.shields.io/gem/v/jekyll-theme-chirpy)][gem]&nbsp;
[![GitHub license](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)][mit]

## Usage


## Automation Workflows

This repository uses GitHub Actions to automate content creation. You can trigger these workflows by creating a GitHub Issue and applying specific labels.

### 1. How to create a post

To create a new blog post via GitHub Issues:

1.  **Open an Issue**: Create a new issue in this repository.
2.  **Title**: The issue title will be used as the post title.
3.  **Content**:
    *   **Tags**: Add a line like `tags: tag1, tag2`.
    *   **Categories**: Add a line like `categories: cat1, cat2`.
    *   **GPX Track**: To include an interactive map:
        1.  Upload your `.gpx` file to `assets/gpx/`.
        2.  Add a line in the issue body: `gpx: assets/gpx/your-track.gpx`.
    *   **Image**: To include a header image for the post:
        *   Add a line `image_path: https://github.com/user-attachments/assets/...` (or a local path).
        *   Add a line `image_alt: A description of the image`.
    *   **Body**: The rest of the issue body will be the post content.
4.  **Labels**: 
    *   Add the `new-post` label to trigger the creation.
    *   Add the `draft` label (optional) to set `published: false` in the post's front matter, keeping it hidden from the live site until manually published.
5.  **Automation**: A GitHub Action will create the post, commit it, and close the issue with a link to the new post.

**Example Issue Body:**
```text
tags: skitour, outdoor
categories: winter, switzerland
image_path: https://github.com/user-attachments/assets/ff368f4c-a4ce-4777-85c6-010b188d66e5
image_alt: Osterschmuck an Kirche
gpx: assets/gpx/bettmerhorn.gpx

This was an amazing day at the Aletschgletscher! The weather was perfect.
```

### 2. How to add a location

To add a new marker to the interactive map:

1.  **Open an Issue**: Create a new issue.
2.  **Title**: The name of the location (e.g., "Tokyo Tower").
3.  **Content**: Provide the coordinates in one of the following formats:
    *   **Google Maps Link**: `https://www.google.com/maps?q=35.658,139.745`
    *   **OpenStreetMap Link**: `https://www.openstreetmap.org/#map=19/35.658/139.745`
    *   **Raw Coordinates**: `35.658, 139.745`
4.  **Label**: Add the `new-location` label.
5.  **Automation**: The coordinates will be extracted and added to `_data/geopoints.yml`.

**Example Issue Body:**
```text
35.658, 139.745
```

## Contributing

This repository is automatically updated with new releases from the theme repository. If you encounter any issues or want to contribute to its improvement, please visit the [theme repository][chirpy] to provide feedback.

## Local development

See the [Jekyll documentation](https://jekyllrb.com/docs/installation/) to get started

## License

This work is published under [MIT][mit] License.

[gem]: https://rubygems.org/gems/jekyll-theme-chirpy
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[CD]: https://en.wikipedia.org/wiki/Continuous_deployment
[mit]: https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE
