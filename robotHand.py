import sys
import math

from Model.Constent import *
from PyQt5.QtCore import pyqtSignal, QRegExp, QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QGridLayout, QInputDialog,
        QLabel, QLineEdit, QMainWindow, QMessageBox, QScrollArea, QSizePolicy,
        QSlider, QWidget)
from PyQt5.QtOpenGL import QGLWidget

try:
    from OpenGL.GL import *
except ImportError:
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "OpenGL grabber",
            "PyOpenGL must be installed to run this example.")
    sys.exit(1)


class GLWidget(QGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.box1 = 0
        self.cylinder1 = 0
        self.gear1 = 0
        self.gear2 = 0
        self.gear3 = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.gear1Rot = 0 # tier
        self.plierClosing = -1
        self.handHorizontal = 0
        self.handVertical = 0
        self.forward = 1
        self.speed = INITSPEED
        self.gear1angle = 15.0 * math.pi / 180.0     # red body
        self.gear2angle = -30.0 * math.pi / 180.0     # green body
        self.gear3angle = 60.0 * math.pi / 180.0     # plier

        self.gear1Rot = 0.0
        self.turn = 1
        self.tier1angle = math.pi / 4.0

        timer = QTimer(self)
        timer.timeout.connect(self.advanceGears)
        timer.start(20)

    def setXRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()

    def setYRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    def setHorizontalChange(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16

        self.gear1angletemp = angle
        self.horizontalChanged.emit(angle)

    def setVerticalChange(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16

        self.gear2angletemp = angle
        self.verticalChanged.emit(angle)

    def setPiterChange(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16

        self.gear3angletemp = angle
        self.piterChanged.emit(angle)

    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        reflectance1 = (1.0, 0.0, 0.0, 1.0)
        reflectance2 = (0.0, 1.0, 0.0, 1.0)
        reflectance3 = (0.0, 0.0, 1.0, 1.0)
        reflectance4 = (1.0, 1.0, 0.0, 1.0)
        reflectance5 = (1.0, 0.0, 1.0, 1.0)

        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        self.box1 = self.box(reflectance1, 0.0, 0.0, 3.0, 1.0, 0.1, 0.0)    # red 1
        self.box2 = self.box(reflectance2, 0.0, 0.0, 7.0, 1.0, 0.1, 0.0)    # green 1
        self.box3 = self.box(reflectance1, 0.0, 0.0, 9.0, 1.0, 0.1, 0.0)    # red 2 connects plier
        self.box4 = self.box(reflectance2, 0.0, 0.0, 7.0, 1.0, 0.1, 0.0)    # green 2
        self.box5 = self.box(reflectance3, 0.0, 0.0, 4.0, 1.0, 0.5, 0.0)    # bottom blue
        self.box6 = self.box(reflectance3, 0.0, 0.0, 2.0, 1.0, 0.1, 0.0)    # hand blue
        self.box7 = self.box(reflectance4, 0.0, 0.0, 2.0, 1.0, 0.1, 0.0)    # hand yellow 1
        self.box8 = self.box(reflectance4, 0.0, 0.0, 2.0, 1.0, 0.1, 0.0)    # hand yellow 2
        self.box9 = self.box(reflectance5, 0.0, 0.0, 2.0, 1.0, 0.1, 0.0)    # hand yellow 2
        self.box10 = self.box(reflectance5, 0.0, 0.0, 2.0, 1.0, 0.1, 0.0)    # hand yellow 2


        self.cylinder1 = self.cylinder(reflectance1, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder2 = self.cylinder(reflectance2, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder3 = self.cylinder(reflectance2, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder4 = self.cylinder(reflectance1, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder5 = self.cylinder(reflectance1, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder6 = self.cylinder(reflectance2, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder7 = self.cylinder(reflectance2, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder8 = self.cylinder(reflectance1, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder9 = self.cylinder(reflectance3, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder10 = self.cylinder(reflectance1, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder11 = self.cylinder(reflectance3, 0.0, 0.5, 1.0, 0.0, 10000)

        self.tier1 = self.tier(reflectance2, 0.0, 2.0, 2.0, 1.0, 20)
        self.tier2 = self.tier(reflectance2, 0.0, 2.0, 2.0, 1.0, 20)
        self.tier3 = self.tier(reflectance4, 0.0, 2.0, 2.0, 1.0, 20)
        self.tier4 = self.tier(reflectance4, 0.0, 2.0, 2.0, 1.0, 20)

        self.cylinder12 = self.cylinder(reflectance3, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder13 = self.cylinder(reflectance5, 0.0, 0.5, 1.0, 0.0, 10000)
        self.cylinder14 = self.cylinder(reflectance5, 0.0, 0.5, 1.0, 0.0, 10000)

        self.box11 = self.box(reflectance1, -6.0, -6.0, 16.0, 3.0, 3.0, 0.0)    # car 1

        glEnable(GL_NORMALIZE)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        self.drawBox(self.box1, 0.0, 0.0, 0.0, 180 / math.pi * self.gear1angle)
        self.drawBox(self.box2, 3.0 * math.cos(self.gear1angle), 3.0 * math.sin(self.gear1angle), 1.0,180 / math.pi * (math.pi / 2.0 + self.gear2angle))
        self.drawBox(self.box3, 3.0 * math.cos(self.gear1angle) - 7.0 * math.sin(self.gear2angle), 3.0 * math.sin(self.gear1angle) + 7.0 * math.cos(self.gear2angle), 0.0, 180 / math.pi * (math.pi + self.gear1angle))
        self.drawBox(self.box4, -7.0 * math.sin(self.gear2angle), 7.0 * math.cos(self.gear2angle), 1.0, 180 / math.pi *(math.pi / -2.0 + self.gear2angle))
        self.drawBox(self.box5, 0.0, 0.0, -1.0, -90.0)
        self.drawBox(self.box6, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)), 21.0 * math.cos(self.gear2angle) - (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)) , -1.0, 180.0)

        self.drawCylinder(self.cylinder1, 0.0, 0.0, 0.0, 0.0)
        self.drawCylinder(self.cylinder2, 0.0, 0.0, 1.0, 0.0)
        self.drawCylinder(self.cylinder3, 3.0 * math.cos(self.gear1angle), 3.0 * math.sin(self.gear1angle), 1.0, 0.0)
        self.drawCylinder(self.cylinder4, 3.0 * math.cos(self.gear1angle), 3.0 * math.sin(self.gear1angle), 0.0, 0.0)
        self.drawCylinder(self.cylinder5, 3.0 * math.cos(self.gear1angle) - 7.0 * math.sin(self.gear2angle), 3.0 * math.sin(self.gear1angle) + 7.0 * math.cos(self.gear2angle), 0.0, 0.0)
        self.drawCylinder(self.cylinder6, 3.0 * math.cos(self.gear1angle) - 7.0 * math.sin(self.gear2angle), 3.0 * math.sin(self.gear1angle) + 7.0 * math.cos(self.gear2angle), 1.0, 0.0)
        self.drawCylinder(self.cylinder7, -7.0 * math.sin(self.gear2angle), 7.0 * math.cos(self.gear2angle), 1.0, 0.0)
        self.drawCylinder(self.cylinder8, -7.0 * math.sin(self.gear2angle), 7.0 * math.cos(self.gear2angle), 0.0, 0.0)
        self.drawCylinder(self.cylinder9, 0.0, 0.0, -1.0, 0.0)
        self.drawCylinder(self.cylinder10, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)), 21.0 * math.cos(self.gear2angle) - (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 0.0, 0.0)
        self.drawCylinder(self.cylinder11, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)), 21.0 * math.cos(self.gear2angle) - (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), -1.0, 0.0)

        self.drawBox(self.box11, 0.0, 0.0, 0.0, 0.0)

        self.drawTier(self.tier1, -4.0, -8.0, 3.5, self.gear1Rot / 16.0, self.tier1angle / math.pi * 180.0)
        self.drawTier(self.tier2, -4.0, -8.0, -3.5, self.gear1Rot / 16.0, self.tier1angle / math.pi * 180.0)
        self.drawTier(self.tier3, 8.0, -8.0, 3.5, self.gear1Rot / 16.0, 0.0)
        self.drawTier(self.tier4, 8.0, -8.0, -3.5, self.gear1Rot / 16.0, 0.0)

        glRotated(+90.0, 1.0, 0.0, 0.0)
        # x = x, y = z, z = -y
        self.drawCylinder(self.cylinder12, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0, -1.0, -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 0.0)
        self.drawBox(self.box7, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0, -1.0, -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 180.0 - self.gear3angle / math.pi * 180.0)
        self.drawBox(self.box8, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0, -1.0, -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 180.0 + self.gear3angle / math.pi * 180.0)
        self.drawCylinder(self.cylinder13, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0 - 2.0 * math.cos(self.gear3angle), -1.0 - 2.0 * math.sin(self.gear3angle), -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 0.0)
        self.drawCylinder(self.cylinder14, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0 - 2.0 * math.cos(self.gear3angle), -1.0 + 2.0 * math.sin(self.gear3angle), -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 0.0)
        self.drawBox(self.box9, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0 - 2.0 * math.cos(self.gear3angle), -1.0 - 2.0 * math.sin(self.gear3angle), -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 180.0)
        self.drawBox(self.box10, -21.0 * math.sin(self.gear2angle) - (6.0 * math.cos(self.gear1angle) - 14.0 * math.sin(self.gear2angle)) - 2.0 - 2.0 * math.cos(self.gear3angle), -1.0 + 2.0 * math.sin(self.gear3angle), -21.0 * math.cos(self.gear2angle) + (6.0 * math.sin(self.gear1angle) + 14.0 * math.cos(self.gear2angle)), 180.0)


        glPopMatrix()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) // 2, (height - side) // 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-2.0, +2.0, -2.0, 2.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def advanceGears(self):

        self.gear1Rot += self.speed * 2 * 16

        if self.gear1angle > 150.0 * math.pi / 180.0:
            self.handHorizontal = 0
        elif self.gear1angle < 15.0 * math.pi / 180.0:
            self.handHorizontal = 0

        if self.handHorizontal == 1 and self.gear1angle - self.gear2angle < 89.0 * math.pi / 180.0:
            self.gear1angle += math.pi / 180.0

        if self.handHorizontal == -1:
            self.gear1angle -= math.pi / 180.0


        if self.gear2angle > 90.0 * math.pi / 180.0:
            self.handVertical = 0
        elif self.gear2angle < -30.0 * math.pi / 180.0:
            self.handVertical = 0

        if self.handVertical == -1 and self.gear1angle - self.gear2angle < 89.0 * math.pi / 180.0:
            self.gear2angle -= math.pi / 180.0

        if self.handVertical == 1:
            self.gear1angle += math.pi / 180.0


        if self.gear3angle > 60.0 * math.pi / 180.0:
            self.plierClosing = 0
        elif self.gear3angle < 16.0 * math.pi / 180.0:
            self.plierClosing = 0

        if self.plierClosing == 1:
            self.gear3angle += 2.0 * math.pi / 180.0
        elif self.plierClosing == -1:
            self.gear3angle -= 2.0 * math.pi / 180.0

        if self.turn == 1:
            self.tier1angle = 45.0 * math.pi / 180.0
        elif self.turn == -1:
            self.tier1angle = -45.0 * math.pi / 180.0



        self.updateGL()    

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def box(self, reflectance, x1, y1, length, width, height, angle):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, reflectance)

        glBegin(GL_QUADS)

        r = width / 2.0

        glVertex3d(x1 - r * math.sin(angle), y1 + r * math.cos(angle), -height)
        glVertex3d(x1 + r * math.sin(angle), y1 - r * math.cos(angle), -height)
        glVertex3d(x1 + length * math.cos(angle) + r * math.sin(angle), y1 + length * math.sin(angle) - r * math.cos(angle), -height)
        glVertex3d(x1 + length * math.cos(angle) - r * math.sin(angle), y1 + length * math.sin(angle) + r * math.cos(angle), -height)

        glVertex3d(x1 + length * math.cos(angle) - r * math.sin(angle), y1 + length * math.sin(angle) + r * math.cos(angle), +height)
        glVertex3d(x1 + length * math.cos(angle) + r * math.sin(angle), y1 + length * math.sin(angle) - r * math.cos(angle), +height)
        glVertex3d(x1 + r * math.sin(angle), y1 - r * math.cos(angle), +height)
        glVertex3d(x1 - r * math.sin(angle), y1 + r * math.cos(angle), +height)


        glVertex3d(x1 - r * math.sin(angle), y1 + r * math.cos(angle), +height)
        glVertex3d(x1 + r * math.sin(angle), y1 - r * math.cos(angle), +height)
        glVertex3d(x1 + r * math.sin(angle), y1 - r * math.cos(angle), -height)
        glVertex3d(x1 - r * math.sin(angle), y1 + r * math.cos(angle), -height)

        glVertex3d(x1 + r * math.sin(angle), y1 - r * math.cos(angle), +height)
        glVertex3d(x1 + length * math.cos(angle) + r * math.sin(angle), y1 + length * math.sin(angle) - r * math.cos(angle), +height)
        glVertex3d(x1 + length * math.cos(angle) + r * math.sin(angle), y1 + length * math.sin(angle) - r * math.cos(angle), -height)
        glVertex3d(x1 + r * math.sin(angle), y1 - r * math.cos(angle), -height)

        glVertex3d(x1 + length * math.cos(angle) + r * math.sin(angle), y1 + length * math.sin(angle) - r * math.cos(angle), +height)
        glVertex3d(x1 + length * math.cos(angle) - r * math.sin(angle), y1 + length * math.sin(angle) + r * math.cos(angle), +height)
        glVertex3d(x1 + length * math.cos(angle) - r * math.sin(angle), y1 + length * math.sin(angle) + r * math.cos(angle), -height)
        glVertex3d(x1 + length * math.cos(angle) + r * math.sin(angle), y1 + length * math.sin(angle) - r * math.cos(angle), -height)

        glVertex3d(x1 + length * math.cos(angle) - r * math.sin(angle), y1 + length * math.sin(angle) + r * math.cos(angle), +height)
        glVertex3d(x1 - r * math.sin(angle), y1 + r * math.cos(angle), +height)
        glVertex3d(x1 - r * math.sin(angle), y1 + r * math.cos(angle), -height)
        glVertex3d(x1 + length * math.cos(angle) - r * math.sin(angle), y1 + length * math.sin(angle) + r * math.cos(angle), -height)

        glEnd()

        glEndList()

        return list

    def cylinder(self, reflectance, innerRadius, outerRadius, thickness, toothSize, toothCount):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, reflectance)

        r0 = 0
        r1 = outerRadius

        delta = (2.0 * math.pi / toothCount) / 4.0
        z = thickness / 2.0

        glShadeModel(GL_FLAT)

        for i in range(2):
            if i == 0:
                sign = +1.0
            else:
                sign = -1.0

            glNormal3d(0.0, 0.0, sign)

            glBegin(GL_QUAD_STRIP)

            for j in range(toothCount):
                angle = 2.0 * math.pi * j / toothCount
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount):

                angle = 2.0 * math.pi * i / toothCount
                s1 = r1

                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), +z)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), -z)
                glVertex3d(s1 * math.sin(angle), s1 * math.cos(angle), -z)
                glVertex3d(s1 * math.sin(angle), s1 * math.cos(angle), +z)

        glVertex3d(r1, 0.0, +z)
        glVertex3d(r1, 0.0, -z)
        glEnd()

        glShadeModel(GL_SMOOTH)

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount+1):
            angle = i * 2.0 * math.pi / toothCount
            glNormal3d(-math.cos(angle), -math.sin(angle), 0.0)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), +z)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), -z)

        glEnd()

        glEndList()

        return list

    def tier(self, reflectance, innerRadius, outerRadius, thickness, toothSize, toothCount):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, reflectance)

        r0 = innerRadius
        r1 = outerRadius - toothSize / 2.0
        r2 = outerRadius + toothSize / 2.0
        delta = (2.0 * math.pi / toothCount) / 4.0
        z = thickness / 2.0

        glShadeModel(GL_FLAT)

        for i in range(2):
            if i == 0:
                sign = +1.0
            else:
                sign = -1.0

            glNormal3d(0.0, 0.0, sign)

            glBegin(GL_QUAD_STRIP)

            for j in range(toothCount+1):
                angle = 2.0 * math.pi * j / toothCount
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

            glBegin(GL_QUADS)

            for j in range(toothCount):
                angle = 2.0 * math.pi * j / toothCount
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r2 * math.cos(angle + delta), r2 * math.sin(angle + delta), sign * z)
                glVertex3d(r2 * math.cos(angle + 2 * delta), r2 * math.sin(angle + 2 * delta), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount):
            for j in range(2):
                angle = 2.0 * math.pi * (i + (j / 2.0)) / toothCount
                s1 = r1
                s2 = r2

                if j == 1:
                    s1, s2 = s2, s1

                glNormal3d(math.cos(angle), math.sin(angle), 0.0)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), +z)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), -z)

                glNormal3d(s2 * math.sin(angle + delta) - s1 * math.sin(angle), s1 * math.cos(angle) - s2 * math.cos(angle + delta), 0.0)
                glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), +z)
                glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), -z)

        glVertex3d(r1, 0.0, +z)
        glVertex3d(r1, 0.0, -z)
        glEnd()

        glShadeModel(GL_SMOOTH)

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount+1):
            angle = i * 2.0 * math.pi / toothCount
            glNormal3d(-math.cos(angle), -math.sin(angle), 0.0)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), +z)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), -z)

        glEnd()

        glEndList()

        return list

    def drawBox(self, box, dx, dy, dz, angle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 0.0, 1.0)
        glCallList(box)
        glPopMatrix()

    def drawCylinder(self, cylinder, dx, dy, dz, angle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 1.0, 0.0)
        glCallList(cylinder)
        glPopMatrix()

    def drawTier(self, gear, dx, dy, dz, angle, turnAngle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(turnAngle, 0.0, 1.0, 0.0)
        glRotated(angle, 0.0, 0.0, 1.0)
        glCallList(gear)
        glPopMatrix()


    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16

    def turnLeft(self):
        self.turn = 1

    def turnRight(self):
        self.turn = -1

    def turnDefault(self):
        self.turn = 0

    def moveForward(self):
        self.forward = 1

    def moveBackward(self):
        self.forward = -1

    def moveDefault(self):
        self.forward = 0

    def plierClose(self):
        self.plierClosing = 1

    def plierOpen(self):
        self.plierClosing = -1

    def plierDefault(self):
        self.plierClosing = 0

    def handForward(self):
        self.handHorizontal = 1

    def handBackward(self):
        self.handHorizontal = -1

    def handHorizontalDefault(self):
        self.handHorizontal = 0

    def handHigher(self):
        self.handVertical = 1

    def handLower(self):
        self.handVertical = -1

    def handVerticalDefault(self):
        self.handVertical = 0

    def updateGraph(self):
        self.speed = self.carEntity.getSpeed()





class MainWindow(QMainWindow):
    def __init__(self):        
        super(MainWindow, self).__init__()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.glWidget = GLWidget()
        self.pixmapLabel = QLabel()

        self.glWidgetArea = QScrollArea()
        self.glWidgetArea.setWidget(self.glWidget)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setSizePolicy(QSizePolicy.Ignored,
                QSizePolicy.Ignored)
        self.glWidgetArea.setMinimumSize(50, 50)

        self.pixmapLabelArea = QScrollArea()
        self.pixmapLabelArea.setWidget(self.pixmapLabel)
        self.pixmapLabelArea.setSizePolicy(QSizePolicy.Ignored,
                QSizePolicy.Ignored)
        self.pixmapLabelArea.setMinimumSize(50, 50)

        self.createActions()
        self.createMenus()

        centralLayout = QGridLayout()
        centralLayout.addWidget(self.glWidgetArea, 0, 0)
        centralLayout.addWidget(self.pixmapLabelArea, 0, 1)
        centralWidget.setLayout(centralLayout)

        self.setWindowTitle("Car")
        self.resize(800, 600)

    def renderIntoPixmap(self):
        size = self.getSize()

        if size.isValid():
            pixmap = self.glWidget.renderPixmap(size.width(), size.height())
            self.setPixmap(pixmap)

    def grabFrameBuffer(self):
        image = self.glWidget.grabFrameBuffer()
        self.setPixmap(QPixmap.fromImage(image))

    def clearPixmap(self):
        self.setPixmap(QPixmap())

    def about(self):
        QMessageBox.about(self, "About Grabber",
                "The <b>Grabber</b> example demonstrates two approaches for "
                "rendering OpenGL into a Qt pixmap.")

    def createActions(self):
        self.renderIntoPixmapAct = QAction("&Render into Pixmap...",
                self, shortcut="Ctrl+R", triggered=self.renderIntoPixmap)

        self.grabFrameBufferAct = QAction("&Grab Frame Buffer", self,
                shortcut="Ctrl+G", triggered=self.grabFrameBuffer)

        self.clearPixmapAct = QAction("&Clear Pixmap", self,
                shortcut="Ctrl+L", triggered=self.clearPixmap)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.renderIntoPixmapAct)
        self.fileMenu.addAction(self.grabFrameBufferAct)
        self.fileMenu.addAction(self.clearPixmapAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createSlider(self, changedSignal, setterSlot):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QSlider.TicksRight)

        slider.valueChanged.connect(setterSlot)
        changedSignal.connect(slider.setValue)

        return slider

    def setPixmap(self, pixmap):
        self.pixmapLabel.setPixmap(pixmap)
        size = pixmap.size()

        if size - QSize(1, 0) == self.pixmapLabelArea.maximumViewportSize():
            size -= QSize(1, 0)

        self.pixmapLabel.resize(size)

    def getSize(self):
        text, ok = QInputDialog.getText(self, "Grabber",
                "Enter pixmap size:", QLineEdit.Normal,
                "%d x %d" % (self.glWidget.width(), self.glWidget.height()))

        if not ok:
            return QSize()

        regExp = QRegExp("([0-9]+) *x *([0-9]+)")

        if regExp.exactMatch(text):
            width = regExp.cap(0).toInt()
            height = regExp.cap(1).toInt()
            if width > 0 and width < 2048 and height > 0 and height < 2048:
                return QSize(width, height)

        return self.glWidget.size()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())    
