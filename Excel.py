# -*- coding: utf-8 -*-
import xlwt
import xlrd
from collections import OrderedDict
#coding=utf-8

def write(data,sheetname):
    workbook=xlwt.Workbook()
    worksheet=workbook.add_sheet(sheetname)

    if isinstance(data,dict):
        i=0
        for key,value in data.items():
            i+=1
            worksheet.write(i,0,key)
            worksheet.write(i,1,value)
    else:
        for i in range(len(data)):
            if not isinstance(data[i], (int, str)):
                for j in range(len(data[i])):
                    worksheet.write(i, j, data[i][j])
            else:
                worksheet.write(i, 0, data[i])


    path="F://"+sheetname+".xls"
    workbook.save(path)


    return worksheet



