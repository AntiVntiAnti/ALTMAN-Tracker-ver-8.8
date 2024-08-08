from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys
from logger_setup import logger
from ui.main_ui import res

def run_app():
    """
    Runs the application.

    This function initializes the application, creates the main window,
    and starts the event loop.

    Raises:
        Exception: If an error occurs during the execution of the application.
    """
    logger.info("Application starting...")
    try:
        app = QApplication(sys.argv)
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
    finally:
        logger.info("Application shutdown.")

if __name__ == "__main__":
    run_app()