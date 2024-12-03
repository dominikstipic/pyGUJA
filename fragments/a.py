import sys
from PyQt5.QtWidgets import QApplication, QScrollArea, QWidget, QVBoxLayout, QLabel

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    scroll_area = QScrollArea()
    layout.addWidget(scroll_area)
    scroll_area.setWidgetResizable(True)

    ## 
    scroll_area_widget = QWidget()
    scroll_area_layout = QVBoxLayout()
    scroll_area_widget.setLayout(scroll_area_layout)

    
    scroll_area.setWidget(scroll_area_widget)  # Set 1 
   
    # Add lots of labels to make the content exceed the viewport
    for i in range(50):
        label = QLabel(f"Label {i+1}")
        scroll_area_layout.addWidget(label)

    window.show()
    sys.exit(app.exec_())