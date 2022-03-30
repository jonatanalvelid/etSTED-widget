# etSTED-widget
Generic event-triggered imaging widget and controller, a generalization of the event-triggered STED widget provided in ImSwitch and presented in Alvelid et al. 2022. Use for implementation in other python-based microscope control software, or as a basis for implementation in non-compatible microscope control software solutions. Alternatively, use the provided widget and controller as a standalone widget to control event-triggered imaging, if an overarching intersoftware communication solution is present and implementable with this widget. Beware that an intersoftware communication solution can significantly slow down the time between fast image and analysis, as well as detected event and scan initiation due to intersoftware communication delays. 

Provided is additionally a folder with the detection pipelines developed as part of Alvelid et al. 2022, together with coordinate transformation pipelines with a cubic polynomial basis. See below for a description of their functionality and individual use cases, as well as a general guide to add your own pipelines. 

## Installation
To run the etSTED-widget as a standalone widget, or to implement it in your own microscope control software, install the dependencies by running the following commands in either conda or pip from the source repository. Python 3.9 or later is tested and recommended. 
```
conda env create -f environment.yml
```

```
pip install -r requirements.txt
```

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

Below follows brief descriptions of the pipelines developed for and used in Alvelid et al. 2022.

### rapid_signal_spikes
Detection pipeline used to detection rapid signal spikes occuring from one analysed frame to the next, such as for the fluorescent calcium chelator BAPTA-OregonGreen. Thanks to the rapidity of the signal spikes, the pipeline is simplified to a direction comparison between the current frame and the previous frame. Initially smoothing and difference of Gaussians is performed on the image. Following this, the previous frame is subtracted from the current, and the result subsequently divided by the previous frame, to finally generate an image where each pixel value corresponds to the ratiometric increase in intensity (independent of the intensity in the raw frame). 

Following this, a peak detection is performed on the ratiometric image, allowing to detect those regions of pixels that have increased significantly in intensity above a user-provided ratiometric threshold. If multiple peaks are detected, the coordinates of the peak with the ratiometrically highest intensity is chosen as the detected event coordinate.

### bapta_calcium_spikes
Detection pipeline used to detect rapid BAPTA signal spikes.

### dynamin_rise
Detection pipeline used to detect slowly rising, and often less bright, signals over multiple frames, such as for dynamin1-GFP and dynamin2-GFP. The pipeline localizes peaks in the cell and tracks the intensity of them over time (using a dataframe returned as exinfo). The pipeline connects the new localizations to the previous tracks, and triggers once the intensity of one localized peak has increased by a certain factor for the last number of frames. 

### vesicle_proximity
Detection pipeline used to detect the proximity of vesicles moving inside the cell, such as for. 

## Coordinate transformations
### coord_transform

### wf_800_scan_80
