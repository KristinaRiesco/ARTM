import sys
from flask import Flask
from backend.core.extensions import db, bcrypt
from backend.core.config import Config
from backend.core.database import init_db
from PyQt5.QtWidgets import QApplication
from ARTM import BasicFrontendApp

def create_flask_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    app.app_context().push()
    return app

def main():

    flask_app = create_flask_app()

    init_db()

    app = QApplication(sys.argv)

    # Load the global stylesheet from style.qss
    with open("style.qss", "r") as f:
        style_sheet = f.read()
    app.setStyleSheet(style_sheet)

    window = BasicFrontendApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
