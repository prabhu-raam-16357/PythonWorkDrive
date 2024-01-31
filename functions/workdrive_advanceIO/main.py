import json
import zcatalyst_sdk
import logging
import os
import requests
from flask import Request, make_response, jsonify

GET = "GET"
DELETE = "DELETE"
WORKDRIVEFILEID = "WorkDriveFileID"
FOLDER_ID =  2113000000017851
TABLE_ID = 2113000000017088
logger = logging.getLogger()
def handler(request: Request):
    app = zcatalyst_sdk.initialize()
    if request.path == "/files" and request.method == 'POST':
        filestore = app.filestore()
        file = request.files['file']
        file.save(os.path.join('/tmp/',file.filename))
        filepath = open(os.path.join(f"/tmp/{file.filename}"),'rb')
        response1 = filestore.folder(FOLDER_ID).upload_file(name=file.filename,file=filepath)
        response = make_response(jsonify({
            'message': response1
        }), 200)
        return response
    
    elif request.path == '/getFiles' and request.method == GET:
        print(app.authentication().get_current_user())
        zcql = app.zcql()
        query = 'SELECT * FROM WorkDriveFileID limit 1,100'
        rowlist = zcql.execute_query(query)
        workdrive = [sub[WORKDRIVEFILEID] for sub in rowlist ]
        response = make_response(workdrive, 200)
        return response 

    elif request.path == f'/deleteFile' and request.method == DELETE:
        fileid = request.args['fileID']
        zcql = app.zcql()
        datastore = app.datastore().table(TABLE_ID)
        filestore = app.filestore().folder(FOLDER_ID)
        query = f'SELECT * FROM WorkDriveFileID where FileID={fileid}'
        rowlist = zcql.execute_query(query)
        workdrive = [sub[WORKDRIVEFILEID] for sub in rowlist]
        rowids = [sub['ROWID'] for sub in workdrive]
        response1 = deleteWorkdriveFile(workdrive[0]['WorkDriveFileID'])

        if response1.status_code == 200:
            filestore.delete_file(fileid)
            ROWID = rowids[0]
            datastore.delete_row(ROWID)
            response = make_response({
                "message":"Deleted Successfully"
            },200)
        else:
            response = make_response({
                "message":"Workdrive API Error"
            },200)
        
        return response


def getAccessToken():
    app = zcatalyst_sdk.initialize()
    print(app.authentication().get_current_user())
    args = {}
    args["client_id"] = '1000.EUR4TXMKTUOTJTEMZI3CQU6PARMB8G'
    args["client_secret"] = 'b69d7e2d67ec8090d051e4e3ed48100636e0dab131'
    args["auth_url"] = 'https://accounts.zoho.com/oauth/v2/token'
    args["refresh_url"] = 'https://accounts.zoho.com/oauth/v2/token'
    args["refresh_token"] = '1000.9fdcabf9246ed16bdec003bb9150086d.71c2cad3420923b7c57221583684c80f'
    connector_service = app.connection({'C1':args})
    access_token = connector_service.get_connector('C1').get_access_token()
    return str(access_token)

def deleteWorkdriveFile(workdDrive_fileid):
    accestoken = getAccessToken()
    url = f'https://www.zohoapis.com/workdrive/api/v1/files/{workdDrive_fileid}'
    data = {}
    attributes = {}
    headers = {}
    attributes['status'] = '51'
    data['attributes'] = attributes
    data['type'] = 'files'
    jsondata = {}
    jsondata['data'] = data
    headers['Authorization'] = f'Zoho-oauthtoken {accestoken}'
    headers['Accept'] = 'application/vnd.api+json'
    response = requests.patch(url=url,headers=headers,json=jsondata)
    return response

