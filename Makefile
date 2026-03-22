# Makefile for Jekyll Chirpy Blog

# Variables
JEKYLL = bundle exec jekyll
TOOLS_DIR = tools

.PHONY: help install serve dev build test clean doctor

# Default target: show help
help:
	@echo "Chirpy Blog Management"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install      Install Ruby dependencies (bundle install)"
	@echo "  serve (dev)  Start local development server with live reload"
	@echo "  build        Build the site for production (JEKYLL_ENV=production)"
	@echo "  test         Build and test the site content (runs tools/test.sh)"
	@echo "  clean        Remove generated files (_site, .jekyll-cache)"
	@echo "  doctor       Run Jekyll doctor to check for configuration issues"
	@echo "  help         Show this help message"

install:
	bundle install

serve dev:
	bash $(TOOLS_DIR)/run.sh

build:
	JEKYLL_ENV=production $(JEKYLL) build

test:
	bash $(TOOLS_DIR)/test.sh

clean:
	$(JEKYLL) clean

doctor:
	$(JEKYLL) doctor
