"""Integration tests for Hello World Web Application.

Tests end-to-end HTTP request/response flow, template rendering, error handling,
and server startup/shutdown processes as specified in requirements 2.1, 2.3, 3.1, and 3.3.
"""

import pytest
import time
import threading
from typing import Generator
from fastapi.testclient import TestClient
from app import create_app
import uvicorn
from config import get_settings


@pytest.fixture
def client():
    """Create a test client for integration testing."""
    app = create_app()
    return TestClient(app)


class TestEndToEndFlow:
    """Test cases for end-to-end HTTP request/response flow."""
    
    def test_complete_hello_world_flow(self, client):
        """Test complete flow from request to rendered HTML response."""
        # Make request to hello world page
        response = client.get("/")
        
        # Verify response status and headers
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        
        # Verify HTML structure and content
        html_content = response.text
        assert "<!DOCTYPE html>" in html_content
        assert "<html" in html_content
        assert "<head>" in html_content
        assert "<body>" in html_content
        assert "Hello World" in html_content
        assert "</html>" in html_content
    
    def test_health_check_integration(self, client):
        """Test complete health check endpoint integration."""
        response = client.get("/health")
        
        # Verify response
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        # Verify JSON structure and content
        data = response.json()
        required_fields = ["status", "message", "timestamp", "app_name", "app_version"]
        
        for field in required_fields:
            assert field in data
        
        assert data["status"] == "healthy"
        assert "Hello World" in data["message"]
        assert isinstance(data["timestamp"], float)
        assert data["timestamp"] > 0
    
    def test_concurrent_requests_handling(self, client):
        """Test that the application handles multiple concurrent requests (requirement 3.4)."""
        import concurrent.futures
        
        def make_request():
            response = client.get("/")
            return response.status_code, "Hello World" in response.text
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all requests succeeded
        for status_code, has_hello_world in results:
            assert status_code == 200
            assert has_hello_world is True


class TestTemplateRendering:
    """Test cases for template rendering integration."""
    
    def test_template_rendering_with_context(self, client):
        """Test that templates are rendered with proper context variables."""
        response = client.get("/")
        
        # Verify template was rendered successfully
        assert response.status_code == 200
        html_content = response.text
        
        # Check that template variables were properly substituted
        assert "Hello World" in html_content
        
        # Verify HTML structure is complete
        assert html_content.count("<html") == 1
        assert html_content.count("</html>") == 1
        assert html_content.count("<head>") == 1
        assert html_content.count("</head>") == 1
        assert html_content.count("<body>") == 1
        assert html_content.count("</body>") == 1
    
    def test_template_file_loading(self, client):
        """Test that template files are properly loaded from templates directory."""
        response = client.get("/")
        
        # Verify response indicates successful template loading
        assert response.status_code == 200
        
        # Verify content suggests template was loaded (not a fallback response)
        html_content = response.text
        assert len(html_content) > 50  # Template should have substantial content
        assert "Hello World" in html_content


class TestErrorHandlingIntegration:
    """Test cases for error handling integration."""
    
    def test_404_error_handling_integration(self, client):
        """Test complete 404 error handling flow (requirement 3.3)."""
        # Test various non-existent paths
        test_paths = ["/nonexistent", "/missing-page", "/404-test", "/random/path"]
        
        for path in test_paths:
            response = client.get(path)
            
            # Verify 404 response
            assert response.status_code == 404
            assert response.headers["content-type"] == "text/html; charset=utf-8"
            
            # Verify error page content
            html_content = response.text
            assert "404" in html_content
            assert "Page Not Found" in html_content or "Not Found" in html_content
            
            # Verify it's proper HTML
            assert "<!DOCTYPE html>" in html_content
            assert "<html>" in html_content
            assert "</html>" in html_content
    
    def test_error_response_format_consistency(self, client):
        """Test that error responses maintain consistent HTML format."""
        response = client.get("/nonexistent-endpoint")
        
        assert response.status_code == 404
        html_content = response.text
        
        # Verify HTML structure
        assert html_content.startswith("<!DOCTYPE html>") or "<html>" in html_content
        assert "<head>" in html_content
        assert "<title>" in html_content
        assert "<body>" in html_content
        assert "</html>" in html_content


class TestPerformanceIntegration:
    """Test cases for performance requirements integration."""
    
    def test_response_time_under_load(self, client):
        """Test response times under multiple requests (requirement 3.1)."""
        response_times = []
        
        # Make 20 requests and measure response times
        for _ in range(20):
            start_time = time.time()
            response = client.get("/")
            end_time = time.time()
            
            response_time = end_time - start_time
            response_times.append(response_time)
            
            # Verify successful response
            assert response.status_code == 200
        
        # Verify all responses were under 1 second
        for response_time in response_times:
            assert response_time < 1.0
        
        # Verify average response time is reasonable
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 0.5  # Should be much faster than 1 second
    
    def test_health_check_performance(self, client):
        """Test health check endpoint performance."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Verify response and performance
        assert response.status_code == 200
        assert response_time < 1.0
        
        # Health check should be very fast
        assert response_time < 0.1


class TestApplicationLifecycle:
    """Test cases for application startup and configuration."""
    
    def test_application_creation_with_settings(self):
        """Test that application is created with proper configuration."""
        app = create_app()
        
        # Verify application properties
        assert app.title == "Hello World Web Application"
        assert app.description == "A simple web application that displays Hello World"
        assert app.version == "1.0.0"
        
        # Verify routes are registered
        route_paths = []
        for route in app.routes:
            if hasattr(route, 'path'):
                route_paths.append(route.path)
        assert "/" in route_paths
        assert "/health" in route_paths
    
    def test_settings_integration(self):
        """Test that settings are properly integrated into the application."""
        settings = get_settings()
        
        # Verify settings are loaded
        assert settings.host is not None
        assert settings.port is not None
        assert isinstance(settings.port, int)
        assert 1 <= settings.port <= 65535
        
        # Verify application settings
        assert settings.app_name is not None
        assert settings.app_version is not None
        assert settings.templates_dir == "templates"