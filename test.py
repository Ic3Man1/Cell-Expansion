from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QPropertyAnimation, Qt, pyqtSlot

def show_fading_message(message, duration=2000):
    label = QLabel()
    label.setAlignment(Qt.AlignCenter)
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    label.setAttribute(Qt.WA_TranslucentBackground)
    label.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; font-size: 20px; padding: 10px;")

    label.setText(message)
    label.adjustSize()
    label.move(QApplication.instance().desktop().screen().rect().center() - label.rect().center())
    label.show()

    # Ustawienie animacji
    animation = QPropertyAnimation(label, b"windowOpacity")
    animation.setDuration(duration)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.finished.connect(label.deleteLater)  # Usunięcie label po zakończeniu animacji

    animation.start()

# Użycie funkcji
if __name__ == "__main__":
    app = QApplication([])
    show_fading_message("Hello, World!", 2000)
    app.exec_()
