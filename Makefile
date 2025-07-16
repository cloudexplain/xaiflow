# Makefile for CE MLflow Extension

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies (Node.js + Python)"
	@echo "  make build          - Build Svelte components to bundle.js"
	@echo "  make test           - Generate a basic test HTML report"
	@echo "  make test-importance - Generate a test report with ImportanceChart"
	@echo "  make clean          - Clean generated files"
	@echo "  make dev            - Build in development mode with watch"
	@echo "  make all            - Install, build, and test"

# Install dependencies
.PHONY: install
install: install-node install-python

.PHONY: install-node
install-node:
	@echo "Installing Node.js dependencies..."
	npm install

.PHONY: install-python
install-python:
	@echo "Installing Python dependencies..."
	source .venv/bin/activate && pip install -r requirements.txt

# Build Svelte components
.PHONY: build
build:
	@echo "Building Svelte components..."
	npm run build
	@echo "✅ Bundle.js generated successfully!"

# Development build with watch mode
.PHONY: dev
dev:
	@echo "Starting development build with watch mode..."
	npm run dev

# Generate test report
.PHONY: test
test: build
	@echo "Generating test HTML report..."
	.venv/bin/python test_simple.py
	@echo "✅ Test report generated!"

# Generate importance chart test report
.PHONY: test-importance
test-importance: build
	@echo "Generating ImportanceChart test report..."
	.venv/bin/python test_importance.py
	@echo "✅ ImportanceChart test report generated!"

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	rm -f src/ce_mlflow_extension/templates/assets/bundle.js
	rm -f src/ce_mlflow_extension/templates/assets/bundle.js.map
	rm -f *.html
	rm -rf node_modules/.cache
	@echo "✅ Cleaned!"

# Full workflow
.PHONY: all
all: install build test
	@echo "✅ Complete workflow finished!"

# Check if bundle.js exists
.PHONY: check-bundle
check-bundle:
	@if [ -f "src/ce_mlflow_extension/templates/assets/bundle.js" ]; then \
		echo "✅ bundle.js exists"; \
		ls -la src/ce_mlflow_extension/templates/assets/bundle.js; \
	else \
		echo "❌ bundle.js not found. Run 'make build' first."; \
		exit 1; \
	fi

# Show project status
.PHONY: status
status:
	@echo "=== Project Status ==="
	@echo "Node.js dependencies:"
	@if [ -d "node_modules" ]; then echo "✅ Installed"; else echo "❌ Not installed (run 'make install-node')"; fi
	@echo "Python virtual environment:"
	@if [ -d ".venv" ]; then echo "✅ Found"; else echo "❌ Not found"; fi
	@echo "Svelte bundle:"
	@if [ -f "src/ce_mlflow_extension/templates/assets/bundle.js" ]; then echo "✅ Built"; else echo "❌ Not built (run 'make build')"; fi
