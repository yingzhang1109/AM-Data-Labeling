# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 10:48:56 2021

@author: Ying Zhang
"""
import os
import numpy as np
import pandas as pd
from lxml import etree

data_excel = pd.read_excel('FDM_DATA.xlsx')
data_scale = pd.read_pickle('FDM_scale_v1.pickle')
data_pre = data_excel.merge(data_scale, how ='left', on = 'FileID')

myPath = "vxc_files"
myFiles = os.listdir(myPath)
lst =[]
for file in myFiles:
    filename = 'vxc_files/' + file 
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(filename,parser)
    root = tree.getroot()

    alldata = root.findall("Structure/Data/Layer")
    matrix = []
    for data in alldata:
        for num in data.text:
            matrix.append(int(num))

    matrix =np.array(matrix)
    final = np.resize(matrix,(128,128,128))
    final = np.transpose(final,(2,1,0))
    stl_file = file.replace(".vxc","")
    lst.append([stl_file, final])



data_stl=pd.DataFrame(lst,columns = ['FileID', 'stl'])
dataset = data_pre.merge(data_stl, how='left', on = 'FileID')
dataset.to_pickle('FDM_v1.pickle')
