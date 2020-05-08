'''
@lanhuage: python
@Descripttion: 
@version: beta
@Author: xiaoshuyui
@Date: 2020-05-08 08:51:22
@LastEditors: xiaoshuyui
@LastEditTime: 2020-05-08 10:15:28
'''
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from shape import Shape

class Winform(QWidget):
    CREATE, EDIT = range(2)
    def __init__(self,parent=None):
        super(Winform,self).__init__(parent)
        self.setWindowTitle("绘图例子") 
        self.pix =  QPixmap()  # 实例化一个 QPixmap 对象
        self.initUi()
        self.lastPoint =  QPoint() # 起始点
        self.endPoint =  QPoint() #终点

        self.shortCut = QShortcut(QKeySequence("Ctrl+Z"),self)
        self.shortCut.activated.connect(self._test)
        

        self.current_brush_path = None
        self.mask_Image = None
        self.brush_point = None
        self.brush_color =QColor(0,0,0,255)
        self.brush_size = 10
        self.brush = QPainter()
        self.mask_pixmap = self.pix
        self.font_size = 50
        self.mode = self.EDIT
        self.shapes = []
        self.current = None
        self._hideBackround = False
        self.hideBackround = False



        self.undoAction = QAction()
        self.undoStack = QUndoStack()
        self.undoAction = self.undoStack.createUndoAction(self,'Undo')
        self.undoAction.setShortcut(QKeySequence.Undo)
        


        
    
    def _test(self):
        print("aaaa")
	
    def initUi(self):
            #窗口大小设置为600*500
        self.resize(600, 500)  
            # 画布大小为400*400，背景为白色
        self.pix = QPixmap(400, 400)
        
        self.pix.fill(Qt.white)

 
    # 重绘的复写函数 主要在这里绘制
    def paintEvent(self, event):
       
        p = QPainter()
        p.begin(self)
        p.setFont(QFont('Times', self.font_size, QFont.Bold))
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        p.drawPixmap(0,0,self.pix)
        p.setOpacity(0.3)
        if self.brush_point:
            p.drawEllipse(self.brush_point,self.brush_size/2,self.brush_size/2)
        if self.current_brush_path:
            # print("================")
            if self.mask_pixmap.isNull():
                self.mask_pixmap = QImage(self.pix.size(),QImage.Format_ARGB32)
                self.mask_pixmap.fill(QColor(255,255,255,0))
                
            self.brush.begin(self.mask_pixmap)


            brush_pen = QPen() # 定义笔格式对象
            self.brush.setCompositionMode(QPainter.CompositionMode_Source)

            brush_pen.setColor(self.brush_color)
            brush_pen.setWidth(self.brush_size)
            brush_pen.setCapStyle(Qt.RoundCap)
            brush_pen.setJoinStyle(Qt.RoundJoin)

            self.brush.setPen(brush_pen)
            self.brush.drawPath(self.current_brush_path)

            self.brush.end()
        p.end()

    def drawing(self):
        return self.mode == self.CREATE


    def finalise(self):
        assert self.current
        self.current.close()
        self.shapes.append(self.current)
        self.current = None
        self.setHiding(False)
        self.newShape.emit()
        self.update()


    def setHiding(self, enable=True):
        self._hideBackround = self.hideBackround if enable else False

   #鼠标按压事件
    def mousePressEvent(self, ev) :
    # 鼠标左键按下  
        pos = ev.pos()
        if ev.button() == Qt.LeftButton:
            if self.drawing():
                if self.shape_type == self.POLYGON_SHAPE and self.current:
                    self.current.addPoint(self.line[1])
                    self.line[0] = self.current[-1]
                    if self.current.isClosed():
                        self.finalise()
                elif self.shape_type == self.RECT_SHAPE and self.current and self.current.reachMaxPoints() is False:
                    initPos = self.current[0]
                    minX = initPos.x()
                    minY = initPos.y()
                    targetPos = self.line[1]
                    maxX = targetPos.x()
                    maxY = targetPos.y()
                    self.current.addPoint(QPointF(minX, maxY))
                    self.current.addPoint(targetPos)
                    self.current.addPoint(QPointF(maxX, minY))
                    self.current.addPoint(initPos)
                    self.line[0] = self.current[-1]
                    if self.current.isClosed():
                        self.finalise()
                elif not self.outOfPixmap(pos):
                    self.current = Shape(shape_type=self.shape_type)
                    self.current.addPoint(pos)
                    self.line.points = [pos, pos]
                    self.setHiding()
                    self.drawingPolygon.emit(True)
                    self.update()
            else:
                # self.selectShapePoint(pos)
                self.prevPoint = pos
                self.repaint()
        elif ev.button() == Qt.RightButton and self.editing():
            # self.selectShapePoint(pos)
            self.prevPoint = pos
            self.repaint()
            

	# 鼠标移动事件
    def mouseMoveEvent(self, ev):
        pos = ev.pos()
        self.brush_point = pos
        if Qt.LeftButton & ev.buttons():
            if not self.current_brush_path:
                self.current_brush_path = QPainterPath()
                self.current_brush_path.moveTo(pos)
            self.repaint()
            return
    # 鼠标左键按下的同时移动鼠标
        # if event.buttons() and Qt.LeftButton :
        #     self.endPoint = event.pos()
        #     #进行重新绘制
        #     self.update()

    # 鼠标释放事件
    def mouseReleaseEvent( self, event):
        print(self.current_brush_path is None)
        self.mask_pixmap.save("./test.jpg","jpg".upper(),100)
        self.current_brush_path = None
        # 鼠标左键释放   
        # if event.button() == Qt.LeftButton :
        #     self.endPoint = event.pos()
        #     #进行重新绘制
        #     self.update()


class PaintCommand(QUndoCommand):
    def __init__(self, line, oldMove):
        super().__init__()

			
if __name__ == "__main__":  
    app = QApplication(sys.argv) 
    form = Winform()
    form.show()
    sys.exit(app.exec_())