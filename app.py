from typing import Dict, Any, Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import time
from config import get_settings

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load application settings
settings = get_settings()


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    message: str
    timestamp: float
    app_name: str
    app_version: str


def create_app() -> FastAPI:
    """
    Application factory function that creates and configures the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Hello World Web Application",
        description="A simple web application that displays Hello World",
        version="1.0.0"
    )
    
    # Add exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(500, internal_server_error_handler)
    
    # Add routes
    app.add_api_route("/", get_hello_page, methods=["GET"], response_class=HTMLResponse, response_model=None)
    app.get("/health", response_model=HealthResponse)(get_health_check)
    
    return app


async def get_hello_page(request: Request) -> HTMLResponse:
    """
    Route handler for the hello world page.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        HTMLResponse: Rendered HTML template with Hello World message
    """
    context: Dict[str, Any] = {
        "request": request,
        "message": "Hello World"
    }
    return templates.TemplateResponse("hello.html", context)


async def get_health_check() -> HealthResponse:
    """
    Health check endpoint that returns application status and basic information.
    
    This endpoint provides:
    - Application status (always "healthy" for this simple app)
    - Current timestamp for response time verification
    - Application name and version from configuration
    - Responds within performance requirements (< 1 second)
    
    Returns:
        HealthResponse: Typed response with application health information
    """
    return HealthResponse(
        status="healthy",
        message="Hello World Web Application is running",
        timestamp=time.time(),
        app_name=settings.app_name,
        app_version=settings.app_version
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """
    Custom HTTP exception handler with typed response.
    
    Args:
        request: FastAPI Request object
        exc: HTTPException instance
        
    Returns:
        HTMLResponse: Formatted error page
    """
    error_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Error {exc.status_code}</title>
    </head>
    <body>
        <h1>Error {exc.status_code}</h1>
        <p>{exc.detail}</p>
    </body>
    </html>
    """
    return HTMLResponse(content=error_content, status_code=exc.status_code)


async def not_found_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """
    Custom 404 error handler.
    
    Args:
        request: FastAPI Request object
        exc: HTTPException instance
        
    Returns:
        HTMLResponse: 404 error page
    """
    error_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Not Found</title>
    </head>
    <body>
        <h1>404 - Page Not Found</h1>
        <p>The requested page could not be found.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=error_content, status_code=404)


async def internal_server_error_handler(request: Request, exc: Exception) -> HTMLResponse:
    """
    Custom 500 error handler.
    
    Args:
        request: FastAPI Request object
        exc: Exception instance
        
    Returns:
        HTMLResponse: 500 error page
    """
    error_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Internal Server Error</title>
    </head>
    <body>
        <h1>500 - Internal Server Error</h1>
        <p>An internal server error occurred.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=error_content, status_code=500)


# Create the application instance
app = create_app()


def main() -> None:
    """
    Application startup function for development.
    """
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()