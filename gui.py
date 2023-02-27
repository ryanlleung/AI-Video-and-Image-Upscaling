
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
	
    def initUI(self):
        
        # Create before layout
        self.before_layout = QVBoxLayout()
        self.before_layout.setContentsMargins(0, 0, 0, 0)
        self.before_title = QLabel('Original')
        self.before_title.setFont(QFont('Helvetica', 10))
        self.before_img = QLabel()
        self.before_img.setAlignment(Qt.AlignCenter)
        self.before_img.setStyleSheet("background-color: black;")
        self.before_layout.addWidget(self.before_title)
        self.before_layout.addWidget(self.before_img)
        self.before_widget = QWidget()
        self.before_widget.setLayout(self.before_layout)

        pixmap = QPixmap('./medias/Array.png')
        pixmap = pixmap.scaled(self.before_img.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.before_img.setPixmap(pixmap)

        # Create after layout 
        self.after_layout = QVBoxLayout()
        self.after_layout.setContentsMargins(0, 0, 0, 0)
        self.after_title = QLabel('Result')
        self.after_title.setFont(QFont('Helvetica', 10))
        self.after_img = QLabel()
        self.after_img.setAlignment(Qt.AlignCenter)
        self.after_img.setStyleSheet("background-color: black;")
        self.after_layout.addWidget(self.after_title)
        self.after_layout.addWidget(self.after_img)
        self.after_widget = QWidget()
        self.after_widget.setLayout(self.after_layout)

        pixmap = QPixmap('./medias/Non-motorised.png')
        pixmap = pixmap.scaled(self.after_img.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.after_img.setPixmap(pixmap)

        # Create arrow
        self.arrow = QLabel('→')
        self.arrow.setAlignment(Qt.AlignCenter)
        self.arrow.setFont(QFont('Arial', 15))
        self.arrow.setStyleSheet("font-weight: bold")

        # Create media layout
        self.media_layout = QHBoxLayout()
        self.media_layout.setContentsMargins(0, 0, 0, 0)
        self.media_layout.addWidget(self.before_widget)
        self.media_layout.addWidget(self.arrow)
        self.media_layout.addWidget(self.after_widget)


        # Create queue
        self.queue = QListWidget()

        # add an item to the list
        self.queue.addItem('Item 1')

        # add multiple items to the list
        self.queue.addItems(['Item 2', 'Item 3', 'Item 4'])
        


        # Create settings layout
        self.settings_layout = QHBoxLayout()
        self.settings_layout.addWidget(self.queue)


        # Create main widget
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addLayout(self.media_layout)
        self.main_layout.addLayout(self.settings_layout)
        self.setLayout(self.main_layout)

        ## Window ##

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setGeometry(1600, 100, 750, 500)
        self.setWindowTitle('QSplitter demo')
        self.show()

            
def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()



"""# Set control layout
controlLayout = QHBoxLayout()
controlLayout.setContentsMargins(0, 0, 0, 0)
controlLayout.addWidget(self.play_button)
controlLayout.addWidget(self.time_label)
controlLayout.addWidget(self.time_slider)
controlLayout.addWidget(self.volume_slider)

# Set layout for video player
vp_layout = QVBoxLayout()
vp_layout.addWidget(self.video_widget)
vp_layout.addLayout(controlLayout)

# Set widget for video player
self.vp_widget = QWidget()
self.vp_widget.setLayout(vp_layout)"""