# Contributing to Nvidia NeMo Guardrails

Thank you for your interest in contributing to the Nvidia NeMo Guardrails project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up the development environment** (see below)
4. **Create a feature branch** for your changes
5. **Make your changes** following the guidelines below
6. **Test your changes** thoroughly
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Installation

```bash
# Clone your fork
git clone https://github.com/yourusername/nvidia-nemo-guardrails.git
cd nvidia-nemo-guardrails

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Environment Variables

Create a `.env` file in the root directory:

```bash
# API Configuration
OPENAI_API_KEY=your_openai_api_key
NEMO_GUARDRAILS_API_KEY=your_nemo_api_key

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/nemo_guardrails

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Development
DEBUG=True
ENVIRONMENT=development
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues and improve reliability
- **New features**: Add new functionality
- **Documentation**: Improve docs, tutorials, and examples
- **Tests**: Add or improve test coverage
- **Performance**: Optimize code and improve efficiency
- **Security**: Identify and fix security issues

### Before You Start

1. **Check existing issues** to avoid duplicates
2. **Discuss major changes** in an issue first
3. **Follow the project structure** and conventions
4. **Keep changes focused** and atomic

### Commit Message Guidelines

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(api): add content safety endpoint
fix(engine): resolve memory leak in safety checks
docs(readme): update installation instructions
test(guardrails): add integration tests
```

## Pull Request Process

### Before Submitting

1. **Ensure tests pass** locally
2. **Update documentation** if needed
3. **Add tests** for new functionality
4. **Follow code style** guidelines
5. **Squash commits** if needed

### Pull Request Template

Use the provided pull request template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Security fix

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes

## Related Issues
Closes #123
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Address feedback** and make changes
4. **Maintainer approval** required
5. **Merge** when ready

## Code Style

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these additions:

- **Line length**: 88 characters (Black default)
- **Docstrings**: Google style
- **Type hints**: Required for public APIs
- **Imports**: Grouped and sorted

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 src/ tests/

# Configuration in setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

### Type Checking

We use [mypy](http://mypy-lang.org/) for type checking:

```bash
# Run type checker
mypy src/

# Configuration in mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
```

## Testing

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── fixtures/      # Test fixtures
└── conftest.py    # Pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_guardrails.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests
pytest tests/integration/

# Run e2e tests
pytest tests/e2e/
```

### Writing Tests

Follow these guidelines:

1. **Test naming**: Descriptive test names
2. **Test isolation**: Each test should be independent
3. **Fixtures**: Use pytest fixtures for common setup
4. **Mocking**: Mock external dependencies
5. **Coverage**: Aim for >90% coverage

Example test:

```python
import pytest
from nemo_guardrails import GuardrailsEngine

@pytest.fixture
def engine():
    return GuardrailsEngine()

class TestGuardrailsEngine:
    async def test_check_content_safe(self, engine):
        """Test content safety check with safe content."""
        result = await engine.check_content("Hello, world!")
        assert result.safe is True
        assert result.score > 0.8

    async def test_check_content_unsafe(self, engine):
        """Test content safety check with unsafe content."""
        result = await engine.check_content("Harmful content here")
        assert result.safe is False
        assert len(result.violations) > 0
```

## Documentation

### Documentation Structure

```
docs/
├── api-reference.md      # API documentation
├── contributing.md       # This file
├── deployment.md         # Deployment guide
├── examples/            # Code examples
├── guides/              # User guides
└── project-plan.md      # Project roadmap
```

### Writing Documentation

1. **Clear and concise**: Write for the target audience
2. **Code examples**: Include working examples
3. **Keep updated**: Update docs with code changes
4. **Use markdown**: Follow markdown best practices

### Building Documentation

```bash
# Install docs dependencies
pip install -r requirements-docs.txt

# Build documentation
mkdocs build

# Serve locally
mkdocs serve
```

## Reporting Issues

### Bug Reports

Use the bug report template:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Version: [e.g., 0.1.0]

## Additional Information
Screenshots, logs, etc.
```

### Security Issues

For security issues, please email security@example.com instead of creating a public issue.

## Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Solution
How the feature should work

## Alternatives Considered
Other approaches considered

## Additional Information
Screenshots, mockups, etc.
```

## Getting Help

- **Documentation**: Check the docs first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Chat**: Join our community chat

## Recognition

Contributors will be recognized in:

- **README.md**: List of contributors
- **Release notes**: Credit for contributions
- **Documentation**: Author attribution

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

If you have questions about contributing, please:

1. Check this document first
2. Search existing issues and discussions
3. Create a new discussion or issue
4. Contact the maintainers directly

Thank you for contributing to Nvidia NeMo Guardrails! 