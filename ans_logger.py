from logging import Logger
import sys
from typing import Dict, Any

class ANSLogger:
    """Handles logging for the ANSE framework, providing structured and contextual logs.
    
    This class abstracts logging operations, allowing different log handlers to be
    plugged in dynamically. It supports both synchronous and asynchronous logging
    operations depending on the backend used.
    
    Attributes:
        logger (Logger): The underlying logger instance.
        handlers (Dict[str, Any]): Dictionary of registered log handlers.
        formatter: Formatter for structuring log messages.
    """

    def __init__(self) -> None:
        """Initialize the ANSLogger with default settings."""
        self.logger = logging.getLogger("ANSLogger")
        self.handlers = {}
        self.formatter = None

    def add_handler(self, name: str, handler_class, *args, **kwargs) -> None:
        """Register a new log handler with the logger."""
        try:
            handler = handler_class(*args, **kwargs)
            self.handlers[name] = handler
            self.logger.addHandler(handler)
            self.logger.info(f"Handler '{name}' added successfully.")
        except Exception as e:
            self.logger.error(f"Failed to add handler '{name}': {str(e)}")
            raise

    def remove_handler(self, name: str) -> None:
        """Remove a registered log handler."""
        try:
            if name in self.handlers:
                handler = self.handlers.pop(name)
                self.logger.removeHandler(handler)
                self.logger.info(f"Handler '{name}' removed successfully.")
            else:
                raise ValueError(f"Handler '{name}' not found.")
        except Exception as e:
            self.logger.error(f"Failed to remove handler '{name}': {str(e)}")
            raise

    def log(self, level: str, message: str, context: Dict[str, Any] = None) -> None:
        """Log a message at the specified level with optional context."""
        try:
            if context is not None:
                self.logger.log(
                    getattr(logging, level.upper()),
                    f"{context} - {message}"
                )
            else:
                self.logger.log(getattr(logging, level.upper()), message)
        except Exception as e:
            self.logger.error(f"Failed to log message: {str(e)}")
            raise

    def _setup_default_formatter(self) -> None:
        """Set up the default formatter for log messages."""
        if not self.formatter:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            self.formatter = formatter