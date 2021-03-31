# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 14:42:41 2021

@author: Ying Zhang
"""
'''
this script is used for voxelize the stl file by using the function from trimesh.
after the voxelization, the data will be stored in the .vxc file format which will
be sent to be labelled.
'''
import trimesh

import numpy as np
import os
from lxml import etree
import pandas as pd

myPath = "STLs/"
myFiles = os.listdir(myPath)
scale_lst =[]
for file in myFiles:
    filename = myPath + file

    mesh = trimesh.load(filename) #binvox_files/fail/stl/252784x10
    
    #voxelized_mesh = trimesh.load('213889.binvox')
    scale = np.max(mesh.extents)
    scale_lst.append([os.path.splitext(file)[0], scale])
    
    voxelized_mesh = mesh.voxelized(scale/128)
    v = voxelized_mesh.copy().fill()
    #voxel1 = voxelized_mesh.matrix 
    voxel1 = v.matrix
    voxel2 = np.zeros((129,129,129))
    voxel2[:voxel1.shape[0],:voxel1.shape[1],:voxel1.shape[2]] = voxel1
    voxel2 = voxel2[:-1, :-1, :-1]
    voxel3 = voxel2.astype('uint8')
    vox = voxel3.T.reshape(128,-1)
    
    

    np.set_printoptions(threshold=np.inf)
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse('template.xml',parser)
    root = tree.getroot()
    
    print(root.tag)
    old_data = tree.xpath('/VXC/Structure/Data')
    print(old_data[0].tag)
    old_data[0].text=None
    for line in vox:
        string = np.array2string(line,max_line_width = np.inf)
        string = string.replace(" ","")
        string = string.replace("[","")
        string = string.replace("]","")
        elem = etree.SubElement(old_data[0],'Layer')
        elem.text = etree.CDATA(string)
     
    #tree = etree.ElementTree(Data)
    out_filename = os.path.splitext(file)[0] + '.vxc'
    tree.write(out_filename, pretty_print=True, xml_declaration=True,   encoding="utf-8")


dataset_pre =pd.DataFrame(scale_lst,columns = ['FileID','scale'])
if os.path.isfile('FDM_scale_v1.pickle'):
    exist_data = pd.read_pickle('FDM_scale_v1.pickle')
    dataset = exist_data.append(dataset_pre,ignore_index=True, verify_integrity = True)
else:
    dataset = dataset_pre
dataset.to_pickle('FDM_scale_v1.pickle')




