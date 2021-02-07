# -*- coding: utf-8 -*-
import xlwt
import os


#coding=utf-8

def write(sheetname,data,data2=None,data3=None):

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
            if not isinstance(data[i], (int, str,dict)):
                for j in range(len(data[i])):

                    worksheet.write(i, j, data[i][j])
            else:
                if isinstance(data[i],dict):
                    worksheet.write(i, 0, str(data[i]))
                else:
                    worksheet.write(i, 0, data[i])

    if isinstance(data[0],str):
        lendata=1
    else:
        lendata=len(data[0])

    if data2 is not None:
        if isinstance(data2, dict):
            i = lendata
            for key, value in data2.items():
                i += 1
                worksheet.write(0, i, key)
                worksheet.write(1, i, value)
        else:
            for i in range(len(data2)):
                if not isinstance(data2[i], (int, str)):
                    for j in range(len(data2[i])):

                        worksheet.write(i, j+lendata, data2[i][j])
                else:
                    worksheet.write(i, 0+lendata, data2[i])

    # if isinstance(data2,str):
    #     lendata2=lendata
    # else:
    #     lendata2=len(data2)+len(data)

    lendata2 = len(data2[0]) + len(data[0])
    print(len(data2[0]))
    print(len(data[0]))
    print(lendata2)
    if data3 is not None:
        i = lendata2
        if isinstance(data3, dict):

            for key, value in data3.items():
                i += 1
                worksheet.write(0, i, key)
                worksheet.write(1, i, value)
        else:
            for i in range(len(data3)):
                if not isinstance(data3[i], (int, str,dict)):
                    for j in range(len(data3[i])):

                        worksheet.write(i, j+lendata2, data3[i][j])
                else:
                    worksheet.write(i, 0+lendata2, str(data3[i]))

    path=os.getcwd()+"/ExcelData/"+sheetname+".xls"
    workbook.save(path)

    return worksheet




