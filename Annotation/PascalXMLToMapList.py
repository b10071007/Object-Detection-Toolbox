
import os
#import sys
#import shutil
import xml.dom.minidom

#-----------------------------------------------------------------------------#

# Convert Pascal format(xml) into mapping list(txt)
def PascalXMLToMapList(srcImgPath, srcAnnotPath, outFilePath, strPrefix, img_format):

    outFObj = open(outFilePath, "w")

    # 
    annotList = os.listdir(srcAnnotPath)
    
    totalCnt = len(annotList)
    showProgrsPerBatch = 500
    fileCnt = 0

    for file in annotList:
        
        xmlfName = file
        imgfName = file.replace('xml', img_format)
        
        xmlfNamePath = srcAnnotPath + xmlfName
        jpgfNamePath = srcImgPath + imgfName
        
        strLine = jpgfNamePath 
        
        dom = xml.dom.minidom.parse(xmlfNamePath)  
        root = dom.documentElement
        
        xmin = root.getElementsByTagName('xmin')
        ymin = root.getElementsByTagName('ymin')
        xmax = root.getElementsByTagName('xmax')
        ymax = root.getElementsByTagName('ymax')
        name = root.getElementsByTagName('name')
        
        for i in range(len(xmin)):
            xmin_value = xmin[i].firstChild.data
            ymin_value = ymin[i].firstChild.data
            xmax_value = xmax[i].firstChild.data
            ymax_value = ymax[i].firstChild.data
            name_value = name[i].firstChild.data
            
            boxinfor = xmin_value + "," + ymin_value + "," + xmax_value + "," + ymax_value + "," + name_value
            
            strLine = strLine + " " + boxinfor
            
        strLine = strLine + "\n"
        strLine = strLine.replace("/", "\\")
        
        outFObj.write(strLine)
        fileCnt = fileCnt + 1
        if fileCnt % showProgrsPerBatch == 0:
            print("Done percent = (%d / %d)" % (fileCnt, totalCnt))

    return fileCnt

#-----------------------------------------------------------------------------#

def main():

  rootPath = "D:/Dataset/Detection/Taiwan_coin/"
  strPrefix = ""

  srcImgDirList = [
                    "_Images/",
                    ]

  srcAnnotDirList = [
                    "annotation/",
                    ]
  
  outFileList = [
                "_image_list_All.txt",
                ]
    
  img_format = 'jpg'  

  for srcImgDir, srcAnnotDir, outFile in zip(srcImgDirList, srcAnnotDirList, outFileList):
    
    srcImgPath   = rootPath + srcImgDir 
    srcAnnotPath    = rootPath + srcAnnotDir 
    outFilePath   = rootPath + outFile

    print("Convert into mapping list...\n")
    fileCnt = PascalXMLToMapList(srcImgPath, srcAnnotPath, outFilePath, strPrefix, img_format)
    print("Done!")
    print("Total # of samples = %d\n" % fileCnt)

#-----------------------------------------------------------------------------#

#
# Usage of this program:
#
# python PascalToMapList.py
#
if __name__ == '__main__':
    main()
