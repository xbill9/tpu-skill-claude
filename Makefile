# Root Makefile for managing all subdirectories

# Dynamically discover all subdirectories containing a Makefile
SUBDIRS := $(patsubst %/,%,$(dir $(wildcard */Makefile)))

SKILL_DIR := .claude/skills/tpu-management
DIST_DIR  := dist

.PHONY: all clean test lint install deploy help init skill skill-install skill-package $(SUBDIRS)

# Default target displays help information
all: help

help:
	@echo "========================================================="
	@echo " Gemma-4 DevOps Agents - Root Makefile"
	@echo "========================================================="
	@echo "Available commands:"
	@echo "  make clean   - Run 'make clean' in all subdirectories"
	@echo "  make test    - Run 'make test' in all subdirectories"
	@echo "  make lint    - Run 'make lint' in all subdirectories"
	@echo "  make install - Run 'make install' in all subdirectories"
	@echo "  make deploy  - Run 'make deploy' in all subdirectories"
	@echo "  make skill         - Refresh tpu-management skill snapshots from server.py / tpu.md"
	@echo "  make skill-install - Refresh + copy the skill to ~/.claude/skills (all projects)"
	@echo "  make skill-package - Refresh + build dist/tpu-management-skill.zip"
	@echo "  make init TARGET=/path/to/project [ARGS='--project my-gcp-id']"
	@echo "                     - Refresh + install skill AND register the tpu-devops MCP"
	@echo "                       server in TARGET (or globally with ARGS='--global')"
	@echo "========================================================="

init: skill
	@if [ -z "$(TARGET)" ] && ! echo "$(ARGS)" | grep -q -- --global; then \
		echo "usage: make init TARGET=/path/to/project [ARGS='--project my-gcp-id ...']"; \
		echo "   or: make init ARGS='--global ...'"; \
		exit 1; \
	fi
	./project-setup.sh $(TARGET) $(ARGS)

skill:
	python3 refresh_skill.py

skill-install: skill
	mkdir -p $(HOME)/.claude/skills
	rm -rf $(HOME)/.claude/skills/tpu-management
	cp -r $(SKILL_DIR) $(HOME)/.claude/skills/tpu-management
	@echo "Installed to $(HOME)/.claude/skills/tpu-management"

skill-package: skill
	mkdir -p $(DIST_DIR)
	rm -f $(DIST_DIR)/tpu-management-skill.zip
	cd $(dir $(SKILL_DIR)) && zip -qr $(CURDIR)/$(DIST_DIR)/tpu-management-skill.zip $(notdir $(SKILL_DIR))
	@echo "Packaged $(DIST_DIR)/tpu-management-skill.zip"
	@unzip -l $(DIST_DIR)/tpu-management-skill.zip

# Target-specific variable assignments
clean: TARGET := clean
clean: $(SUBDIRS)

test: TARGET := test
test: $(SUBDIRS)

lint: TARGET := lint
lint: $(SUBDIRS)

install: TARGET := install
install: $(SUBDIRS)

deploy: TARGET := deploy
deploy: $(SUBDIRS)

# Run the specified target in each subdirectory if a Makefile exists
$(SUBDIRS):
	@if [ -f $@/Makefile ]; then \
		if [ -z "$(TARGET)" ]; then \
			echo "⚙️ Executing default target in $@..."; \
			$(MAKE) -C $@; \
		else \
			echo "⚙️ Executing 'make $(TARGET)' in $@..."; \
			$(MAKE) -C $@ $(TARGET); \
		fi \
	fi
