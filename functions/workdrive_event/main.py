import logging
import zcatalyst_sdk
import requests

WORKDRIVE_FOLDERID = "87wwh345f66cdec2641aa8b978130eedc1405"
logger = logging.getLogger()
def handler(event, context):
    try:
        app = zcatalyst_sdk.initialize()
        Zcql = app.zcql()
        Datastore = app.datastore()
        event_data = event.get_data()
        filestore_service = app.filestore()
        folder_service = filestore_service.folder(event_data['folder_details']) 
        FileBuffer = (folder_service.download_file(event_data['id']))
        response = uploadFiletoWorkdrive(FileBuffer,event_data)
        
        if(response.status_code == 200):
            res = response.json()
            array = res['data']
            data = array[0]
            attributes = data['attributes']
            resourceId = attributes['resource_id']
            logger.info(resourceId)
            query = f'Select ROWID from WorkDriveFileID where FileID={event_data["id"]}'
            rowList = Zcql.execute_query(query)
            ROWID = [sub['WorkDriveFileID']['ROWID'] for sub in rowList]
            table = Datastore.table(2113000000017088)
            rows = {}
            rows['WorkDriveFileID'] = resourceId
            rows['WorkDriveSync'] = 'Completed'
            rows['ROWID'] = ROWID[0]
            table.update_row(rows)
            context.close_with_success()
        else:
            logger.error("WorkDrive API Exception")
            context.close_with_failure()
    except Exception as err:
        logger.error(f'Exception in WDSync Function:{err}')
        context.close_with_failure()

def getAccessToken():
    app = zcatalyst_sdk.initialize()
    args = {}
    args["client_id"] = '1000.EUR4TXMKTUOTJTEMZI3CQU6PARMB8G'
    args["client_secret"] = 'b69d7e2d67ec8090d051e4e3ed48100636e0dab131'
    args["auth_url"] = 'https://accounts.zoho.com/oauth/v2/token'
    args["refresh_url"] = 'https://accounts.zoho.com/oauth/v2/token'
    args["refresh_token"] = '1000.9fdcabf9246ed16bdec003bb9150086d.71c2cad3420923b7c57221583684c80f'
    connector_service = app.connection({'C1':args})
    access_token = connector_service.get_connector('C1').get_access_token()
    return str(access_token)

def uploadFiletoWorkdrive(filebuffer,eventdata):
    accesstoken = getAccessToken()
    params = {
        'filename':f"{eventdata['file_name']}",
        'override-name-exist':'true',
        'parent_id':f"{WORKDRIVE_FOLDERID}"
    }
    url = 'https://workdrive.zoho.com/api/v1/upload'
    headers = {
        'Authorization':f'Zoho-oauthtoken {accesstoken}'
    }
    files=[('',(f'{eventdata["file_name"]}',filebuffer))]
    response = requests.post(url=url,params=params,headers=headers,files=files)
    return response



    