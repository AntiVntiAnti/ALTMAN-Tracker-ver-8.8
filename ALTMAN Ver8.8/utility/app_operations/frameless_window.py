from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPainterPath, QRegion, QMouseEvent, QResizeEvent
from logger_setup import logger


class FramelessWindow(QMainWindow):
    """
    A custom QMainWindow subclass that creates a frameless window.

    This class provides functionality to create a frameless window with a translucent background.
    It also handles mouse events for dragging and resizing the window.

    Attributes:
        startPos (QPoint): The starting position of the mouse press event.
        pressing (bool): Indicates whether the mouse button is currently pressed.

    """

    def __init__(self) -> None:
        super().__init__()
        self.startPos: QPoint = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.pressing: bool = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle the mouse press event.

        Parameters:
            event (QMouseEvent): The mouse event object.

        Returns:
            None
        """
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.pressing = True
                self.startPos = event.position().toPoint()
        except Exception as e:
            logger.error(f"Error in mousePressEvent: {e}", exc_info=True)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Handles the mouse move event.

        Args:
            event (QMouseEvent): The mouse event object.

        Returns:
            None
        """
        try:
            if self.pressing and self.startPos is not None:
                self.move(self.pos() + event.position().toPoint() - self.startPos)
        except Exception as e:
            logger.error(f"Error in mouseMoveEvent: {e}", exc_info=True)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        This method is called when a mouse button is released.

        Args:
            event (QMouseEvent): The mouse event object containing information about the event.

        Returns:
            None
        """
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.pressing = False
        except Exception as e:
            logger.error(f"Error occurred in mouseReleaseEvent: {e}", exc_info=True)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Event handler for the resize event of the widget.

        Args:
            event (QResizeEvent): The resize event object.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the resize event.

        """
        try:
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), 10.0, 10.0)

            # Create a QRegion from the QPainterPath
            region = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(region)
        except Exception as e:
            logger.error(f"Error occurred in resizeEvent: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        app = QApplication([])
        window = FramelessWindow()
        window.show()
        app.exec()
    except Exception as e:
        logger.exception("Error in main: %s", str(e))
