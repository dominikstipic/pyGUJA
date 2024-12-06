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
import math


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
        self.search.setPlaceholderText("Enter the path")
        self.submit = QPushButton(">>")
        self.viz    = QPushButton("|||")
        self.addWidget(self.search)
        self.addWidget(self.submit)
        self.addWidget(self.viz)
        self.submit.clicked.connect(self.on_submit_click)
        self.viz.clicked.connect(self.on_viz_click)

class QListLayout(QVBoxLayout):
    current_files = []

    def __init__(self, main):
        super().__init__()
        self.main = main
    
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
            suf = f.split(".")
            name = f"{"".join(ns)}.{suf[-1]}"
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
        NH = label.size().height()
        RATIO = math.ceil(NH / self.main.HEIGHT * 1.1111) 
        self.main.scale_window(RATIO)

    def update(self, path):
        self.clear()
        ms = model.file_walker_leveled(path)
        self.current_files = ms
        max_sen_size = 0
        for m in ms:
            file_name = m.split("/")[-1] 
            max_sen_size = max(max_sen_size, len(file_name))
            self.add(file_name)
        print(max_sen_size)
        CHAR_PX = 7
        NEW_WIDTH = CHAR_PX*max_sen_size
        RATIO = math.ceil(NEW_WIDTH / self.main.WIDTH)
        self.main.scale_window(RATIO)

class QMainWindows(QWidget):
    title = "Darth Vader Starship"
    WIDTH  = 200
    HEIGHT = 600

    def resizeEvent(self, event):
        new_size = self.size() 
        self.WIDTH = new_size.width()
        self.HEIGHT = new_size.height()
        print(f"Window resized to width: {self.WIDTH}, height: {self.HEIGHT}")

    def scale_window(self, factor):
        geometry = self.geometry()
        self.WIDTH = geometry.width() * factor
        self.HEIGHT = geometry.height() * factor
        self.resize(self.HEIGHT, self.WIDTH)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.move(200, 200)
        self.scale_window(1)
        self.search_widget = QSearchLayout(self)
        self.list_widget   = QListLayout(self)

        # A
        self.outerLayout = QVBoxLayout()
        self.outerLayout.addLayout(self.search_widget)
        self.setLayout(self.outerLayout)

        # S
        scroll_area = QScrollArea()
        self.outerLayout.addWidget(scroll_area)
        scroll_area.setWidgetResizable(True)

        # B
        b_widget = QWidget()
        b_widget.setLayout(self.list_widget)
        scroll_area.setWidget(b_widget)
        
    def moveEvent(self, event):
        new_pos = event.pos()
        self.x, self.y = new_pos.x(), new_pos.y()
        super().moveEvent(event) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindows()
    win.show()
    sys.exit(app.exec_())