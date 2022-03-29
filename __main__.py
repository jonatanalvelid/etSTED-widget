from EtSTEDController import EtSTEDController
from EtSTEDWidget import EtSTEDWidget
from mockcamera import MockCamera
from PyQt5 import QtWidgets
import sys

setupInfo = None

etSTEDapp = QtWidgets.QApplication(sys.argv)
camera = MockCamera()
widget = EtSTEDWidget()
controller = EtSTEDController(camera, setupInfo, widget)

widget.show()
sys.exit(etSTEDapp.exec_())
