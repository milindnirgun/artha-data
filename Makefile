UV_PROJECT_ENVIRONMENT := "$(HOME)/venvs/artha"
VENV_DIR := "$(HOME)/venvs/artha"
OLD_EXT := ".old"
export VENV_DIR UV_PROJECT_ENVIRONMENT

.PHONY: venv
venv:
	@if [ -d $(VENV_DIR) ]; then \
		echo "$(VENV_DIR) already exists, moving it to $(VENV_DIR)$(OLD_EXT)";\
		mv $(VENV_DIR) $(VENV_DIR)$(OLD_EXT);\
	fi
	@echo "🚀 Creating new virtual environment using uv."
	@uv run python -m venv $(VENV_DIR)
	@touch $(VENV_DIR)/.created

.PHONY: install
install: venv
	## Installing packages in virtual environment
	@echo "🚀 Installing packages in virtual environment $(VENV_DIR)"
	$(VENV_DIR)/bin/pip install -r requirements.txt

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
