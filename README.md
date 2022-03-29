# etSTED-widget
Generic event-triggered imaging widget and controller, a generalization of the event-triggered STED widget provided in ImSwitch and presented in Alvelid et al. 2022. Use for implementation in other python-based microscope control software, or as a basis for implementation in non-compatible microscope control software solutions. Alternatively, use the provided widget and controller as a standalone widget to control event-triggered imaging, if an overarching intersoftware communication solution is present and implementable with this widget. Beware that an intersoftware communication solution can significantly slow down the time between fast image and analysis, as well as detected event and scan initiation due to intersoftware communication delays. 

Provided is additionally a folder with the detection pipelines developed as part of Alvelid et al. 2022, together with coordinate transformation pipelines with a cubic polynomial basis. See below for a description of their functionality and individual use cases. 

## Detection pipelines
### rapid_signal_spikes
Detection pipeline used to detection rapid signal spikes occuring from one analysed frame to the next, such as for the fluorescent calcium chelator BAPTA-OregonGreen. Thanks to the rapidity of the signal spikes, the pipeline is simplified to a direction comparison between the current frame and the previous frame. Initially smoothing and difference of Gaussians is performed on the image. Following this, the previous frame is subtracted from the current, and the result subsequently divided by the previous frame, to finally generate an image where each pixel value corresponds to the ratiometric increase in intensity (independent of the intensity in the raw frame). 

Following this, a peak detection is performed on the ratiometric image, allowing to detect those regions of pixels that have increased significantly in intensity above a user-provided ratiometric threshold. If multiple peaks are detected, the coordinates of the peak with the ratiometrically highest intensity is chosen as the detected event coordinate.

### bapta_calcium_spikes

### dynamin_rise

### vesicle_proximity


## Coordinate transformations
### coord_transform

### wf_800_scan_80
