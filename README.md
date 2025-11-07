# Hello World Web Application

A simple, well-typed Python web application that serves a "Hello World" page. Built with FastAPI to demonstrate modern Python web development with comprehensive type safety and testing.

## Features

- Clean HTML page displaying "Hello World"
- Health check endpoint for monitoring
- Full type annotations with mypy validation
- Graceful error handling (404, 500)
- Environment-based configuration
- Comprehensive test suite

## Requirements

- Python 3.12+
- pip

## Quick Start

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

Visit http://127.0.0.1:8000 to see the application.

**Available endpoints:**
- `/` - Hello World page
- `/health` - Health check endpoint
- `/docs` - API documentation

## Development

### Running Tests

```bash
pytest              # Run all tests
pytest -v           # Verbose output
pytest --cov=.      # With coverage
```

### Type Checking

```bash
mypy .
```

### Configuration

Configure via environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `HELLO_HOST` | `127.0.0.1` | Server host |
| `HELLO_PORT` | `8000` | Server port |
| `HELLO_DEBUG` | `True` | Debug mode |
| `HELLO_APP_NAME` | `Hello World Web App` | App name |
| `HELLO_APP_VERSION` | `0.1.0` | App version |

 
## Tech Stack

- **FastAPI** - Modern async web framework
- **Uvicorn** - ASGI server with hot reload
- **Jinja2** - Template engine
- **Pydantic** - Data validation and settings
- **pytest** - Testing framework
- **mypy** - Static type checker

## Troubleshooting

**Port already in use:**
```bash
HELLO_PORT=8080 python run.py
```

**Import errors:**
Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Virtual environment issues:**
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
