import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit, 
    QVBoxLayout,
    QLabel, 
    QWidget)

class QSearchWidget(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(QLineEdit())
        self.addWidget(QPushButton(">>"))
        self.addWidget(QPushButton("|||"))

class QListWidget(QVBoxLayout):
    def __init__(self):
        super().__init__()
    
    def add(self, message):
        self.addWidget(QLabel(message))

class QInfoWidget(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(QPushButton("|||"))

class QMainWindows(QWidget):
    title = "Pile file"
    #search_widget = QSearchWidget()
    #list_widget   = QListWidget()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.move(0, 0)
        self.resize(400, 100)

        outerLayout = QVBoxLayout()
        top_layout  = QSearchWidget()
        bottom_layout = QListWidget()
        outerLayout.addLayout(top_layout)
        outerLayout.addLayout(bottom_layout)
        self.setLayout(outerLayout)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindows()
    win.show()
    sys.exit(app.exec_())