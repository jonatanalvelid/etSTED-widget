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

Prepare the etSTED-widget by downloading or forking the code, and to start it by running the ``` __main__.py ``` file.

In order to run the GPU-boosted analysis pipelines in real etSTED experiments, CUDA Toolkit has additionally to be installed on the machine, together with the cupy package in the same environment. See instructions at https://docs.cupy.dev/en/stable/install.html. 

Certain analysis pipelines may require additional packages to be installed, see respective pipeline for the full list of dependencies. For the provided pipelines, the additional dependencies are as follows: dynamin_rise - trackpy, pandas; vesicle_proximity - trackpy, pandas

## Demo - mock etSTED experiment
Mock etSTED experiments can be performed with the simulated camera and image viewer provided in in the widget. The mock camera generates noisy images with occasional intensity spikes. The following steps can be followed to initiate a mock experiment, taking 1-3 min to set up and run:

1. Record a binary mask containing a selection of pixels with the default binary threshold by pressing ```Record binary mask```. 
2. Load a CPU-version of the ```rapid_signal_spikes_cpu``` detection pipeline by choosing it in the dropdown menu and pressing ```Load pipeline```. 
3. Change to the pre-calibrated coordinate transformation ```wf_800_scan_80```.
4. Change experiment mode from the dropdown menu to ```TestVisualize``` in order to run the mock experiment while showing the preprocessed images in real-time in the pop-out help widget.
5. Run mock experiment by pressing ```Initiate```.
6. The real-time white circles on the image in the image viewer shows detected events and spots where the STED scanning would have taken place. The mock camera returns an image with at most 1 peak at the same time, and as such at most 1 detected event will be displayed at the same time.

If the widget softlocks due to not following the steps above or for other reasons, press the ```Unlock softlock``` button. 

The main version of [ImSwitch](https://github.com/kasasxav/ImSwitch) is capable of running in full simulation mode, and using the provided etsted_sim.json setup configuration, a basic experimental setup for event-triggered imaging experiments can be tested. Follow the same instructions as in the repository of the separate version of ImSwitch provided at [ImSwitch-etSTED](https://github.com/jonatanalvelid/ImSwitch-etSTED) for testing it out.

## Running etSTED experiments
For real etSTED experiments, the widget requires an implementation in a complete microscope control software. Follow the instructions at the [ImSwitch repository](https://github.com/kasasxav/ImSwitch) to find and run a full microscope control software with etSTED implemented, also capable of running in full simulation mode. In order to run etSTED experiments, use at least one camera for the fast method, one laser for the fast method, one laser for the scanning method, and one point-detector for the scanning method. 

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
