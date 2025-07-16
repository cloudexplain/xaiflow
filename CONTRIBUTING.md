# Contributing to Xflow

Thank you for your interest in contributing to Xflow. This document outlines how to contribute to the project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/cloudexplain/xflow
cd xflow
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Project Structure

The project is organized as follows:
- `src/xflow/` - Main package code
- `tests/` - Test suites
- `dev/` - Development tools and frontend build scripts
- `pyproject.toml` - Package configuration
- `MANIFEST.in` - Package file inclusion rules

## Making Changes

### Code Style

We follow Python best practices:
- Use meaningful variable and function names
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Testing

Before submitting changes:
1. Run existing tests: `pytest tests/`
2. Add tests for new functionality
3. Test with a real MLflow experiment to ensure integration works

### Frontend Development

The frontend components are built with Svelte and compiled to `bundle.js`. If you need to modify the frontend:

1. Navigate to the `dev/` directory
2. Install Node.js dependencies: `npm install`
3. Make your changes to Svelte components
4. Build the bundle: `npm run build`
5. Copy the built files to `src/xflow/templates/assets/`

## Submitting Changes

1. Create a new branch for your feature or bug fix
2. Make your changes with clear commit messages
3. Test your changes thoroughly
4. Submit a pull request with a clear description of what you've changed

## Reporting Issues

When reporting issues, please include:
- Python version and operating system
- MLflow version
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Any error messages or logs

## Getting Help

If you need help with development or have questions about the codebase:
- Open an issue for discussion
- Check existing issues for similar problems
- Review the project documentation

## Code of Conduct

Please be respectful and constructive in all interactions. We want to maintain a welcoming environment for all contributors.