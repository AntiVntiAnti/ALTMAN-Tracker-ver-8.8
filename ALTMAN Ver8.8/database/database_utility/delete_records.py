from PyQt6.QtWidgets import QTableView, QMainWindow
from logger_setup import logger


def delete_selected_rows(main_window_instance: QMainWindow, table_view_widget_name: str,
                         model_name: str) -> None:
    """
    Delete the selected rows from the specified QTableView model.

    Args:
        main_window_instance (QMainWindow): The instance of the main window.
        table_view_widget_name (str): The name of the QTableView widget in the main window.
        model_name (str): The name of the model associated with the QTableView.

    Raises:
        Exception: If an error occurs while deleting records.

    Returns:
        None

    """
    try:
        # Retrieve the QTableView and model instances from the main window
        table_view: QTableView = getattr(main_window_instance, table_view_widget_name)
        model = getattr(main_window_instance, model_name)  # The model's specific type could vary
        
        if table_view is not None:
            # Get indices of selected rows, sorted in reverse order for deletion
            selected_rows = table_view.selectionModel().selectedRows()
            rows_to_delete = sorted([index.row() for index in selected_rows], reverse=True)
            
            # Delete each selected row from the model
            for row in rows_to_delete:
                model.removeRow(row)
            
            # Submit changes and refresh the model
            model.submitAll()
            model.select()
    
    except Exception as e:
        logger.error(f"An error occurred while deleting records: {str(e)}")
