et_to_fixation(path_to_fixation,survey_area,path_info,path_to_result=None,geolocalisation=False,export_argument_on_result=False,export_argument_on_fixation=False,name_export='coord_fixation_on_map.csv'):

The function allows to pass from output fixation points (relative to a surface) produced by the pupil-core eye tracker to fixation points in a 2D scene (screen)

path_to_fixation: path of the fixation points file. The file is generated by pupil_player after exorting the surface (fixation_on_surface "name on surface".csv)

path_info: path of the file info.player.json generated by the eye tracker. It allows to know the machine time at the time of the acquisition.

survey_area : the location of the map on the screen : [xmin,ymin,xmax,ymax] in percentage

path_to_result: path of the result file. This file gives information about what was on the screen at the time of acquisition.
To be able to link the fixation points to a state on the screen, the acquisition and the application that generates this file must be on the same computer.
This file must be a csv with a header and must open with the pandas library. It must at least have a time column (with machine times)


export_argument_on_result: this is the list of additional elements that we want to have for each fixation point compared to what was displayed on the screen during the experiment. 
These data are saved in the result file as for example the name of the displayed image, the displayed flow, the stage of the investigation, the zoom, the coordinates, the position of a mouse or other arguments as needed at each moment of the experiment. 
example header :
- time,image
- time,zoom,xmin,ymin,xmax,ymax,stage
- time,zoom,xmin,ymin,xmax,ymax,stage,n_iteration,repetition



example 1: as soon as the image was changed, a line was added with the time of the change and the name of the new image.
example 2: was a free map manipulation with several steps. every 100 ms the coordinates of the map were added as well as the step we were at (a button allowed to change) in order to be able to set the fixations to the closest possible state to reality

export_argument_on_fixation: this is the list of additional elements that we want to have for each fixation point that are in the eye tracker export file, such as the dispersion and duration

geolocalisation : allows to know if the person wants the relative position of the points in relation to the display or to geolocate the points in case a map is displayed on the screen. In the case of geolocation the result file must have the coordinates of the corners of the map called : xmin,ymin,xmax,ymax


name_export : name of the export file