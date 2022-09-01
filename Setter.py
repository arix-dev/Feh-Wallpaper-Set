#!/usr/bin/env python3
"""
FEH Wallpaper Setter for desktop enviroments that have no settings panel.
Writen in Python and Qt5
Version: 0.2
Author: Andrew Rix
"""

import sys, subprocess, os, requests, json, datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Feh Wallpaper Setter')
        self.setGeometry(0, 0, 580, 180)
        self.move(60, 45)

        def selectLocalWall():
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;JPEG Files (*.jpg)", options=options)
            if fileName:
                print(fileName)
                subprocess.run(['feh', '--bg-scale',  fileName])

        def selectRandWall():
            self.homeLoc = os.environ['HOME']
            if self.combo1.currentText() == 'Unsplash':
                response = requests.get("https://source.unsplash.com/random/1920x1080")
                with open(self.homeLoc + '/.randomOnlinepic.png' , 'wb') as f:
                    f.write(response.content)
                subprocess.run(['feh', '--bg-scale',  self.homeLoc + '/.randomOnlinepic.png'])
            elif self.combo1.currentText()  == 'Nasa':
                response = requests.get("https://source.unsplash.com/user/nasa")
                with open(self.homeLoc + '/.randomOnlinepic.png' , 'wb') as f:
                    f.write(response.content)
                subprocess.run(['feh', '--bg-scale',  self.homeLoc + '/.randomOnlinepic.png'])
            elif self.combo1.currentText()  == 'Bing':
                response = requests.get("https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US")
                bing_image_data = json.loads(response.text)
                bing_image_url = bing_image_data["images"][0]["url"]
                bing_image_url = bing_image_url.split("&")[0]
                full_image_url = "https://www.bing.com" + bing_image_url
                image_name = datetime.date.today().strftime("%Y%m%d")
                image_extension = bing_image_url.split(".")[-1]
                image_name = image_name + "." + image_extension
                img_data = requests.get(full_image_url).content
                with open(self.homeLoc + '/.randomOnlinepic.png' , 'wb') as f:
                    f.write(img_data)
                subprocess.run(['feh', '--bg-scale',  self.homeLoc + '/.randomOnlinepic.png'])
            else:
                messagebox.showinfo("Selected Source",self.combo1.currentText() )


        hbox = QHBoxLayout()
        frm1 = QFrame()
        self.btn1 = QPushButton(frm1)
        self.btn1.setText('Select Local Wallpaper')
        self.btn1.setGeometry(0, 0, 160, 24)
        self.btn1.setStyleSheet("QPushButton::hover"
                            "{"
                            "background-color : lightgreen;"
                            "}")
        self.btn1.clicked.connect(selectLocalWall)  # Connect clicked to selectLocalWall()

        self.btn2 = QPushButton(frm1)
        self.btn2.setText('Select Random Wallpaper')
        self.btn2.setGeometry(180, 0, 160, 24)
        self.btn2.setStyleSheet("QPushButton::hover"
                            "{"
                            "background-color : lightgreen;"
                            "}")
        self.btn2.clicked.connect(selectRandWall)  # Connect clicked to selectRandWall()

        self.label1 = QLabel(frm1)
        self.label1.setGeometry(0, 50, 110, 24)
        self.label1.setText('Random Source')

        self.combo1 = QComboBox(frm1)
        # setting geometry of combo box
        self.combo1.setGeometry(100, 47, 120, 30)
        random_list = ["Unsplash", "Nasa", "Bing"]
        # adding list of items to combo box
        self.combo1.addItems(random_list)

        hbox.addWidget(frm1)
        self.setLayout(hbox)
        self.show()

   

# Initialize App
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
