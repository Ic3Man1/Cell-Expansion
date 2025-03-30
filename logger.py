import sys
import logging
from logging.handlers import RotatingFileHandler
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget

class LogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_logger()
        
    def init_logger(self):
        self.loger_editor = QTextEdit(self)
        self.loger_editor.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.loger_editor)

        self.setLayout(layout)
        self.setWindowTitle('Log Viewer')
        self.setGeometry(1440, 275, 350, 250)
        self.show()

    def log_message(self, message):
        self.loger_editor.append(message)

def setup_logger():
    logger = logging.getLogger("AppLogger")
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger