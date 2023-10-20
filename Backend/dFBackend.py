from base64 import decode
from datetime import timedelta, datetime
from operator import itemgetter
import sys

from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
# import ldap
# import requests

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import decode_token
import requests
from configBackend import *

import numpy as np
import pandas as pd
import psycopg2
import json
import jwt
from flask_cors import CORS



import datetime
from datetime import timedelta, datetime

# APIs

conn.autocommit = True
cursor = conn.cursor()




from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

# app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/api/login", methods=["POST"])
def login():
    try:

        username=request.get_json()['username']
        password=request.get_json()['password']

        # print(username, password)


        e_name = ''

        role = ''

        state_name = ''

        state_id = ''



        
        cursor.execute("select username, password_hash, user_role, state_name, state_id from states where username= '{0}'".format(username))
        login_data = cursor.fetchall()

        if len(login_data) > 0:
            e_name = login_data[0][0]
            enc_password = login_data[0][1]
            role = login_data[0][2]
            state_name = login_data[0][3]
            state_id = login_data[0][4]
            status=bcrypt.check_password_hash(enc_password, password)
            if not status:
                return jsonify(error="Entered Password is Incorrect, Please try again!", data="Entered Password is Incorrect!", status="failure")
        
        else:
            return jsonify(error="Invalid Credentials!", data="Entered Password is Incorrect!", status="failure")

        
        jwt_data = {"sub": username, "exp": datetime.utcnow() + app.config.get('JWT_ACCESS_TOKEN_EXPIRES'), "role": role}
        access_token = jwt.encode(payload=jwt_data, key=app.config.get('JWT_SECRET_KEY'), algorithm=app.config.get('ALGORITHM'))
        # return encoded_jwt

        # print(access_token)



        # access_token = create_access_token(identity=username)
        # refresh_token = create_refresh_token(identity=username)
        # print()
        
        # print(x['sub'])

        # x = decode_token(access_token, csrf_value=None, allow_expired=False)

        decoded_data = jwt.decode(jwt=access_token,
                              key=app.config.get('JWT_SECRET_KEY'),
                              algorithms=[app.config.get('ALGORITHM')])

        # print(decoded_data['sub'])

        return jsonify(token=access_token, user=decoded_data['sub'], username=state_name, role=role, status="success", state_id=state_id)

    except Exception as e:
        print("Error", e)
        # print(e)
        return jsonify(error="Problem in logging in, Please contact SRLDC IT!", status="failure")






@app.route('/api/fetchrevisions', methods=['POST'])
def fetchRevisions():
    params = request.get_json()
    date = params["date"]
    params["date"] = date
    cursor.execute("select revision_no from file_uploads where state_id = {0} and upload_date = to_date('{1}', 'DD/MM/YYYY')".format(params["state"], params["date"]))
    revisions_data = cursor.fetchall()
    revision_list = [i[0] for i in revisions_data]

    if len(revision_list) > 0:
        return jsonify(status="success", message="Fetched Successfully for {0}".format(date), revisions=revision_list)
    else:
        return jsonify(status="failure", message="There are no Uploads on {0}".format(date))
    
    






@app.route('/api/fetchrevisionsdata', methods=['POST'])
def checkUploaded():
    params = request.get_json()
    print(params)
    cursor.execute("select file_data, upload_date, upload_time, uploaded_by, revision_no from file_uploads where state_id = {0} and upload_date = to_date('{1}', 'DD/MM/YYYY') and revision_no={2}".format(params["state"], params["date"], int(params["revision"])))
    data = cursor.fetchall()

    file_data = []
    uploaded_time = ''
    uploaded_date = ''
    uploaded_by = ''
    # role = ''
    revision_no = int()



    if len(data) > 0:
        file_data = data[0][0]
        uploaded_date = data[0][1].strftime('%d-%b-%Y')
        uploaded_time = data[0][2].strftime('%d-%b-%Y %H:%M:%S %p')
        uploaded_by = data[0][3]
        revision_no = data[0][4]
        print(type(uploaded_date), type(uploaded_time))
        # print(type(file_data), uploaded_time, uploaded_date, uploaded_by, revision_no)
        # print(file_data[-1])
        print(len(file_data), len(file_data[0]))
        return jsonify(status="success", data=file_data, time=uploaded_time, date=uploaded_date, revision=revision_no, role=uploaded_by)
    else:
        return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
        

    return jsonify(message="Fetched Successfully")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


state_revision_numbers = {}


@app.route('/api/upload', methods=['POST'])
def upload_data_and_file():
    # print(request.get_json())
    # print(request["form_data"])
    # print(request["data"])
    header_data = dict(request.headers)
    # print(header_data)
    state = request.form.get('state')
    # print("state",state)
    disabledDate = request.form.get('disabledDate')
    # print(disabledDate)
    data = request.form.get('data')
    data = json.loads(data)

    data = json.dumps(data)
    # print(data[0])

    token = header_data['Authorization'].split()[1]
    x = decode_token(token, csrf_value=None, allow_expired=False)

    username = x['sub']
    # print(username, "username")
    role = x['role']
    

    cursor.execute("select state_name, acronym from states where state_id='{0}'".format(state))

    state_name = cursor.fetchall()[0][0]


        


    date_string = disabledDate

# Define the format of the input date string
    date_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"

