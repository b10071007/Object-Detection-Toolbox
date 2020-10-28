#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from random import shuffle

def shuffle_Flist(Flist):
    shuffle(Flist)
    shuffle(Flist)
    shuffle(Flist)

def SplitMapListIntoPartition(rootPath, srcMapList, partitions, fileDir):

    print('Split dataset partition...')
    num_partition = len(partitions)
    if len(fileDir)!= num_partition:
        raise ValueError('The number of partition cannot match the name of partition.')
    if np.sum(partitions) != 1:
        raise ValueError('The sum of proportion is not equal to 1.')

    srcFObj = open(srcMapList, "r")
    srcFList = srcFObj.readlines()
    srcFObj.close()

    shuffle_Flist(srcFList)
    srcFList = np.array(srcFList)

    num_file = len(srcFList)
    cumsum = np.round(np.cumsum([0] + partitions), 2)
    intervals = (cumsum * num_file).astype(int)
    
    # Copy the top # of files as test files.
    for i in range(num_partition):
        print(' - File: {}'.format(fileDir[i]))
        destFObj = open(fileDir[i], "w")
        fList_part = srcFList[intervals[i]:intervals[i+1]]
        for line in fList_part:
            destFObj.write(line)
        destFObj.close()

def main():
    rootPath =  "D:/Dataset/Detection/Taiwan_coin/"
    srcMapList = rootPath + "_image_list_All.txt"
    partitions = [0.7, 0.1, 0.2]
    name = ["train", "val", "test"]
    fileDir = [os.path.join(rootPath, '_{}_map.txt'.format(elem)) for elem in name]
    
    SplitMapListIntoPartition(rootPath, srcMapList, partitions, fileDir)
    
#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    main()