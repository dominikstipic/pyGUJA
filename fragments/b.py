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
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # A: manageable
    a = QWidget()
    a_layout = QVBoxLayout()
    a.setLayout(a_layout)
    
    # Make A scrolable
    scroll = QScrollArea() # Widget which is capable of being scrolled
    a_layout.addWidget(scroll) # Make it manageble
    scroll.setWidgetResizable(True)

    # B : managable
    b = QWidget()
    b_layout = QVBoxLayout()
    b.setLayout(b_layout)

    # A < B : both of them most be of the same type
    scroll.setWidget(b)

    for i in range(40):
        b_layout.addWidget(QLabel("123456789"))
        b_layout.addWidget(QLabel("123456789"))

        b_layout.addWidget(QLabel("123456789"))

    #scroll_layout = QVBoxLayout()
    #scroll_layout.addWidget(scroll)

    #scro.addWidget(QLabel("123456789"))

    #scroll_layout = QVBoxLayout()
    #scroll_layout.addWidget(scroll)

   
   #scroll_layout.addWidget(QLabel("123456789"))
   #scroll_layout.addWidget(QLabel("123456789"))
   #scroll_layout.addWidget(QLabel("123456789"))
   #scroll_layout.addWidget(QLabel("123456789"))
   #scroll_layout.addWidget(QLabel("123456789"))


    a.show()
    sys.exit(app.exec_())