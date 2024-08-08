from typing import Any


# toggle_view.py
def toggle_views(view_object: Any) -> None:
    """
    Toggles the visibility of the given view object.

    Args:
    view_object (Any): The view object to toggle.

    Returns:
    None
    """
    view_object.setVisible(not view_object.isVisible())