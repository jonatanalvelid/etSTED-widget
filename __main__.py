from EtSTEDController import EtSTEDController
from EtSTEDWidget import EtSTEDWidget
from mockcamera import MockCamera
from PyQt5 import QtWidgets
import sys

_setupInfo = None


if __name__ == "__main__":
    etSTEDapp = QtWidgets.QApplication(sys.argv)
    camera = MockCamera()
    widget = EtSTEDWidget()
    controller = EtSTEDController(camera, _setupInfo, widget)
    widget.show()

    sys.exit(etSTEDapp.exec_())
