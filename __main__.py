from EtSTEDController import EtSTEDController
from EtSTEDWidget import EtSTEDWidget
from basecontrollers import ImConWidgetControllerFactory
from qtpy import QtWidgets
import sys

setupInfo = None
options = None

etSTEDapp = QtWidgets.QApplication(sys.argv)
widget = EtSTEDWidget(options)
controllerfactory = ImConWidgetControllerFactory(setupInfo)
controller = EtSTEDController(setupInfo, widget, controllerfactory)

widget.show()
sys.exit(etSTEDapp.exec_())
