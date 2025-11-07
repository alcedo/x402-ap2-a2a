#!/usr/bin/env python3
"""Development server launcher for Hello World Web Application.

This module provides a typed server startup function with proper configuration,
startup confirmation messages, and error handling for development use.
"""

import sys
import signal
import logging
from typing import NoReturn, Optional
import uvicorn
from config import get_settings


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def setup_signal_handlers() -> None:
    """Set up signal handlers for graceful shutdown."""
    def signal_handler(signum: int, frame: Optional[object]) -> NoReturn:
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}. Shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def run_server() -> None:
    """Start the uvicorn server with proper configuration.
    
    This function configures and starts the development server with:
    - Proper settings from configuration module
    - Startup confirmation messages
    - Error handling for server startup issues
    - Graceful shutdown handling
    
    Raises:
        SystemExit: If server fails to start or encounters critical errors
    """
    try:
        # Load application settings
        settings = get_settings()
        
        # Set up signal handlers for graceful shutdown
        setup_signal_handlers()
        
        # Log startup information
        logger.info("=" * 50)
        logger.info("Hello World Web Application")
        logger.info("=" * 50)
        logger.info(f"Application: {settings.app_name} v{settings.app_version}")
        logger.info(f"Debug mode: {settings.debug}")
        logger.info(f"Server starting on: http://{settings.host}:{settings.port}")
        logger.info("Press CTRL+C to stop the server")
        logger.info("=" * 50)
        
        # Configure uvicorn server
        config = uvicorn.Config(
            app="app:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level="info" if settings.debug else "warning",
            access_log=settings.debug,
            reload_dirs=[".", "templates"] if settings.debug else None,
            reload_excludes=["*.pyc", "__pycache__", ".git", ".pytest_cache"] if settings.debug else None
        )
        
        # Create and run server
        server = uvicorn.Server(config)
        
        # Log successful startup
        logger.info("Server started successfully!")
        logger.info(f"Visit http://{settings.host}:{settings.port} to view the application")
        
        # Run the server (this blocks until shutdown)
        server.run()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            logger.error(f"Port {settings.port} is already in use. Please choose a different port.")
            logger.error("You can set a different port using the HELLO_PORT environment variable.")
        else:
            logger.error(f"Network error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.error("Please check your configuration and try again.")
        sys.exit(1)
    finally:
        logger.info("Server shutdown complete")


def main() -> None:
    """Main entry point for the development server launcher."""
    run_server()


if __name__ == "__main__":
    main()