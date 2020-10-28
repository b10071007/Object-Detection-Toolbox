#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:44:35 2019

@author: a60508
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from PIL import Image
from PIL import ImageFile
import imghdr
ImageFile.LOAD_TRUNCATED_IMAGES = True

#-----------------------------------------------------------------------------#

def GetFileNameInDir(srcDir):
    if srcDir.find('\\')==-1:
        FName = srcDir.split('/')[-1]
    elif srcDir.find('/')==-1:
        FName = srcDir.split('\\')[-1]
    else:
        raise ValueError('No known seperator string.')
        
    return FName
    

def parse_real_dir(srcImgPath, map_list, img_format):
    map_list_real = []
    for temp_dir in map_list:
        temp_dir = temp_dir.split(img_format)[0] + img_format
        FName = GetFileNameInDir(temp_dir)
        real_dir = os.path.join(srcImgPath, FName)
        map_list_real.append(real_dir)
    return map_list_real
    
#-----------------------------------------------------------------------------#

''' Functions for CreateLinkDir '''

def RemoveNewLineChar(string):
    if string[-1]=='\n':
        string = string[:-1]
    return string

def CreateLinkDir(srcImgPath, out_path_list, dir_map_lists, img_format, removeSpaceInFName):
    
    print("[Create links of images]")
    
    for idx_mlist in range(len(dir_map_lists)):
        srcImgPath_i = srcImgPath[idx_mlist]
        dir_map_list = dir_map_lists[idx_mlist]
        out_path = os.path.join(out_path_list[idx_mlist], "Images")
        
        # Load annotation list.
        fObj = open(dir_map_list, "r")
        map_list = fObj.readlines()
        fObj.close()
        
        map_list_real = parse_real_dir(srcImgPath_i, map_list, img_format)
        data_size = len(map_list)
        
        if not os.path.exists(out_path): os.makedirs(out_path)

        for idx in range(data_size):
            srcDir = map_list_real[idx]
            srcDir = srcDir.replace('\\', '/')
            outDir = os.path.join(out_path, srcDir.split('/')[-1])
            
            srcDir = RemoveNewLineChar(srcDir)
            outDir = RemoveNewLineChar(outDir)
            
            if removeSpaceInFName: 
                srcDir = srcDir.replace(' ', '_')
                outDir = outDir.replace(' ', '_')
            
            if not os.path.isfile(outDir):
                os.symlink(srcDir, outDir)
            
    print("Done.\n")

#-----------------------------------------------------------------------------#

''' Functions for AnnotationsToPascalXML '''
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

#def find_invalid(img_info, box_info):
#    for box in box_info:
#        box = box.split(',')
#        if int(box[0])>img_info['width']: print('box over...')
#        if int(box[2])>img_info['width']: print('box over...')
#        if int(box[1])>img_info['height']: print('box over...')
#        if int(box[3])>img_info['height']: print('box over...')
            
