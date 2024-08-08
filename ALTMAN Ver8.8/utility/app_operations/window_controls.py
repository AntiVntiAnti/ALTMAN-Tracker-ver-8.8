from typing import Any
from logger_setup import logger


class WindowController:
    
    def __init__(self) -> None:
        """Initialize the class with default values for window state."""
        self.is_minimized: bool = False
        self.is_maximized: bool = False
    
    def toggle_minimize(self, window: Any) -> None:
        """
        Toggles the minimize state of the window.

        Args:
            self: The instance of the class.
            window (Any): The window to be minimized or restored.

        Returns:
            None
        """
        try:
            if self.is_minimized:
                window.showNormal()
                self.is_minimized = False
            else:
                window.showMinimized()
                self.is_minimized = True
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def toggle_maximize(self, window: Any) -> None:
        """
        Toggles the maximize state of the window.

        Args:
            self: The current instance of the class.
            window (Any): The window to be toggled.

        Returns:
            None
        """
        if self.is_maximized:
            window.showNormal()
            self.is_maximized = False
        else:
            window.showMaximized()
            self.is_maximized = True
