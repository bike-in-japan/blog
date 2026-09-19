ARG VARIANT=3.4-bookworm
FROM mcr.microsoft.com/devcontainers/ruby:${VARIANT}

USER root

# ENV Variables required by Jekyll
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    TZ=Etc/UTC \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US

# Install bundler, latest jekyll, and github-pages for older jekyll
RUN gem update --system

# https://github.com/ntkme/sass-embedded-host-ruby/issues/130
RUN gem install sass-embedded -v 1.62.1
RUN gem install jekyll-sass-converter -v 3.0.0
RUN gem install bundler jekyll github-pages

# Gems were installed as root into GEM_HOME=/usr/local/bundle, but the
# postCreateCommand runs `gem install`/`bundle install` as the non-root
# `vscode` user, so hand the gem home over to that user.
# (Replaces the obsolete chown of the removed /usr/local/rvm directory.)
RUN chown -R vscode:vscode "/usr/local/bundle"

# NOTE: The current devcontainers/ruby base image no longer uses rvm.
# Ruby lives in /usr/local/rubies (root:ruby, vscode is in the ruby group)
# and gems install to /usr/local/bundle (world-writable), so no manual
# chown/chmod of a gem directory is needed anymore.

COPY post-create.sh /usr/local/post-create.sh
RUN chmod +x /usr/local/post-create.sh

USER vscode

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1
