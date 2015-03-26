import sys
import math
import numpy as np

from Model.CommonFunction import *
from Model.Constant import *
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
            "PyOpenGL must be installed to run this widget.")
    sys.exit(1)


class RobotHandWidget(QGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(RobotHandWidget, self).__init__(parent)

        self.xRot = 0   # initial angle of view
        self.yRot = 0   # initial angle of view
        self.zRot = 0   # initial angle of view

        self.speed = INITSPEED
        self.gear1angle = INISERVOANGLE1 * math.pi / 180.0     # red body left
        self.gear2angle = INISERVOANGLE2 * math.pi / 180.0     # green body right
        self.gear3angle = INISERVOANGLE4 * math.pi / 180.0     # plier
        self.gear4angle = INISERVOANGLE3 * math.pi / 180.0     # head base

        self.gear1angle2 = self.gear1angle
        self.gear2angle2 = self.gear2angle
        self.gear3angle2 = self.gear3angle
        self.gear4angle2 = self.gear4angle


        self.gear1Rot = 0.0 # tier
        self.tire1angle = (INITDIR - 1) * math.pi / 4.0

        self.isUpdate = False


        # Update graph per 20ms
        timer = QTimer(self)
        timer.timeout.connect(self.advanceGears)
        timer.timeout.connect(self.updateArmPosition)
        timer.timeout.connect(self.updateGL)
        # timer.start(1000/FPS)
        timer.start(20)

        # Update target position per 100ms
        timer2 = QTimer(self)
        timer2.timeout.connect(self.getCarInfo)
        timer2.start(100)

        self.smoothUpdate =  SMOOTH_UPDATE_MODEL
        self.ArmMoveSpeed = ARM_MOVE_RATE # This only works if Smooth update model is true

    # def setCarEntity(self, carEntity):
    #     self.carEntity = carEntity

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

    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        reflectance1 = (1.0, 0.0, 0.0, 1.0) # red
        reflectance2 = (0.0, 1.0, 0.0, 1.0) # green
        reflectance3 = (0.0, 0.0, 1.0, 1.0) # blue
        reflectance4 = (1.0, 1.0, 0.0, 1.0) # yellow
        reflectance5 = (1.0, 0.0, 1.0, 1.0) # purple

        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        self.box1 = self.box(reflectance1, ARM_HORIZONTAL_W, 1.0, 0.1)    # red 1
        self.box2 = self.box(reflectance2, ARM_VERTICAL_L, 1.0, 0.1)    # green 1
        self.box3 = self.box(reflectance1, ARM_HORIZONTAL_W+ARM_HORIZONTAL_K, 1.0, 0.1)    # red 2 connects plier
        self.box4 = self.box(reflectance2, ARM_HORIZONTAL_K, 1.0, 0.1)    # green 2
        self.box5 = self.box(reflectance3, BASE_CONNECTION_B, 1.0, 1.0)    # bottom blue
        self.box6 = self.box(reflectance3, HAND_LENGTH_H, 1.0, 0.1)    # hand blue
        self.box7 = self.box(reflectance4, GRABBER_LENGTH_P, 1.0, 0.1)    # hand yellow 1
        self.box8 = self.box(reflectance4, GRABBER_LENGTH_P, 1.0, 0.1)    # hand yellow 2
        self.box9 = self.box(reflectance5, GRABBER_LENGTH_P, 0.2, 1.0)    # hand purple 1
        self.box10 = self.box(reflectance5, GRABBER_LENGTH_P, 0.2, 1.0)    # hand purple 2

        self.cylinder1 = self.cylinder(reflectance1, 0.5, 1.0)
        self.cylinder2 = self.cylinder(reflectance2, 0.5, 1.0)
        self.cylinder3 = self.cylinder(reflectance2, 0.5, 1.0)
        self.cylinder4 = self.cylinder(reflectance1, 0.5, 1.0)
        self.cylinder5 = self.cylinder(reflectance1, 0.5, 1.0)
        self.cylinder6 = self.cylinder(reflectance2, 0.5, 1.0)
        self.cylinder7 = self.cylinder(reflectance2, 0.5, 1.0)
        self.cylinder8 = self.cylinder(reflectance1, 0.5, 1.0)
        self.cylinder9 = self.cylinder(reflectance3, 0.5, 1.0)
        self.cylinder10 = self.cylinder(reflectance3, 0.5, 1.0)

        self.tire1 = self.tire(reflectance2, 2.0, 2.0, 1.0, 20)
        self.tire2 = self.tire(reflectance2, 2.0, 2.0, 1.0, 20)
        self.tire3 = self.tire(reflectance4, 2.0, 2.0, 1.0, 20)
        self.tire4 = self.tire(reflectance4, 2.0, 2.0, 1.0, 20)

        self.cylinder11 = self.cylinder(reflectance3, 0.5, 1.0)
        self.cylinder12 = self.cylinder(reflectance5, 0.5, 1.0)
        self.cylinder13 = self.cylinder(reflectance5, 0.5, 1.0)

        self.box11 = self.box(reflectance1, 16.0, 3.0, 6.0)    # carbody

        glEnable(GL_NORMALIZE)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotated(self.xRot, 1.0, 0.0, 0.0)
        glRotated(self.yRot, 0.0, 1.0, 0.0)
        glRotated(self.zRot, 0.0, 0.0, 1.0)

        self.x0 = 0.0
        self.y0 = 0.0
        self.z0 = 0.0

        self.x1 = ARM_HORIZONTAL_W * math.cos(self.gear1angle)
        self.y1 = ARM_HORIZONTAL_W * math.sin(self.gear1angle)
        self.z1 = 1.0       #horizontal movement

        self.x2 = -ARM_VERTICAL_L * math.sin(self.gear2angle)
        self.y2 = ARM_VERTICAL_L * math.cos(self.gear2angle)

        self.x3 = -ARM_VERTICAL_L * math.sin(self.gear2angle) - ARM_HORIZONTAL_K * math.cos(self.gear1angle)
        self.y3 = ARM_VERTICAL_L * math.cos(self.gear2angle) - ARM_HORIZONTAL_K * math.sin(self.gear1angle)

        self.drawBox(self.box1, self.x0, self.y0, self.z0, 180 / math.pi * self.gear1angle, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawBox(self.box2, self.x1, self.y1, self.z1, 180 / math.pi * (math.pi / 2.0 + self.gear2angle), 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawBox(self.box3, self.x1 + self.x2, self.y1 + self.y2, self.z0, 180.0 + 180.0 / math.pi * self.gear1angle, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawBox(self.box4, self.x0, self.y0, self.z1,  180 / math.pi * (math.pi / 2.0 + self.gear2angle), 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawBox(self.box5, self.x0, self.y0, self.z0, -90.0, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawBox(self.box6, self.x3, self.y3, self.z0, 180.0, 180.0 / math.pi * self.gear4angle, 0.0)

        self.drawCylinder(self.cylinder1, self.x0, self.y0, self.z0, 0.0, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawCylinder(self.cylinder2, self.x0, self.y0, self.z1, 0.0, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawCylinder(self.cylinder3, self.x1, self.y1, self.z1, 180 / math.pi * (math.pi / 2.0 + self.gear2angle), 180.0 / math.pi * self.gear4angle, 0.0) # 0.0)
        self.drawCylinder(self.cylinder4, self.x1, self.y1, self.z0, 180 / math.pi * (math.pi / 2.0 + self.gear2angle), 180.0 / math.pi * self.gear4angle, 0.0) # 0.0)
        self.drawCylinder(self.cylinder5, self.x1 + self.x2, self.y1 + self.y2, self.z0, 180.0 + 180.0 / math.pi * self.gear1angle, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawCylinder(self.cylinder6, self.x1 + self.x2, self.y1 + self.y2, self.z1, 180.0 + 180.0 / math.pi * self.gear1angle, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawCylinder(self.cylinder7, self.x2, self.y2, self.z1, 180.0 + 180.0 / math.pi * self.gear1angle, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawCylinder(self.cylinder8, self.x2, self.y2, self.z0, 180.0 + 180.0 / math.pi * self.gear1angle, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawCylinder(self.cylinder9, self.x0, -BASE_CONNECTION_B, self.z0, 0.0, 180.0 / math.pi * self.gear4angle, 0.0)

        self.drawBox(self.box7, self.x3 - GRABBER_LENGTH_P, self.y3, self.z0, 180.0, 180.0 / math.pi * self.gear4angle, 180.0 / math.pi * self.gear3angle)
        self.drawBox(self.box8, self.x3 - GRABBER_LENGTH_P, self.y3, self.z0, 180.0, 180.0 / math.pi * self.gear4angle, -180.0 / math.pi * self.gear3angle)

        self.drawCylinder(self.cylinder10, self.x3, self.y3, self.z0, 0.0, 180.0 / math.pi * self.gear4angle, 0.0)

        self.drawBox(self.box9, self.x3 - GRABBER_LENGTH_P - GRABBER_LENGTH_P * math.cos(self.gear3angle), self.y3, -GRABBER_LENGTH_P * math.sin(self.gear3angle), 180.0, 180.0 / math.pi * self.gear4angle, 0.0)
        self.drawBox(self.box10, self.x3 - GRABBER_LENGTH_P - GRABBER_LENGTH_P * math.cos(self.gear3angle), self.y3, GRABBER_LENGTH_P * math.sin(self.gear3angle), 180.0, 180.0 / math.pi * self.gear4angle, 0.0)

        self.drawCylinder(self.cylinder11, self.x3 - GRABBER_LENGTH_P, self.y3, self.z0, 0.0, 180.0 / math.pi * self.gear4angle, 90.0)
        self.drawCylinder(self.cylinder12, self.x3 - GRABBER_LENGTH_P - GRABBER_LENGTH_P * math.cos(self.gear3angle), self.y3, -GRABBER_LENGTH_P * math.sin(self.gear3angle), 0.0, 180.0 / math.pi * self.gear4angle, 90.0)
        self.drawCylinder(self.cylinder13, self.x3 - GRABBER_LENGTH_P - GRABBER_LENGTH_P * math.cos(self.gear3angle), self.y3, GRABBER_LENGTH_P * math.sin(self.gear3angle), 0.0, 180.0 / math.pi * self.gear4angle, 90.0)

        self.drawBox(self.box11, -6.0, -6.0, 0.0, 0.0, 0.0, 0.0)

        self.drawTire(self.tire1, -4.0, -8.0, 3.5, self.gear1Rot, self.tire1angle / math.pi * 180.0)
        self.drawTire(self.tire2, -4.0, -8.0, -3.5, self.gear1Rot, self.tire1angle / math.pi * 180.0)
        self.drawTire(self.tire3, 8.0, -8.0, 3.5, self.gear1Rot, 0.0)
        self.drawTire(self.tire4, 8.0, -8.0, -3.5, self.gear1Rot, 0.0)

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
            self.setXRotation(self.xRot + 8.0 * dy)
            self.setYRotation(self.yRot + 8.0 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8.0 * dy)
            self.setZRotation(self.zRot + 8.0 * dx)

        self.lastPos = event.pos()

    def advanceGears(self):
        self.gear1Rot += self.speed * 0.06

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def box(self, reflectance, length, width, height):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, reflectance)

        glBegin(GL_QUADS)

        r = width / 2.0
        h = height / 2.0

        glVertex3d(0.0, r, -h)
        glVertex3d(0.0, -r, -h)
        glVertex3d(length, -r, -h)
        glVertex3d(length, r, -h)

        glVertex3d(length, r , h)
        glVertex3d(length, -r , h)
        glVertex3d(0.0, -r , h)
        glVertex3d(0.0, r , h)


        glVertex3d(0.0, r, h)
        glVertex3d(0.0, -r, h)
        glVertex3d(0.0, -r, -h)
        glVertex3d(0.0, r, -h)

        glVertex3d(0.0, -r, h)
        glVertex3d(length, -r, h)
        glVertex3d(length, -r, -h)
        glVertex3d(0.0, -r, -h)

        glVertex3d(length, -r, h)
        glVertex3d(length, r, h)
        glVertex3d(length, r, -h)
        glVertex3d(length, -r, -h)

        glVertex3d(length, r, h)
        glVertex3d(0.0, r, h)
        glVertex3d(0.0, r, -h)
        glVertex3d(length, r, -h)

        glEnd()

        glEndList()

        return list

    def cylinder(self, reflectance, radius, thickness):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, reflectance)

        r1 = radius
        density = 50
        delta = (2.0 * math.pi / density) / 4.0
        z = thickness / 2.0

        glShadeModel(GL_FLAT)

        for i in range(2):
            if i == 0:
                sign = +1.0
            else:
                sign = -1.0

            glNormal3d(0.0, 0.0, sign)

            glBegin(GL_QUAD_STRIP)

            for j in range(density):
                angle = 2.0 * math.pi * j / density
                glVertex3d(0.0, 0.0, sign * z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(0.0, 0.0, sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

        glBegin(GL_QUAD_STRIP)

        for i in range(density):

                angle = 2.0 * math.pi * i / 50

                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), +z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), -z)
                glVertex3d(r1 * math.sin(angle), r1 * math.cos(angle), -z)
                glVertex3d(r1 * math.sin(angle), r1 * math.cos(angle), +z)

        glVertex3d(r1, 0.0, +z)
        glVertex3d(r1, 0.0, -z)
        glEnd()

        glShadeModel(GL_SMOOTH)

        glBegin(GL_QUAD_STRIP)

        for i in range(density + 1):
            angle = i * 2.0 * math.pi / 50
            glNormal3d(-math.cos(angle), -math.sin(angle), 0.0)
            glVertex3d(0.0, 0.0, +z)
            glVertex3d(0.0, 0.0, -z)

        glEnd()

        glEndList()

        return list

    def tire(self, reflectance, radius, thickness, toothSize, toothCount):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, reflectance)

        r1 = radius - toothSize / 2.0
        r2 = radius + toothSize / 2.0
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
                glVertex3d(0.0, 0.0, sign * z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(0.0, 0.0, sign * z)
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
            glVertex3d(0.0, 0.0, +z)
            glVertex3d(0.0, 0.0, -z)

        glEnd()

        glEndList()

        return list

    def drawBox(self, box, dx, dy, dz, angle, turnAngle, piterAngle):
        glPushMatrix()
        glRotated(turnAngle, 0.0, 1.0, 0.0)
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 0.0, 1.0)
        glRotated(piterAngle, 0.0, 1.0, 0.0)
        glCallList(box)
        glPopMatrix()

    def drawCylinder(self, cylinder, dx, dy, dz, angle, turnAngle, piterAngle):
        glPushMatrix()
        glRotated(turnAngle, 0.0, 1.0, 0.0)
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 0.0, 1.0)
        glRotated(piterAngle, 1.0, 0.0, 0.0)
        glCallList(cylinder)
        glPopMatrix()

    def drawTire(self, gear, dx, dy, dz, angle, turnAngle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(turnAngle, 0.0, 1.0, 0.0)
        glRotated(angle, 0.0, 0.0, 1.0)
        glCallList(gear)
        glPopMatrix()

    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360

        while (angle > 360):
            angle -= 360


    def setUpdateFlag(self, dataList):
        self.isUpdate = True
        self.dataList = dataList



    def getCarInfo(self):

        # Update Information fro CarEntity
        if self.isUpdate:
            self.isUpdate = False

            self.speed = self.dataList[0]

            dirc = self.dataList[1]
            if dirc == 0:
                self.tire1angle = 30.0 * math.pi / 180.0
                # dirstr = 'left'
            elif dirc == 1:
                self.tire1angle = 0.0
                # dirstr = 'straight'
            elif dirc == 2:
                self.tire1angle = -30.0 * math.pi / 180.0
                # dirstr = 'right'

            self.gear1angle2 = self.dataList[2] * math.pi / 180.0  # left
            self.gear2angle2 = self.dataList[3] * math.pi / 180.0  # right
            self.gear3angle2 = self.dataList[5] * math.pi / 180.0  # clipper
            self.gear4angle2 = self.dataList[4] * math.pi / 180.0  # base

            self.gear1angle2 = setValueWithinLimit(self.gear1angle2, 45.0 * math.pi / 180.0 , -45.0 * math.pi / 180.0)
            self.gear2angle2 = setValueWithinLimit(self.gear2angle2, 45.0 * math.pi / 180.0 , -45.0 * math.pi / 180.0)
            #self.gear4angle2 = setValueWithinLimit(self.gear4angle2, 90.0 * math.pi / 180.0 , -90.0 * math.pi / 180.0)

    def updateArmPosition(self):

        if self.smoothUpdate == True:
            self.gear1angle = approach(self.gear1angle, self.gear1angle2, self.ArmMoveSpeed)
            self.gear2angle = approach(self.gear2angle, self.gear2angle2, self.ArmMoveSpeed)
            self.gear3angle = approach(self.gear3angle, self.gear3angle2, self.ArmMoveSpeed)
            self.gear4angle = approach(self.gear4angle, self.gear4angle2, self.ArmMoveSpeed)

        else :
            self.gear1angle = self.gear1angle2
            self.gear2angle = self.gear2angle2
            self.gear3angle = self.gear3angle2
            self.gear4angle = self.gear4angle2


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainWin = RobotHandWidget()
    mainWin.show()
    sys.exit(app.exec_())
