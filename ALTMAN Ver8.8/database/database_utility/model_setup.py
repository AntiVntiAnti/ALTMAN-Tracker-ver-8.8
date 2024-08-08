from PyQt6 import QtSql
from PyQt6.QtWidgets import QAbstractItemView
from logger_setup import logger


def create_and_set_model(table_name: str, view_widget: QAbstractItemView) -> QtSql.QSqlTableModel:
    """
    Creates and sets up a QSqlTableModel for the specified table name and view widget.

    Args:
        table_name (str): The name of the table to create the model for.
        view_widget (QAbstractItemView): The view widget to set the model on.

    Returns:
        QSqlTableModel: The created QSqlTableModel.

    Raises:
        RuntimeError: If there is an error selecting data from the table.
    """
    model = QtSql.QSqlTableModel()
    model.setTable(table_name)
    model.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnFieldChange)

    if not model.select():
        error_message = f"Error selecting data from table: {table_name}, {model.lastError().text()}"
        logger.error(error_message)
        raise RuntimeError(error_message)

    view_widget.setModel(model)
    return model
