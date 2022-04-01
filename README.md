# etSTED-widget
Generic event-triggered imaging widget and controller, a generalization of the event-triggered STED widget provided in ImSwitch and presented in Alvelid et al. 2022. Use for implementation in other Python-based microscope control software, or as a basis for implementation in non-compatible microscope control software solutions. Alternatively, use the provided widget and controller as a standalone widget to control event-triggered imaging, if an overarching intersoftware communication solution is present and implementable with this widget. Beware that an intersoftware communication solution can significantly slow down the time between fast image and analysis, as well as detected event and scan initiation due to intersoftware communication delays. 

Provided is additionally a folder with the detection pipelines developed as part of Alvelid et al. 2022, together with coordinate transformation pipelines with a cubic polynomial basis. See below for a description of their functionality and individual use cases, as well as a general guide to add your own pipelines. 

## Versions
This version contains a mock camera used for simulating the fast imaging part of the event-triggered imaging, for use with the ```rapid_signal_spikes``` pipeline.

The version [etSTED-widget-base](https://github.com/jonatanalvelid/etSTED-widget-base) is the most generalized version, specifically tailored for implementation in external Python-based microscope control software. 

[ImSwitch](https://github.com/kasasxav/ImSwitch) has the etSTED widget integrated, and can be used as a full solution for microscope control and event-triggered imaging. 

## Installation
To run the etSTED-widget as a standalone widget, or to implement it in your own microscope control software, install the dependencies by running the following command in pip from the source repository and in the virtual environment of choice. Python 3.7 or later is tested and recommended. 

```
pip install -r requirements.txt
```

GPU-versions of detection pipelines (see below) additionally requires ```cupy``` to be installed. Follow installation instructions for the specific CUDA-version of your GPU. 

Certain analysis pipelines may require additional packages to be installed, see respective pipeline for the full list of dependencies. For the provided pipelines, the additional dependencies are as follows: dynamin_rise - trackpy, pandas; vesicle_proximity - trackpy, pandas

## Detection pipelines
Detection pipelines are the basis of the event-triggered method, and new ones can easily be added by creating a .py file with an analysis function of the same name. This function should as a basis take the following five arguments:
| Arguments      | Description | Default value |
| --- | --- | --- |
| img | The latest fast imaging frame | - |
| bkg | The previous fast imaging frames, length decided in controller | None |
| binary_mask | A binary mask of the region of interest | None |
| exinfo | Any object that should be passed on to the next pipeline run (e.g. tracks etc.) | None |
| testmode | Boolean used to decide if to return preprocessed image or not | None |

The function can additionally take any parameters with numerical values (float or int) which will be loaded with the name as the label and with a text field in the widget GUI, for the user to interactively change the parameter values. Example can be thresholds for preprocessing, number of coordinates to maximally locate, boolean (0/1) parameters for running certain code blocks, smoothing radii, etc.

The function should return the detected coordinate(s), as a 2D numpy array with X and Y coordinates as the two columns, as well as any object saved to exinfo as explained above. Additionally, if testmode is True, the function should return any state of preprocessed image that the user would like to view during visualization runs, and/or save during validatio runs, for inspecting if the pipeline is performing well and be able to adjust the pipeline parameters to liking. 

Below follows brief descriptions of the pipelines developed for and used in Alvelid et al. 2022. Each pipeline is provided in a CPU-only as well as a higher-performing GPU version (using cupy). 

### rapid_signal_spikes
Detection pipeline used for detection of rapid signal spikes occuring from one analysed frame to the next, applicable both to the fluorescent calcium chelator BAPTA-OregonGreen (frame rate 20 Hz) or CD63-pHluorin (frame rate 20 Hz). Thanks to the rapidity of the signal spikes, the pipeline is simplified to a direct comparison between the current frame and the previous frame. Initially smoothing and difference of Gaussians is performed on the image. Following this, the previous frame is subtracted from the current, and the result subsequently divided by the previous frame, to finally generate an image where each pixel value corresponds to the ratiometric increase in intensity (independent of the intensity in the raw frame). 

Following this, a peak detection is performed on the ratiometric image, allowing to detect those regions of pixels that have increased significantly in intensity above a user-provided ratiometric threshold. If multiple peaks are detected, the coordinates of the peak with the ratiometrically highest intensity is chosen as the detected event coordinate.

### bapta_calcium_spikes
Detection pipeline used to detect rapid BAPTA signal spikes. See description above of the more generalized version rapid_signal_spikes.

### dynamin_rise
Detection pipeline used to detect slowly rising, and often less bright, signals over multiple frames, such as for dynamin1-GFP and dynamin2-GFP. The pipeline localizes peaks in the cell and tracks the intensity of them over time (using a dataframe returned as exinfo). The pipeline connects the new localizations to the previous tracks, and triggers once the intensity of one newly localized peak has increased by a certain factor for the last number of frames. The track additionally has to stay for the same number of frames without disappearing, to ensure that we are not considering noise spikes.

### vesicle_proximity
Detection pipeline used to detect the proximity of vesicles moving inside the cell, e.g. endosomes, lysosomes etc, for example for CD63-GFP. This pipeline can be used to predict sites for interaction and fusion. The pipeline works by initial preprocessing, peak detection, and track connection, similar to that in dynamin_rise. Following this, the event detection is performed as a set of condition checks on pairs of tracks. Event are detected when: one track disappears (check #1), another track is close-by at the time of disappearance (#2), both tracks have tracked points in a ratio of frames leading up to the disappearance (#3), at least one track has moved an accumulated vectorial distance above a threshold (#4), and at least one track has moved an accumulated absolute distance above a threshold (#5). Thresholds for all the conditions can be set by the user in the GUI, and will vary depending on the type of vesicle investigated and the cellular conditions. 

## Coordinate transformations
Coordinate transformations translate the coordinates between the fast imaging space (for etSTED a camera) and the triggered imaging space (for etSTED the scanned images). The coordinate transform used in Alvelid et al. 2022 is a two-variable third-order polynomial transformation, which can be calibrated using the GUI. The calibration fits the 20 constants in the polynomial. 

### coord_transform
The general third-order polynomial transform function, that takes fitted parameters from the same etSTED instance and detected coordinates in the fast imaging space as arguments and translates the coordinates to the triggered imaging space.

### wf_800_scan_80
The same third-order polynomial transform function without the fitted parameters as an argument, for use with pre-calibrated fitted parameters put directly in the function. The parameters provided is an example of the transformation between a 800x800 widefield camera image and a 80x80 µm STED scanning space used in Alvelid et al. 2022. The widefield coordinates from the function argument is in pixels of the camera, while the returned transformed coordinates are in µm of the scanning space. 
