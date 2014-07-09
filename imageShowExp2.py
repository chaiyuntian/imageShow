# -*- coding: utf-8 -*-
import sys, os, random
from PySide.QtCore import *
from PySide.QtGui import *
from xlsRead import *
from recordData import *
from time import localtime,strftime
SCENE_FILE = 'scene.xlsx'

class ImageViewer(QMainWindow):
    def __init__(self, parent=None):
        """
        """
        super(ImageViewer, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1920, 1080)
        self.keyValue = 0
        self.keyMax = 0.5
        self.keyMin = 0
        self.sceneIndex = 0
        participantName = raw_input("Please input ID:")

        scene_table = read_xls(SCENE_FILE, 'scene_list', ['scene', 'lum'])
        self.sceneList=[(scene_table['scene'][i], scene_table['lum'][i]) for i in range(len(scene_table['scene']))]
        random.shuffle(self.sceneList)

        self.delta = 0.01
        self.started = False
        self.fileFormat='.jpg'
        self.infoLabel = QLabel("<font color=black size=200>Press Space To Start</font>")
        self.infoLabel.adjustSize()
        self.infoLabel.move(1925,0)
        #self.infoLabel.setFont()
        self.infoLabel.show()

        self.datafile='result_'+participantName+'_'+strftime("%Y-%m-%d_%H_%M_%S", localtime())

    def setInfo(self, txt):
        self.infoLabel.setText("<font color=black size=40>"+txt+"</font>")
        self.infoLabel.adjustSize()
        self.infoLabel.show()

    def setImage(self):
        self.imageLabel=QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.resize(1920, 1080)
        #filename = os.getcwd()+os.sep+"ScenePic"+os.sep+'3_DN.jpg'
        self.imageLabel.move(0, 0)
        self.setWindowTitle("Image Viewer")
        self.setCentralWidget(self.imageLabel)

        #self.showImage(filename)

    def keyPressEvent(self, event):
        # go to next scene

        if not self.started:
            if event.key() == Qt.Key_Space:
                self.started = True
                self.keyValue=random.randrange(0, 50, 1)/100.
                self.showImage()

            return

        if event.key() == Qt.Key_N:
            self.record()
            self.sceneIndex += 1
            if self.sceneIndex > len(self.sceneList)-1:
                self.imageLabel.close()
                self.close()
                QCoreApplication.quit()
                return

            else:
                self.keyValue=random.randrange(0, 50, 1)/100.

            self.showImage()
            # give an original key

        # go to previous scene
        if event.key() == Qt.Key_P:
            self.sceneIndex -= 1
            if self.sceneIndex < 0:
                self.sceneIndex = 0
            self.showImage()

        # adjust key value
        if event.key() == Qt.Key_Up:

            self.keyValue += self.delta
            if self.keyValue > self.keyMax:
                self.keyValue = self.keyMax
            self.showImage()

        if event.key() == Qt.Key_Down:
            self.keyValue -= self.delta
            if self.keyValue < self.keyMin:
                self.keyValue = self.keyMin
            self.showImage()

        if event.key()==Qt.Key_Escape:
            self.quitApp()


    def showImage(self):
        key_str = "%1d" % int(self.keyValue*100)
        scene, status = self.sceneList[self.sceneIndex]
        filename = os.getcwd()+os.sep+"ScenePic"+os.sep+scene+"key"+key_str+self.fileFormat
        print filename
        if filename:
            self.image = QImage(filename)
            if not self.image:
                QMessageBox.information(None, "Error", "Cannot load ")
            else:
                self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
                #self.imageLabel.adjustSize()
                #self.imageLabel.resize(1920, 1080)
        #self.imageLabel.show()

                self.setInfo("%s,Status:%s,Key Value:%.3f" % (scene, status,self.keyValue))

    def testPrint(self):
        print 'scene:', self.sceneList[self.sceneIndex]
        print 'keyValue:', self.keyValue

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.closeAct)
        self.mb = self.menuBar()
        self.mb.addMenu(self.fileMenu)
        pass

    def record(self):
        scene, level=self.sceneList[self.sceneIndex]
        record(self.datafile, {"Scene": scene, "Level": level, "Key Value": self.keyValue})


    def quitApp(self):
           """ Function to confirm a message from the user
           """
           userInfo = QMessageBox.question(self, 'Confirmation',
                                           "This will quit the application. Do you want to Continue?",
                                           QMessageBox.Yes | QMessageBox.No)
           if userInfo == QMessageBox.Yes:
               QCoreApplication.quit()
           if userInfo == QMessageBox.No:
               pass


if __name__ == "__main__":



    app = QApplication(sys.argv)
    fm = ImageViewer()
    fm.setImage()
    fm.show()
#全屏使用下句
#    fm.showFullScreen()
    app.exec_()