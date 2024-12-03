import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit, 
    QVBoxLayout,
    QLabel, 
    QWidget,
    QMessageBox)
from PyQt5.QtGui import QPixmap
from pathlib import Path
from PyQt5.QtCore import Qt
import model
import os


def fire_message(message, x, y):
    msg_box = QMessageBox() 
    msg_box.setIcon(QMessageBox.Information) 
    msg_box.setText(message)
    msg_box.setWindowTitle("Info!")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.move(x, y)
    msg_box.exec_()

class QSearchLayout(QHBoxLayout):
    is_init = False
    def on_submit_click(self):
        path = self.search.text()
        path = Path(path)
        if not path.exists():
            message = "Path does not exist"
            fire_message(message, self.main_window.x, self.main_window.y)
        else:
            self.is_init = True
            self.main_window.list_widget.update(path)

    def on_viz_click(self):
        if self.is_init:
            self.main_window.list_widget.vizualize()
            
        else:
            fire_message("Cannot vizualize", self.main_window.x, self.main_window.y)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.search = QLineEdit()
        self.submit = QPushButton(">>")
        self.viz    = QPushButton("|||")
        self.addWidget(self.search)
        self.addWidget(self.submit)
        self.addWidget(self.viz)
        self.submit.clicked.connect(self.on_submit_click)
        self.viz.clicked.connect(self.on_viz_click)

class QListLayout(QVBoxLayout):
    current_files = []

    def __init__(self):
        super().__init__()
    
    def add(self, message):
        label = QLabel(message)
        label.setStyleSheet("border: 2px solid black;") 
        self.addWidget(label)

    def clear(self):
        self.current_files = []
        for i in reversed(range(self.count())):
            item = self.takeAt(i)
            if item.widget():
                widget = item.widget()
                self.removeWidget(widget)
                widget.deleteLater()  

    def file_size(self, file):
        absolute_path = Path(file).resolve()
        return os.path.getsize(absolute_path) / 1000

    def vizualize(self):
        file_name = [fs.split("/")[-1] for fs in self.current_files]
        file_sizes = [self.file_size(fs) for fs in self.current_files]
        
        self.clear()
        print(file_name)
        model.create_bar(file_name, file_sizes)
        pixmap = QPixmap('data.png')
        label = QLabel()
        label.setAlignment(Qt.AlignHCenter)
        label.setPixmap(pixmap)
        self.addWidget(label)

    def update(self, path):
        self.clear()
        ms = model.file_walker_leveled(path)
        self.current_files = ms
        for m in ms:
            file_name = m.split("/")[-1] 
            self.add(file_name)

class QMainWindows(QWidget):
    title = "File analysis"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.move(70, 70)
        self.resize(400, 100)

        # Creational dependency
        self.list_widget   = QListLayout()
        self.search_widget = QSearchLayout(self)

        outerLayout = QVBoxLayout()
        outerLayout.addLayout(self.search_widget)
        outerLayout.addLayout(self.list_widget)
        self.setLayout(outerLayout)

    def moveEvent(self, event):
        new_pos = event.pos()
        self.x, self.y = new_pos.x(), new_pos.y()
        super().moveEvent(event) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindows()
    win.show()
    sys.exit(app.exec_())