# Parse the date string into a datetime object
    disabledDate = (datetime.strptime(date_string, date_format)).strftime("%Y-%m-%d")

    # print(state, type(disabledDate) )
    # print("Data Received")


    if 'excelFile' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['excelFile']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)

        directory_path = os.path.join("D:\\","Day_Ahead_Forecast_Files", disabledDate,  state_name)

        cursor.execute("select * from file_uploads where upload_date = to_date('{0}', 'YYYY-MM-DD') and state_id = {1}".format(disabledDate, state))

        existing_revs = cursor.fetchall()


        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Get the current revision number for the state and increment it
        filename = f"{disabledDate}_{state_name}_rev{len(existing_revs) + 1}.xlsx"

        # Generate the filename based on the current revision number

        file_path = os.path.join(directory_path, filename)

        print(directory_path, "This is the directory path")

        print("file path", file_path)

        # Save the uploaded file in the directory
        if 'excelFile' in request.files:
            file = request.files['excelFile']
            if file.filename != '':
                print("entered in save")
                file.save(file_path)
                if len(existing_revs) > 0:
                    cursor.execute("insert into file_uploads (state_id, upload_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'YYYY-MM-DD HH24:MI:SS'), '{3}', {4}, '{5}', '{6}')".format(state, disabledDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs)+1, role, data))
                    cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded {0} times'.format(len(existing_revs)+1)})

                else:
                    cursor.execute("insert into file_uploads (state_id, upload_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'YYYY-MM-DD HH24:MI:SS'), '{3}', {4}, '{5}', '{6}')".format(state, disabledDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs)+1, role, data))
                    cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                    return jsonify({'message': 'Data and file uploaded successfully, File Uploaded for the first time'})

        # file.save("D:\\forecast_excel_store\\"+file_name)
        print("file saved successfully")
        # Process the form data and uploaded file as needed
        # You can access 'name' and 'email' here

        # return jsonify({'message': 'Data and file uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file type'})
    

@app.route('/api/pendingentries', methods=['GET'])
@jwt_required()
def pendingTimingEntries():
    try:
        response = requests.get("http://10.0.100.58:8999/Codebook/getDueTimingEntryData")

        data = response.json()["data"]["dueTiminingEntryList"]

        # print(data)

        header_data = dict(request.headers)
        # print(header_data)
        token = header_data['Authorization'].split()[1]
        x = decode_token(token, csrf_value=None, allow_expired=False)

        username = x['sub']   # username in database

        role = x['role']       # role in database

        states_entities_dict = {}
        states_entities_dict["kar_state"] = ['kptcl', 'KTL']
        states_entities_dict["ap_state"] = ['LKPPLSTG3', 'APTRANSCO']
        states_entities_dict["tn_state"] = ['TN','TANTRANSCO']
        states_entities_dict["ker_state"] = []
        states_entities_dict["tg_state"] = ['TSTRANSCO']
        states_entities_dict["pondy_state"] = []
        states_entities_dict["pgcil_sr_1"] = ['PGCIL SR-1']
        states_entities_dict["pgcil_sr_2"] = ['PGCIL SR-2']


        admin_states_list = []

        for key, value in states_entities_dict.items():
            for v in value:
                admin_states_list.append(v)


        # PGCIL SR-2, PGCIL SR-1

        # print(states_entities_dict[username])


        entities_data = []

        # print(data)

        id = 1

        if role == 'user':
            for i in data:
                if (i["codeIssuedto"] in states_entities_dict[username] or i["codeRequestedby"] in states_entities_dict[username]) and (i["constituentEnteredTime"] == ""):
                    entities_data.append({"id": id, "codeIssueTime": i["codeIssuedTime"], "elementType": i["entityFeatureName"], "elementName": i["elementName"], "switching": i["end"], "srldcCode": i["codeNo"], "category": i["outageCategory"], "codeIssuedTo": i["codeIssuedto"], "codeRequestedBy": i["codeRequestedby"], "codeId": i["codeId"], "isSelected": False})
                    id = id + 1
        
        else:
            for i in data:
                if (i["codeIssuedto"] in admin_states_list or i["codeRequestedby"] in admin_states_list) and (i["constituentEnteredTime"] == ""):
                    entities_data.append({"id": id, "codeIssueTime": i["codeIssuedTime"], "elementType": i["entityFeatureName"], "elementName": i["elementName"], "switching": i["end"], "srldcCode": i["codeNo"], "category": i["outageCategory"], "codeIssuedTo": i["codeIssuedto"], "codeRequestedBy": i["codeRequestedby"],  "codeId": i["codeId"], "isSelected": False})
                    id = id + 1


        if len(entities_data) == 0:
            return jsonify(status="failure", message="Data is Empty!")
        


        return jsonify(status="success", message="Message fetched successfully!", data=entities_data )


    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify(status="failure", message="There is a problem in fetching the data, Please contact SRLDC IT!")
    
@app.route('/api/submitentries', methods=['POST'])
@jwt_required()
def submitTimingEntries():
    try:
        data = request.get_json()

        # data = json.loads(data)

        data = data["data"]

        for i in data:

            if 'T' in i["codeIssueTime"]:
                i["codeIssueTime"] = datetime.fromisoformat(i["codeIssueTime"]).strftime("%Y-%m-%d %H:%M")
            else:
                i["codeIssueTime"] = datetime.strptime(i["codeIssueTime"], "%d/%m/%Y, %H:%M")

                # Format the datetime object as "yyyy-mm-dd hh:mm"
                i["codeIssueTime"] = i["codeIssueTime"].strftime("%Y-%m-%d %H:%M")

            response = requests.get("https://oms2.srldc.in/Codebook/EnterConstituentTime?codeId={0}&enteredTime={1}".format(i["codeId"], i["codeIssueTime"]))

            print(response)

        return jsonify(status="success", message="Sent Successfully!")
    except Exception as error:
        print(error)
        return jsonify(status="failure", message="There is a problem, Please contact SRLDC IT!")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)






