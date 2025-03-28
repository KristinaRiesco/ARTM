from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from backend.services.user_service import register_user

class RegisterPage(QWidget):
    back_to_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Large "Register" title
        title_label = QLabel("Register")
        title_label.setObjectName("RegisterTitle")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        #Username input for registration
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(300)
        self.username_input.setObjectName("RegisterField")
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)


        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedWidth(300)
        self.email_input.setObjectName("RegisterField")
        layout.addWidget(self.email_input, alignment=Qt.AlignCenter)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setObjectName("RegisterField")
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setObjectName("RegisterButton")
        self.register_button.clicked.connect(self.attempt_register)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        layout.addSpacing(10)

        # "or, log in" link
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)

        or_label = QLabel("or,")
        or_label.setObjectName("OrLabel")
        bottom_layout.addWidget(or_label)

        back_link = QPushButton("log in")
        back_link.setObjectName("BackToLoginLink")
        back_link.setFlat(True)
        back_link.clicked.connect(self.go_back_to_login)
        bottom_layout.addWidget(back_link)

        layout.addLayout(bottom_layout)

    def attempt_register(self):

        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox(self, "Error", "All fields are required!")
            return

        result = register_user(username, email, password)

        if "error" in result:
            QMessageBox.warning(self, "Error", result["error"])
        else:
            QMessageBox.information(self, "Success", result["message"])

    def go_back_to_login(self):
        self.back_to_login.emit()
