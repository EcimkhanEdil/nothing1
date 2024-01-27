#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
    QApplication,QListWidget,
    QFileDialog,
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR,CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,
    EMBOSS,FIND_EDGES,SMOOTH,SMOOTH_MORE,SHARPEN,
    GaussianBlur,UnsharpMask
)

app=QApplication([])
win=QWidget()
win.resize(700,500)
win.setWindowTitle('Easy editor')
lb_image=QLabel('FILE')
btn_dir=QPushButton('Directory')
lw_files=QListWidget()

btn_left=QPushButton('left')
btn_right=QPushButton('right')
btn_flip=QPushButton('zerkalo')
btn_sharp=QPushButton('PE3KOCTb')
btn_bw=QPushButton('4/B')

row=QHBoxLayout()
col1=QVBoxLayout()
col2=QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image,95)
row_tools=QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1,20)
row.addLayout(col2,80)
win.setLayout(row)

win.show()

workdir=''

def filter(files, extentions):
    result=[]
    for filename in files:
        for ext in extentions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir=QFileDialog.getExistingDirectory()

def showFilenamesList():
    extentions=['.jpg','.png','.jpeg','.gif','.bmp']
    chooseWorkdir()
    filenames=filter(os.listdir(workdir),extentions)

    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image=None
        self.dir=None
        self.filename=None
        self.save_dir='Modified/'

    def LoadImage(self,dir,filename):
        self.filename=filename
        fullname=os.path.join(workdir,filename)
        self.image=Image.open(fullname)

    def showImage(self,path):
        lb_image.hide()
        pixmapimage=QPixmap(path)
        w,h=lb_image.width(),lb_image.height()
        pixmapimage=pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        path=os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname=os.path.join(path,self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image=self.image.convert('L')
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image=self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image=self.image.filter(SHARPEN)
        self.saveImage()
        image_path=os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

def showChosenImage():
    if lw_files.currentRow()>=0:
        filename=lw_files.currentItem().text()
        workimage.LoadImage(workdir,filename)
        workimage.showImage(os.path.join(workdir,workimage.filename))

workimage=ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)

lw_files.currentRowChanged.connect(showChosenImage)

app.exec()