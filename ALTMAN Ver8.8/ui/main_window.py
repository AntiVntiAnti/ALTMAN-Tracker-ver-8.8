import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime, QAbstractTableModel
from PyQt6.QtGui import QCloseEvent
from typing import Any, Optional
import tracker_config as tkc
from ui.main_ui.gui import Ui_MainWindow
from logger_setup import logger
from navigation.master_navigation import change_stack_page
from utility.app_operations.show_hide import toggle_views
from database.altman_add_data import add_altmans_data

# ////////////////////////////////////////////////////////////////////////////////////////
# UI
# ////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////
# LOGGER
# ////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////
# NAVIGATION
# ////////////////////////////////////////////////////////////////////////////////////////

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)

# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# ////////////////////////////////////////////////////////////////////////////////////////
# ADD DATA MODULES
# ////////////////////////////////////////////////////////////////////////////////////////


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    This class represents the main window of the application. It inherits from `FramelessWindow`,
    `QtWidgets.QMainWindow`, and `Ui_MainWindow`. It provides methods for handling various actions
    and events related to the main window.

    Attributes:
        becks_model (Optional[QAbstractTableModel]): The model for the mental mental table.
        ui (Ui_MainWindow): The user interface object for the main window.

    """
    
    def __init__(self,
                 *args: Any,
                 **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.becks_model: Optional[QAbstractTableModel] = None
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager: DataManager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings: QSettings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller: WindowController = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.app_operations()
        self.restore_state()
        # self.slider_set_spinbox()
        self.stack_navigation()
        self.delete_group()
        self.update_altmans_summary()
        self.altman_table_commit()
        self.switch_page_view_setup()
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # APP-OPERATIONS setup
    # ////////////////////////////////////////////////////////////////////////////////////////
    def app_operations(self) -> None:
        """
        Performs the necessary operations for setting up the application.

        This method connects signals and slots, sets the initial state of the UI elements,
        and handles various actions triggered by the user.

        Raises:
            Exception: If an error occurs while setting up the app_operations.

        """
        try:
            self.stackedWidget.currentChanged.connect(self.on_page_changed)
            last_index: int = self.settings.value("lastPageIndex", 0, type=int)
            self.stackedWidget.setCurrentIndex(last_index)
            # auto date time
            self.altman_time.setTime(QTime.currentTime())
            self.altman_date.setDate(QDate.currentDate())
            # nav actions
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    
    def switchone(self) -> None:
        """
        Switches the current widget to the 'onepage' widget and resizes the main window.

        Parameters:
            None

        Returns:
            None
        """
        self.stackedWidget.setCurrentWidget(self.onepage)
        self.resize(476, 175)
        self.setFixedSize(476, 175)
    
    def switchtwo(self) -> None:
        """
        Switches the current widget to the 'twopage' widget and resizes the main window to a fixed size of 800x460.
        """
        self.stackedWidget.setCurrentWidget(self.twopage)
        self.resize(800, 460)
        self.setFixedSize(800, 460)
    
    def switch_page_view_setup(self) -> None:
        """
        Connects the various actions to their corresponding methods for switching pages/views.

        This method sets up the connections between the menu actions and the methods that handle
        switching to different pages/views in the application.

        """
        self.actionShowAltmanExam.triggered.connect(self.switchone)
        self.actionShowAltmanTable.triggered.connect(self.switchtwo)
        
    def on_page_changed(self, index: int) -> None:
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.

        Raises:
            Exception: If an error occurs while setting the last page index.

        """
        try:
            self.settings.setValue("lastPageIndex", index)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def stack_navigation(self) -> None:
        """
        Connects the triggered signals of certain actions to change the stack pages.

        The method creates a dictionary `change_stack_pages` that maps actions to their corresponding page index.
        It then iterates over the dictionary and connects the `triggered` signal of each action to a lambda function
        that calls the `change_stack_page` method with the corresponding page index.

        Raises:
            Exception: If an error occurs during the connection of signals.

        """
        try:
            change_stack_pages = {
                self.actionShowAltmanExam: 0,
                self.actionShowAltmanTable: 1,
            }
            
            for action, page in change_stack_pages.items():
                action.triggered.connect(lambda _, p=page: change_stack_page(self.stackedWidget, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def altman_table_commit(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into the altman_table.

        This method connects the 'commit' action to the 'add_mentalsolo_data' function, which inserts data into the altman_table.
        The data to be inserted is obtained from various widgets in the UI and passed as arguments to the 'add_altmans_data' function.
        The 'add_altmans_data' function is called with the appropriate arguments and the 'insert_into_altman_table' method of the 'db_manager' object.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommit.triggered.connect(
                lambda: add_altmans_data(
                    self, {
                        "altman_date": "altman_date",
                        "altman_time": "altman_time",
                        "altmans_sleep": "altmans_sleep",
                        "altmans_speech": "altmans_speech",
                        "altmans_activity": "altmans_activity",
                        "altmans_cheer": "altmans_cheer",
                        "altmans_confidence": "altmans_confidence",
                        "altmans_summary": "altmans_summary",
                        "model": "altmans_model"
                    },
                    self.db_manager.insert_into_altman_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
        
        self.altmans_summary.setEnabled(False)
        for slider in [
            self.altmans_sleep, self.altmans_speech, self.altmans_activity, self.
                altmans_cheer, self.altmans_confidence, ]:
            slider.setRange(0, 4)
        
        self.altmans_sleep.valueChanged.connect(self.update_altmans_summary)
        self.altmans_speech.valueChanged.connect(self.update_altmans_summary)
        self.altmans_activity.valueChanged.connect(self.update_altmans_summary)
        self.altmans_cheer.valueChanged.connect(self.update_altmans_summary)
        self.altmans_confidence.valueChanged.connect(self.update_altmans_summary)
    
    def update_altmans_summary(self) -> None:
        """
        Updates the averages of the sliders in the wellbeing and pain module such that
        the overall is the average of the whole.

        :return: None
        """
        try:
            values = [slider.value() for slider in
                      [self.altmans_sleep, self.altmans_speech, self.altmans_activity, self.altmans_cheer,
                       self.altmans_confidence] if slider.value() > 0]

            altmans_sum = sum(values)

            self.altmans_summary.setValue(int(altmans_sum))

        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
    def delete_group(self) -> None:
        """
        Connects the delete action to the delete_selected_rows function.

        This method connects the delete action to the delete_selected_rows function,
        passing the necessary arguments to delete the selected rows in the altman_table.

        Args:
            self: The instance of the main window.

        Returns:
            None
        """
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'altmans_manic_rating_table',
                'altmans_model'
            )
        )
        
    def setup_models(self) -> None:
        """
        Set up the models for the main window.

        This method creates and sets the becks_model using the altman_table.

        Returns:
            None
        """
        self.altmans_model = create_and_set_model(
            "altman_table",
            self.altmans_manic_rating_table
        )
        
    def save_state(self) -> None:
            """
            Saves the window geometry state and window state.

            This method saves the current geometry and state of the window
            using the QSettings object. It saves the window geometry state
            and the window state separately.

            Raises:
                Exception: If there is an error saving the window geometry state
                           or the window state.

            """
            try:
                self.settings.setValue("geometry", self.saveGeometry())
            except Exception as e:
                logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
            try:
                self.settings.setValue("windowState", self.saveState())
            except Exception as e:
                logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
    
    def restore_state(self) -> None:
        """
        Restores the window geometry and state.

        This method restores the previous geometry and state of the window
        by retrieving the values from the settings. If an error occurs during
        the restoration process, an error message is logged.

        Raises:
            Exception: If an error occurs while restoring the window geometry or state.
        """
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self, event: QCloseEvent) -> None:
            """
            Event handler for the close event of the window.

            Saves the state before closing the window.

            Args:
                event (QCloseEvent): The close event object.

            Returns:
                None
            """
            try:
                self.save_state()
            except Exception as e:
                logger.error(f"error saving state during closure: {e}", exc_info=True)
