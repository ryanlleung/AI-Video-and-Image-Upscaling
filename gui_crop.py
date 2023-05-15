
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
        x = event.x()
        y = event.y()
        self.mousePressed.emit(event)
        event.accept()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.mouseMoved.emit(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        x = event.x()
        y = event.y()
        self.mouseReleased.emit(event)
        event.accept()


class ImageWidget(QWidget):

    def __init__(self, image_path):
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
        self.resizeEdge = None

        # Load the image
        self.image = QPixmap(image_path)

        # Create a QLabel to display the image
        self.label = MQLabel(self)
        self.label.mousePressed.connect(self.mousePressEvent)
        self.label.mouseMoved.connect(self.mouseMoveEvent)
        self.label.mouseReleased.connect(self.mouseReleaseEvent)
        self.label.setPixmap(self.image)

        # Create a QRect to draw the rectangle
        self.rect = QRect(0, 0, 100, 100)
        self.rect_pen = QPen(QColor(255, 0, 0), 1)
        self.rect_brush = QBrush(Qt.NoBrush)

        # Set the size of the widget to the size of the image
        self.setFixedSize(self.image.width(), self.image.height())

    def paintEvent(self, event):
        # Call the paintEvent of the parent class
        super().paintEvent(event)

        # Clear the pixmap of the QLabel
        self.label.setPixmap(self.image)

        # Create a QPainter to draw the rectangle on the QLabel
        painter = QPainter(self.label.pixmap())
        painter.setPen(self.rect_pen)
        painter.setBrush(self.rect_brush)
        painter.drawRect(self.rect)
        painter.end()

    def mousePressEvent(self, event):

        if self.mode == 'move':
            self.drag_start = event.pos() - self.rect.topLeft()

        elif self.mode == 'resize':
            if self.resizeEdge == 'top_left':
                self.drag_start = event.pos() - self.rect.topLeft()
            elif self.resizeEdge == 'top_right':
                self.drag_start = event.pos() - self.rect.topRight()
            elif self.resizeEdge == 'bottom_left':
                self.drag_start = event.pos() - self.rect.bottomLeft()
            elif self.resizeEdge == 'bottom_right':
                self.drag_start = event.pos() - self.rect.bottomRight()
            elif self.resizeEdge == 'top':
                self.drag_start = event.pos() - self.rect.topLeft()
            elif self.resizeEdge == 'right':
                self.drag_start = event.pos() - self.rect.topRight()
            elif self.resizeEdge == 'bottom':
                self.drag_start = event.pos() - self.rect.bottomLeft()
            elif self.resizeEdge == 'left':
                self.drag_start = event.pos() - self.rect.topLeft()
            
    def mouseMoveEvent(self, event):

        #print(f'Position: {event.pos()}')

        EDGE_THRESH = 10

        # Check if the mouse is near any of the edges or corners of the rectangle
        self.edge_status['left'] = self.rect.left() - EDGE_THRESH < event.pos().x() < self.rect.left() + EDGE_THRESH and \
                                    self.rect.top() - EDGE_THRESH < event.pos().y() < self.rect.bottom() + EDGE_THRESH
        self.edge_status['right'] = self.rect.right() - EDGE_THRESH < event.pos().x() < self.rect.right() + EDGE_THRESH and \
                                    self.rect.top() - EDGE_THRESH < event.pos().y() < self.rect.bottom() + EDGE_THRESH
        self.edge_status['top'] = self.rect.top() - EDGE_THRESH < event.pos().y() < self.rect.top() + EDGE_THRESH and \
                                self.rect.left() - EDGE_THRESH < event.pos().x() < self.rect.right() + EDGE_THRESH
        self.edge_status['bottom'] = self.rect.bottom() - EDGE_THRESH < event.pos().y() < self.rect.bottom() + EDGE_THRESH and \
                                    self.rect.left() - EDGE_THRESH < event.pos().x() < self.rect.right() + EDGE_THRESH
        self.edge_status['top_left'] = self.edge_status['left'] and self.edge_status['top']
        self.edge_status['top_right'] = self.edge_status['right'] and self.edge_status['top']
        self.edge_status['bottom_left'] = self.edge_status['left'] and self.edge_status['bottom']
        self.edge_status['bottom_right'] = self.edge_status['right'] and self.edge_status['bottom']

        # Check if mouse is inside the rectangle and not near any of the edges or corners
        if not any(self.edge_status.values()) and not self.rect.contains(event.pos()):
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

        elif self.rect.contains(event.pos()):
            self.mode = 'move'
            self.setCursor(Qt.SizeAllCursor)

        else:
            raise Exception('Something went wrong')

        if self.drag_start is not None:
            # Calculate the new position of the top-left corner of the rectangle
            new_pos = event.pos() - self.drag_start

            if self.mode == 'move':
                self.rect.moveTopLeft(new_pos)
            elif self.mode == 'resize':
                if self.resizeEdge == 'top_left':
                    self.rect.setTopLeft(new_pos)
                elif self.resizeEdge == 'top_right':
                    self.rect.setTopRight(new_pos)
                elif self.resizeEdge == 'bottom_left':
                    self.rect.setBottomLeft(new_pos)
                elif self.resizeEdge == 'bottom_right':
                    self.rect.setBottomRight(new_pos)
                elif self.resizeEdge == 'top':
                    self.rect.setTop(new_pos.y())
                elif self.resizeEdge == 'right':
                    self.rect.setRight(new_pos.x())
                elif self.resizeEdge == 'bottom':
                    self.rect.setBottom(new_pos.y())
                elif self.resizeEdge == 'left':
                    self.rect.setLeft(new_pos.x())

            # Redraw the rectangle on the QLabel
            self.update()

    def mouseReleaseEvent(self, event):
        self.drag_start = None
        


class MainWindow(QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        
        # Create the ImageWidget
        self.image_widget = ImageWidget("medias/New_0 degree - Plan view_x0.5.png")

        box = QVBoxLayout(self)
        box.addWidget(self.image_widget)
        self.setLayout(box)

        self.setMouseTracking(True)

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle("GUI")
        self.show()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.NoButton:
            # print coordinates
            print(event.pos())


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