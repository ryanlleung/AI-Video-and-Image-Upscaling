
import os
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import cv2
from cv2 import dnn_superres
from img_ops import upscale_ff
from PIL import Image


class MQLabel(QLabel):
    
    mousePressed = pyqtSignal(QMouseEvent)
    mouseMoved = pyqtSignal(QMouseEvent)
    mouseReleased = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover)
    
    def mousePressEvent(self, event):
        self.mousePressed.emit(event)
        event.accept()

    def mouseMoveEvent(self, event):
        self.mouseMoved.emit(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.mouseReleased.emit(event)
        event.accept()


class ImageWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        # Initialise variables
        self.drag_start = None
        self.edge_status = {'left': False, 
                            'right': False, 
                            'top': False, 
                            'bottom': False,
                            'top_left': False,
                            'top_right': False,
                            'bottom_left': False,
                            'bottom_right': False}
        self.mode = None
        self.unlock = True
        self.resizeEdge = None
        self.showGuides = True

        # Create a QLabel to display the image
        self.label = MQLabel(self)
        self.label.setFixedSize(1000, 500)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: white; border: 1px solid grey;")

        self.label.mousePressed.connect(self.mousePressEvent)
        self.label.mouseMoved.connect(self.mouseMoveEvent)
        self.label.mouseReleased.connect(self.mouseReleaseEvent)

        # Create a QRect to draw the cropping rectangle
        self.rtg = QRect(0, 0, 200, 200)
        self.rtg_pen = QPen(QColor(0, 255, 255), 1)
        self.rtg_brush = QBrush(Qt.NoBrush)

        # Create guide lines
        self.guide_v1 = QPen(QColor(0, 200, 200), 1, Qt.SolidLine)
        self.guide_v2 = QPen(QColor(0, 200, 200), 1, Qt.SolidLine)
        self.guide_h1 = QPen(QColor(0, 200, 200), 1, Qt.SolidLine)
        self.guide_h2 = QPen(QColor(0, 200, 200), 1, Qt.SolidLine)

        # Set widget size
        self.setFixedSize(self.label.width(), self.label.height())
        self.setImage('ico/white.png')


    def setImage(self, path):
        pixmap = QPixmap(path)
        self.scaled_pixmap = pixmap.scaled(self.label.width()-2, self.label.height()-2, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        width_diff = self.label.width() - self.scaled_pixmap.width()
        height_diff = self.label.height() - self.scaled_pixmap.height()

        self.label.setPixmap(self.scaled_pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setContentsMargins(width_diff//2, height_diff//2, width_diff//2, height_diff//2)
        
        self.rtg_X = width_diff//2
        self.rtg_Y = height_diff//2

        self.pixrtg = self.label.pixmap().rect()

        # print pixmap location
        print(f'pixmap: {self.label.pixmap().rect()}')
        # print label location
        print(f'label: {self.label.rect()}')


    def paintEvent(self, event):
        # Call the paintEvent of the parent class
        super().paintEvent(event)

        # Clear the pixmap of the QLabel
        self.label.setPixmap(self.scaled_pixmap)

        # Create a QPainter to draw the rectangle and guide lines on the QLabel
        painter = QPainter(self.label.pixmap())
        
        if self.showGuides:
            painter.setPen(self.guide_v1)
            painter.drawLine(self.rtg.width()//3 + self.rtg.x(), self.rtg.y(), self.rtg.width()//3 + self.rtg.x(), self.rtg.y() + self.rtg.height())
            painter.setPen(self.guide_v2)
            painter.drawLine(self.rtg.width()//3*2 + self.rtg.x(), self.rtg.y(), self.rtg.width()//3*2 + self.rtg.x(), self.rtg.y() + self.rtg.height())
            painter.setPen(self.guide_h1)
            painter.drawLine(self.rtg.x(), self.rtg.height()//3 + self.rtg.y(), self.rtg.x() + self.rtg.width(), self.rtg.height()//3 + self.rtg.y())
            painter.setPen(self.guide_h2)
            painter.drawLine(self.rtg.x(), self.rtg.height()//3*2 + self.rtg.y(), self.rtg.x() + self.rtg.width(), self.rtg.height()//3*2 + self.rtg.y())
            
        painter.setPen(self.rtg_pen)
        painter.setBrush(self.rtg_brush)
        painter.drawRect(self.rtg)

        painter.end()

    # Lock mode to prevent changing the mode while the mouse is pressed due to mouse moving too fast
    def mousePressEvent(self, event):

        print(f'Pressed')

        if self.unlock:
            self.unlock = False
            self.lockedMode = self.mode
            self.lockedEdge = self.resizeEdge

        if self.lockedMode == 'move':
            self.drag_start = event.pos() - self.rtg.topLeft()

        elif self.lockedMode == 'resize':
            if self.lockedEdge == 'top_left':
                self.drag_start = event.pos() - self.rtg.topLeft()
            elif self.lockedEdge == 'top_right':
                self.drag_start = event.pos() - self.rtg.topRight()
            elif self.lockedEdge == 'bottom_left':
                self.drag_start = event.pos() - self.rtg.bottomLeft()
            elif self.lockedEdge == 'bottom_right':
                self.drag_start = event.pos() - self.rtg.bottomRight()
            elif self.lockedEdge == 'top':
                self.drag_start = event.pos() - self.rtg.topLeft()
            elif self.lockedEdge == 'right':
                self.drag_start = event.pos() - self.rtg.bottomRight()
            elif self.lockedEdge == 'bottom':
                self.drag_start = event.pos() - self.rtg.bottomLeft()
            elif self.lockedEdge == 'left':
                self.drag_start = event.pos() - self.rtg.topLeft()
            
    def mouseMoveEvent(self, event):

        #print(f'Position: {event.pos()}')

        EDGE_THRESH = 10

        # Check if the mouse is near any of the edges or corners of the rectangle
        self.real_rtg = QRect(self.rtg.left()+self.rtg_X, self.rtg.top()+self.rtg_Y, self.rtg.width(), self.rtg.height())
        print('GlobalRtg', self.real_rtg.getCoords())

        self.rtg_coords = self.rtg.getCoords()
        print('LocalRtg', self.rtg_coords)

        print('LocalPixrtg:',self.pixrtg.getCoords(), '\n')

        self.edge_status['left'] = self.real_rtg.left() - EDGE_THRESH < event.pos().x() < self.real_rtg.left() + EDGE_THRESH and \
                                    self.real_rtg.top() - EDGE_THRESH < event.pos().y() < self.real_rtg.bottom() + EDGE_THRESH
        self.edge_status['right'] = self.real_rtg.right() - EDGE_THRESH < event.pos().x() < self.real_rtg.right() + EDGE_THRESH and \
                                    self.real_rtg.top() - EDGE_THRESH < event.pos().y() < self.real_rtg.bottom() + EDGE_THRESH
        self.edge_status['top'] = self.real_rtg.top() - EDGE_THRESH < event.pos().y() < self.real_rtg.top() + EDGE_THRESH and \
                                    self.real_rtg.left() - EDGE_THRESH < event.pos().x() < self.real_rtg.right() + EDGE_THRESH
        self.edge_status['bottom'] = self.real_rtg.bottom() - EDGE_THRESH < event.pos().y() < self.real_rtg.bottom() + EDGE_THRESH and \
                                        self.real_rtg.left() - EDGE_THRESH < event.pos().x() < self.real_rtg.right() + EDGE_THRESH
        self.edge_status['top_left'] = self.edge_status['left'] and self.edge_status['top']
        self.edge_status['top_right'] = self.edge_status['right'] and self.edge_status['top']
        self.edge_status['bottom_left'] = self.edge_status['left'] and self.edge_status['bottom']
        self.edge_status['bottom_right'] = self.edge_status['right'] and self.edge_status['bottom']

        # Check mouse location to determine the mode and cursor shape
        if not any(self.edge_status.values()) and not self.real_rtg.contains(event.pos()):
            self.setCursor(Qt.ArrowCursor)
            self.mode = None

        elif any(self.edge_status.values()):
            self.mode = 'resize'

            # Change the cursor shape if the mouse is near any of the edges or corners of the rectangle
            if self.edge_status['top_left'] or self.edge_status['bottom_right']:
                self.setCursor(Qt.SizeFDiagCursor)
                self.resizeEdge = 'top_left' if self.edge_status['top_left'] else 'bottom_right'
            elif self.edge_status['top_right'] or self.edge_status['bottom_left']:
                self.setCursor(Qt.SizeBDiagCursor)
                self.resizeEdge = 'top_right' if self.edge_status['top_right'] else 'bottom_left'
            elif self.edge_status['left'] or self.edge_status['right']:
                self.setCursor(Qt.SizeHorCursor)
                self.resizeEdge = 'left' if self.edge_status['left'] else 'right'
            elif self.edge_status['top'] or self.edge_status['bottom']:
                self.setCursor(Qt.SizeVerCursor)
                self.resizeEdge = 'top' if self.edge_status['top'] else 'bottom'

        elif self.real_rtg.contains(event.pos()):
            self.mode = 'move'
            self.setCursor(Qt.SizeAllCursor)

        else:
            raise Exception('Mouse location error')

         # If the mouse is pressed
        if self.drag_start is not None:

            new_pos = event.pos() - self.drag_start

            if self.lockedMode == 'move':
                self.rtg.moveTopLeft(new_pos)
            elif self.lockedMode == 'resize':
                if self.lockedEdge == 'top' or self.lockedEdge == 'top_left' or self.lockedEdge == 'top_right':
                    newSize = self.rtg.bottomLeft() - new_pos
                    if newSize.y() > 2*EDGE_THRESH:
                        self.rtg.setTop(new_pos.y())
                if self.lockedEdge == 'right' or self.lockedEdge == 'top_right' or self.lockedEdge == 'bottom_right':
                    newSize = self.rtg.topLeft() - new_pos
                    if -newSize.x() > 2*EDGE_THRESH:
                        self.rtg.setRight(new_pos.x())
                if self.lockedEdge == 'bottom' or self.lockedEdge == 'bottom_left' or self.lockedEdge == 'bottom_right':
                    newSize = self.rtg.topLeft() - new_pos
                    if -newSize.y() > 2*EDGE_THRESH:
                        self.rtg.setBottom(new_pos.y())
                if self.lockedEdge == 'left' or self.lockedEdge == 'top_left' or self.lockedEdge == 'bottom_left':
                    newSize = self.rtg.topRight() - new_pos
                    if newSize.x() > 2*EDGE_THRESH:
                        self.rtg.setLeft(new_pos.x())

            self.update()

    def mouseReleaseEvent(self, event):
        self.drag_start = None
        self.unlock = True
        
        # Limit rectangle size
        self.rtg_coords = self.rtg.getCoords()
        if self.rtg_coords[0] < 0:
            self.rtg.setLeft(0)
        if self.rtg_coords[1] < 0:
            self.rtg.setTop(0)
        if self.rtg_coords[2] > self.pixrtg.width():
            self.rtg.setRight(self.pixrtg.width()-2)
        if self.rtg_coords[3] > self.pixrtg.height():
            self.rtg.setBottom(self.pixrtg.height()-2)

        print('Released')


class MainWindow(QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        
        # Create the ImageWidget
        self.image_widget = ImageWidget()
        # self.image_widget.label.mousePressed.connect(self.mousePressEvent)
        self.image_widget.label.mouseMoved.connect(self.mouseMoveEvent)
        self.image_widget.label.mouseReleased.connect(self.mouseReleaseEvent)

        # Create the settings box
        self.settings_box = QVBoxLayout(self)

        # Top: Command box
        self.command_box = QVBoxLayout(self)
        self.command_box.setAlignment(Qt.AlignTop)

        self.oridims = QLabel("Original Dimensions")
        self.oridims.setContentsMargins(0, 10, 0, 0)
        self.oridims_box = QHBoxLayout(self)
        self.oridims_width = QLabel("Width: ")
        self.oridims_width_val = QLineEdit()
        self.oridims_width_val.setReadOnly(True)
        self.oridims_height = QLabel("Height: ")
        self.oridims_height_val = QLineEdit()
        self.oridims_height_val.setReadOnly(True)
        self.oridims_box.addWidget(self.oridims_width)
        self.oridims_box.addWidget(self.oridims_width_val)
        self.oridims_box.addWidget(self.oridims_height)
        self.oridims_box.addWidget(self.oridims_height_val)

        self.newdims = QLabel("Cropped Dimensions")
        self.newdims.setContentsMargins(0, 10, 0, 0)
        self.newdims_box = QHBoxLayout(self)
        self.newdims_width = QLabel("Width: ")
        self.newdims_width_val = QLineEdit()
        self.newdims_width_val.setReadOnly(True)
        self.newdims_height = QLabel("Height: ")
        self.newdims_height_val = QLineEdit()
        self.newdims_height_val.setReadOnly(True)
        self.newdims_box.addWidget(self.newdims_width)
        self.newdims_box.addWidget(self.newdims_width_val)
        self.newdims_box.addWidget(self.newdims_height)
        self.newdims_box.addWidget(self.newdims_height_val)

        self.command_box.addWidget(self.oridims)
        self.command_box.addLayout(self.oridims_box)
        self.command_box.addWidget(self.newdims)
        self.command_box.addLayout(self.newdims_box)

        self.command_widget = QWidget()
        self.command_widget.setFixedWidth(300)
        self.command_widget.setLayout(self.command_box)

        # Bottom: File box
        self.file_box = QHBoxLayout(self)
        self.file_box.setAlignment(Qt.AlignBottom)
        
        self.file_button = QPushButton("Open File")
        self.file_button.clicked.connect(lambda: self.openFile(imgpath=None))
        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.saveFile)

        self.file_box.addWidget(self.file_button)
        self.file_box.addWidget(self.save_button)

        self.settings_box.addWidget(self.command_widget)
        self.settings_box.addLayout(self.file_box)

        self.settings_widget = QWidget()
        self.command_widget.setFixedWidth(300)
        self.settings_widget.setLayout(self.settings_box)

        box = QHBoxLayout(self)
        box.addWidget(self.image_widget)
        box.addWidget(self.settings_widget)
        self.setLayout(box)

        self.setMouseTracking(True)

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle("GUI")
        self.show()

        self.openFile('./medias/New_0 degree - probe set-up_x0.5.png')

    def mouseMoveEvent(self, event):
        self.updateNewDims()

    def mouseReleaseEvent(self, event):
        self.updateNewDims()

    def updateNewDims(self):
        # Get the coordinates of the displayed pixmap rtg
        x0, y0, width, height = self.image_widget.pixrtg.getCoords()
        scale = float(width+1) / self.img.shape[1]
        c_x0, c_y0, c_x1, c_y1 = self.image_widget.rtg.getCoords()
        self.cropped_x0 = int(c_x0/scale)
        self.cropped_y0 = int(c_y0/scale)
        self.cropped_width = int((c_x1-c_x0)/scale)+4
        self.cropped_height = int((c_y1-c_y0)/scale)+4
        if self.cropped_width > self.img.shape[1]:
            self.cropped_width = self.img.shape[1]
        if self.cropped_height > self.img.shape[0]:
            self.cropped_height = self.img.shape[0]
        self.newdims_width_val.setText(str(self.cropped_width))
        self.newdims_height_val.setText(str(self.cropped_height))

    def openFile(self, imgpath=None):
        if imgpath is None:
            print('Open file')
            self.imgpath = QFileDialog.getOpenFileName(self, 'Open file', './medias', "Image files (*.jpg *.gif *.png)")[0]
            print('File opened')
            if self.imgpath == '': return
        else:
            print(f'Open file {imgpath}')
            self.imgpath = imgpath
        self.image_widget.setImage(self.imgpath)
        self.img = cv2.imread(self.imgpath)        
        self.oridims_width_val.setText(str(self.img.shape[1]))
        self.oridims_height_val.setText(str(self.img.shape[0]))

    def saveFile(self):
        print('Save file')
        cropped_img = self.img[self.cropped_y0:self.cropped_y0+self.cropped_height, self.cropped_x0:self.cropped_x0+self.cropped_width]
        cv2.imwrite('cropped.png', cropped_img)
        print('File saved')


app = QCoreApplication.instance()
if app is None:
    app = QApplication([])
window = MainWindow()
window.show()

try:
    from IPython.lib.guisupport import start_event_loop_qt5
    start_event_loop_qt5(app)
except ImportError:
    app.exec_()