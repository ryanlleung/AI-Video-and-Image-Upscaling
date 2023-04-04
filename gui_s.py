
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import cv2
from cv2 import dnn_superres
from img_ops import upscale_img
from PIL import Image

COL1_WIDTH = 200
COL2_WIDTH = 500
ROW1_HEIGHT = 500
ROW2_HEIGHT = 150

Font = 'Helvetica'
Size = 10

class FileOps(QWidget):

    def __init__(self):
        super(FileOps, self).__init__()
        self.initUI()

    def initUI(self):

        self.file_layout = QVBoxLayout()

        self.title = QLabel('Queue')
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setFont(QFont(Font, Size))
        self.title.setFixedHeight(Size+5)

        self.queue_list = QListWidget()
        
        self.buttons_layout = QHBoxLayout()

        self.file_button = QPushButton('Add File(s)')
        self.file_button.clicked.connect(self.add_files)

        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset)

        self.buttons_layout.addWidget(self.file_button)
        self.buttons_layout.addWidget(self.reset_button)

        self.file_layout.addWidget(self.title)
        self.file_layout.addWidget(self.queue_list)
        self.file_layout.addLayout(self.buttons_layout)

        self.setLayout(self.file_layout)
        self.setFixedSize(COL1_WIDTH, ROW1_HEIGHT)
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select File(s)', '', 'All Files (*)')
        for file in files:
            self.queue_list.addItem(file)

    def reset(self):
        self.queue_list.clear()
        if hasattr(self, 'outdir'):
            del self.outdir
        print('Reset')

class MediaDisplay(QWidget):

    def __init__(self):
        super(MediaDisplay, self).__init__()
        self.initUI()

    def initUI(self):

        self.media_layout = QVBoxLayout()

        self.title = QLabel('Media')
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setFont(QFont(Font, Size))
        self.title.setFixedHeight(Size+5)

        self.media_label = QLabel()
        self.media_label.setScaledContents(True)
        self.media_label.setAlignment(Qt.AlignCenter)
        self.media_label.setStyleSheet("background-color: white; border: 1px solid grey;")

        self.media_description = QLineEdit()
        self.media_description.setReadOnly(True)

        self.media_layout.addWidget(self.title)
        self.media_layout.addWidget(self.media_label)
        self.media_layout.addWidget(self.media_description)

        self.setLayout(self.media_layout)
        self.setFixedSize(COL2_WIDTH, ROW1_HEIGHT)

    def set_image(self, path):
        self.media_label.setPixmap(QPixmap(path))

    def set_description(self, description):
        self.media_description.setText(description)

class Settings(QWidget):

    def __init__(self):
        super(Settings, self).__init__()
        self.initUI()

    def initUI(self):

        self.settings_layout = QVBoxLayout()

        self.title = QLabel('Settings')
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setFont(QFont(Font, Size))
        self.title.setFixedHeight(Size+5)

        ## Model Selection ##
        self.model_layout = QHBoxLayout()

        self.model_label = QLabel('Model:')
        self.model_combo = QComboBox()
        self.model_combo.addItems(['EDSR', 'ESPCN', 'FSRCNN', 'LapSRN'])
        self.model_combo.setCurrentIndex(3)

        self.model_layout.addWidget(self.model_label)
        self.model_layout.addWidget(self.model_combo)

        ## Scale Line ##
        self.scale_layout = QHBoxLayout()

        self.scale_label = QLabel('Scale:')
        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(2, 8)
        self.scale_spin.setValue(2)

        self.scale_layout.addWidget(self.scale_label)
        self.scale_layout.addWidget(self.scale_spin)

        ## Height Line ##
        self.height_layout = QHBoxLayout()

        self.height_button = QPushButton('Height:')
        self.height_button.setAlignment(Qt.AlignLeft)
        self.height_button.clicked.connect(self.set_height)        
        self.height_box = QLineEdit()

        self.height_layout.addWidget(self.height_button)
        self.height_layout.addWidget(self.height_box)

        ## Width Line ##
        self.width_layout = QHBoxLayout()
        
        self.width_button = QPushButton('Width:')
        self.width_button.setAlignment(Qt.AlignLeft)
        self.width_button.clicked.connect(self.set_width)
        self.width_box = QLineEdit()

        self.width_layout.addWidget(self.width_button)
        self.width_layout.addWidget(self.width_box)

        ## Output Directory Selection ##
        self.outdir_button = QPushButton('Set Output Directory')
        self.outdir_button.clicked.connect(self.set_outdir)

        self.settings_layout.addWidget(self.title)
        self.settings_layout.addLayout(self.model_layout)
        self.settings_layout.addLayout(self.scale_layout)
        self.settings_layout.addLayout(self.height_layout)
        self.settings_layout.addLayout(self.width_layout)
        self.settings_layout.addWidget(self.outdir_button)

        self.setLayout(self.settings_layout)
        self.setFixedSize(COL1_WIDTH, ROW2_HEIGHT)

    def set_outdir(self):
        self.outdir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        

class Console(QWidget):

    def __init__(self):
        super(Console, self).__init__()
        self.initUI()

    def initUI(self):
            
        self.console_layout = QVBoxLayout()

        self.console_label = QLabel('Console')
        self.console_label.setAlignment(Qt.AlignLeft)
        self.console_label.setFont(QFont(Font, Size))
        self.console_label.setFixedHeight(Size+5)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)

        self.console_layout.addWidget(self.console_label)
        self.console_layout.addWidget(self.console)

        self.setLayout(self.console_layout)
        self.setFixedSize(COL2_WIDTH, ROW2_HEIGHT)

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        fileops_widget = FileOps()
        media_display = MediaDisplay()
        settings = Settings()
        console = Console()

        ####### Main ########
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(fileops_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(media_display, 0, 1, 1, 1)
        self.main_layout.addWidget(settings, 1, 0, 1, 1)
        self.main_layout.addWidget(console, 1, 1, 1, 1)

        self.setLayout(self.main_layout)

        ###---------Window---------###

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle('AI Upscaler')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
