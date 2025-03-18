import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

import requests
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QSystemTrayIcon, QMenu, QAction, QApplication, QMessageBox,
    QVBoxLayout, QStackedWidget, QPushButton, QHBoxLayout, QWidget, QLabel, QFrame
)

from pages.Home_Page import HomePage
from pages.Gesture_Capture_Page import GestureCapturePage
from pages.Profile_Page import ProfilePage
from pages.Settings_Page import SettingsPage
from pages.Login_Page import LoginPage
from pages.Register_Page import RegisterPage

class BasicFrontendApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.username = None  # We'll store username here to pass to Profile page
        self.setWindowTitle("ARTM")
        self.setGeometry(300, 300, 900, 600)
        self.initUI()

    def initUI(self):
        # Central widget + layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

        # ------------------- TOP BAR -------------------
        self.top_bar = QFrame()
        self.top_bar.setObjectName("TopBar")
        top_bar_layout = QHBoxLayout(self.top_bar)
        top_bar_layout.setContentsMargins(15, 5, 15, 5)
        top_bar_layout.setSpacing(10)

        # Left stretch, ARTM centered, right stretch
        top_bar_layout.addStretch()
        self.title_button = QPushButton("ARTM")
        self.title_button.setObjectName("TitleButton")
        self.title_button.clicked.connect(self.show_home_page)
        top_bar_layout.addWidget(self.title_button, alignment=QtCore.Qt.AlignCenter)
        top_bar_layout.addStretch()

        main_layout.addWidget(self.top_bar)

        # ------------------- MAIN CONTENT (sidebar + pages) -------------------
        content_frame = QFrame()
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # Buttons for pages
        sidebar_buttons = [
            ("Gesture Capture", 1),
            ("Profile", 2),
            ("Settings", 3)
        ]
        for name, idx in sidebar_buttons:
            btn = QPushButton(name)
            btn.setObjectName("SidebarButton")
            btn.clicked.connect(lambda _, i=idx: self.show_page(i))
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.setObjectName("LogoutButton")
        logout_button.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_button)

        content_layout.addWidget(self.sidebar, stretch=1)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget, stretch=3)
        main_layout.addWidget(content_frame)

        # ------------------- ADD PAGES TO STACK -------------------
        self.home_page = HomePage()
        self.stacked_widget.addWidget(self.home_page)            # index 0

        self.gesture_capture_page = GestureCapturePage()
        self.stacked_widget.addWidget(self.gesture_capture_page) # index 1

        self.profile_page = ProfilePage()
        self.stacked_widget.addWidget(self.profile_page)         # index 2

        self.app_settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.app_settings_page)    # index 3

        # Login page
        self.login_page = LoginPage()
        self.login_page.login_success.connect(self.handle_login_success)
        self.login_page.register_requested.connect(self.open_register_page)
        self.stacked_widget.addWidget(self.login_page)           # index 4

        # Register page
        self.register_page = RegisterPage()
        self.register_page.back_to_login.connect(self.open_login_page)
        self.stacked_widget.addWidget(self.register_page)        # index 5

        # ------------------- SYSTEM TRAY -------------------
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("icon.png"))
        tray_menu = QMenu()
        open_action = QAction("Open", self)
        quit_action = QAction("Quit", self)
        open_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # ------------------- HIDE TOP BAR & SIDEBAR UNTIL LOGIN -------------------
        self.top_bar.setVisible(False)
        self.sidebar.setVisible(False)
        self.show_page(4)  # Show the login page at startup

    # ------------------- EVENTS & METHODS -------------------
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
        self.show_page(0)

    def open_login_page(self):
        self.show_page(4)

    def open_register_page(self):
        self.show_page(5)

    def handle_login_success(self, user_id):
        self.user_id = user_id
        response = requests.get(f"http://127.0.0.1:5000/users/profile/{user_id}")
        if response.status_code == 200:
            user_data = response.json()
            self.username = user_data.get("username", "Unknown User")
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to fetch user data")

        # Show top bar & sidebar, go to home page
        self.top_bar.setVisible(True)
        self.sidebar.setVisible(True)

        # Pass username to the Profile page
        self.profile_page.load_profile(self.user_id, self.username)

        self.show_home_page()

    def logout(self):
        """ Clears the session and returns to the login page. """
        self.user_id = None
        self.username = None
        self.top_bar.setVisible(False)
        self.sidebar.setVisible(False)
        self.show_page(4)

    def quit_app(self):
        QApplication.quit()
