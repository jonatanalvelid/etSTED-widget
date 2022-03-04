from EtSTEDController import EtSTEDController
from EtSTEDWidget import EtSTEDWidget
from basecontrollers import ImConWidgetControllerFactory

setupInfo = None
options = None

widget = EtSTEDWidget(options)
controllerfactory = ImConWidgetControllerFactory(setupInfo)
controller = EtSTEDController(setupInfo, widget, controllerfactory)
