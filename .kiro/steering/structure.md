# Project Structure

## Directory Layout

```
hello-world-webapp/
├── app.py                 # Main FastAPI application with routes and handlers
├── config.py              # Pydantic settings with environment variable support
├── run.py                 # Development server launcher script
├── templates/             # Jinja2 HTML templates
│   └── hello.html         # Main hello world page template
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_app.py        # Application route and handler tests
│   ├── test_config.py     # Configuration tests
│   └── test_integration.py # Integration tests
├── scripts/               # Utility scripts
│   └── type_check.py      # Type checking helper
├── requirements.txt       # Python dependencies (pinned versions)
├── pyproject.toml         # Project metadata and tool configuration
├── mypy.ini              # Type checker configuration
├── .env.example          # Example environment variables
└── venv/                 # Virtual environment (not in git)
```

## Key Files

### app.py
- Application factory pattern: `create_app()` function
- Route handlers as async functions with full type annotations
- Custom exception handlers for HTTP errors
- Pydantic models for response validation (e.g., `HealthResponse`)

### config.py
- Single `Settings` class using Pydantic BaseSettings
- All settings have type annotations and Field descriptions
- Environment variables prefixed with `HELLO_`
- Global `get_settings()` function for dependency injection

### tests/
- Organized by test type (unit, integration)
- Test classes group related test cases
- Fixtures defined at module level
- All tests must pass before deployment

## Architecture Patterns

### Application Factory
Use `create_app()` function to instantiate FastAPI app, enabling easier testing and configuration.

### Dependency Injection
Settings loaded via `get_settings()` function, allowing easy mocking in tests.

### Typed Responses
All route handlers return typed responses (HTMLResponse, Pydantic models) for better IDE support and validation.

### Template Organization
HTML templates in `templates/` directory, referenced by name in route handlers.
