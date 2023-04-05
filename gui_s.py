
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import cv2
from cv2 import dnn_superres
from img_ops import upscale_ff
from PIL import Image

COL1_WIDTH = 250
COL2_WIDTH = 500
ROW1_HEIGHT = 500
ROW2_HEIGHT = 175

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
        self.title.setFixedHeight(Size+10)

        self.queue_list = QListWidget()
        
        self.buttons_layout = QHBoxLayout()
        self.file_button = QPushButton('Add File(s)')
        self.reset_button = QPushButton('Reset')
        self.buttons_layout.addWidget(self.file_button)
        self.buttons_layout.addWidget(self.reset_button)

        self.file_layout.addWidget(self.title)
        self.file_layout.addWidget(self.queue_list)
        self.file_layout.addLayout(self.buttons_layout)

        self.setLayout(self.file_layout)
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(COL1_WIDTH, ROW1_HEIGHT)

class MediaDisplay(QWidget):

    def __init__(self):
        super(MediaDisplay, self).__init__()
        self.initUI()

    def initUI(self):

        self.media_layout = QVBoxLayout()

        self.title = QLabel('Media')
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setFont(QFont(Font, Size))
        self.title.setFixedHeight(Size+10)

        self.media_label = QLabel()
        self.media_label.setScaledContents(True)
        self.media_label.setAlignment(Qt.AlignCenter)
        self.media_label.setStyleSheet("background-color: white; border: 1px solid grey;")

        self.media_desc_layout = QHBoxLayout()
        self.media_name = QLineEdit()
        self.media_name.setReadOnly(True)
        self.media_info = QLineEdit()
        self.media_info.setReadOnly(True)
        self.media_info.setFixedWidth(150)
        self.media_info.setAlignment(Qt.AlignRight)
        self.media_desc_layout.addWidget(self.media_name)
        self.media_desc_layout.addWidget(self.media_info)

        self.media_layout.addWidget(self.title)
        self.media_layout.addWidget(self.media_label)
        self.media_layout.addLayout(self.media_desc_layout)

        self.setLayout(self.media_layout)
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(COL2_WIDTH, ROW1_HEIGHT)

class Settings(QWidget):

    def __init__(self):
        super(Settings, self).__init__()
        self.initUI()

    def initUI(self):

        self.settings_layout = QVBoxLayout()

        self.title = QLabel('Settings')
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setFont(QFont(Font, Size))
        self.title.setFixedHeight(Size+10)

        ## Model Selection ##
        self.model_layout = QHBoxLayout()

        self.model_label = QLabel('  Model:')
        self.model_combo = QComboBox()
        self.model_combo.addItems(['EDSR', 'ESPCN', 'FSRCNN', 'LapSRN'])
        self.model_combo.setCurrentIndex(3)

        self.model_layout.addWidget(self.model_label)
        self.model_layout.addWidget(self.model_combo)

        ## Scale Line ##
        self.scale_layout = QHBoxLayout()

        self.scale_button = QPushButton(' Scale:')
        self.scale_button.setStyleSheet('text-align:left;')
        self.scale_button.setFixedWidth(80)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setDecimals(2)
        self.scale_spin.setRange(0.125, 8)
        self.scale_spin.setValue(2)

        self.scale_layout.addWidget(self.scale_button)
        self.scale_layout.addWidget(self.scale_spin)

        ## Height Line ##
        self.height_layout = QHBoxLayout()

        self.height_button = QPushButton(' Height:')
        self.height_button.setStyleSheet('text-align:left;')
        self.height_button.setFixedWidth(80)     
        self.height_box = QLineEdit()
        self.height_box.setReadOnly(True)
        self.height_box.setPlaceholderText('---')

        self.height_layout.addWidget(self.height_button)
        self.height_layout.addWidget(self.height_box)
        self.height_layout.addWidget(QLabel(' px'))

        ## Width Line ##
        self.width_layout = QHBoxLayout()
        
        self.width_button = QPushButton(' Width:')
        self.width_button.setStyleSheet('text-align:left;')
        self.width_button.setFixedWidth(80)
        self.width_box = QLineEdit()
        self.width_box.setReadOnly(True)
        self.width_box.setPlaceholderText('---')

        self.width_layout.addWidget(self.width_button)
        self.width_layout.addWidget(self.width_box)
        self.width_layout.addWidget(QLabel(' px'))

        ## Output Directory Selection ##
        self.outdir_button = QPushButton('Set Output Directory')

        self.settings_layout.addWidget(self.title)
        self.settings_layout.addLayout(self.model_layout)
        self.settings_layout.addLayout(self.scale_layout)
        self.settings_layout.addLayout(self.height_layout)
        self.settings_layout.addLayout(self.width_layout)
        self.settings_layout.addWidget(self.outdir_button)

        self.setLayout(self.settings_layout)
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(COL1_WIDTH, ROW2_HEIGHT)

