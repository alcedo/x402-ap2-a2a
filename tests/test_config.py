"""Unit tests for configuration loading and validation.

Tests configuration settings, environment variable loading, and validation
as specified in requirements 1.1, 1.2, and 3.1.
"""

import pytest
import os
from unittest.mock import patch
from config import Settings, get_settings


class TestSettingsModel:
    """Test cases for the Settings Pydantic model."""
    
    def test_default_settings_values(self):
        """Test that default settings values are correct."""
        settings = Settings()
        
        assert settings.host == "127.0.0.1"
        assert settings.port == 8000
        assert settings.debug is True
        assert settings.app_name == "Hello World Web App"
        assert settings.app_version == "0.1.0"
        assert settings.templates_dir == "templates"
    
    def test_settings_with_custom_values(self):
        """Test that settings can be initialized with custom values."""
        settings = Settings(
            host="0.0.0.0",
            port=3000,
            debug=False,
            app_name="Custom App",
            app_version="2.0.0"
        )
        
        assert settings.host == "0.0.0.0"
        assert settings.port == 3000
        assert settings.debug is False
        assert settings.app_name == "Custom App"
        assert settings.app_version == "2.0.0"
    
    def test_port_validation_valid_range(self):
        """Test that port validation accepts valid port numbers."""
        # Test minimum valid port
        settings = Settings(port=1)
        assert settings.port == 1
        
        # Test maximum valid port
        settings = Settings(port=65535)
        assert settings.port == 65535
        
        # Test common port
        settings = Settings(port=8080)
        assert settings.port == 8080
    
    def test_port_validation_invalid_range(self):
        """Test that port validation rejects invalid port numbers."""
        with pytest.raises(ValueError):
            Settings(port=0)
        
        with pytest.raises(ValueError):
            Settings(port=65536)
        
        with pytest.raises(ValueError):
            Settings(port=-1)


class TestEnvironmentVariables:
    """Test cases for environment variable loading."""
    
    def test_environment_variable_loading(self):
        """Test that environment variables are loaded with HELLO_ prefix."""
        with patch.dict(os.environ, {
            'HELLO_HOST': '192.168.1.1',
            'HELLO_PORT': '9000',
            'HELLO_DEBUG': 'false',
            'HELLO_APP_NAME': 'Test App'
        }):
            settings = Settings()
            
            assert settings.host == "192.168.1.1"
            assert settings.port == 9000
            assert settings.debug is False
            assert settings.app_name == "Test App"
    
    def test_case_insensitive_env_vars(self):
        """Test that environment variables are case insensitive."""
        with patch.dict(os.environ, {
            'hello_host': '10.0.0.1',
            'HELLO_PORT': '7000'
        }):
            settings = Settings()
            
            assert settings.host == "10.0.0.1"
            assert settings.port == 7000
    
    def test_env_vars_override_defaults(self):
        """Test that environment variables override default values."""
        with patch.dict(os.environ, {
            'HELLO_DEBUG': 'false'
        }):
            settings = Settings()
            assert settings.debug is False
        
        # Test without env var
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            assert settings.debug is True


class TestGetSettingsFunction:
    """Test cases for the get_settings function."""
    
    def test_get_settings_returns_settings_instance(self):
        """Test that get_settings returns a Settings instance."""
        settings = get_settings()
        assert isinstance(settings, Settings)
    
    def test_get_settings_loads_environment(self):
        """Test that get_settings loads environment variables."""
        with patch.dict(os.environ, {
            'HELLO_HOST': '127.0.0.2',
            'HELLO_PORT': '8001'
        }):
            settings = get_settings()
            
            assert settings.host == "127.0.0.2"
            assert settings.port == 8001


class TestSettingsValidation:
    """Test cases for settings validation and type conversion."""
    
    def test_boolean_conversion(self):
        """Test that boolean values are properly converted from strings."""
        with patch.dict(os.environ, {
            'HELLO_DEBUG': 'true'
        }):
            settings = Settings()
            assert settings.debug is True
        
        with patch.dict(os.environ, {
            'HELLO_DEBUG': 'false'
        }):
            settings = Settings()
            assert settings.debug is False
    
    def test_integer_conversion(self):
        """Test that integer values are properly converted from strings."""
        with patch.dict(os.environ, {
            'HELLO_PORT': '5000'
        }):
            settings = Settings()
            assert settings.port == 5000
            assert isinstance(settings.port, int)
    
    def test_string_values_preserved(self):
        """Test that string values are preserved correctly."""
        with patch.dict(os.environ, {
            'HELLO_HOST': 'localhost',
            'HELLO_APP_NAME': 'My Test App'
        }):
            settings = Settings()
            assert settings.host == "localhost"
            assert settings.app_name == "My Test App"