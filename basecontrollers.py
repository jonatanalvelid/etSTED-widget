import weakref
from abc import ABC, abstractmethod
from imswitch.imcommon.framework import SignalInterface


class MainController:
    def closeEvent(self):
        pass


class SignalInterface(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass


class WidgetController(SignalInterface):
    """ Superclass for all WidgetControllers. """

    def __init__(self, widget, factory, *args, **kwargs):
        self._widget = widget
        self._factory = factory
        super().__init__()

    def closeEvent(self):
        pass

    @classmethod
    def create(cls, widget):
        """ Initialize a factory and create this controller with it. Returns
        the created controller. """
        factory = WidgetControllerFactory()
        return factory.createController(cls, widget)


class ImConWidgetController(WidgetController):
    """ Superclass for all ImConWidgetController.
    All WidgetControllers should have access to the setup information,
    MasterController, CommunicationChannel and the linked Widget. """

    def __init__(self, setupInfo, *args, **kwargs):
        # Protected attributes, which should only be accessed from controller and its subclasses
        self._setupInfo = setupInfo

        # Init superclass
        super().__init__(*args, **kwargs)


class WidgetControllerFactory:
    """ Factory class for creating a WidgetController object. """

    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__createdControllers = []


    def createController(self, controllerClass, widget, *args, **kwargs):
        controller = controllerClass(*self.__args, *args,
                                     widget=widget, factory=self
                                     **self.__kwargs, **kwargs)
        self.__createdControllers.append(weakref.ref(controller))
        return controller

    def closeAllCreatedControllers(self):
        for controllerRef in self.__createdControllers:
            controller = controllerRef()
            if controller is not None:
                try:
                    controller.closeEvent()
                except Exception:
                    print(f'Error closing {type(controller).__name__}')


class ImConWidgetControllerFactory(WidgetControllerFactory):
    """ Factory class for creating a ImConWidgetController object. """

    def __init__(self, setupInfo):
        super().__init__(setupInfo=setupInfo)



# Copyright (C) 2020-2021 ImSwitch developers
# This file is part of ImSwitch.
#
# ImSwitch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ImSwitch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
