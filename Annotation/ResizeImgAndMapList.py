# -*- coding: utf-8 -*-

import os
import cv2
from PIL import Image

def ResizeImageAndAnnotation(srcAnnotPath, destAnnotPath, srcImgDir, destImgDir, new_size, bool_resizeAnnot, bool_resizeImg):

    display_interval = 100
        
    with open(srcAnnotPath, 'r') as fObj:
        fList = fObj.readlines()
        num_file = len(fList)

    if bool_resizeAnnot:
        os.makedirs(os.path.split(destAnnotPath)[0], exist_ok = True)
        fObj = open(destAnnotPath, 'w')

    for idx, file in enumerate(fList):

        if idx % display_interval == 0:
            print("Process: [{}/{}]".format(idx, num_file))

        if file[-1]=='\n': file = file[:-1]
        if file[-1]==' ': file = file[:-1]
        
        file_split = file.split(' ')
        fName_complete = file_split[0]
        # fName_complete = fName_complete.replace("\\", "/")
        fName = os.path.split(fName_complete)[-1]
        boxs = file_split[1:]

        srcImgPath = os.path.join(srcImgDir, fName)
        img = Image.open(srcImgPath)

        # Resize Annotation
        if bool_resizeAnnot:
            orig_size = img.size
            ratio = [int(new)/int(orig) for new, orig in zip(new_size, orig_size)]
            
            new_box = ''
            for box in boxs:
                x_min, y_min, x_max, y_max, label = box.split(',')
                x_min = round(int(x_min)*ratio[0])
                y_min = round(int(y_min)*ratio[1])
                x_max = round(int(x_max)*ratio[0])
                y_max = round(int(y_max)*ratio[1])
                
                x_min = max(1, x_min)
                y_min = max(1, y_min)
                x_max = min(new_size[0]-1, x_max)
                y_max = min(new_size[1]-1, y_max)
                
                new_box += " {},{},{},{},{}".format(x_min, y_min, x_max, y_max, label)
            new_box += '\n'  
            fObj.write(fName + new_box)

        # Resize Image
        if bool_resizeImg:
            if not os.path.exists(destImgDir): os.makedirs(destImgDir)
            destImgPath = os.path.join(destImgDir, fName)
            
            if os.path.isfile(srcImgPath):
                img_resize = img.resize(new_size, Image.BILINEAR)
                img_resize.save(destImgPath)

                # img = cv2.imread(srcImgPath)
                # new_img = cv2.resize(img, new_size)
                # cv2.imwrite(destImgPath, new_img)
            else:
                raise OSError("Not found file: \"{}\"".format(srcImgPath))
    
    print("Process: [{}/{}]".format(num_file, num_file))

    if bool_resizeAnnot:
        fObj.close()

#-----------------------------------------------------------------------------#          

def main():
    
    rootPath = "D:/Dataset/Detection/Taiwan_coin/"

    srcAnnotPathList = [rootPath + "_train_map.txt",
                        rootPath + "_val_map.txt",
                        rootPath + "_test_map.txt",
                        ]
    destAnnotPathList = [rootPath + "_train_map_512x512.txt",
                         rootPath + "_val_map_512x512.txt",
                         rootPath + "_test_map_512x512.txt",
                         ]
    
    srcImgDirs = [rootPath + "_Images/"] * 3
    destImgDirs = [rootPath + "_Images_512x512/"] * 3

    new_size = (512, 512)

    bool_resizeAnnot = True
    bool_resizeImg = True
    
    print("[Resize Image and Annotations]")
    for srcAnnotPath, destAnnotPath, srcImgDir, destImgDir in zip(srcAnnotPathList, destAnnotPathList, srcImgDirs, destImgDirs):
        if bool_resizeAnnot:
            print(" - Reize Annotation from \"{}\" to \"{}\"".format(srcAnnotPath, destAnnotPath))
        if bool_resizeImg:
            print(" - Reize Images from \"{}\" to \"{}\"".format(srcImgDir, destImgDir))
        ResizeImageAndAnnotation(srcAnnotPath, destAnnotPath, srcImgDir, destImgDir, new_size, bool_resizeAnnot, bool_resizeImg)
    
#-----------------------------------------------------------------------------#

if __name__ == "__main__":
    main()