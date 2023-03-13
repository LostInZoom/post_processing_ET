 et_to_fixation(path_to_fixation,box_map,path_info,path_to_result=None,geolocalisation=False,export_argument_on_result=False,name_export='coord_fixation_on_map.csv'):


path_to_fixation : chemin du fichier des points de fixation. Le fichier est généré par player après exort de la surface (fixation_on_surface "name on surface".csv)

path_info :chemin du fichier généré par l'eye tracker. Il permet de connaitre le temps machine au moment de l'acquisition.

box_map : l'emplacement de la carte sur l'écran : [xmin,ymin,xmax,ymax] en pourcentage

path_to_result : chemin du fichier résutat. ce fichier permet de donner des informations sur ce qui composait l'écran lors de l'acquisition.
Pour pouvoir relier les points de fixation à un état sur l'écran, l'acquisition et l'application qui génére ce fichier doit être sur le même ordinateur.
ce fichier doit être un csv avec un entête et doit s'ouvrir avec la librairie pandas. Il doit au minima avoir une colonne time (avec les temps machine)


export_argument_on_result : c'est la liste des éléments supplémentaire qu'on souhaite avoir pour chaque point de fixation par rapport à ce qui était affiché à l'écran pendant l'expérience. 
ces données sont enregistrés dans le fichiers résultats comme par exemple le nom de l'image affiché, le flux affiché, l'étape de l'enquête, le zoom, les coordonnées, la position d'une souris  ou encore d'autre argument selon le besoin à chaque moment de l'expérience. 
exemple d'entête :
- time,image
- time,zoom,xmin,ymin,xmax,ymax,etape,
- time,zoom,xmin,ymin,xmax,ymax,etape,n_iteration,repetition

l'exemple 1: dès qu'on changeait l'image on ajoutait une ligne avec le moment(time) du changment et le nom de la nouvelle image.
l'exemple 2: était une manipulation libre de carte avec plusieurs étapes. toutes les 100 ms les coordonnées de la carte étaient ajoutés ainsi que  l'étape à laquelle on était (un bouton permettait de changer) afin de pouvoir racorder les fixations à l'état le plus proche possible de la réalité

geolocalisation : permet de savoir si la personne souhaite la position relatif des points par rapport à l'affichage ou alors géolocaliser les points dans le cas qu'une carte est affichée sur l'écran. dans le cas de la géolocalisation le fichier résultat doit avoir les coordonnées des coins de la carte appelé : xmin,ymin,xmax,ymax


name_export : nom du fichier d'export 