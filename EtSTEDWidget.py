import os
import napari
from napari.utils.translations import trans

import pyqtgraph as pg
#from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Qt import QtCore
from qtpy import QtGui, QtWidgets

from basewidgets import Widget

_etstedDir = os.path.join('C:\\etSTED', 'imcontrol_etsted')


class EtSTEDWidget(Widget):
    """ Widget for controlling the etSTED implementation. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.analysisDir = os.path.join(_etstedDir, 'analysis_pipelines')
        self.transformDir = os.path.join(_etstedDir, 'transform_pipelines')
        
        if not os.path.exists(self.analysisDir):
            os.makedirs(self.analysisDir)

        if not os.path.exists(self.transformDir):
            os.makedirs(self.transformDir)
        
        # add all available analysis pipelines to the dropdown list
        self.analysisPipelines = list()
        self.analysisPipelinePar = QtGui.QComboBox()
        for pipeline in os.listdir(self.analysisDir):
            if os.path.isfile(os.path.join(self.analysisDir, pipeline)):
                pipeline = pipeline.split('.')[0]
                self.analysisPipelines.append(pipeline)
        
        self.analysisPipelinePar.addItems(self.analysisPipelines)
        self.analysisPipelinePar.setCurrentIndex(0)
        
        self.__paramsExclude = ['img', 'bkg', 'binary_mask', 'exinfo', 'testmode']
        
        #TODO: add way to save current coordinate transform as a file that can be loaded from the list
        # add all available coordinate transformations to the dropdown list
        self.transformPipelines = list()
        self.transformPipelinePar = QtGui.QComboBox()
        for transform in os.listdir(self.transformDir):
            if os.path.isfile(os.path.join(self.transformDir, transform)):
                transform = transform.split('.')[0]
                self.transformPipelines.append(transform)
        
        self.transformPipelinePar.addItems(self.transformPipelines)
        self.transformPipelinePar.setCurrentIndex(0)

        # add all forAcquisition detectors in a dropdown list, for being the fastImgDetector (widefield)
        self.fastImgDetectors = list()
        self.fastImgDetectorsPar = QtGui.QComboBox()
        self.fastImgDetectorsPar_label = QtGui.QLabel('Fast detector')
        self.fastImgDetectorsPar_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        # add all lasers in a dropdown list, for being the fastImgLaser (widefield)
        self.fastImgLasers = list()
        self.fastImgLasersPar = QtGui.QComboBox()
        self.fastImgLasersPar_label = QtGui.QLabel('Fast laser')
        self.fastImgLasersPar_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        # add all experiment modes a dropdown list
        self.experimentModes = ['Experiment','Test:Visualize','Test:Validate']
        self.experimentModesPar = QtGui.QComboBox()
        self.experimentModesPar_label = QtGui.QLabel('Experiment mode')
        self.experimentModesPar_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter)
        self.experimentModesPar.addItems(self.experimentModes)
        self.experimentModesPar.setCurrentIndex(0)

        self.param_names = list()
        self.param_edits = list()

        self.initiateButton = BetterPushButton('Initiate etSTED')
        self.initiateButton.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.loadPipelineButton = BetterPushButton('Load pipeline')
        
        self.coordTransfCalibButton = BetterPushButton('Transform calibration')
        self.recordBinaryMaskButton = BetterPushButton('Record binary mask')
        self.loadScanParametersButton = BetterPushButton('Load scan parameters')
        self.setUpdatePeriodButton = BetterPushButton('Set update period')
        self.setBusyFalseButton = BetterPushButton('Unlock softlock')

        self.endlessScanCheck = QtGui.QCheckBox('Endless')
        self.visualizeCheck = QtGui.QCheckBox('Visualize')
        self.validateCheck = QtGui.QCheckBox('Validate')

        self.bin_thresh_label = QtGui.QLabel('Bin. threshold')
        self.bin_thresh_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.bin_thresh_edit = QtGui.QLineEdit(str(9))
        self.bin_smooth_label = QtGui.QLabel('Bin. smooth (px)')
        self.bin_smooth_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.bin_smooth_edit = QtGui.QLineEdit(str(2))
        self.throw_delay_label = QtGui.QLabel('Throw delay (us)')
        self.throw_delay_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.throw_delay_edit = QtGui.QLineEdit(str(30))
        self.update_period_label = QtGui.QLabel('Update period (ms)')
        self.update_period_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.update_period_edit = QtGui.QLineEdit(str(100))

        # help widget for coordinate transform
        self.coordTransformWidget = CoordTransformWidget(*args, **kwargs)

        # help widget for showing images from the analysis pipelines, i.e. binary masks or analysed images in live
        self.analysisHelpWidget = AnalysisWidget(*args, **kwargs)

        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)

        # initialize widget controls
        currentRow = 0

        self.grid.addWidget(self.initiateButton, currentRow, 0)
        self.grid.addWidget(self.endlessScanCheck, currentRow, 1)
        self.grid.addWidget(self.experimentModesPar_label, currentRow, 2)
        self.grid.addWidget(self.experimentModesPar, currentRow, 3)
        
        currentRow += 1

        self.grid.addWidget(self.throw_delay_label, currentRow, 0)
        self.grid.addWidget(self.throw_delay_edit, currentRow, 1)
        self.grid.addWidget(self.bin_thresh_label, currentRow, 2)
        self.grid.addWidget(self.bin_thresh_edit, currentRow, 3)

        currentRow += 1

        self.grid.addWidget(self.loadPipelineButton, currentRow, 0)
        self.grid.addWidget(self.analysisPipelinePar, currentRow, 1)
        self.grid.addWidget(self.bin_smooth_label, currentRow, 2)
        self.grid.addWidget(self.bin_smooth_edit, currentRow, 3)

        currentRow += 1

        self.grid.addWidget(self.transformPipelinePar, currentRow, 2)
        self.grid.addWidget(self.coordTransfCalibButton, currentRow, 3)

        currentRow += 1

        self.grid.addWidget(self.update_period_label, currentRow, 2)
        self.grid.addWidget(self.update_period_edit, currentRow, 3)

        currentRow += 1

        self.grid.addWidget(self.setUpdatePeriodButton, currentRow, 2)
        self.grid.addWidget(self.recordBinaryMaskButton, currentRow, 3)

        currentRow +=1

        self.grid.addWidget(self.fastImgDetectorsPar_label, currentRow, 2)
        self.grid.addWidget(self.fastImgDetectorsPar, currentRow, 3)

        currentRow += 1

        self.grid.addWidget(self.fastImgLasersPar_label, currentRow, 2)
        self.grid.addWidget(self.fastImgLasersPar, currentRow, 3)

        currentRow +=1 

        self.grid.addWidget(self.loadScanParametersButton, currentRow, 2)
        self.grid.addWidget(self.setBusyFalseButton, currentRow, 3)

    def initParamFields(self, parameters: dict):
        """ Initialized etSTED widget parameter fields. """
        # remove previous parameter fields for the previously loaded pipeline
        for param in self.param_names:
            self.grid.removeWidget(param)
        for param in self.param_edits:
            self.grid.removeWidget(param)

        # initiate parameter fields for all the parameters in the pipeline chosen
        currentRow = 4
        
        self.param_names = list()
        self.param_edits = list()
        for pipeline_param_name, pipeline_param_val in parameters.items():
            if pipeline_param_name != 'img' and pipeline_param_name != 'bkg' and pipeline_param_name != 'binary_mask' and pipeline_param_name != 'testmode':
                # create param for input
                param_name = QtGui.QLabel('{}'.format(pipeline_param_name))
                param_value = pipeline_param_val.default if pipeline_param_val.default is not pipeline_param_val.empty else 0
                param_edit = QtGui.QLineEdit(str(param_value))
                # add param name and param to grid
                self.grid.addWidget(param_name, currentRow, 0)
                self.grid.addWidget(param_edit, currentRow, 1)
                # add param name and param to object list of temp widgets
                self.param_names.append(param_name)
                self.param_edits.append(param_edit)

                currentRow += 1

    def setFastDetectorList(self, detectorNames):
        """ Set combobox with available detectors to use for the fast method. """
        self.fastImgDetectors = detectorNames
        self.fastImgDetectorsPar.addItems(self.fastImgDetectors)
        self.fastImgDetectorsPar.setCurrentIndex(0)

    def setFastLaserList(self, laserNames):
        """ Set combobox with available lasers to use for the fast method. """
        self.fastImgLasers = laserNames
        self.fastImgLasersPar.addItems(self.fastImgLasers)
        self.fastImgLasersPar.setCurrentIndex(0)

    def launchHelpWidget(self, widget, init=True):
        """ Launch the help widget. """
        if init:
            widget.show()
        else:
            widget.hide()


class BetterPushButton(QtWidgets.QPushButton):
    """BetterPushButton is a QPushButton that does not become too small when
    styled."""

    def __init__(self, text=None, minMinWidth=20, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self._minMinWidth = minMinWidth
        self.updateMinWidth(text)

    def setText(self, text, *args, **kwargs):
        super().setText(text, *args, **kwargs)
        self.updateMinWidth(text)

    def updateMinWidth(self, text=None):
        if text is None:
            text = self.text()

        fontMetrics = QtGui.QFontMetrics(self.font())
        textWidth = fontMetrics.width(text)
        minWidth = max(self._minMinWidth, textWidth + 8)
        self.setStyleSheet(f'min-width: {minWidth}px')


class EmbeddedNapari(napari.Viewer):
    """ Napari viewer to be embedded in non-napari windows. Also includes a
    feature to protect certain layers from being removed when added using
    the add_image method. """

    def __init__(self, *args, show=False, **kwargs):
        super().__init__(*args, show=show, **kwargs)

        # Monkeypatch layer removal methods
        oldDelitemIndices = self.layers._delitem_indices

        def newDelitemIndices(key):
            indices = oldDelitemIndices(key)
            for index in indices[:]:
                layer = index[0][index[1]]
                if hasattr(layer, 'protected') and layer.protected:
                    indices.remove(index)
            return indices

        self.layers._delitem_indices = newDelitemIndices

        # Make menu bar not native
        self.window._qt_window.menuBar().setNativeMenuBar(False)

        # Remove unwanted menu bar items
        menuChildren = self.window._qt_window.findChildren(QtWidgets.QAction)
        for menuChild in menuChildren:
            try:
                if menuChild.text() in [trans._('Close Window'), trans._('Exit')]:
                    self.window.file_menu.removeAction(menuChild)
            except Exception:
                pass

    def add_image(self, *args, protected=False, **kwargs):
        result = super().add_image(*args, **kwargs)

        if isinstance(result, list):
            for layer in result:
                layer.protected = protected
        else:
            result.protected = protected
        return result

    def get_widget(self):
        return self.window._qt_window


class AnalysisWidget(Widget):
    """ Pop-up widget for the live analysis images or binary masks. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.imgVbWidget = pg.GraphicsLayoutWidget()
        self.imgVb = self.imgVbWidget.addViewBox(row=1, col=1)

        self.img = pg.ImageItem(axisOrder = 'row-major')
        self.img.translate(-0.5, -0.5)

        self.imgVb.addItem(self.img)
        self.imgVb.setAspectLocked(True)

        self.info_label = QtGui.QLabel('<image info>')
        
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.info_label, 0, 0)
        self.grid.addWidget(self.imgVbWidget, 1, 0)


