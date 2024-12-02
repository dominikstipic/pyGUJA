import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit, 
    QVBoxLayout,
    QLabel, 
    QWidget)

class QSearchLayout(QHBoxLayout):
    def on_click(self):
        text = self.search.text()

    def __init__(self):
        super().__init__()
        self.search = QLineEdit()
        self.submit = QPushButton(">>")
        self.viz    = QPushButton("|||")
        self.addWidget(self.search)
        self.addWidget(self.submit)
        self.addWidget(self.viz)

        self.submit.clicked.connect(self.on_click)

class QListLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
    
    def add(self, message):
        self.addWidget(QLabel(message))

class QMainWindows(QWidget):
    title = "Pile file"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.move(0, 0)
        self.resize(400, 100)

        self.list_widget   = QListLayout()
        self.search_widget = QSearchLayout()

        outerLayout = QVBoxLayout()
        outerLayout.addLayout(self.search_widget)
        outerLayout.addLayout(self.list_widget)
        self.setLayout(outerLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindows()
    win.show()
    sys.exit(app.exec_())