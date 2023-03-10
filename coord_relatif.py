import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import json





def calcul_box_carte(xmin,xmax,ymin,ymax,shape_screen):
    return([xmin/shape_screen[0],ymin/shape_screen[1],xmax/shape_screen[0],ymax/shape_screen[1]]) # a calculer en pourcentage (xmin,ymin,xmax,ymax)

def calcul_pos_relatif(box_carte,x_pos,y_pos):
    if x_pos > box_carte[0] and x_pos[k] < box_carte[2]:   
        if y_pos > box_carte[1] and y_pos < box_carte[3]:
            x_relatif = (x_pos-box_carte[0])/(box_carte[2]-box_carte[0])
            y_relatif = (y_pos-box_carte[1])/(box_carte[3]-box_carte[1])
            return x_relatif,y_relatif
        else:
            return False
    else:
        return False
    
def etat_ecran(timestamp,resultat,offset,geolocalisation=False,argument_export=False):
    time= 0

    if geolocalisation == False:
        for t in range(len(resultat)):
            autre =[]
            if (timestamp+offset)*1000 >= resultat["time"][t]:
                if argument_export != False:
                    for k in range(argument_export):
                        autre.append(resultat[argument_export[k][t]])
    
                time = resultat["time"][t]
                continue
            else:
                break
        return time,autre
 
    else:
        box = [0,0,0,0]
        time =0
        for t in range(len(resultat)):
            autre =[]
            if (timestamp+offset)*1000 >= resultat["time"][t]:
                box = [float(resultat["xmin"][t]),float(resultat["ymin"][t]),float(resultat["xmax"][t]),float(resultat["ymax"][t])]
                time = resultat["time"][t]
                if argument_export != False:
                    for k in range(argument_export):
                        autre.append(resultat[argument_export[k][t]])
                continue
            else:
                break
    
        return box,time,autre
  

def calcul_loc(x_rel,y_rel,coord_carte):
    x_coord = coord_carte[0] + x_rel*(coord_carte[2]-coord_carte[0] )
    y_coord = coord_carte[1] + y_rel*(coord_carte[3]-coord_carte[1] )
    return [x_coord,y_coord] 


def et_to_fixation(path_to_fixation,box_carte,path_info,path_to_resultat=None,geolocalisation=False,argument_export_on_resultat=None,name_export='coord_fixation_on_map.csv'):

    try :
        f = open(path_info,)
    except:
        print("Failed to load json")
    try :
        fixation = pd.read_csv(path_to_fixation)
    except:
        print("Failed to load fixation")  
    
    if "norm_pos_x" and "norm_pos_y" and "world_timestamp" and "fixation_id" and "world_index" and "dispersion" not in fixation.columns:
        raise KeyError("mauvais format des données")


    json_time = json.load(f)
    start_time_system = float(json_time["start_time_system_s"]) # System Time at recording start
    start_time_synced = float(json_time["start_time_synced_s"])
    offset = start_time_system - start_time_synced 

    if path_to_resultat != None:
        assert os.path.exists(path_to_resultat)
        resultat = pd.read_csv(path_to_resultat) 
        if argument_export_on_resultat != None :
            for i in range(len(argument_export_on_resultat)):
                if argument_export_on_resultat[i] not in fixation.columns:
                    raise KeyError("l'argument n'est pas dans le fichier fixation")  
    if geolocalisation == True :
        if "xmin" and "ymin" and "xmax" and "ymax" not in fixation.columns:
            raise KeyError("error data")
    coord_fixation = []
    for k in range(len(fixation)):
        id = fixation["fixation_id"][k]
        world_index = fixation["world_index"][k]
        dispersion = fixation["dispersion"][k]
        x_rel,y_rel = calcul_pos_relatif(box_carte,fixation["norm_pos_x"][k],fixation["norm_pos_y"][k])
        if x_rel != False:
            if path_to_resultat == None:
                coord_fixation.append([world_index,id,x_rel,y_rel,dispersion,(fixation["world_timestamp"][k]+offset)*1000])
            else:
                if geolocalisation == False:
                    time,autre =  etat_ecran(fixation["world_timestamp"][k],resultat,offset)
                    liste = [world_index,id,time,x_rel,y_rel,dispersion]
                    if argument_export_on_resultat != None:
                        for t in range(len(autre)):
                            liste.append(autre[t])
                    coord_fixation.append([liste])

                else:
                    box,time,autre = etat_ecran(fixation["world_timestamp"][k],resultat,offset,geolocalisation=geolocalisation)
                    x_loc,y_loc =calcul_loc(x_rel,y_rel,box)
                    liste = [world_index,id,time,x_loc,y_loc,dispersion]
                    if argument_export_on_resultat != None:
                        for t in range(len(autre)):
                            liste.append(autre[t])
                    coord_fixation.append([liste])

    if path_to_resultat == None:
        with open(name_export, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["world_index","id_fixation","x","y","dispersion","time"]) # rajouter le zoom
            for i in range(len(coord_fixation)):
                writer.writerow(coord_fixation[i])
    else:
        if geolocalisation == False:
            if argument_export_on_resultat == None :

                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["world_index","id_fixation","time","x_rel","y_rel","dispersion"]) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])
            else:
                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    entete = ["world_index","id_fixation","time","x_rel","y_rel","dispersion"]
                    for t in range(len(argument_export_on_resultat)):
                        entete.append(autre[t])
                    writer.writerow(entete) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])

        else:
            if argument_export_on_resultat == None :
                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["world_index","id_fixation","time","x","y","dispersion"]) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])
            else:
                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    entete = ["world_index","id_fixation","time","x","y","dispersion"]
                    for t in range(len(argument_export_on_resultat)):
                        entete.append(autre[t])
                    writer.writerow(entete) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])

            

     

