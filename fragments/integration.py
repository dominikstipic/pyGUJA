import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QLineEdit, 
    QVBoxLayout,
    QLabel, 
    QWidget,
    QMessageBox, 
    QScrollArea)
from PyQt5.QtGui import QPixmap
from pathlib import Path
from PyQt5.QtCore import Qt
import model
import os
import random


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
    
    def get_file_encoded_names(self, f):
        ns = f.split()
        ns = [n[0].lower() for n in ns]
        if "." in f:
            _, suf = f.split(".")
            name = f"{"".join(ns)}.{suf}"
        else:
            name = f"{"".join(ns)}"
        return name 

    def vizualize(self):
        file_name = [self.get_file_encoded_names(fs.split("/")[-1]) for fs in self.current_files]
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


def generate_random_string(length):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = ''.join(random.choice(characters) for i in range(length))
    return result

class QMainWindows(QWidget):
    title = "File analysis"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.move(70, 70)
        self.resize(400, 100)
        self.list_widget   = QListLayout()

        # A
        self.outerLayout = QVBoxLayout()
        self.setLayout(self.outerLayout)

        # S
        scroll_area = QScrollArea()
        self.outerLayout.addWidget(scroll_area)
        scroll_area.setWidgetResizable(True)

        b_widget = QWidget()
        b_widget.setLayout(self.list_widget)
        scroll_area.setWidget(b_widget)

        ######### TEST ##############
        for _ in range(100):
            X = generate_random_string(10)
            self.list_widget.add(X)
        #######################

    def moveEvent(self, event):
        new_pos = event.pos()
        self.x, self.y = new_pos.x(), new_pos.y()
        super().moveEvent(event) 



def populate(window):
    for _ in range(100):
        X = generate_random_string(10)
        window.list_widget.add(X)

app = QApplication(sys.argv)
win = QMainWindows()
#populate(win)
win.show()
sys.exit(app.exec_())