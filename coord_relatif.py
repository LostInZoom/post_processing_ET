import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import json





def calcul_box_map(xmin,xmax,ymin,ymax,shape_screen):
    return([xmin/shape_screen[0],ymin/shape_screen[1],xmax/shape_screen[0],ymax/shape_screen[1]]) # a calculer en pourcentage (xmin,ymin,xmax,ymax)

def calcul_pos_relative(box_map,x_pos,y_pos):
    if x_pos > box_map[0] and x_pos[k] < box_map[2]:   
        if y_pos > box_map[1] and y_pos < box_map[3]:
            x_relatif = (x_pos-box_map[0])/(box_map[2]-box_map[0])
            y_relatif = (y_pos-box_map[1])/(box_map[3]-box_map[1])
            return x_relatif,y_relatif
        else:
            return False
    else:
        return False
    
def state_screen(timestamp,result,offset,geolocalisation=False,export_argument=False):
    time= 0

    if geolocalisation == False:
        for t in range(len(result)):
            other =[]
            if (timestamp+offset)*1000 >= result["time"][t]:
                if export_argument != False:
                    for k in range(export_argument):
                        other.append(result[export_argument[k][t]])
    
                time = result["time"][t]
                continue
            else:
                break
        return time,other
 
    else:
        box = [0,0,0,0]
        time =0
        for t in range(len(result)):
            other =[]
            if (timestamp+offset)*1000 >= result["time"][t]:
                box = [float(result["xmin"][t]),float(result["ymin"][t]),float(result["xmax"][t]),float(result["ymax"][t])]
                time = result["time"][t]
                if export_argument != False:
                    for k in range(export_argument):
                        other.append(result[export_argument[k][t]])
                continue
            else:
                break
    
        return box,time,other
  

def calcul_loc(x_rel,y_rel,coord_carte):
    x_coord = coord_carte[0] + x_rel*(coord_carte[2]-coord_carte[0] )
    y_coord = coord_carte[1] + y_rel*(coord_carte[3]-coord_carte[1] )
    return [x_coord,y_coord] 


def et_to_fixation(path_to_fixation,box_map,path_info,path_to_result=None,geolocalisation=False,export_argument_on_result=False,name_export='coord_fixation_on_map.csv'):

    try :
        f = open(path_info,)
    except:
        print("Failed to load json")
    try :
        fixation = pd.read_csv(path_to_fixation)
    except:
        print("Failed to load fixation")  
    
    if "norm_pos_x" and "norm_pos_y" and "world_timestamp" and "fixation_id" and "world_index" and "dispersion" not in fixation.columns:
        raise KeyError("wrong format of the fixation file")


    json_time = json.load(f)
    start_time_system = float(json_time["start_time_system_s"]) # System Time at recording start
    start_time_synced = float(json_time["start_time_synced_s"])
    offset = start_time_system - start_time_synced 

    if path_to_result != None:
        assert os.path.exists(path_to_result)
        result = pd.read_csv(path_to_result) 
        if export_argument_on_result != False :
            for i in range(len(export_argument_on_result)):
                if export_argument_on_result[i] not in fixation.columns:
                    raise KeyError("the argument"+ export_argument_on_result[i]+" is not in the result file")  
    if geolocalisation == True :
        if "xmin" and "ymin" and "xmax" and "ymax" not in fixation.columns:
            raise KeyError("error data")
    coord_fixation = []
    for k in range(len(fixation)):
        id = fixation["fixation_id"][k]
        world_index = fixation["world_index"][k]
        dispersion = fixation["dispersion"][k]
        x_rel,y_rel = calcul_pos_relative(box_map,fixation["norm_pos_x"][k],fixation["norm_pos_y"][k])
        if x_rel != False:
            if path_to_result == None:
                coord_fixation.append([world_index,id,x_rel,y_rel,dispersion,(fixation["world_timestamp"][k]+offset)*1000])
            else:
                if geolocalisation == False:
                    time,other =  state_screen(fixation["world_timestamp"][k],result,offset,export_argument=export_argument_on_result)
                    list = [world_index,id,time,x_rel,y_rel,dispersion]
                    if export_argument_on_result != False:
                        for t in range(len(other)):
                            list.append(other[t])
                    coord_fixation.append([list])

                else:
                    box,time,other = state_screen(fixation["world_timestamp"][k],result,offset,geolocalisation=geolocalisation,export_argument=export_argument_on_result)
                    x_loc,y_loc =calcul_loc(x_rel,y_rel,box)
                    list = [world_index,id,time,x_loc,y_loc,dispersion]
                    if export_argument_on_result != False:
                        for t in range(len(other)):
                            list.append(other[t])
                    coord_fixation.append([list])

    if path_to_result == None:
        with open(name_export, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["world_index","id_fixation","x","y","dispersion","time"]) # rajouter le zoom
            for i in range(len(coord_fixation)):
                writer.writerow(coord_fixation[i])
    else:
        if geolocalisation == False:
            if export_argument_on_result == None :

                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["world_index","id_fixation","time","x_rel","y_rel","dispersion"]) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])
            else:
                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    entete = ["world_index","id_fixation","time","x_rel","y_rel","dispersion"]
                    for t in range(len(export_argument_on_result)):
                        entete.append(other[t])
                    writer.writerow(entete) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])

        else:
            if export_argument_on_result == None :
                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["world_index","id_fixation","time","x","y","dispersion"]) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])
            else:
                with open(name_export, 'w', newline='') as file:
                    writer = csv.writer(file)
                    entete = ["world_index","id_fixation","time","x","y","dispersion"]
                    for t in range(len(export_argument_on_result)):
                        entete.append(other[t])
                    writer.writerow(entete) # rajouter le zoom
                    for i in range(len(coord_fixation)):
                        writer.writerow(coord_fixation[i])

            

     

