
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
        
        ### Before ###

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

        ### After ###

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

        ### Arrow ###

        self.arrow = QLabel('→')
        self.arrow.setAlignment(Qt.AlignCenter)
        self.arrow.setFont(QFont('Arial', 15))
        self.arrow.setStyleSheet("font-weight: bold")

        ##### Media #####

        self.media_layout = QHBoxLayout()
        self.media_layout.setContentsMargins(0, 0, 0, 0)
        self.media_layout.addWidget(self.before_widget)
        self.media_layout.addWidget(self.arrow)
        self.media_layout.addWidget(self.after_widget)
        self.media = QWidget()
        self.media.setLayout(self.media_layout)

        ############################################################

        ### Queue ###

        self.queue_title = QLabel('Queue')
        self.queue_title.setFont(QFont('Helvetica', 10))

        self.queue_list = QListWidget()
        self.queue_list.addItem('Item 1')
        self.queue_list.addItems(['Item 2', 'Item 3', 'Item 4'])

        self.queue_layout = QVBoxLayout()
        self.queue_layout.setContentsMargins(0, 0, 0, 0)
        self.queue_layout.addWidget(self.queue_title)
        self.queue_layout.addWidget(self.queue_list)

        self.queue = QWidget()
        self.queue.setLayout(self.queue_layout)

        ### Console ###

        # Create 

        # Create console widget
        self.console_layout = QVBoxLayout()
        self.console_layout.setContentsMargins(0, 0, 0, 0)

        self.console = QWidget()
        self.console.setLayout(self.console_layout)


        ### Options ###

        self.options_title = QLabel('Options')
        self.options_title.setFont(QFont('Helvetica', 10))

        # Create size widget
        self.height_label = QLabel('Height:')
        self.input_height = QLineEdit()
        self.input_height.setFixedWidth(50)
        self.input_height.returnPressed.connect(self.onHeightReturnPressed)
        self.width_label = QLabel('Width:')
        self.input_width = QLineEdit()
        self.input_width.setFixedWidth(50)
        self.input_width.returnPressed.connect(self.onWidthReturnPressed)

        self.size_layout = QHBoxLayout()
        self.size_layout.setContentsMargins(0, 0, 0, 0)
        self.size_layout.addWidget(self.height_label)
        self.size_layout.addWidget(self.input_height)
        self.size_layout.addWidget(self.width_label)
        self.size_layout.addWidget(self.input_width)

        self.size = QWidget()
        self.size.setLayout(self.size_layout)

        # Create scale widget
        self.scale_label = QLabel('Scale:')
        self.scale_radio_1 = QRadioButton('x2')
        self.scale_radio_2 = QRadioButton('x3')
        self.scale_radio_3 = QRadioButton('x4')
        self.scale_radio_4 = QRadioButton('x8')

        self.scale_layout = QHBoxLayout()
        self.scale_layout.setContentsMargins(0, 0, 0, 0)
        self.scale_layout.addWidget(self.scale_label)
        self.scale_layout.addWidget(self.scale_radio_1)
        self.scale_layout.addWidget(self.scale_radio_2)
        self.scale_layout.addWidget(self.scale_radio_3)
        self.scale_layout.addWidget(self.scale_radio_4)
        self.scale = QWidget()
        self.scale.setLayout(self.scale_layout)

        # Create model widget
        self.model_label = QLabel('Model:')
        self.model_combo = QComboBox()
        self.model_combo.addItems(['EDSR', 'ESPCN', 'FSRCNN', 'LapSRN'])
        self.model_combo.setCurrentIndex(3)

        self.model_layout = QHBoxLayout()
        self.model_layout.setContentsMargins(0, 0, 0, 0)
        self.model_layout.addWidget(self.model_label)
        self.model_layout.addWidget(self.model_combo)

        self.model = QWidget()
        self.model.setLayout(self.model_layout)

        # Create set button
        self.set_button = QPushButton('Set')

        # Create options widget
        self.options_layout = QVBoxLayout()
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.addWidget(self.options_title)
        self.options_layout.addWidget(self.size)
        self.options_layout.addWidget(self.scale)
        self.options_layout.addWidget(self.model)
        self.options_layout.addWidget(self.set_button)

        self.options = QWidget()
        self.options.setLayout(self.options_layout)

        ##### Settings #####

        # Create settings layout
        self.settings_layout = QHBoxLayout()
        self.settings_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_layout.addWidget(self.queue, 3)
        self.settings_layout.addWidget(self.console, 5)
        self.settings_layout.addWidget(self.options, 3)
        self.settings = QWidget()
        self.settings.setLayout(self.settings_layout)

        ############################################################

        ####### Main ########
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.addWidget(self.media, 7)
        self.main_layout.addWidget(self.settings, 3)
        self.setLayout(self.main_layout)

        ###---------Window---------###

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setGeometry(1600, 100, 750, 500)
        self.setWindowTitle('AI Upscaler')
        self.show()

    def onHeightReturnPressed(self):
        print(self.input_height.text())

    def onWidthReturnPressed(self):
        print(self.input_width.text())


            
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