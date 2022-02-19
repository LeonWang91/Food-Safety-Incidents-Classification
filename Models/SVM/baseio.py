import codecs
import os
import json
# import xlrd
# import xlsxwriter
# import time

############################################################################   excel
#
#
# def writeexcel(data, excelPath, sheen = 0):
#     start_time = time.time()
#     file = xlsxwriter.Workbook(excelPath)
#     sheet1 = file.add_worksheet("sheet1")
#     for i in range(len(data)):
#         for j in range(len(data[0])):
#             sheet1.write(i,j,data[i][j])
#     file.close()
#     end_time = time.time()
#     print("write into excel use time: " + str(end_time - start_time) + "s")
#
# #list按行写入
# def writeexcelrow(data, rowline, excelPath, sheetname):
#     file = xlsxwriter.Workbook(excelPath)
#     sheet1 = file.add_worksheet(sheetname)
#     sheet1.write_row(rowline, 0, data)
#     file.close()
#
#
# # 读excel文件 返回整个表格内容
# def readexcel(excelPath, sheetId = 0, startline = 0):
#     result = []
#     data = xlrd.open_workbook(excelPath)
#     table = data.sheet_by_index(sheetId)
#     nrows = table.nrows
#     ncols = table.ncols
#     for i in range(0, nrows):
#         row = table.row_values(i)
#         result.append(row)
#     return result
#
#
# # 读excel文件指定列
# def readexcelcol(excelPath,sheetID = 0 ,colu = 0):
#     result = []
#     data = xlrd.open_workbook(excelPath)
#     table = data.sheet_by_index(sheetID)
#     result = table.col_values(colu)
#     return result
#
# # 指定行
# def readexcelrow(excelPath,sheetID = 0 ,row = 0):
#     result = []
#     data = xlrd.open_workbook(excelPath)
#     table = data.sheet_by_index(sheetID)
#     result = table.row_values(row)
#     return result

############################################################################   txt

#读txt文件 一次全读完 返回list 去换行
def readtxt_list_all_strip(path):
    lines = []
    with codecs.open(path,'r','utf-8') as r:
        for line in r.readlines():
            line = line.strip('\n').strip("\r")
            lines.append(line)
        return lines

# 读txt 一次读一行 最后返回list
def readtxt_list_each(path):
    lines = []
    with codecs.open(path,'r','utf-8') as r:
        line = r.readline()
        while line:
            lines.append(line)
            line = r.readline()
    return lines


# 读txt 一次读一行 最后返回list 去换行
def readtxt_list_each_strip(path):
    lines = []
    with codecs.open(path,'r','utf-8') as r:
        line = r.readline()
        while line:
            lines.append(line.strip("\n").strip("\r"))
            line = r.readline()
    return lines


#读txt文件 一次全读完 返回list
def readtxt_list_all(path):
    with codecs.open(path,'r','utf-8') as r:
        lines = r.readlines()
        return lines


#读txt文件 读成一条string
def readtxt_string(path):
    with codecs.open(path,'r','utf-8') as r:
        lines = r.read()
        return lines


#写txt文件覆盖
def writetxt_w(txt,path):
    with codecs.open(path,'w','utf-8') as w:
        w.writelines(txt)


#写txt文件追加
def writetxt_a(txt,path):
    with codecs.open(path,'a','utf-8') as w:
        w.writelines(txt)

def writetxt(txt, path):
    with codecs.open(path, 'a', "utf-8") as w:
        w.write(txt)

# 写list 追加
def writetxt_a_list(list, path):
    with codecs.open(path, 'a', "utf-8") as w:
        for i in list:
            w.write(i)
        w.write("\n")

# 写二维list 追加
def writetxt_a_2list(list, path):
    with codecs.open(path, 'a', "utf-8") as w:
        for i in list:
            for j in i:
                w.write(j)
            w.write("\n")


######################################################################################
#统计词频
def calc_word_count(list_word, path):
    word_count = {}
    for key in list_word:
        if key not in word_count:
            word_count[key] = 1
        else:
            word_count[key] += 1
    word_dict_sort = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    for key in word_dict_sort:
        writetxt_a(key[0] + '\t' + str(key[1]) + '\n',path)

# 合并文件
def imgrate_files(path):
    filenames = os.listdir(path)
    return None



def SaveToJson(content, path):
    with codecs.open(path, "w", "utf-8") as w:
        json.dump(content, w)

def LoadFromJson(path):
    with codecs.open(path, "r", "utf-8") as r:
        content = json.load(r)
        return content

#读txt文件 读成一条string if gb2312
def readtxt_string_all_encoding(path):
        try:
            with codecs.open(path,'r', "utf-8-sig") as r:
                lines = r.read()
                return lines
        except:
            with codecs.open(path,'rb', "gb2312") as r:
                lines = r.read()
                return lines