"""Unit tests for the main FastAPI application.

Tests route handlers, response content, status codes, and core functionality
using FastAPI TestClient as specified in requirements 1.1, 1.2, and 3.1.
"""

import pytest
from fastapi.testclient import TestClient
from app import create_app, HealthResponse
import time


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    app = create_app()
    return TestClient(app)


class TestHelloWorldRoute:
    """Test cases for the hello world route handler."""
    
    def test_get_hello_page_returns_200(self, client):
        """Test that the hello page returns HTTP 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_get_hello_page_returns_html(self, client):
        """Test that the hello page returns HTML content."""
        response = client.get("/")
        assert response.headers["content-type"] == "text/html; charset=utf-8"
    
    def test_get_hello_page_contains_hello_world(self, client):
        """Test that the hello page contains 'Hello World' message."""
        response = client.get("/")
        assert "Hello World" in response.text
    
    def test_get_hello_page_response_time(self, client):
        """Test that the hello page responds within 1 second (requirement 3.1)."""
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0


class TestHealthCheckRoute:
    """Test cases for the health check endpoint."""
    
    def test_health_check_returns_200(self, client):
        """Test that health check returns HTTP 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON content."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_check_response_structure(self, client):
        """Test that health check returns proper response structure."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "message" in data
        assert "timestamp" in data
        assert "app_name" in data
        assert "app_version" in data
        
        assert data["status"] == "healthy"
        assert isinstance(data["timestamp"], float)
    
    def test_health_check_response_time(self, client):
        """Test that health check responds within 1 second (requirement 3.1)."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0


class TestErrorHandling:
    """Test cases for error handling functionality."""
    
    def test_404_error_handler(self, client):
        """Test that 404 errors are handled properly (requirement 3.3)."""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404
        assert "404" in response.text
        assert "Page Not Found" in response.text
    
    def test_404_returns_html(self, client):
        """Test that 404 error returns HTML content."""
        response = client.get("/nonexistent-page")
        assert response.headers["content-type"] == "text/html; charset=utf-8"


class TestApplicationFactory:
    """Test cases for the application factory function."""
    
    def test_create_app_returns_fastapi_instance(self):
        """Test that create_app returns a FastAPI instance."""
        from fastapi import FastAPI
        app = create_app()
        assert isinstance(app, FastAPI)
    
    def test_create_app_has_correct_metadata(self):
        """Test that the created app has correct title and version."""
        app = create_app()
        assert app.title == "Hello World Web Application"
        assert app.version == "1.0.0"