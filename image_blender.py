from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2


class ImageBlender(QWidget):
    def __init__(self):
        super().__init__()
        self.image1 = None
        self.image2 = None
        self.blended_image = None
        self.blending_factor = 0.5
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Blender')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Add label to display the blended image
        self.blended_image_label = QLabel()
        self.blended_image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.blended_image_label)

        # Add text box to display current blending factor value
        self.blending_factor_textbox = QLineEdit()
        self.blending_factor_textbox.setReadOnly(True)
        self.blending_factor_textbox.setAlignment(Qt.AlignCenter)
        self.blending_factor_textbox.setVisible(False)
        layout.addWidget(self.blending_factor_textbox)

        # Add button to select images
        self.select_images_button = QPushButton('Select Images')
        self.select_images_button.clicked.connect(self.selectImages)
        layout.addWidget(self.select_images_button)

        # Add slider to control blending factor (initially hidden)
        self.blending_slider = QSlider(Qt.Horizontal)
        self.blending_slider.setMinimum(0)
        self.blending_slider.setMaximum(100)
        self.blending_slider.setValue(50)
        self.blending_slider.setTickInterval(1)
        self.blending_slider.setTickPosition(QSlider.TicksBelow)
        self.blending_slider.valueChanged.connect(self.updateBlendedImage)
        self.blending_slider.setVisible(False)
        layout.addWidget(self.blending_slider)

        # Add button to save image (initially hidden)
        self.save_image_button = QPushButton('Save Image')
        self.save_image_button.clicked.connect(self.saveImage)
        self.save_image_button.setVisible(False)
        layout.addWidget(self.save_image_button)

        self.setLayout(layout)

    def selectImages(self):
        options = QFileDialog.Options()
        file_name1, _ = QFileDialog.getOpenFileName(self, "Select Image 1", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        file_name2, _ = QFileDialog.getOpenFileName(self, "Select Image 2", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_name1 and file_name2:
            self.image1 = cv2.imread(file_name1)
            self.image2 = cv2.imread(file_name2)

            if self.image1 is None or self.image2 is None:
                print("Error loading images!")
                return

            # Check if dimensions match
            if self.image1.shape != self.image2.shape:
                # Resize the images to have the same dimensions
                height = min(self.image1.shape[0], self.image2.shape[0])
                width = min(self.image1.shape[1], self.image2.shape[1])

                self.image1 = cv2.resize(self.image1, (width, height))
                self.image2 = cv2.resize(self.image2, (width, height))

            # Show the textbox
            self.blending_factor_textbox.setVisible(True)
            # Show the slider
            self.blending_slider.setVisible(True)
            # Show the "Save Image" button
            self.save_image_button.setVisible(True)

            self.updateBlendedImage()

    def updateBlendedImage(self):
        if self.image1 is not None and self.image2 is not None:
            self.blending_factor = self.blending_slider.value() / 100.0
            self.blending_factor_textbox.setText(f'Blending Factor: {self.blending_factor:.2f}')
            blended_image = cv2.addWeighted(self.image1, self.blending_factor, self.image2, 1 - self.blending_factor, 0)
            blended_image_rgb = cv2.cvtColor(blended_image, cv2.COLOR_BGR2RGB)
            self.blended_image = blended_image_rgb
            q_image = QImage(blended_image_rgb.data, blended_image_rgb.shape[1], blended_image_rgb.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.blended_image_label.setPixmap(pixmap)
            self.blended_image_label.setScaledContents(True)

    def saveImage(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)", options=options)
        if file_name:
            cv2.imwrite(file_name, cv2.cvtColor(self.blended_image, cv2.COLOR_BGR2RGB))
            QMessageBox.information(self, "Image Saved", "The blended image has been saved successfully!")


if __name__ == '__main__':
    app = QApplication([])
    window = ImageBlender()
    window.show()
    app.exec_()
