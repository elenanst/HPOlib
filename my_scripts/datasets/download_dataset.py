## Downloads all repositories specified in file repos

import os
import csv
import shutil
datasets_dir = "/home/elena/R_ws/automl/ADS_workspace/datasets_repo"
current_dir = os.path.dirname(os.path.realpath(__file__))
#download file .data from repository
file = open("repos.txt", "r")
lines = file.readlines()
lines = [line.strip() for line in lines]

folderName=""
fileName=""
changedDIR=0
for line in lines:
    if line.startswith("/"):
        if changedDIR!=0:
            os.chdir("../")
        folderName=line
        try:
            os.mkdir(folderName.split('/')[-1])
        except:
            print("dir exists")
        changedDIR=1
        os.chdir(folderName.split('/')[-1])
    else:
        fileName = line
    if  fileName:
        os.popen('wget -c http://archive.ics.uci.edu'+ folderName + "/" + fileName)
        print folderName
        start = folderName.rindex('/') + len('/')
        folderName_temp = folderName[start:]
        data_file = current_dir +"/" + folderName_temp + "/" + fileName
        print data_file
        print fileName
        try:
            end = fileName.index(".data")
            fileName = fileName[:end]
            fileNameCsv = fileName + ".csv"
            data_file_csv = datasets_dir + '/' + fileNameCsv
            print data_file
            print data_file_csv
            os.rename(data_file, data_file_csv)
        except ValueError:
            print 's'