class Console(QWidget):

    def __init__(self):
        super(Console, self).__init__()
        self.initUI()

    def initUI(self):
            
        self.console_layout = QVBoxLayout()

        self.console_label = QLabel('Console')
        self.console_label.setAlignment(Qt.AlignLeft)
        self.console_label.setFont(QFont(Font, Size))
        self.console_label.setFixedHeight(Size+10)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)

        self.line_layout = QHBoxLayout()
        self.line = QLineEdit()
        self.line.setReadOnly(True)
        self.line.setPlaceholderText(' Set Output Directory')
        self.start_button = QPushButton('Start')
        self.start_button.setStyleSheet('text-align:center;')
        self.start_button.setFixedWidth(80)
        self.line_layout.addWidget(self.line)
        self.line_layout.addWidget(self.start_button)

        self.console_layout.addWidget(self.console_label)
        self.console_layout.addWidget(self.console)
        self.console_layout.addLayout(self.line_layout)

        self.setLayout(self.console_layout)
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(COL2_WIDTH, ROW2_HEIGHT)

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.file_list = []
        self.initUI()
        self.to_scale()

    def initUI(self):

        self.fileops = FileOps()
        self.media_display = MediaDisplay()
        self.settings = Settings()
        self.console = Console()

        self.fileops.file_button.clicked.connect(self.add_files)
        self.fileops.reset_button.clicked.connect(self.reset)
        self.fileops.queue_list.itemSelectionChanged.connect(self.selected_item)

        self.settings.outdir_button.clicked.connect(self.set_outdir)
        self.settings.scale_button.clicked.connect(self.to_scale)
        self.settings.height_button.clicked.connect(self.to_height)
        self.settings.width_button.clicked.connect(self.to_width)

        self.settings.scale_spin.valueChanged.connect(self.set_scale)
        self.settings.height_box.returnPressed.connect(self.set_height)
        self.settings.width_box.returnPressed.connect(self.set_width)

        self.console.start_button.clicked.connect(self.start_process)

        ####### Main ########
        self.main_layout = QGridLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.fileops, 0, 0, 1, 1)
        self.main_layout.addWidget(self.media_display, 0, 1, 1, 1)
        self.main_layout.addWidget(self.settings, 1, 0, 1, 1)
        self.main_layout.addWidget(self.console, 1, 1, 1, 1)

        self.setLayout(self.main_layout)

        ##### Set Flags #####
        self.by_scale = True
        self.by_height = False
        self.by_width = False

        ###---------Window---------###

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle('AI Upscaler')
        self.show()

    def cprint(self, text):
        self.console.console.append(f'>>   {text}')

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select File(s)', '', 'All Files (*)')
        for file in files:
            self.file_list.append(file)
            self.fileops.queue_list.addItem(os.path.basename(os.path.dirname(file)) + '/' + os.path.basename(file))

    def reset(self):
        self.file_list = []
        self.fileops.queue_list.clear()
        if hasattr(self.fileops, 'outdir'):
            del self.fileops.outdir
            self.console.line.setPlaceholderText(' Set Output Directory')
        self.file_list = []
        self.cprint('Reset')

    # Function to enable scale input
    def to_scale(self):
        self.by_scale = True
        self.by_height = False
        self.by_width = False
        self.settings.scale_spin.setEnabled(True)
        self.settings.scale_spin.setStyleSheet('color:black;')
        self.settings.height_box.setReadOnly(True)
        self.settings.height_box.setStyleSheet('color:grey;')
        self.settings.width_box.setReadOnly(True)
        self.settings.width_box.setStyleSheet('color:grey;')

    # Function to enable height input
    def to_height(self):
        self.by_scale = False
        self.by_height = True
        self.by_width = False
        self.settings.scale_spin.setEnabled(False)
        self.settings.scale_spin.setStyleSheet('color:grey;')
        self.settings.height_box.setReadOnly(False)
        self.settings.height_box.setPlaceholderText('')
        self.settings.height_box.setStyleSheet('color:black;')
        self.settings.width_box.setReadOnly(True)
        self.settings.width_box.setStyleSheet('color:grey;')

    # Function to enable width input
    def to_width(self):
        self.by_scale = False
        self.by_height = False
        self.by_width = True
        self.settings.scale_spin.setEnabled(False)
        self.settings.scale_spin.setStyleSheet('color:grey;')
        self.settings.height_box.setReadOnly(True)
        self.settings.height_box.setStyleSheet('color:grey;')
        self.settings.width_box.setReadOnly(False)
        self.settings.width_box.setPlaceholderText('')
        self.settings.width_box.setStyleSheet('color:black;')

    # Function to base output size on scale
    def set_scale(self, value, path=None):

        if path is None:
            try: path = self.file_list[self.fileops.queue_list.currentRow()]
            except: 
                self.cprint('No file selected')
                return

        img = cv2.imread(path)
        height, width, _ = img.shape
        self.scale = self.settings.scale_spin.value()

        new_height = int(height * self.scale)
        self.settings.height_box.setText(str(new_height))
        new_width = int(width * self.scale)
        self.settings.width_box.setText(str(new_width))

    # Function to base output size on height
    def set_height(self, path=None, getHeight=True):

        if path is None:
            try: path = self.file_list[self.fileops.queue_list.currentRow()]
            except: 
                self.cprint('No file selected')
                return
    
        img = cv2.imread(path)
        height, width, _ = img.shape
        if self.settings.height_box.text() == '':
            self.cprint('Please enter a height')
            return
        
        if getHeight or not hasattr(self, 'new_height'):
            print('got height from text')
            self.new_height = float(self.settings.height_box.text())

        self.scale = self.new_height / height
        if self.scale < 0.125:
            self.scale = 0.125
            self.new_height = int(height * 0.125)
            self.cprint(f'Height too small. Flooring to {self.new_height} px.')
            self.settings.height_box.setText(f'{self.new_height}')
        elif self.scale > 8:
            self.scale = 8
            self.new_height = int(height * 8)
            self.cprint(f'Height too large. Capping to {self.new_height} px.')
            self.settings.height_box.setText(f'{self.new_height}')

        self.settings.scale_spin.setValue(self.scale)
        self.settings.height_box.setText(f'{int(self.new_height)}')
        self.new_width = width * self.scale
        self.settings.width_box.setText(f'{int(self.new_width)}')
        

    # Function to base output scale on width
    def set_width(self, path=None, getWidth=True):

        if path is None:
            try: path = self.file_list[self.fileops.queue_list.currentRow()]
            except: 
                self.cprint('No file selected')
                return
    
        img = cv2.imread(path)
        height, width, _ = img.shape
        if self.settings.width_box.text() == '':
            self.cprint('Please enter a width')
            return

        if getWidth or not hasattr(self, 'new_width'):
            print('got width from text')
            self.new_width = float(self.settings.width_box.text())

        self.scale = self.new_width / width
        if self.scale < 0.125:
            self.scale = 0.125
            self.new_width = int(width * 0.125)
            self.cprint(f'Width too small. Flooring to {self.new_width} px.')
            self.settings.width_box.setText(f'{self.new_width}')
        elif self.scale > 8:
            self.scale = 8
            self.new_width = int(width * 8)
            self.cprint(f'Width too large. Capping to {self.new_width} px.')
            self.settings.width_box.setText(f'{self.new_width}')

        self.settings.scale_spin.setValue(self.scale)
        self.settings.width_box.setText(f'{int(self.new_width)}')
        self.new_height = height * self.scale
        self.settings.height_box.setText(f'{int(self.new_height)}')

    # Function to handle selection changes in the queue list
    def selected_item(self):

        path = self.file_list[self.fileops.queue_list.currentRow()]
        self.set_description(path)
        self.set_image(path)
        if self.by_scale:
            self.set_scale(path)
        elif self.by_height:
            self.set_height(path, getHeight=False)
        elif self.by_width:
            self.set_width(path, getWidth=False)

    # Function to set image in media display
    def set_image(self, path):
        
        label = self.media_display.media_label
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(label.width()-2, label.height()-2, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        width_diff = label.width() - scaled_pixmap.width()
        height_diff = label.height() - scaled_pixmap.height()

        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setContentsMargins(width_diff//2, height_diff//2, width_diff//2, height_diff//2)

    # Function to set description in media display
    def set_description(self, path):

        img = cv2.imread(path)
        height, width, _ = img.shape
        size = os.path.getsize(path)
        size = f'{size/1000000:.2f} MB' if size > 1000000 else f'{size/1000:.2f} KB'

        self.media_display.media_name.setText(f' {path}')
        self.media_display.media_info.setText(f'{width}x{height} px  {size} ')

    # Function to set output directory
    def set_outdir(self):
        self.outdir = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        self.console.line.setText(f" {self.outdir}")
        print(self.outdir)

    # Function to start process
    def start_process(self):
        path = self.file_list[self.fileops.queue_list.currentRow()]
        basename, extension = os.path.splitext(os.path.basename(path))
        new_name = f'{basename}_x{self.scale:.1f}{extension}'
        out_path = os.path.join(self.outdir, new_name)

        self.cprint(f'Processing: {new_name} ...')

        upscale_ff(path, out_path, scale=self.scale)

        self.cprint(f'Finished: {new_name}')

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
