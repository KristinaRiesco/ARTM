from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Profile Page")
        layout.addWidget(label)
        self.setLayout(layout)
