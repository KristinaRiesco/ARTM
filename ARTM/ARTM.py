import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QVBoxLayout, QStackedWidget, QPushButton, QHBoxLayout
from pages.Home_Page import HomePage
from pages.Gesture_Capture_Page import GestureCapturePage
from pages.Profile_Page import ProfilePage
from pages.Settings_Page import SettingsPage

class BasicFrontendApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Basic Frontend App')
        self.setGeometry(300, 300, 800, 600)

        # Create central widget with a layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

        # Add app name label at the top
        self.app_name_label = QPushButton("Basic Frontend App")
        self.app_name_label.setStyleSheet("text-align: center;")
        self.app_name_label.clicked.connect(self.show_home_page)
        main_layout.addWidget(self.app_name_label, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        # Create main content layout
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Create sidebar layout
        sidebar_layout = QVBoxLayout()
        content_layout.addLayout(sidebar_layout)

        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        # Add buttons to sidebar for switching pages
        button_gesture_capture = QPushButton("Gesture Capture")
        button_gesture_capture.clicked.connect(lambda: self.show_page(1))
        sidebar_layout.addWidget(button_gesture_capture)

        button_profile = QPushButton("Profile")
        button_profile.clicked.connect(lambda: self.show_page(2))
        sidebar_layout.addWidget(button_profile)

        button_app_settings = QPushButton("App Settings")
        button_app_settings.clicked.connect(lambda: self.show_page(3))
        sidebar_layout.addWidget(button_app_settings)

        # Add pages to stacked widget
        self.home_page = HomePage()
        self.stacked_widget.addWidget(self.home_page)

        self.gesture_capture_page = GestureCapturePage()
        self.stacked_widget.addWidget(self.gesture_capture_page)

        self.profile_page = ProfilePage()
        self.stacked_widget.addWidget(self.profile_page)

        self.app_settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.app_settings_page)

        # Set the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("icon.png"))  # Add your application icon here

        # Create the menu for tray icon
        tray_menu = QMenu()
        open_action = QAction("Open", self)
        quit_action = QAction("Quit", self)

        open_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)

        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # Show the system tray icon
        self.tray_icon.show()

        # Trigger when the tray icon is clicked
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Show home page on start
        self.show_home_page()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "App Running",
            "The app is still running in the background.",
            QSystemTrayIcon.Information,
            2000
        )

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()
            self.activateWindow()

    def show_page(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def show_home_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def quit_app(self):
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(False)
    window = BasicFrontendApp()
    window.show()
    sys.exit(app.exec_())
