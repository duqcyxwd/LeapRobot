import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType


app = QApplication(sys.argv)
form_class, base_class = loadUiType('controlPage.ui')
class ControlPage(base_class, form_class):
    def __init__(self, *args):
        super(ControlPage, self).__init__(*args)
        self.setupUi(self)
        # self.setWindowTitle('control page')
    
    @pyqtSlot()
    def on_button1_clicked(self):
        for s in "This is a demo".split(" "):
            self.list.addItem(s)

if __name__ == '__main__':

  form = ControlPage()
  form.show()
  sys.exit(app.exec_())
