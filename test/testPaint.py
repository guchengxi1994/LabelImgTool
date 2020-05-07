'''
@lanhuage: python
@Descripttion: 
@version: beta
@Author: xiaoshuyui
@Date: 2020-05-07 14:56:39
@LastEditors: xiaoshuyui
@LastEditTime: 2020-05-07 15:03:23
'''
# -*- coding: utf-8 -*-
 
"""
    【简介】
    使用paintEvent在窗口实现划线例子
    
    
"""

import sys
from PyQt5.QtWidgets import QApplication  ,QWidget 
from PyQt5.QtGui import   QPainter ,QPixmap ,QPen
from PyQt5.QtCore import Qt , QPoint

class Winform(QWidget):
    def __init__(self,parent=None):
        super(Winform,self).__init__(parent)
        self.setWindowTitle("绘图例子") 
        self.pix =  QPixmap()  # 实例化一个 QPixmap 对象
        self.lastPoint =  QPoint() # 起始点
        self.endPoint =  QPoint() #终点
        self.initUi()
	
    def initUi(self):
            #窗口大小设置为600*500
        self.resize(600, 500)  
            # 画布大小为400*400，背景为白色
        self.pix = QPixmap(400, 400)
        self.pix.fill(Qt.white)

 
    # 重绘的复写函数 主要在这里绘制
    def paintEvent(self, event):
        pp = QPainter(self.pix)

        pen = QPen() # 定义笔格式对象
        pen.setWidth(10)  # 设置笔的宽度
        pp.setPen(pen) #将笔格式赋值给 画笔

        # 根据鼠标指针前后两个位置绘制直线
        pp.drawLine(self.lastPoint, self.endPoint)
        # 让前一个坐标值等于后一个坐标值，
        # 这样就能实现画出连续的线
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pix)  # 在画布上画出


   #鼠标按压事件
    def mousePressEvent(self, event) :
    # 鼠标左键按下  
        if event.button() == Qt.LeftButton :
            self.lastPoint = event.pos()
            self.endPoint = self.lastPoint

	# 鼠标移动事件
    def mouseMoveEvent(self, event):	
    # 鼠标左键按下的同时移动鼠标
        if event.buttons() and Qt.LeftButton :
            self.endPoint = event.pos()
            #进行重新绘制
            self.update()

    # 鼠标释放事件
    def mouseReleaseEvent( self, event):
        # 鼠标左键释放   
        if event.button() == Qt.LeftButton :
            self.endPoint = event.pos()
            #进行重新绘制
            self.update()
			
if __name__ == "__main__":  
    app = QApplication(sys.argv) 
    form = Winform()
    form.show()
    sys.exit(app.exec_())