def XML_converter(out_path, img_info, box_info, merge_class, classAddOne):
    
    root = ET.Element('annotation')
    
    ### image information ###
    # folder
    ET.SubElement(root, 'folder').text = img_info['folder']
    # filename
    ET.SubElement(root, 'filename').text = img_info['filename']
    # source
    source = ET.SubElement(root, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'
    # size
    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(img_info['width'])
    ET.SubElement(size, 'height').text = str(img_info['height'])
    ET.SubElement(size, 'depth').text = str(img_info['depth'])
    # segmented
    ET.SubElement(root, 'segmented').text = '0'
    
    ### box information ###
    # object
    for box in box_info:
        if box=='': continue
        if box[-1]=='\n':
            box = box[:-1]
        box = box.split(',')
        obj = ET.SubElement(root, 'object')
        if merge_class:
            ET.SubElement(obj, 'name').text = str(1)
        else:
            ET.SubElement(obj, 'name').text = str(int(box[-1])+classAddOne)
        ET.SubElement(obj, 'pose').text = 'None'
        ET.SubElement(obj, 'truncated').text = '0'
        ET.SubElement(obj, 'difficult').text = '0'
        ET.SubElement(obj, 'occluded').text = '0'
        bndbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = box[0]
        ET.SubElement(bndbox, 'xmax').text = box[2]
        ET.SubElement(bndbox, 'ymin').text = box[1]
        ET.SubElement(bndbox, 'ymax').text = box[3]
        
        # check invalid box
        if int(box[2])>img_info['width']: print('box over...')
        if int(box[3])>img_info['height']: print('box over...')
    
    filename = img_info['filename']
    output_name = filename[:filename.rfind('.')] + '.xml'
    output_file = open( os.path.join(out_path, output_name), 'w' )
    output_file.write( prettify(root))
    output_file.close()

def convert_each(file, srcImgPath, out_path, img_format, 
                 merge_class, classAddOne, removeSpaceInFName):
    # file=map_list[idx]
    if file[-1]=='\n': file = file[:-1]
    completeDir = file.split(img_format)[0] + img_format
    FName = GetFileNameInDir(completeDir)
    
    if removeSpaceInFName:
        FName = FName.replace(" ", "_")
    
    box_info = file.split(img_format)[1].split(" ")
    file_dir = os.path.join(srcImgPath, FName)
        
    if imghdr.what(file_dir) == "png":
        Image.open(file_dir).convert("RGB").save(file_dir)
    
    img = Image.open(file_dir)
    img_info = {'filename' : FName,
                'folder' : out_path,
                'height': img.height,
                'width': img.width,
                'depth': 3}
    
    XML_converter(out_path, img_info, box_info, merge_class, classAddOne)

    
def MapListToPascalXML(srcImgPathList, out_path_list, dir_map_lists, img_format, 
                           merge_class, classAddOne, removeSpaceInFName):

    print('[Parse Annotation]')
    display_iter = 1000
    for idx_mlist in range(len(dir_map_lists)):  
        srcImgPath = srcImgPathList[idx_mlist]
        dir_map_list = dir_map_lists[idx_mlist]
        out_path = os.path.join(out_path_list[idx_mlist], "Annotations")
        
        print('- File list: {}'.format(dir_map_list))
        
        if not os.path.exists(out_path): os.makedirs(out_path)

        # Load annotation list.
        fObj = open(dir_map_list, "r")
        map_list = fObj.readlines()
        fObj.close()
        data_size = len(map_list)
        
        for idx in range(data_size):
            convert_each(map_list[idx], srcImgPath, out_path, img_format, 
                         merge_class, classAddOne, removeSpaceInFName)
            if (idx+1) % display_iter == 0:
                print('converting... [{}/{}]'.format(idx+1, data_size))

            
        print(' converting... [{}/{}]'.format(data_size, data_size))
    print('Done.\n') 
    
#-------------------------------------------------------------------------------------------------#

def main():
    
    rootPath = "D:/Dataset/Detection/Taiwan_coin/"
    
    srcImgPathList = [os.path.join(rootPath, "_Images")] * 3
    
    outPath = os.path.join(rootPath, "Pascal_format")
    img_format=".jpg"
    
    dir_map_lists = [os.path.join(rootPath, "_train_map.txt"),
                     os.path.join(rootPath, "_val_map.txt"),
                     os.path.join(rootPath, "_test_map.txt"),
                     ]
    
    out_path_list = [os.path.join(outPath, "train"),
                     os.path.join(outPath, "val"),
                     os.path.join(outPath, "test"),
                     ]
    
    merge_class = False
    classAddOne = True
    removeSpaceInFName = True

    MapListToPascalXML(srcImgPathList, out_path_list, dir_map_lists, img_format, merge_class, 
                       classAddOne, removeSpaceInFName) 

#-------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    print("")
    main()

    
    
