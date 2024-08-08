from PyQt6.QtCore import QDate, QTime
import tracker_config as tkc
from logger_setup import logger


def add_beck_data(main_window_instance, widget_names, db_insert_method):
    """
    Add mental solo data to the database.

    Args:
        main_window_instance (object): The instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.
        db_insert_method (function): The method used to insert data into the database.

    Returns:
        None

    Raises:
        Exception: If there is an error getting the value from a widget or inserting data into the database.
    """
    widget_methods = {
        widget_names['beck_date']: (None, 'date', "yyyy-MM-dd"),
        widget_names['beck_time']: (None, 'time', "hh:mm:ss"),
        widget_names['sadness']: (None, 'value', None),
        widget_names['outlook']: (None, 'value', None),
        widget_names['guilt']: (None, 'value', None),
        widget_names['solitude']: (None, 'value', None),        
        widget_names['sexdrive']: (None, 'value', None),
        widget_names['hygiene']: (None, 'value', None),
        widget_names['decisiveness']: (None, 'value', None),
        widget_names['effort']: (None, 'value', None),
        widget_names['victimhood']: (None, 'value', None),
        widget_names['pessimism']: (None, 'value', None),
        widget_names['interest']: (None, 'value', None),
        widget_names['sleep']: (None, 'value', None),
        widget_names['beck_summary']: (None, 'value', None),
    }

    data_to_insert = []
    for widget_name, (widget_attr, method, format_type) in widget_methods.items():
        widget = getattr(main_window_instance, widget_name)
        try:
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        except Exception as e:
            logger.error(f"Error getting value from widget {widget_name}: {e}")

    try:
        db_insert_method(*data_to_insert)
        reset_beck_exam(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error inserting data into the database: {e}")


def reset_beck_exam(main_window_instance, widget_names):
    """
    Reset the values of the mental_mental form in the main window.

    Args:
        main_window_instance (object): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets used in the mental_mental form.

    Raises:
        Exception: If there is an error resetting the form.

    Returns:
        None
    """
    try:
        getattr(main_window_instance, widget_names['beck_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['beck_time']).setTime(QTime.currentTime())
        getattr(main_window_instance, widget_names['sadness']).setValue(0)
        getattr(main_window_instance, widget_names['outlook']).setValue(0)
        getattr(main_window_instance, widget_names['guilt']).setValue(0)
        getattr(main_window_instance, widget_names['solitude']).setValue(0)
        getattr(main_window_instance, widget_names['sexdrive']).setValue(0)
        getattr(main_window_instance, widget_names['hygiene']).setValue(0)
        getattr(main_window_instance, widget_names['decisiveness']).setValue(0)
        getattr(main_window_instance, widget_names['effort']).setValue(0)
        getattr(main_window_instance, widget_names['interest']).setValue(0)
        getattr(main_window_instance, widget_names['pessimism']).setValue(0)
        getattr(main_window_instance, widget_names['victimhood']).setValue(0)
        getattr(main_window_instance, widget_names['sleep']).setValue(0)
        getattr(main_window_instance, widget_names['beck_summary']).setValue(0)
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error resetting pain levels form: {e}")
