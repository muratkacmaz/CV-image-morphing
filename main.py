#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 17:21:55 2018

@author: muratkacmaz
"""

#Murat Kaçmaz 150140052

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout,QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np 
import cv2
import random

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
       # Check if a point is inside a rectangle


    def __init__(self):
        super(App, self).__init__()
        self.showFullScreen()
        self.LoadedTarget=None
        self.LoadedInput =None
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.title = 'Mapping'
        self.toolbar= self.addToolBar('Create Triangulation')
        self.toolbar= self.addToolBar('Morph')
        
        EqAction = QAction("Create Triangulation",self)
        EqAction.triggered.connect(self.triangleButtonClicked)
        self.toolbar.addAction(EqAction)
        
        EqAction = QAction("Morph",self)
        EqAction.triggered.connect(self.morphButton)
        self.toolbar.addAction(EqAction)
        
        action = QAction ("&Open Input",self)
        action.triggered.connect(self.openInputImage)
        
        action2 = QAction ("&Open Target",self)
        action2.triggered.connect(self.openTargetImage)
        
        action3 = QAction ("&EX1IT",self)
        action3.triggered.connect(self.closeApp)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(action)
        fileMenu.addAction(action2)
        fileMenu.addAction(action3)
        
        
        self.initUI()

    def openInputImage(self):
        self.inputLabel = QLabel('input')
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
       
 
        self.InputImage = cv2.imread(imagePath)
        self.LoadedInput = self.InputImage
        self.InputImage  = cv2.cvtColor(self.InputImage , cv2.COLOR_BGR2RGB)
        
     
        self.InputRed= self.InputImage [:,:,0]
 
        row,column= self.InputRed.shape  #shapeler aynı
        bytesPerLine = 3 * column
       
        
        self.inputPixmap = QImage(self.InputImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.inputLabel.setPixmap(QPixmap.fromImage(self.inputPixmap))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(self.inputLabel)
 
        self.canvasInput.draw()
       
    
        return NotImplementedError

    
    def openTargetImage(self):
        self.targetLabel= QLabel('target')
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
       
 
        self.targetImage = cv2.imread(imagePath)
        self.LoadedTarget= self.targetImage 
        self.targetImage  = cv2.cvtColor(self.targetImage , cv2.COLOR_BGR2RGB)
        
        self.TargetRed= self.targetImage [:,:,0]
        
        
        row,column= self.TargetRed.shape  #shapeler aynı
        bytesPerLine = 3 * column
        
        
        
        self.targetPixmap = QImage(self.targetImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.targetLabel.setPixmap(QPixmap.fromImage(self.targetPixmap))
        self.targetLabel.setAlignment(Qt.AlignCenter)
        self.targetGridBox.layout().addWidget(self.targetLabel)
        
    
        self.canvasTarget.draw()
 
        
        return NotImplementedError
    
    def closeApp(self):
        exit()
        app.quit()
        return NotImplementedError
  
    
    

        
        
        
    def initUI(self):
         
        self.gLayout = QGridLayout()
        
        self.figureInput = Figure()
        self.canvasInput =FigureCanvas(self.figureInput)
        self.figureTarget = Figure()
        self.canvasTarget =FigureCanvas(self.figureTarget)
        self.figureResult = Figure()
        self.canvasResult =FigureCanvas(self.figureResult)
        
        self.inputGridBox = QGroupBox('Input')
        inputLayout = QVBoxLayout()
        self.inputGridBox.setLayout(inputLayout)
        
        self.targetGridBox = QGroupBox('Target')
        targetLayout = QVBoxLayout()
        self.targetGridBox.setLayout(targetLayout)
        
        self.resultGridBox = QGroupBox('Result')
        resultLayout = QVBoxLayout()
        self.resultGridBox.setLayout(resultLayout)
        
        self.gLayout.addWidget(self.inputGridBox, 0, 0)
        self.gLayout.addWidget(self.targetGridBox, 0, 1)
        self.gLayout.addWidget(self.resultGridBox, 0, 2)
        
        self.window.setLayout(self.gLayout)
        self.setWindowTitle(self.title)
        self.show()







    def triangleButtonClicked(self):
        if  self.LoadedInput is None and  self.LoadedTarget is None:
            QMessageBox.about(self,"Error","Load input and target images")
            return NotImplementedError
        if  self.LoadedInput is None:
            QMessageBox.about(self,"Error","Load input image")
            return NotImplementedError
        elif self.LoadedTarget is None:
           QMessageBox.about(self,"Error","Load target image")
           return NotImplementedError
        filename1 = 'bushcopy.txt'
        filename2 = 'arniecopy.txt'
       
        self.data1 = []
        with open(filename1) as file:
            for line in file:
                x,y = line.split()
                self.data1.append((int(x),int(y)))
        self.data2 = []
        with open(filename2) as file:
            for line in file:
                x,y = line.split()
                self.data2.append((int(x),int(y)))
         
    
     
        im1Copy= self.InputImage.copy()
        size = self.InputImage.shape
        rect1 = (0,0,size[1],size[0])
        self.subdiv1 = cv2.Subdiv2D(rect1);
        
        for p in self.data1:
            self.subdiv1.insert(p)
                
        
        draw_delaunay(im1Copy,self.subdiv1,(255,255,255)) ;
        for p in self.data1:
            draw_point(im1Copy,p,(0,0,255))
        
         
        
        rect2 = (0,0,size[1],size[0])
        self.subdiv2 = cv2.Subdiv2D(rect2);
        im2Copy = self.targetImage.copy()
        for p in self.data2:
            self.subdiv2.insert(p)
                
        
        draw_delaunay(im2Copy,self.subdiv2,(255,255,255)) ;
        for p in self.data2:
            draw_point(im2Copy,p,(0,0,255))
        
        triangleList1 = self.subdiv1.getTriangleList();
        triangleList2 = self.subdiv2.getTriangleList();
        print(triangleList1[0])
         
        
        row,column= self.InputRed.shape
        bytesPerLine = 3 * column
        self.inputPixmap = QImage(im1Copy.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.inputLabel.setPixmap(QPixmap.fromImage(self.inputPixmap))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(self.inputLabel)
         
        self.targetPixmap = QImage(im2Copy.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.targetLabel.setPixmap(QPixmap.fromImage(self.targetPixmap))
        self.targetLabel.setAlignment(Qt.AlignCenter)
        self.targetGridBox.layout().addWidget(self.targetLabel)

        
    def morphButton(self):
        self.resultLabel= QLabel('result')
        triangleList1 = self.subdiv1.getTriangleList();
        triangleList2 = self.subdiv2.getTriangleList();
        resultImage  = np.zeros(self.InputImage.shape)
        
        for t in triangleList1:
            m = 0
            for i in range(6):
                if t[i] == 1440 or t[i]== -1440 :
                    m = 1
                    break
            if m ==1:
                continue
                    
            pt = []
            
            pt2 = []
            p = (t[0], t[1])
            pt.append(p)
            pt2.append(self.data2[self.data1.index(p)])
            p=(t[2], t[3])
            pt.append((t[2], t[3]))
            pt2.append(self.data2[self.data1.index(p)])
            p = (t[4], t[5])
            pt.append((t[4], t[5]))
            pt2.append(self.data2[self.data1.index(p)])
            
            
            pt2.append(self.data2)
            
            minx = int(min(pt2[0][0],pt2[1][0],pt2[2][0]))
            miny = int(min(pt2[0][1],pt2[1][1],pt2[2][1]))
            maxx = int(max(pt2[0][0],pt2[1][0],pt2[2][0]))
            maxy = int(max(pt2[0][1],pt2[1][1],pt2[2][1]))
            
            diffx = int(maxx - minx) 
            diffy = int(maxy - miny)    #farkları tutuyor 
            rect =  []
        
            arrayInput = [[t[0],  t[1], 1, 0, 0, 0] ,
                      [t[2],  t[3], 1, 0, 0, 0],
                      [t[4],  t[5], 1, 0, 0, 0],
                      [0, 0, 0, t[0], t[1], 1 ],
                      [0, 0, 0, t[2], t[3], 1 ],
                      [0, 0, 0, t[4], t[5], 1 ] ]
            arrayTarget = [[pt2[0][0]],
                           [pt2[1][0]],
                           [pt2[2][0]],
                           [pt2[0][1]],
                           [pt2[1][1]],
                           [pt2[2][1]]]
            
            coeff = np.matmul(np.linalg.inv(arrayInput),arrayTarget )
            coeffFinal = [ [coeff[0][0],coeff[1][0],coeff[2][0]],
                          [coeff[3][0],coeff[4][0],coeff[5][0]],
                          [0,0,1]]
            
            for i in range(0, 3):
                rect.append(((pt2[i][0] - minx),(pt2[i][1] - miny)))
                
            
            mask = np.zeros((int(diffy), int(diffx)))
            srcTri= []
            srcTri.append((t[0], t[1]))
            srcTri.append((t[2], t[3]))
            srcTri.append((t[4], t[5]))
            
            destTri = []
            destTri.append((pt2[0][0],pt2[0][1]))
            destTri.append((pt2[1][0],pt2[1][1]))
            destTri.append((pt2[2][0],pt2[2][1]))
        
            cv2.fillConvexPoly(mask, np.int32(rect), 1, 16, 0);
            
          
          

            
            for j in range(diffy):
                for i in range(diffx):
                    if mask[j][i] == 0:
                        continue
                    newMatris = [ [i+minx],
                                 [j+miny],
                                 [1]]
                    
                    
                    ResultMatris = np.matmul(np.linalg.inv(coeffFinal), newMatris)
                    x = int(ResultMatris[0][0])
                    y = int(ResultMatris[1][0])
                    x = min(max(0, x), resultImage.shape[1] - 1)
                    y = min(max(0, y), resultImage.shape[0] - 1)
                    resultImage[j+miny][i+minx] = self.InputImage[y][x]
                    
                    
                    
        row,column,channel= self.InputImage.shape  #shapeler aynı
        bytesPerLine = 3 * column
        
        resultImage = resultImage.astype('uint8')
        self.resultPixmap = QImage(resultImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.resultLabel.setPixmap(QPixmap.fromImage(self.resultPixmap))
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultGridBox.layout().addWidget(self.resultLabel)
        
            

        
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    def rect_contains(rect, point) :
        if point[0] < rect[0] :
            return False
        elif point[1] < rect[1] :
            return False
        elif point[0] > rect[2] :
            return False
        elif point[1] > rect[3] :
            return False
        return True

 
    def draw_point(img, p, color ) :
        cv2.circle( img, p, 2, color, cv2.FILLED, cv2.LINE_AA, 0 )
    
    
 
    def draw_delaunay(img, subdiv, delaunay_color ) :
    
        triangleList = subdiv.getTriangleList();
        size = img.shape
        r = (0, 0, size[1], size[0])
    
        for t in triangleList :
    
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])
    
            if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3) :
    
                cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
        
    
    ex = App()
    sys.exit(app.exec_())
