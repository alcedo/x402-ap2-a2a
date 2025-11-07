"""Configuration module for the Hello World web application.

This module provides typed configuration settings using Pydantic Settings
with support for environment variables and .env file loading.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with type annotations and environment variable support.
    
    All settings can be overridden via environment variables or .env file.
    Environment variables should be prefixed with 'HELLO_' (e.g., HELLO_HOST).
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="HELLO_",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Server configuration
    host: str = Field(
        default="127.0.0.1",
        description="Host address for the web server"
    )
    
    port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="Port number for the web server"
    )
    
    debug: bool = Field(
        default=True,
        description="Enable debug mode for development"
    )
    
    # Application configuration
    app_name: str = Field(
        default="Hello World Web App",
        description="Application name displayed in responses"
    )
    
    app_version: str = Field(
        default="0.1.0",
        description="Application version"
    )
    
    # Template configuration
    templates_dir: str = Field(
        default="templates",
        description="Directory containing HTML templates"
    )


def get_settings() -> Settings:
    """Get application settings instance.
    
    Returns:
        Settings: Configured settings instance with environment variables loaded.
    """
    return Settings()


# Global settings instance
settings = get_settings()