# Technology Stack

## Core Framework & Libraries

- **Python**: 3.12+ (required)
- **FastAPI**: Modern async web framework with automatic API documentation
- **Uvicorn**: ASGI server with hot reload support
- **Jinja2**: Template engine for HTML rendering
- **Pydantic**: Data validation and settings management (v2.8+)
- **Pydantic Settings**: Environment-based configuration

## Development Tools

- **pytest**: Testing framework with async support
- **mypy**: Static type checker (strict mode enabled)
- **httpx**: HTTP client for testing

## Environment Management

- **venv**: Python virtual environment (standard library)
- Configuration via environment variables or `.env` file
- All settings prefixed with `HELLO_` (e.g., `HELLO_HOST`, `HELLO_PORT`)

## Common Commands

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running
```bash
# Start development server (with hot reload)
python run.py

# Server runs on http://127.0.0.1:8000 by default
```

### Testing
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_app.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Type Checking
```bash
# Run mypy type checker (must pass with no errors)
mypy .
```

## Build Configuration

- **pyproject.toml**: Project metadata, dependencies, and tool configuration
- **mypy.ini**: Type checker configuration (strict mode)
- **requirements.txt**: Pinned dependencies for reproducible builds
