from EtSTEDController import EtSTEDController
from EtSTEDWidget import EtSTEDWidget
from mockcamera import MockCamera
from qtpy import QtWidgets
import sys

setupInfo = None
options = None

etSTEDapp = QtWidgets.QApplication(sys.argv)
camera = MockCamera()
widget = EtSTEDWidget(options)
controller = EtSTEDController(camera, setupInfo, widget)

widget.show()
sys.exit(etSTEDapp.exec_())
