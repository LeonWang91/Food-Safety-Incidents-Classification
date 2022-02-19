

# -*- coding: utf-8 -*-
# @Time    : 2020/7/24 0024 16:35
# @Author  : Wang
# @FileName: baseio.py
# @Software: PyCharm

import os
import xlrd
import codecs

#################################################################遍历文件夹
def fun_files(path):
    fileArray = []      #建立列表储存各个文件fn #os_walk()该函数遍历根目录top，并递归地返回一个三元组：（root,dirs,files）
    for root, dirs, files in os.walk(path):     #root为根目录路径，dirs为root路径下的目录列表，files为root路径下的文件列表。
        for fn in files:
            eachpath = str(root + '\\' + fn)
            fileArray.append(eachpath)
    # print(fileArray)
    return fileArray

def fun_dirs(path):      #path = r'C:\Users\PC\Desktop\748学社任务\python任务\任务五\语料库' --->文件夹的路径
    dirArray = []      #建立列表储存各个文件fn #os_walk()该函数遍历根目录top，并递归地返回一个三元组：（root,dirs,files）
    for root, dirs, files in os.walk(path):     #root为根目录路径，dirs为root路径下的目录列表，files为root路径下的文件列表。
        for dir in dirs:
            eachpath = str(root + '\\' + dir)
            dirArray.append(eachpath)
            # print(os.path.basename(eachpath))
    # print(dirArray)
    return dirArray

################################################################ excel
# 按行读excel文件 自定义返回表格内容
def readexcel(excelPath, sheetId = 0):
     result = []
     data = xlrd.open_workbook(excelPath)
     table = data.sheet_by_index(sheetId)
     nrows = table.nrows
     # ncols = table.ncols
     # 从第二行开始读取
     for i in range(1, nrows):
         row = str(table.row_values(i)[5][0]) + '\t' + str(table.row_values(i)[6])
         result.append(row)
     return result

#按列读excel文件
def readxls(path, colnum):#path = r'E:\wanglei_hello\new work\words.xlsx'/path = r'E:\wanglei_hello\new work\stopwords.xlsx'
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0]#0表示读取第一个sheet
    data = list(sheet.col_values(colnum)[1::])#col_values(colnum)表示按照这一列中的所有单元格遍历读取
    # print(data)
    return data  #分别读取的匹配词表

################################################################ txt
#读取文本,返回字符串
def read_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore')as f_txt:
        lines = f_txt.read()
    #print(lines)
    return (lines)

#读txt文件 一次全读完 返回list 去换行
def readtxt_list_all_strip(path):
    lines = []
    with codecs.open(path,'r','utf-8') as r:
        # print(len(r.readlines()))
        for line in r.readlines():
            # strip() 方法用于移除字符串头尾指定的字符(默认为空格或换行符)或字符序列。
            line = line.strip()
            line = line.strip('\n').strip("\r")
            lines.append(line)
        # print(type(lines))
        # print(len(lines))
        return lines

#写txt文件覆盖
def writetxt_w(txt,path):
    with codecs.open(path,'w','utf-8') as w:
        w.writelines(txt)

#写txt文件追加
def writetxt_a(txt,path):
    with codecs.open(path,'a','utf-8') as w:
        w.write(txt)


# 写list 追加
def writetxt_a_list(list, path):
    with codecs.open(path, 'a', "utf-8") as w:
        for i in range(len(list)):
            # print(i)
            w.write(list[i] + "\t")
        w.write("\n")
        # w.write("\n") ##### 会导致最后一行为空，读取后split会报错