class CoordTransformWidget(Widget):
    """ Pop-up widget for the coordinate transform between the two etSTED modalities. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loadLoResButton = BetterPushButton('Load low-res calibration image')
        self.loadHiResButton = BetterPushButton('Load high-res calibration image')
        self.saveCalibButton = BetterPushButton('Save calibration')
        self.resetCoordsButton = BetterPushButton('Reset coordinates')

        self.napariViewerLo = EmbeddedNapari()
        self.napariViewerHi = EmbeddedNapari()

        # add points layers to the viewer
        self.pointsLayerLo = self.napariViewerLo.add_points(name="lo_points", symbol='ring', size=20, face_color='green', edge_color='green')
        self.pointsLayerTransf = self.napariViewerHi.add_points(name="transf_points", symbol='cross', size=20, face_color='red', edge_color='red')
        self.pointsLayerHi = self.napariViewerHi.add_points(name="hi_points", symbol='ring', size=20, face_color='green', edge_color='green')
        

        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
    
        # initialize the controls for the coordinate transform help widget
        currentRow = 0
        self.grid.addWidget(self.loadLoResButton, currentRow, 0)
        self.grid.addWidget(self.loadHiResButton, currentRow, 1)
        
        currentRow += 1
        self.grid.addWidget(self.napariViewerLo.get_widget(), currentRow, 0)
        self.grid.addWidget(self.napariViewerHi.get_widget(), currentRow, 1)

        currentRow += 1
        self.grid.addWidget(self.saveCalibButton, currentRow, 0)
        self.grid.addWidget(self.resetCoordsButton, currentRow, 1)

