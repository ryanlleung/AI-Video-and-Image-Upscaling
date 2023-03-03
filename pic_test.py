
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class PictureDisplay(QWidget):
    def __init__(self, image_path):
        super().__init__()

        # Create a QLabel widget and set its minimum size
        self.label = QLabel(self)
        self.label.setMinimumSize(400, 400)

        # Load the image file and create a QPixmap object from it
        pixmap = QPixmap(image_path)

        # Set the QPixmap object as the QLabel's pixmap and get its size
        self.label.setPixmap(pixmap)
        pixmap_size = pixmap.size()

        # Create a QSizePolicy object for the QLabel
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the QLabel's size policy to the QSizePolicy object
        self.label.setSizePolicy(size_policy)

        # Create a QSize object with the dimensions of the QLabel widget
        label_size = QSize(self.label.width(), self.label.height())

        # Use the QPixmap.scaled() method to scale the QPixmap object to fit the QLabel's size while maintaining its aspect ratio
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

        # Set the scaled QPixmap object as the QLabel's pixmap
        self.label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        # When the window is resized, get the new size of the QLabel widget and scale the QPixmap object to fit the new size while maintaining its aspect ratio
        label_size = QSize(self.label.width(), self.label.height())
        pixmap = self.label.pixmap()
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    picture_display = PictureDisplay('./medias/Array Targetry.png')
    picture_display.show()
    sys.exit(app.exec_())




