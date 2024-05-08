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
import json
import jwt
from flask_cors import CORS
import psycopg2



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


def subtract_months(source_date, months):
    month = source_date.month - 1 - months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, [31, 29 if year % 4 == 0 and not year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return datetime(year, month, day)

@app.route("/api/login", methods=["POST"])
def login():
    try:

        username=request.get_json()['username']
        password=request.get_json()['password']

        print(username, password)

        # username = 

       
        

       



        e_name = ''

        role = ''

        state_name = ''

        state_id = ''

        


        
        # query = sql.SQL("select username, password_hash, user_role, state_name, state_id from states where username= {}'".format(sql.Literal(username)))
        # cursor.execute(query)

        query = "SELECT username, password_hash, user_role, state_name, state_id from states WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch the result (if any)
        # result = cursor.fetchone()


        login_data = cursor.fetchall()

        # print(login_data)

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
@jwt_required()
def fetchRevisions():
    params = request.get_json()
    date = params["date"]
    params["date"] = date
    state = params["state"]
    cursor.execute("select revision_no from file_uploads where state_id = {0} and upload_date = to_date('{1}', 'DD/MM/YYYY')".format(params["state"], params["date"]))
    revisions_data = cursor.fetchall()

    revision_list = [i[0] for i in revisions_data]

    cursor.execute("select state_name from states where state_id = {0}".format(state))
    state_name = cursor.fetchall()[0][0]

    if len(revision_list) > 0:
        return jsonify(status="success", message="Fetched Successfully for {0}".format(date), revisions=revision_list)
    else:
        return jsonify(status="failure", message="There are no Uploads for {0} state for date {1}".format(state_name, date))
    

    
@app.route('/api/fetchweekrevisions', methods=['POST'])
@jwt_required()
def fetchWeekRevisions():
    params = request.get_json()
    from_date = params["from_date"]
    to_date = params["to_date"]
    state = params["state"]
    cursor.execute("select revision_no from week_ahead_file_uploads where state_id = {0} and from_date = to_date('{1}', 'DD/MM/YYYY') and to_date=to_date('{2}', 'DD/MM/YYYY')".format(params["state"], from_date, to_date))
    revisions_data = cursor.fetchall()
    revision_list = [i[0] for i in revisions_data]

    cursor.execute("select state_name from states where state_id = {0}".format(state))
    state_name = cursor.fetchall()[0][0]


    if len(revision_list) > 0:
        return jsonify(status="success", message="Fetched Successfully for '{0}'-'{1}'".format(from_date, to_date), revisions=revision_list, from_date=from_date, to_date=to_date)
    else:
        return jsonify(status="failure", message="There are no Uploads for state {0} for week '{1}'-'{2}'".format(state_name, from_date, to_date))    
    

@app.route('/api/fetchweeklyrevisionsdata', methods=['POST'])
@jwt_required()
def fetchWeeklyRevisionsData():
    params = request.get_json()
    print(params)
    cursor.execute("select file_data, from_date, to_date, upload_time, uploaded_by, revision_no from week_ahead_file_uploads where state_id = {0} and from_date = to_date('{1}', 'DD/MM/YYYY') and to_date=to_date('{2}', 'DD/MM/YYYY') and revision_no={3}".format(params["state"], params["from_date"], params["to_date"], int(params["revision"])))
    data = cursor.fetchall()

    file_data = []
    uploaded_time = ''
    from_date = ''
    to_date = ''
    uploaded_by = ''
    # role = ''
    revision_no = int()



    if len(data) > 0:
        file_data = data[0][0]
        from_date = data[0][1].strftime('%d-%b-%Y')
        to_date = data[0][2].strftime('%d-%b-%Y')
        uploaded_time = data[0][3].strftime('%d-%b-%Y %H:%M:%S %p')
        uploaded_by = data[0][4]
        revision_no = data[0][5]

        # print(len(file_data), len(file_data[0]))
        return jsonify(status="success", data=file_data, time=uploaded_time, from_date=from_date,to_date=to_date, revision=revision_no, role=uploaded_by)
    else:
        return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
        

    return jsonify(message="Fetched Successfully")




@app.route('/api/fetchrevisionsdata', methods=['POST'])
@jwt_required()
def checkUploaded():
    params = request.get_json()
    # print(params)
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
        # print(type(uploaded_date), type(uploaded_time))
        # print(type(file_data), uploaded_time, uploaded_date, uploaded_by, revision_no)
        # print(file_data[-1])
        # print(len(file_data), len(file_data[0]))
        return jsonify(status="success", data=file_data, time=uploaded_time, date=uploaded_date, revision=revision_no, role=uploaded_by)
    else:
        return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
        

    return jsonify(message="Fetched Successfully")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


state_revision_numbers = {}


@app.route('/api/uploaddayahead', methods=['POST'])
@jwt_required()
def uploadDayAheadDataAndFile():
    try:
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

        # print(data)
        # print("data received!")

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

        # print(data)
        # print("Data recieived!")

        if 'excelFile' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['excelFile']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)

            current_directory = os.getcwd()
            drive_name, path = os.path.splitdrive(current_directory)


            directory_path = os.path.join(path,"DAY_AHEAD_FORECAST_FILES", disabledDate,  state_name)

            # print(directory_path)

            cursor.execute("select * from file_uploads where upload_date = to_date('{0}', 'YYYY-MM-DD') and state_id = {1}".format(disabledDate, state))

            existing_revs = cursor.fetchall()


            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)

            # Get the current revision number for the state and increment it
        
            filename = f"{disabledDate}_{state_name}_rev{len(existing_revs)}.xlsx"

            # Generate the filename based on the current revision number

            file_path = os.path.join(directory_path, filename)

            # print(directory_path, "This is the directory path")

            # print("file path", file_path)

            # Save the uploaded file in the directory
            if 'excelFile' in request.files:
                file = request.files['excelFile']
                if file.filename != '':
                    # print("entered in save")
                    file.save(file_path)
                          
                    cursor.execute("insert into file_uploads (state_id, upload_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'YYYY-MM-DD HH24:MI:SS'), '{3}', {4}, '{5}', '{6}')".format(state, disabledDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded for Revision-{}'.format(len(existing_revs))})

            # file.save("D:\\forecast_excel_store\\"+file_name)
            # print("file saved successfully")
            # Process the form data and uploaded file as needed
            # You can access 'name' and 'email' here

            # return jsonify({'message': 'Data and file uploaded successfully'})
        else:
            return jsonify({'error': 'Invalid file type'})
        
    except Exception as error:
        logger.error("An error occurred: %s", error)
        return jsonify(message="There is problem in uploading, Please contact SRLDC IT!")

    

@app.route('/api/pendingentries', methods=['GET'])
@jwt_required()
def pendingTimingEntries():
    try:
        response = requests.get("https://oms2.srldc.in/Codebook/getDueTimingEntryData")

        data = response.json()["data"]["dueTiminingEntryList"]

        # print(data[0])

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

        # print(type(entities_data[0]["codeIssueTime"]))
        # formatted_data_list = [{'date_key': datetime.strptime(item['date_key'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d/%m/%Y, %H:%M') for item in data_list]
                               
        for i in range(len(entities_data)):
            entities_data[i]["codeIssueTime"] = datetime.strptime(entities_data[i]["codeIssueTime"], '%Y-%m-%dT%H:%M:%S.%f').isoformat()
        
        # print(entities_data[0]["codeIssueTime"])

        if len(entities_data) == 0:
            return jsonify(status="failure", message="Data is Empty!")
        


        return jsonify(status="success", message="Message fetched successfully!", data=entities_data )


    except Exception as e:
        # print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify(status="failure", message="There is a problem in fetching the data, Please contact SRLDC IT!")
    

@app.route('/api/weekaheadformat')
@jwt_required()
def weekAheadFormat():
    try:
        # Function to find the date of the next Monday
        def next_monday(d):
            # Calculate the number of days until the next Monday
            days_til_monday = (7 - d.weekday()) % 7
            if days_til_monday == 0:
                # If today is Monday, add 7 days to get the next Monday
                days_til_monday = 7
            return d + timedelta(days=days_til_monday)

# Function to create the 2D list
        def create_2d_list(start_date, num_days, num_blocks_per_day):
            data = []

            for day in range(num_days):
                current_date = start_date + timedelta(days=day)
                for block in range(num_blocks_per_day):
                    current_time = (datetime.min + timedelta(minutes=block * 15)).time()
                    next_time = (datetime.min + timedelta(minutes=(block + 1) * 15)).time()
                    timestamp = f"{current_time:%H:%M} - {next_time:%H:%M}"
                    row = [current_date.strftime('%Y-%m-%d'), block + 1, timestamp] + [0] * 19
                    data.append(row)

            return data

        # Find the next Monday
        today = datetime.now()
        next_monday_date = next_monday(today)

        # Create the 2D list for 7 days with 96 blocks each
        num_days = 7
        num_blocks_per_day = 96
        data = create_2d_list(next_monday_date, num_days, num_blocks_per_day)

        
        return jsonify(status="success", data=data)
    
    except Exception as error:
        return jsonify(msg="Problem in fetching the data, Please contact SRLDC IT", status="failure")


@app.route('/api/monthaheadformat')
@jwt_required()
def monthAheadFormat():

    try:

        def create_2d_list(start_date, end_date, num_blocks_per_day):
            data = []
            
            while start_date <= end_date:
                for block in range(num_blocks_per_day):
                    current_time = (datetime.min + timedelta(minutes=block * 15)).time()
                    next_time = (datetime.min + timedelta(minutes=(block + 1) * 15)).time()
                    timestamp = f"{current_time:%H:%M} - {next_time:%H:%M}"
                    row = [start_date.strftime('%Y-%m-%d'), block + 1, timestamp] + [0] * 19
                    data.append(row)
                
                start_date += timedelta(days=1)
            
            return data

        today = datetime.now()

        # Calculate the start and end dates of the next month
        start_of_next_month = datetime(today.year, today.month + 1, 1)
        end_of_next_month = datetime(today.year, today.month + 2, 1) - timedelta(days=1)


        # Create the 2D list for the entire next month with 96 blocks each day
        num_blocks_per_day = 96
        data = create_2d_list(start_of_next_month, end_of_next_month, num_blocks_per_day)

        # print(len(data))

        return jsonify(data=data, status="success")
    except Exception as error:
        return jsonify(status="failure", msg="Problem in Fetching the data, Please contact SRLDC IT!")



@app.route('/api/yearaheadformat')
@jwt_required()
def yearheadFormat():
    try:
        def create_2d_list_for_year(start_date, end_date, num_blocks_per_day):
            data = []

            while start_date <= end_date:
                for block in range(num_blocks_per_day):
                    current_time = (datetime.min + timedelta(minutes=block * 60)).time()
                    next_time = (datetime.min + timedelta(minutes=(block + 1) * 60)).time()
                    # timestamp = f"{current_time:%H:%M} - {next_time:%H:%M}"
                    row = [start_date.strftime('%Y-%m-%d'), block + 1] + [0] * 19
                    data.append(row)

                start_date += timedelta(days=1)

            return data

        # Example usage for a range of dates within a year
        today = datetime.now()
        start_of_next_year = datetime(today.year + 1, 1, 1)
        end_of_next_year = datetime(today.year + 1, 12, 31)

        # num_blocks_per_day = 96
        data_for_next_year = create_2d_list_for_year(start_of_next_year, end_of_next_year, num_blocks_per_day=24)

        # Display the generated data for the next year
        # for row in data_for_next_year:
        #     print(row)

        return jsonify(data=data_for_next_year, status="success")
    except Exception as error:
        return jsonify(status="failure", msg="Problem in Fetching the data, Please contact SRLDC IT!")



    
    
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

            # print(response)

        return jsonify(status="success", message="Sent Successfully!")
    except Exception as error:
        # print(error)
        return jsonify(status="failure", message="There is a problem, Please contact SRLDC IT!")
    

@app.route('/api/weeekaheadforecast', methods=['POST'])
@jwt_required()
def weekAheadForecast():
    try: 
        return jsonify(msg="Successful!", status="failure")
    except Exception as error:
        return jsonify(msg="There is some problem, Please contact SRLDC IT!")
    


@app.route('/api/uploadweekahead', methods=['POST'])
@jwt_required()
def uploadWeekAheadDataAndFile():
    # print(request.get_json())
    # print(request["form_data"])
    # print(request["data"])
    header_data = dict(request.headers)
    # print(header_data)
    state = request.form.get('state')
    # print("state",state)
    fromDate = request.form.get('fromDate')

    toDate = request.form.get('toDate')
    # print(disabledDate)
    data = request.form.get('data')
    data = json.loads(data)

    # print(disabledDate, "Date range")

    data = json.dumps(data)
    # print(data[0])

    token = header_data['Authorization'].split()[1]
    x = decode_token(token, csrf_value=None, allow_expired=False)

    username = x['sub']
    # print(username, "username")
    role = x['role']
    

    cursor.execute("select state_name, acronym from states where state_id='{0}'".format(state))

    state_name = cursor.fetchall()[0][0]


    if 'excelFile' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['excelFile']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)

        current_directory = os.getcwd()
        drive_name, path = os.path.splitdrive(current_directory)

        print(drive_name)

        from_date = datetime.strptime(fromDate, '%d/%m/%Y').strftime('%d.%m.%Y')
        to_date = datetime.strptime(toDate, '%d/%m/%Y').strftime('%d.%m.%Y')

        directory_path = os.path.join(shared_drive_path,"WEEK_AHEAD_FORECAST_FILES", from_date+"-"+ to_date, state_name)

        cursor.execute("select * from week_ahead_file_uploads where from_date = to_date('{0}', 'DD/MM/YYYY') and to_date = to_date('{1}','DD/MM/YYYY') and state_id = {2}".format(fromDate,toDate,  state))

        existing_revs = cursor.fetchall()


        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Get the current revision number for the state and increment it
        filename = f"{from_date}_{to_date}_{state_name}_rev{len(existing_revs)}.xlsx"

        # Generate the filename based on the current revision number

        file_path = os.path.join(directory_path, filename)

        # Save the uploaded file in the directory
        if 'excelFile' in request.files:
            file = request.files['excelFile']
            if file.filename != '':
                # print("entered in save")
                file.save(file_path)
                if len(existing_revs) > 0:
                    cursor.execute("insert into week_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate, toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded for Revision-{0} '.format(len(existing_revs))})

                else:
                    cursor.execute("insert into week_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate,toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded for Revision-{0} '.format(len(existing_revs))})

        # file.save("D:\\forecast_excel_store\\"+file_name)
        # print("file saved successfully")

    else:
        return jsonify({'error': 'Invalid file type'})
    


@app.route('/api/uploadmonthahead', methods=['POST'])
@jwt_required()
def uploadMonthAheadDataAndFile():
    # print(request.get_json())
    # print(request["form_data"])
    # print(request["data"])
    header_data = dict(request.headers)
    # print(header_data)
    state = request.form.get('state')
    # print("state",state)
    fromDate = request.form.get('fromDate')

    toDate = request.form.get('toDate')
    # print(disabledDate)
    data = request.form.get('data')
    data = json.loads(data)

    # print(disabledDate, "Date range")

    data = json.dumps(data)
    # print(data[0])

    token = header_data['Authorization'].split()[1]
    x = decode_token(token, csrf_value=None, allow_expired=False)

    username = x['sub']
    # print(username, "username")
    role = x['role']
    

    cursor.execute("select state_name, acronym from states where state_id='{0}'".format(state))

    state_name = cursor.fetchall()[0][0]


        


    # date_string = disabledDate

# Define the format of the input date string
    # date_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"

# Parse the date string into a datetime object
    # disabledDate = (datetime.strptime(date_string, date_format)).strftime("%Y-%m-%d")

    # print(state, type(disabledDate) )
    # print("Data Received")


    if 'excelFile' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['excelFile']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)

        current_directory = os.getcwd()
        drive_name, path = os.path.splitdrive(current_directory)


        from_date = datetime.strptime(fromDate, '%d/%m/%Y').strftime('%d.%m.%Y')
        to_date = datetime.strptime(toDate, '%d/%m/%Y').strftime('%d.%m.%Y')

        directory_path = os.path.join(shared_drive_path,"MONTH_AHEAD_FORECAST_FILES", from_date+"-"+ to_date, state_name)

        cursor.execute("select * from month_ahead_file_uploads where from_date = to_date('{0}', 'DD/MM/YYYY') and to_date = to_date('{1}','DD/MM/YYYY') and state_id = {2}".format(fromDate,toDate,  state))

        existing_revs = cursor.fetchall()


        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Get the current revision number for the state and increment it
        filename = f"{from_date}_{to_date}_{state_name}_rev{len(existing_revs) + 1}.xlsx"

        # Generate the filename based on the current revision number

        file_path = os.path.join(directory_path, filename)

        print(directory_path, "This is the directory path")

        print("file path", file_path)

        # Save the uploaded file in the directory
        if 'excelFile' in request.files:
            file = request.files['excelFile']
            if file.filename != '':
                # print("entered in save")
                file.save(file_path)
                if len(existing_revs) > 0:
                    cursor.execute("insert into month_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate, toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs))})

                else:
                    cursor.execute("insert into month_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate,toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs))})


    else:
        return jsonify({'error': 'Invalid file type'})



@app.route('/api/fetchmonthrevisions', methods=['POST'])
@jwt_required()
def fetchMonthRevisions():
    params = request.get_json()
    from_date = params["from_date"]
    to_date = params["to_date"]
    state = params["state"]
    cursor.execute("select revision_no from month_ahead_file_uploads where state_id = {0} and from_date = to_date('{1}', 'DD/MM/YYYY') and to_date=to_date('{2}', 'DD/MM/YYYY')".format(params["state"], from_date, to_date))
    revisions_data = cursor.fetchall()
    revision_list = [i[0] for i in revisions_data]

    cursor.execute("select state_name from states where state_id = {0}".format(state))
    state_name = cursor.fetchall()[0][0]


    if len(revision_list) > 0:
        return jsonify(status="success", message="Fetched Successfully for '{0}'-'{1}'".format(from_date, to_date), revisions=revision_list, from_date=from_date, to_date=to_date)
    else:
        return jsonify(status="failure", message="There are no Uploads for state {0} for the month '{1}'-'{2}'".format(state_name, from_date, to_date))    
    

@app.route('/api/fetchmonthlyrevisionsdata', methods=['POST'])
@jwt_required()
def fetchMonthlyRevisionsData():
    params = request.get_json()
    # print(params)
    cursor.execute("select file_data, from_date, to_date, upload_time, uploaded_by, revision_no from month_ahead_file_uploads where state_id = {0} and from_date = to_date('{1}', 'DD/MM/YYYY') and to_date=to_date('{2}', 'DD/MM/YYYY') and revision_no={3}".format(params["state"], params["from_date"], params["to_date"], int(params["revision"])))
    data = cursor.fetchall()

    file_data = []
    uploaded_time = ''
    from_date = ''
    to_date = ''
    uploaded_by = ''
    # role = ''
    revision_no = int()



    if len(data) > 0:
        file_data = data[0][0]
        from_date = data[0][1].strftime('%d-%b-%Y')
        to_date = data[0][2].strftime('%d-%b-%Y')
        uploaded_time = data[0][3].strftime('%d-%b-%Y %H:%M:%S %p')
        uploaded_by = data[0][4]
        revision_no = data[0][5]

        # print(len(file_data), len(file_data[0]))
        return jsonify(status="success", data=file_data, time=uploaded_time, from_date=from_date,to_date=to_date, revision=revision_no, role=uploaded_by)
    else:
        return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
        

    return jsonify(message="Fetched Successfully")




@app.route('/api/uploadyearahead', methods=['POST'])
@jwt_required()
def uploadYearAheadDataAndFile():
    # print(request.get_json())
    # print(request["form_data"])
    # print(request["data"])
    header_data = dict(request.headers)
    # print(header_data)
    state = request.form.get('state')
    # print("state",state)
    fromDate = request.form.get('fromDate')

    toDate = request.form.get('toDate')
    # print(disabledDate)
    data = request.form.get('data')
    data = json.loads(data)

    # print(disabledDate, "Date range")

    data = json.dumps(data)
    # print(data[0])

    token = header_data['Authorization'].split()[1]
    x = decode_token(token, csrf_value=None, allow_expired=False)

    username = x['sub']
    # print(username, "username")
    role = x['role']
    

    cursor.execute("select state_name, acronym from states where state_id='{0}'".format(state))

    state_name = cursor.fetchall()[0][0]


        


    # date_string = disabledDate

# Define the format of the input date string
    # date_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"

# Parse the date string into a datetime object
    # disabledDate = (datetime.strptime(date_string, date_format)).strftime("%Y-%m-%d")

    # print(state, type(disabledDate) )
    # print("Data Received")


    if 'excelFile' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['excelFile']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)

        current_directory = os.getcwd()
        drive_name, path = os.path.splitdrive(current_directory)

        print(drive_name)

        from_date = datetime.strptime(fromDate, '%d/%m/%Y').strftime('%d.%m.%Y')
        to_date = datetime.strptime(toDate, '%d/%m/%Y').strftime('%d.%m.%Y')

        directory_path = os.path.join(shared_drive_path,"Year_Ahead_Forecast_Files", from_date+"-"+ to_date, state_name)

        cursor.execute("select * from year_ahead_file_uploads where from_date = to_date('{0}', 'DD/MM/YYYY') and to_date = to_date('{1}','DD/MM/YYYY') and state_id = {2}".format(fromDate,toDate,  state))

        existing_revs = cursor.fetchall()


        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Get the current revision number for the state and increment it
        filename = f"{from_date}_{to_date}_{state_name}_rev{len(existing_revs) + 1}.xlsx"

        # Generate the filename based on the current revision number

        file_path = os.path.join(directory_path, filename)

        # print(directory_path, "This is the directory path")

        # print("file path", file_path)

        # Save the uploaded file in the directory
        if 'excelFile' in request.files:
            file = request.files['excelFile']
            if file.filename != '':
                # print("entered in save")
                file.save(file_path)
                if len(existing_revs) > 0:
                    cursor.execute("insert into year_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate, toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs))})

                else:
                    cursor.execute("insert into year_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate,toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                    # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs))})
        # file.save("D:\\forecast_excel_store\\"+file_name)
        # print("file saved successfully")
        # Process the form data and uploaded file as needed
        # You can access 'name' and 'email' here

        # return jsonify({'message': 'Data and file uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file type'})






@app.route('/api/fetchyearlyrevisionsdata', methods=['POST'])
@jwt_required()
def fetchYearlyRevisionsData():
    params = request.get_json()
    # print(params)
    cursor.execute("select file_data, from_date, to_date, upload_time, uploaded_by, revision_no from year_ahead_file_uploads where state_id = {0} and from_date = to_date('{1}', 'DD/MM/YYYY') and to_date=to_date('{2}', 'DD/MM/YYYY') and revision_no={3}".format(params["state"], params["from_date"], params["to_date"], int(params["revision"])))
    data = cursor.fetchall()

    file_data = []
    uploaded_time = ''
    from_date = ''
    to_date = ''
    uploaded_by = ''
    # role = ''
    revision_no = int()



    if len(data) > 0:
        file_data = data[0][0]
        from_date = data[0][1].strftime('%d-%b-%Y')
        to_date = data[0][2].strftime('%d-%b-%Y')
        uploaded_time = data[0][3].strftime('%d-%b-%Y %H:%M:%S %p')
        uploaded_by = data[0][4]
        revision_no = data[0][5]

        # print(len(file_data), len(file_data[0]))
        return jsonify(status="success", data=file_data, time=uploaded_time, from_date=from_date,to_date=to_date, revision=revision_no, role=uploaded_by)
    else:
        return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
        

    return jsonify(message="Fetched Successfully")



@app.route('/api/fetchyearrevisions', methods=['POST'])
@jwt_required()
def fetchYearRevisions():
    params = request.get_json()
    from_date = params["from_date"]
    to_date = params["to_date"]
    state = params["state"]
    cursor.execute("select revision_no from year_ahead_file_uploads where state_id = {0} and from_date = to_date('{1}', 'DD/MM/YYYY') and to_date=to_date('{2}', 'DD/MM/YYYY')".format(params["state"], from_date, to_date))
    revisions_data = cursor.fetchall()
    revision_list = [i[0] for i in revisions_data]

    cursor.execute("select state_name from states where state_id = {0}".format(state))
    state_name = cursor.fetchall()[0][0]


    if len(revision_list) > 0:
        return jsonify(status="success", message="Fetched Successfully for '{0}'-'{1}'".format(from_date, to_date), revisions=revision_list, from_date=from_date, to_date=to_date)
    else:
        return jsonify(status="failure", message="There are no Uploads for state {0} for the year '{1}'-'{2}'".format(state_name, from_date, to_date))    
    


@app.route('/api/uploadstatus')
@jwt_required()
def scatterPlotUploadStatus():
    try:
        end_date = datetime.now() + timedelta(days=1)
        start_date = end_date - timedelta(days=30)

        sql_query = """
            SELECT 
                states.state_name,
                COALESCE(file_uploads.upload_date, %s) AS upload_date,
                COALESCE(file_uploads.upload_time, NULL) AS upload_time,
                CASE
                    WHEN file_uploads.upload_time IS NULL THEN 2  -- Not Uploaded
                    WHEN file_uploads.upload_date < %s AND (file_uploads.upload_date + INTERVAL '1 day') <= %s THEN 0  -- Uploaded
                    ELSE 1  -- Late Upload
                END AS upload_status_code,
                COUNT(file_uploads.state_id) AS upload_count
            FROM 
                states
            LEFT JOIN 
                file_uploads ON states.state_id = file_uploads.state_id
                AND file_uploads.upload_date BETWEEN %s AND %s
            WHERE states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2')
            GROUP BY 
                states.state_name, 
                file_uploads.upload_date,
                file_uploads.upload_time  
            ORDER BY
                states.state_name,
                upload_date DESC
        """
        cursor.execute(sql_query, (end_date, end_date, end_date, start_date, end_date))
        results = cursor.fetchall()

        data = []
        date_range = [end_date - timedelta(days=i) for i in range(30)]
        state_names = set(result[0] for result in results)

        for state_name in state_names:
            state_data = {"name": state_name, "data": []}
            for date in date_range:
                date_str = date.strftime('%Y-%m-%d')
                found_result = False
                for result in results:
                    if result[0] == state_name and result[1].strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
                        upload_count = result[4]
                        upload_time = result[2].strftime("%d/%m/%Y %H:%M:%S %p") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break
                if not found_result:
                    upload_count = 0
                    upload_time = None
                    # For dates with no uploads, consider them as "Not Uploaded"
                    upload_status_code = 2  # Not Uploaded
                state_data["data"].append({'x': date_str, 'y': upload_status_code, 'upload_time': upload_time, 'upload_count': upload_count})  
            data.append(state_data)

        day_data = data
        # Print or return the JSON data
        # print(data)

        #######################################################################################################################################
        #######################################################################################################################################
        # Now implementing week ahead forecast data for dashboard 

                
        today = datetime.now()
        end_date = today - timedelta(days=(today.weekday() + 1) % 7)  # Adjust to get the last Sunday
        start_date = end_date - timedelta(weeks=5)  # Start date 5 weeks ago



        # SQL query to fetch data for week ahead
        sql_query = """
            SELECT 
                states.state_name,
                week_ahead_file_uploads.from_date AS week_start_date,
                COALESCE(week_ahead_file_uploads.upload_time, NULL) AS upload_time,
                CASE
                    WHEN week_ahead_file_uploads.upload_time IS NULL THEN 2  -- Not Uploaded
                    WHEN week_ahead_file_uploads.from_date < %s AND (week_ahead_file_uploads.from_date + INTERVAL '7 day') <= %s THEN 0  -- Uploaded
                    ELSE 1  -- Late Upload
                END AS upload_status_code,
                COUNT(week_ahead_file_uploads.state_id) AS upload_count
            FROM 
                states
            LEFT JOIN 
                week_ahead_file_uploads ON states.state_id = week_ahead_file_uploads.state_id
                AND week_ahead_file_uploads.from_date BETWEEN %s AND %s
            WHERE states.username not in ('admin', 'pgcil_sr_1', 'pgcil_sr_2')
            GROUP BY 
                states.state_name, 
                week_ahead_file_uploads.from_date,
                week_ahead_file_uploads.upload_time
            ORDER BY
                states.state_name,
                week_start_date DESC
        """
        cursor.execute(sql_query, (end_date, end_date, start_date, end_date))
        results = cursor.fetchall()

        # Ensure all states are included
        cursor.execute("SELECT state_name FROM states WHERE username not in ('admin', 'pgcil_sr_1', 'pgcil_sr_2')")
        all_states = [row[0] for row in cursor.fetchall()]

        # Create a list of the starting Mondays for each week in the range
        week_range = [(end_date - timedelta(days=i * 7)).date() for i in range(5)]

        # Prepare data structure for JSON output
        data = []
        for state_name in all_states:
            state_data = {"name": state_name, "data": []}
            for week_start in week_range:
                week_start_date = (week_start - timedelta(days=week_start.weekday()))
                week_end_date = week_start_date + timedelta(days=6)
                week_range_str = f"{week_start_date.strftime('%Y-%m-%d')} to {week_end_date.strftime('%Y-%m-%d')}"

                # Initialize upload count, upload status code, and upload time for the week
                upload_count = 0
                upload_status_code = 2  # Default to Not Uploaded
                upload_time = None
                found_result = False
                for result in results:
                    if result[0] == state_name and result[1] == week_start_date:
                        upload_count = result[4]
                        upload_time = result[2].strftime("%d/%m/%Y %H:%M:%S %p") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break

                # If no result found, set upload count to 0 and upload status code to 2
                if not found_result:
                    upload_count = 0
                    upload_status_code = 2  # Not Uploaded
                state_data["data"].append({'x': week_range_str, 'y': upload_status_code, 'upload_time': upload_time, 'upload_count': upload_count})
            data.append(state_data)

        week_data = data



        #######################################################################################################################################
        #######################################################################################################################################
        # Now implementing month ahead forecast data for dashboard 


        today = datetime.now()
        # Ensure that 'today' is set to a specific date for your scenario
        # today = datetime(2024, 4, 24)

        # Start of the current month
        start_of_current_month = today.replace(day=1)

        # Creating list of start dates for the last three complete months
        month_ranges = [subtract_months(start_of_current_month, i) for i in range(1, 4)]

        # SQL query to fetch upload counts by state and month
        sql_query = """
            SELECT 
                states.state_name,
                DATE_TRUNC('month', month_ahead_file_uploads.from_date) AS month_start_date,
                COALESCE(month_ahead_file_uploads.upload_time, NULL) AS upload_time,
                CASE
                    WHEN month_ahead_file_uploads.upload_time IS NULL THEN 2  -- Not Uploaded
                    WHEN month_ahead_file_uploads.from_date < %s AND (month_ahead_file_uploads.from_date + INTERVAL '30 day') <= %s THEN 0  -- Uploaded
                    ELSE 1  -- Late Upload
                END AS upload_status_code,
                COUNT(month_ahead_file_uploads.state_id) AS upload_count
            FROM 
                states
            LEFT JOIN 
                month_ahead_file_uploads ON states.state_id = month_ahead_file_uploads.state_id
                AND month_ahead_file_uploads.from_date BETWEEN %s AND %s
            WHERE states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2')
            GROUP BY 
                states.state_name, 
                month_start_date,
                month_ahead_file_uploads.upload_time,
                month_ahead_file_uploads.from_date  -- Include from_date in GROUP BY clause
            ORDER BY
                states.state_name,
                month_start_date DESC
        """
        cursor.execute(sql_query, (month_ranges[-1], start_of_current_month - timedelta(days=1), month_ranges[-1], start_of_current_month - timedelta(days=1)))
        results = cursor.fetchall()

        # Fetch all states
        cursor.execute("SELECT state_name FROM states WHERE username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2')")
        all_states = [row[0] for row in cursor.fetchall()]

        # Data structure for JSON output
        data = []
        for state_name in all_states:
            state_data = {"name": state_name, "data": []}
            for month_start in month_ranges:
                month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                month_range_str = f"{month_start.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}"

                upload_count = 0
                upload_status_code = 2  # Default to Not Uploaded
                upload_time = None
                found_result = False
                for result in results:
                    result_month_start = result[1]
                    if result[0] == state_name and result_month_start == month_start:
                        upload_count = result[4]
                        upload_time = result[2].strftime("%d/%m/%Y %H:%M:%S %p") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break

                if not found_result:
                    upload_count = 0
                state_data["data"].append({'x': month_range_str, 'y': upload_status_code, 'upload_time': upload_time, 'upload_count': upload_count})
            data.append(state_data)

        month_data = data

        
        
        return jsonify(day=day_data, week=week_data, month = month_data)
    except Exception as error:
        # print(error)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify(message="There is a problem, please contact SRLDC IT!")


@app.route('/api/mapechart', methods=['POST'])
@jwt_required()
def mapeChart():
    params = request.get_json()
    # print(params)

    from_date = params["params"]["fromDate"]
    to_date = params["params"]["toDate"]  
    state_id = params["params"]["state"]

    cursor.execute("select state_name from states where state_id = {0}".format(state_id))

    state_name = cursor.fetchall()[0][0]


    ########### Fetch Actual data

    cursor.execute('''
        select process_date, demand_met from states s join actual_demand ad on s.reporting_state_id = ad.state_id 
        where process_date between to_date('{0}', 'DD/MM/YYYY') and to_date('{1}', 'DD/MM/YYYY') and s.state_id = {2}
        order by process_date
    '''.format(from_date, to_date, state_id))

    actual_data = cursor.fetchall()

    day_actual_json_list = []

    for i in actual_data:
        temp = {}
        temp["A_DATE"] = i[0].strftime("%Y-%m-%d")
        temp["DAY_ACTUAL"] = i[1]
        day_actual_json_list.append(temp)

    
    actual_day_df = pd.DataFrame(day_actual_json_list)

    final_data = []

    

    ############ Fetch day forecast data

    cursor.execute('''
    WITH MaxRevisions AS (
    SELECT state_id, upload_date, MAX(revision_no) AS max_revision
    FROM file_uploads
    WHERE upload_date BETWEEN to_date('{0}', 'DD/MM/YYYY') AND to_date('{1}', 'DD/MM/YYYY') 
    GROUP BY state_id, upload_date
    )
    SELECT t.state_id, t.upload_date, t.revision_no, t.file_data
    FROM file_uploads t
    INNER JOIN MaxRevisions mr
        ON t.state_id = mr.state_id
        AND t.upload_date = mr.upload_date
        AND t.revision_no = mr.max_revision
        AND t.state_id = {2}
        order by t.upload_date;
        '''.format(from_date, to_date, state_id))

    day_data = cursor.fetchall()

    if len(day_data) > 0:

    
        

        # print(day_data[0])

        day_forecast_json_list = []

        for i in day_data:
            temp = {}
            temp["D_F_DATE"] = i[1].strftime("%Y-%m-%d")
            temp["DAY_FORECAST"] = [j[2] for j in i[3]]
            day_forecast_json_list.append(temp)

        
        forecast_day_df = pd.DataFrame(day_forecast_json_list)
        

        result_df = pd.merge(forecast_day_df, actual_day_df, left_on='D_F_DATE', right_on="A_DATE")

        mape_result_day = []

        

        mape_dict = {}
        mape_dict["name"] = "Day Ahead"
        mape_dict["data"] = []

        for index, row in result_df.iterrows():
            temp = {}
            temp["x"] = row["A_DATE"]
            mape_value = calculate_mape(row["DAY_ACTUAL"], row["DAY_FORECAST"])
            if isinstance(mape_value, str):
                return jsonify(title=mape_value+"between {0} and {1} for {2}".format(from_date, to_date, state_name), status="failure")
            
            temp["y"] = round(mape_value,2)
            mape_dict["data"].append(temp)



        
        final_data.append(mape_dict)
    


    ########## Fetch Week Forecast Data

    cursor.execute('''
        WITH MaxRevisions AS (
            SELECT
                state_id,
                from_date,
                to_date,
                MAX(revision_no) AS max_revision
            FROM week_ahead_file_uploads
            -- Ensure that the records fetched lie within the specified date range (overlapping range logic)
            WHERE
                (from_date <= to_date('{1}', 'DD/MM/YYYY') AND to_date >= to_date('{0}', 'DD/MM/YYYY'))
            GROUP BY state_id, from_date, to_date
        )
        SELECT
            t.state_id,
            t.from_date,
            t.to_date,
            t.revision_no,
            t.file_data
        FROM week_ahead_file_uploads t
        INNER JOIN MaxRevisions mr
            ON t.state_id = mr.state_id
            AND t.from_date = mr.from_date
            AND t.to_date = mr.to_date
            AND t.revision_no = mr.max_revision
        WHERE
            t.state_id = {2}
        ORDER BY t.from_date;
    '''.format(from_date, to_date, state_id))

    
    week_data = cursor.fetchall()

    if len(week_data) > 0:

        week_forecast_json_list = []

        # print(week_data[0][4][2][3])
        # print(week_data[0][4])

        week_data_array = []


        demand_by_date = {}
        for i in week_data:
            for j in i[4]:
                if j[0] != "Invalid Date":
                    week_data_array.append([datetime.strptime(j[0], '%d/%m/%Y').strftime('%Y-%m-%d'), j[1], j[3]])

        
        sorted_week_data_array = sorted(week_data_array, key=lambda x: (x[0], x[1]))

        # print(sorted_week_data_array)

        # print(sorted_week_data_array)


        grouped_data = defaultdict(list)
        for row in sorted_week_data_array:
            grouped_data[row[0]].append(row[2])

        # Construct the desired JSON format
        # week_forecast_json_list = []
        for key, values in grouped_data.items():
            week_forecast_json_list.append({"W_F_DATE": key, "WEEK_FORECAST": values})

        # Print the formatted data


        
        forecast_week_df = pd.DataFrame(week_forecast_json_list)

        result_week_df = pd.merge(forecast_week_df, actual_day_df, left_on='W_F_DATE', right_on="A_DATE", how="right")

        mape_result_week = []

        

        mape_dict = {}
        mape_dict["name"] = "Week Ahead"
        mape_dict["data"] = []

        for index, row in result_week_df.iterrows():
            # print(row["A_DATE"])
            temp = {}
            temp["x"] = row["A_DATE"]
            if np.isnan(row["WEEK_FORECAST"]).any():
                temp["y"] = ""
                
            else:
                mape_value = calculate_mape(row["DAY_ACTUAL"], row["WEEK_FORECAST"])
                if isinstance(mape_value, str):
                    return jsonify(title=mape_value, status="failure")
                if mape_value != -50:
                    temp["y"] = round(mape_value,2)     
                else:
                    temp["y"] = ""
            mape_dict["data"].append(temp)
            
            
                
        final_data.append(mape_dict)


        # print(final_data)



    ####### Fetch Month Forecast Data

    cursor.execute('''
        WITH MaxRevisions AS (
            SELECT
                state_id,
                from_date,
                to_date,
                MAX(revision_no) AS max_revision
            FROM month_ahead_file_uploads
            -- Ensure that the records fetched lie within the specified date range (overlapping range logic)
            WHERE
                (from_date <= to_date('{1}', 'DD/MM/YYYY') AND to_date >= to_date('{0}', 'DD/MM/YYYY'))
            GROUP BY state_id, from_date, to_date
        )
        SELECT
            t.state_id,
            t.from_date,
            t.to_date,
            t.revision_no,
            t.file_data
        FROM month_ahead_file_uploads t
        INNER JOIN MaxRevisions mr
            ON t.state_id = mr.state_id
            AND t.from_date = mr.from_date
            AND t.to_date = mr.to_date
            AND t.revision_no = mr.max_revision
        WHERE
            t.state_id = {2}
        ORDER BY t.from_date;
    '''.format(from_date, to_date, state_id))

    month_data = cursor.fetchall()

    # print("Month data", len(month_data))

    if len(month_data) > 0:
        month_forecast_json_list = []

        # print(week_data[0][4][2][3])
        # print(week_data[0][4])

        month_data_array = []


        demand_by_date = {}
        for i in month_data:
            for j in i[4]:
                if j[0] != "Invalid Date":
                    month_data_array.append([datetime.strptime(j[0], '%d/%m/%Y').strftime('%Y-%m-%d'), j[1], j[3]])

        
        sorted_month_data_array = sorted(month_data_array, key=lambda x: (x[0], x[1]))




        grouped_data = defaultdict(list)
        for row in sorted_month_data_array:
            grouped_data[row[0]].append(row[2])

        # Construct the desired JSON format
        # week_forecast_json_list = []
        for key, values in grouped_data.items():
            month_forecast_json_list.append({"M_F_DATE": key, "MONTH_FORECAST": values})

        # Print the formatted data


        
        forecast_month_df = pd.DataFrame(month_forecast_json_list)

        result_month_df = pd.merge(forecast_month_df, actual_day_df, left_on='M_F_DATE', right_on="A_DATE", how="right")

        mape_result_month = []

        

        mape_dict = {}
        mape_dict["name"] = "Month Ahead"
        mape_dict["data"] = []

        for index, row in result_month_df.iterrows():
            # print(row["A_DATE"])
            temp = {}
            temp["x"] = row["A_DATE"]
            if np.isnan(row["MONTH_FORECAST"]).any():
                temp["y"] = ""
                
            else:
                mape_value = calculate_mape(row["DAY_ACTUAL"], row["MONTH_FORECAST"])
                if isinstance(mape_value, str):
                    return jsonify(title=mape_value, status="failure")
                if mape_value != -50:
                    temp["y"] = round(mape_value,2)     
                else:
                    temp["y"] = ""
            mape_dict["data"].append(temp)
            
            
                
        final_data.append(mape_dict)








            


    


    




    return jsonify(status="success", data=final_data, title="MAPE for the data between {0} and {1} for {2}".format(from_date, to_date, state_name ))

    



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)






