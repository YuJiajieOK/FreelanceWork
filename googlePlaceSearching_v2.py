from xlrd import open_workbook
# from googleplaces import GooglePlaces, types, lang
import requests
import xlsxwriter
import json


outputImageFolder = "D:\\copy\\jobs\\images2\\"#This is the directory for final images

heading = "225"#Horizontal angle
pitch="-0.76"#Vertical angle
zoom = "20"#Zooming


MY_API_KEY = 'AIzaSyBuIKILnkgDwaQ3VmBQg49oankyqu-4j-c'

addressFile = open_workbook('mailtest.xlsx') # The file with addresses for searching

def readXlsx(addressFile):# This function is loading address into an array
    for s in addressFile.sheets():
        addresses = []*s.nrows
        for row in range(0,s.nrows):
            col_value = []
            for col in range(s.ncols):
                 value  = (s.cell(row,col).value)
                 try : value = str(value)
                 except : pass
                 col_value.append(value)
            addresses.append(col_value)
    return addresses

addresses = readXlsx(addressFile)

for i in range(1,len(addresses)):
    loc = addresses[i][3]
    queryText = addresses[i][2]
    name = addresses[i][0]+addresses[i][1]
    varifyUrl = 'https://maps.googleapis.com/maps/api/streetview/metadata?size=600x300&location='+ queryText + ',' + loc + '&heading='+heading+'&pitch='+pitch+'&key=' + MY_API_KEY

    respVariry = requests.get(varifyUrl, stream=True)

    json_content = (respVariry.content.decode('utf8').replace("'", '"'))#converting byte to json
    data_content = json.loads(json_content)

    if data_content['status'] == 'ZERO_RESULTS': #varify if there is a street view or not. This is no street view
       urlSatellite = 'https://maps.googleapis.com/maps/api/staticmap?center='+ queryText + loc+'&zoom='+zoom+'&size=400x400&maptype=satellite& key='+ MY_API_KEY
       responseSatellite = requests.get(urlSatellite, stream=True)
       with open(outputImageFolder+queryText + '.jpg', 'wb') as handler:
           handler.write(responseSatellite.content)
       addresses[i][6] = outputImageFolder + queryText + '.jpg'

    elif data_content['status'] =='OK':
        urlStreet = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=' + queryText + ',' + loc + '&heading=' + heading + '&pitch=' + pitch + '&key=' + MY_API_KEY
        response = requests.get(urlStreet, stream=True)
        with open(outputImageFolder+queryText + '.jpg', 'wb') as handler:
            handler.write(response.content)
        addresses[i][6] = outputImageFolder + queryText + '.jpg'
    else:
        urlSatellite = 'https://maps.googleapis.com/maps/api/staticmap?center=' + queryText + loc + '&zoom=' + zoom + '&size=400x400&maptype=satellite&key=' + MY_API_KEY
        responseSatellite = requests.get(urlSatellite, stream=True)
        with open(outputImageFolder+queryText + '.jpg', 'wb') as handler:
            handler.write(responseSatellite.content)
        addresses[i][6] = outputImageFolder + queryText + '.jpg'

workbook = xlsxwriter.Workbook('Searched.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(addresses):
    worksheet.write_row(col, row, data)
workbook.close()








