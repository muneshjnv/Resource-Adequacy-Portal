from base64 import decode
from datetime import timedelta, datetime
from functools import wraps
from operator import itemgetter
import sys
import re

from flask import Flask, request, send_file
from flask import jsonify
from flask_cors import CORS
# import ldap
# import requests

from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import decode_token
import openpyxl
import requests
from configBackend import *

import numpy as np
import pandas as pd
import json
import jwt
from flask_cors import CORS
import psycopg2
from calendar import monthrange

import datetime
from datetime import timedelta, datetime

# APIs

conn.autocommit = True
cursor = conn.cursor()


cur = conn2.cursor()



from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

# app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def log_error(api_name, error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    line_number = exc_tb.tb_lineno
    logger.error("Error in %s: %s at %s:%d", api_name, error, fname, line_number)


def subtract_months(source_date, months):
    month = source_date.month - 1 - months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, [31, 29 if year % 4 == 0 and not year % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return datetime(year, month, day)

# Function to generate the date range with each date repeating 96 times
def generate_date_range(from_date, to_date):
    num_days = (to_date - from_date).days + 1
    date_list = []
    for single_date in (from_date + timedelta(n) for n in range(num_days)):
        date_list.extend([single_date] * 96)  # Repeat each date 96 times
    return date_list


# Helper function to generate empty columns
def _column(df, col_name):
    df[col_name] = '--'
    return df

# Function to calculate column statistics
def calculate_column_stats(column):
    pos_sum = ( column[column > 0].sum() ) /1000
    neg_sum = ( column[column < 0].sum() ) /1000
    pos_max = ( column[column > 0].max() ) *4 if len(column[column > 0]) > 0 else 0
    neg_max = ( column[column < 0].min() )*4  if len(column[column < 0]) > 0 else 0

    return pd.Series([pos_sum, neg_sum, pos_max, neg_max], index=['Pos_Sum', 'Neg_Sum', 'Pos_Max', 'Neg_Max'])

def split_string(string):
    return re.findall(r'\(([A-Za-z0-9-]+)\)', string)

def generate_dataframe_forrange(start_date,end_date):
      data = []
      current_date = start_date
      # while current_date <= end_date:
      while current_date<=end_date:
            current_time = datetime.combine(current_date, datetime.min.time())
            end_time = datetime.combine(current_date, datetime.min.time()) + timedelta(days=1)
            while current_time < end_time:
                  data.append({
                  'DATE': current_date,
                  'TIME': current_time.time()
                  })
                  current_time += timedelta(minutes=15)
            
            current_date += timedelta(days=1)
      
      df = pd.DataFrame(data)
      return df


# Function to check start and end date for column
def check_start_enddate_col(full_data_df , start_date_time , end_date_time,col_name):
      try:
            full_data_df['DATETIME'] = pd.to_datetime(full_data_df['DATE'].astype(str) + ' ' + full_data_df['TIME'].astype(str))
                                               
            temp_endtimestamp=pd.to_datetime(end_date_time,errors='coerce')
            
            if pd.isnull(temp_endtimestamp):
                  default_endtimestamp = pd.to_datetime('2050-01-01')
            else: default_endtimestamp = temp_endtimestamp

            record_dt_time_condition=full_data_df['DATETIME'].apply(lambda dt: dt >= start_date_time and dt <= default_endtimestamp )
            
            full_data_df.loc[~(record_dt_time_condition), col_name] = '--'
            full_data_df.drop(columns=['DATETIME'],inplace=True)

            return full_data_df
      except Exception as e:
            return full_data_df


def calculate_formula(row,short_locations,formula):
    try:
        for loc in short_locations:
                formula=formula.replace(loc , str(row[loc]))
        return eval(formula)
    except Exception as e:
        # extractdb_errormsg(e)
        return '--'
    




# Custom token_required decorator for script access
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        jwt_data = get_jwt()

        # Check for the 'script_access' claim in the token
        # print(jwt_data, "This is JWT Data")
        if jwt_data.get('script_access'):
            # Only allow access to the /data endpoint
            if request.endpoint != 'get_data':  # 'get_data' is the function name for /data route
                return jsonify({'message': 'Access denied: this token is not authorized for this endpoint'}), 403

        return f(*args, **kwargs)

    return decorated


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

        # recaptcha_response = request.get_json()('recaptcha')

        # # Verify reCAPTCHA
        # recaptcha_secret = app.config.get('RECAPTCHA_SECRET_KEY')
        # recaptcha_verification_url = 'https://www.google.com/recaptcha/api/siteverify'
        # recaptcha_payload = {
        #     'secret': recaptcha_secret,
        #     'response': recaptcha_response
        # }
        # recaptcha_response = requests.post(recaptcha_verification_url, data=recaptcha_payload)
        # recaptcha_result = recaptcha_response.json()

        # if not recaptcha_result.get('success'):
        #     return jsonify(error="reCAPTCHA verification failed!", status="failure")

        

        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        
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
        if username == 'sr_internal' and password == 'Srldc#$1234':  # Check credentials
            additional_claims = {'script_access': True}  # Only this user gets the script_access claim
            # Merging additional claims if necessary
            jwt_data.update(additional_claims)
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
        log_error("login", e)
        # print(e)
        return jsonify(error="Problem in logging in, Please contact SRLDC IT!", status="failure")






@app.route('/api/fetchrevisions', methods=['POST'])
@jwt_required()
@token_required
def fetchRevisions():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            return jsonify(status="success", message="Fetched Successfully for {0}".format(date), revisions=revision_list)
        else:
            cursor.close()
            return jsonify(status="failure", message="There are no Uploads for {0} state for date {1}".format(state_name, date))
    except Exception as e:
        log_error("fetchrevisions", e)
        return jsonify(message="There is Some Problem, Please contact SRLDC IT")


@app.route('/api/fetchweekrevisions', methods=['POST'])
@jwt_required()
@token_required
def fetchWeekRevisions():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            return jsonify(status="success", message="Fetched Successfully for '{0}'-'{1}'".format(from_date, to_date), revisions=revision_list, from_date=from_date, to_date=to_date)
        else:
            cursor.close()
            return jsonify(status="failure", message="There are no Uploads for state {0} for week '{1}'-'{2}'".format(state_name, from_date, to_date))    
    
    except Exception as e:
        log_error("fetchweekrevisions", e)
        return jsonify(message="There is Some Problem, Please contact SRLDC IT")

@app.route('/api/fetchweeklyrevisionsdata', methods=['POST'])
@jwt_required()
@token_required
def fetchWeeklyRevisionsData():
    try:

        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            return jsonify(status="success", data=file_data, time=uploaded_time, from_date=from_date,to_date=to_date, revision=revision_no, role=uploaded_by)
        else:
            cursor.close()
            return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
            

        # return jsonify(message="Fetched Successfully")

    except Exception as e:
        log_error("weeklyrevisionsdata", e)
        return jsonify(message="There is Some Problem, Please contact SRLDC IT")
 


@app.route('/api/fetchrevisionsdata', methods=['POST'])
@jwt_required()
@token_required
def checkUploaded():
    try:

        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            return jsonify(status="success", data=file_data, time=uploaded_time, date=uploaded_date, revision=revision_no, role=uploaded_by)
        else:
            cursor.close()
            return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
    except Exception as e:
        log_error("fetchrevisionsdata", e)
        
        

    # return jsonify(message="Fetched Successfully")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


state_revision_numbers = {}


@app.route('/api/uploaddayahead', methods=['POST'])
@jwt_required()
@token_required
def uploadDayAheadDataAndFile():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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


            directory_path = os.path.join(shared_drive_path,"DAY_AHEAD", disabledDate,  state_name)

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
                    conn.commit()
                    cursor.close()
                    # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                    return jsonify({'message': 'Data and file uploaded successfully. Uploaded for Revision-{}'.format(len(existing_revs))})

            # file.save("D:\\forecast_excel_store\\"+file_name)
            # print("file saved successfully")
            # Process the form data and uploaded file as needed
            # You can access 'name' and 'email' here

            # return jsonify({'message': 'Data and file uploaded successfully'})
        else:
            return jsonify({'error': 'Invalid file type'})
        
    except Exception as e:
        log_error("uploaddayahead", e)
        cursor.close()
        return jsonify(message="There is problem in uploading, Please contact SRLDC IT!")

        
        # return jsonify(message="There is problem in uploading, Please contact SRLDC IT!")
    

@app.route("/api/downloaddayahead", methods=["POST"])
@jwt_required()
@token_required
def downloadDayAhead():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        # Parse the JSON input from the frontend
        data_json = request.get_json()
        state_id = data_json.get('state')
        upload_date = data_json.get('date')  # Expected in 'YYYY-MM-DD' format
        revision_no = data_json.get('revision')

        print(data_json)

        # Query the database to fetch the file_name (which is the file path)
        query = """
            SELECT file_name 
            FROM public.file_uploads 
            WHERE state_id = %s 
            AND upload_date = %s 
            AND revision_no = %s
        """
        cursor = conn.cursor()
        cursor.execute(query, (state_id, upload_date, revision_no))
        result = cursor.fetchone()

        if not result:
            print("File not found")
            return jsonify({'status': 'failure', 'error': 'File not found'}), 404

        # Extract the file path
        file_path = result[0]
        print(file_path)

        # Ensure the file exists before sending it
        if not os.path.exists(file_path):
            print("Path does not exists")
            cursor.close()
            return jsonify({'status': 'failure', 'error': 'File not found on server'}), 404

        # Send the file as an attachment
        return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        log_error("downloaddayahead", e)
        cursor.close()
        
        # cursor.close()
        return jsonify({'status': 'failure', 'error': str(e)}), 500



@app.route("/api/downloadweekahead", methods=["POST"])
@jwt_required()
@token_required
def downloadWeekAhead():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        # Parse the JSON input from the frontend
        data_json = request.get_json()
        state_id = data_json.get('state')
        upload_from_date = data_json.get('from_date')  # Expected in 'YYYY-MM-DD' format
        upload_to_date = data_json.get('to_date')
        revision_no = data_json.get('revision')

        print(data_json)

        # Query the database to fetch the file_name (which is the file path)
        query = """
            SELECT file_name 
            FROM public.week_ahead_file_uploads 
            WHERE state_id = %s 
            AND from_date = %s
            AND to_date = %s 
            AND revision_no = %s
        """
        cursor = conn.cursor()
        cursor.execute(query, (state_id, upload_from_date, upload_to_date, revision_no))
        result = cursor.fetchone()

        if not result:
            print("File not found")
            return jsonify({'status': 'failure', 'error': 'File not found'}), 404

        # Extract the file path
        file_path = result[0]
        print(file_path)

        # Ensure the file exists before sending it
        if not os.path.exists(file_path):
            print("Path does not exists")
            cursor.close()
            return jsonify({'status': 'failure', 'error': 'File not found on server'}), 404

        # Send the file as an attachment
        return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        log_error("downloadweekahead", e)
        cursor.close()
        
        # cursor.close()
        return jsonify({'status': 'failure', 'error': str(e)}), 500


@app.route("/api/downloadmonthahead", methods=["POST"])
@jwt_required()
@token_required
def downloadMonthAhead():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        # Parse the JSON input from the frontend
        data_json = request.get_json()
        state_id = data_json.get('state')
        upload_from_date = data_json.get('from_date')  # Expected in 'YYYY-MM-DD' format
        upload_to_date = data_json.get('to_date')
        revision_no = data_json.get('revision')

        print(data_json)

        # Query the database to fetch the file_name (which is the file path)
        query = """
            SELECT file_name 
            FROM public.month_ahead_file_uploads 
            WHERE state_id = %s 
            AND from_date = %s
            AND to_date = %s 
            AND revision_no = %s
        """
        cursor = conn.cursor()
        cursor.execute(query, (state_id, upload_from_date, upload_to_date, revision_no))
        result = cursor.fetchone()

        if not result:
            print("File not found")
            return jsonify({'status': 'failure', 'error': 'File not found'}), 404

        # Extract the file path
        file_path = result[0]
        print(file_path)

        # Ensure the file exists before sending it
        if not os.path.exists(file_path):
            print("Path does not exists")
            cursor.close()
            return jsonify({'status': 'failure', 'error': 'File not found on server'}), 404

        # Send the file as an attachment
        return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        log_error("downloadweekahead", e)
        cursor.close()
        
        # cursor.close()
        return jsonify({'status': 'failure', 'error': str(e)}), 500

@app.route('/api/pendingentries', methods=['GET'])
@jwt_required()
@token_required
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
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        log_error("pendingtimingentries", e)
        cursor.close()
        return jsonify(status="failure", message="There is a problem in fetching the data, Please contact SRLDC IT!")


@app.route('/api/getelementpreviouscodes', methods=['POST'])
@jwt_required()
@token_required
def getPreviousCodes():
    try:
        params = request.get_json()

        print(params)

        params = params["params"]
        from_date = params["from_date"]
        to_date = params["to_date"]
        feature_name = params.get("feature_name", "")  # Provide a default value if not present
        pwcEntityId = params.get("pwcEntityId", "")  # Provide a default value if not present


        


        # Create the payload to send in the POST request
        payload = json.dumps({
            "startDate": from_date,
            "endDate": to_date,
            "pwcEntityId": "",
            "elementId": "",
            "featureName": ""
        })

        headers = {
            "Content-Type": "application/json"
            # "Authorization": "Bearer your_token"  # If authentication is required
        }

        response = requests.post("https://oms2.srldc.in/Codebook/getElementPreviousCodes", data=payload, headers=headers)

        print(response.status_code)
        # print(response.json())

        header_data = dict(request.headers)
        # print(header_data)
        token = header_data['Authorization'].split()[1]
        x = decode_token(token, csrf_value=None, allow_expired=False)

        username = x['sub']   # username in database

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



        if response.status_code == 200:
            data = response.json()["data"]["previousCodes"]
            # print(data)
            # print(data['data']["previousCodes"].keys())
                    
            entities_data = []

            # print(data)

            id = 1

            if role == 'user':
                for i in data:
                    if (i["codeIssuedto"] in states_entities_dict[username] or i["codeRequestedby"] in states_entities_dict[username]):
                        entities_data.append({"id": id, "codeIssueTime": i["codeIssuedTime"], "elementType": i["entityFeatureName"], "elementName": i["elementName"], "switching": i["end"], "srldcCode": i["codeNo"], "category": i["outageCategory"], "codeIssuedTo": i["codeIssuedto"], "codeRequestedBy": i["codeRequestedby"], "codeId": i["codeId"], "isSelected": False})
                        id = id + 1
            
            else:
                for i in data:
                    # print(i.keys())
                    # print('constituentEnteredTime' in i.keys())
                    if (i["codeIssuedto"] in admin_states_list or i["codeRequestedby"] in admin_states_list):
                        entities_data.append({"id": id, "codeIssueTime": i["codeIssuedTime"], "elementType": i["entityFeatureName"], "elementName": i["elementName"], "switching": i["end"], "srldcCode": i["codeNo"], "category": i["outageCategory"], "codeIssuedTo": i["codeIssuedto"], "codeRequestedBy": i["codeRequestedby"],  "codeId": i["codeId"], "isSelected": False})
                        id = id + 1

            # print(type(entities_data[0]["codeIssueTime"]))
            # formatted_data_list = [{'date_key': datetime.strptime(item['date_key'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d/%m/%Y, %H:%M') for item in data_list]
                                
            for i in range(len(entities_data)):
                entities_data[i]["codeIssueTime"] = datetime.strptime(entities_data[i]["codeIssueTime"], '%Y-%m-%dT%H:%M:%S.%f').isoformat()
            
            # print(entities_data[0]["codeIssueTime"])

            if len(entities_data) == 0:
                return jsonify(status="failure", message="Data is Empty!")
        else:
            print(response.status_code)
            return jsonify(status="failure", message="There is a problem in fetching data, Please contact SRLDC IT!")
        return jsonify(status="success", message="Message fetched successfully!", data=entities_data )
    except Exception as e:
        # print(e)
        log_error("getpreviouscodes", e)
        cursor.close()
        return jsonify(status="failure", message="There is a problem in fetching the data, Please contact SRLDC IT!")
 

@app.route('/api/weekaheadformat')
@jwt_required()
@token_required
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
    
    except Exception as e:
        log_error("weekaheadformat", e)
        cursor.close()
        return jsonify(msg="Problem in fetching the data, Please contact SRLDC IT", status="failure")


@app.route('/api/monthaheadformat')
@jwt_required()
@token_required
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
    except Exception as e:
        log_error("monthaheadformat", e)
        cursor.close()
        return jsonify(status="failure", msg="Problem in Fetching the data, Please contact SRLDC IT!")



@app.route('/api/yearaheadformat')
@jwt_required()
@token_required
def yearheadFormat():
    try:
        def create_2d_list_for_year(start_date, end_date, num_blocks_per_day):
            data = []

            while start_date <= end_date:
                for block in range(num_blocks_per_day):
                    current_time = (datetime.min + timedelta(minutes=block * 60)).time()
                    next_time = (datetime.min + timedelta(minutes=(block + 1) * 60)).time()
                    row = [start_date.strftime('%Y-%m-%d'), block + 1] + [0] * 19
                    data.append(row)

                start_date += timedelta(days=1)

            return data

        # Get the current date
        today = datetime.now()
        
        # Define the financial year starting from the next April 1st
        if today.month >= 4:
            start_of_financial_year = datetime(today.year + 1, 4, 1)
            end_of_financial_year = datetime(today.year + 2, 3, 31)
        else:
            start_of_financial_year = datetime(today.year, 4, 1)
            end_of_financial_year = datetime(today.year + 1, 3, 31)

        # num_blocks_per_day = 24
        data_for_financial_year = create_2d_list_for_year(start_of_financial_year, end_of_financial_year, num_blocks_per_day=24)

        return jsonify(data=data_for_financial_year, status="success")
    
    except Exception as e:
        log_error("yearaheadformat", e)
        cursor.close()
        return jsonify(status="failure", msg="Problem in Fetching the data, Please contact SRLDC IT!")

    
@app.route('/api/submitentries', methods=['POST'])
@jwt_required()
@token_required
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
    except Exception as e:
        log_error("submittimingentries", e)
        cursor.close()
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
@token_required
def uploadWeekAheadDataAndFile():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
                        conn.commit()
                        cursor.close()
                        # cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                        return jsonify({'message': 'Data and file uploaded successfully. Uploaded for Revision-{0} '.format(len(existing_revs)), "status": "success"})

                    else:
                        cursor.execute("insert into week_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate,toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                        conn.commit()
                        cursor.close()
                        
                        # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                        return jsonify({'message': 'Data and file uploaded successfully. Uploaded for Revision-{0} '.format(len(existing_revs)), "status": "success"})

            # file.save("D:\\forecast_excel_store\\"+file_name)
            # print("file saved successfully")

        else:
            cursor.close()
            return jsonify({'error': 'Invalid file type'})

    except Exception as e:
        log_error("uploadweekahead", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
    


@app.route('/api/uploadmonthahead', methods=['POST'])
@jwt_required()
@token_required
def uploadMonthAheadDataAndFile():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            filename = f"{from_date}_{to_date}_{state_name}_rev{len(existing_revs)}.xlsx"

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
                        conn.commit()
                        cursor.close()
                        # cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                        return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs))})

                    else:
                        cursor.execute("insert into month_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate,toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                        conn.commit()
                        cursor.close()
                        # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                        return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs))})


        else:
            cursor.close()
            return jsonify({'error': 'Invalid file type'})

    except Exception as e:
        log_error("uploadmonthahead", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
        



@app.route('/api/fetchmonthrevisions', methods=['POST'])
@jwt_required()
@token_required
def fetchMonthRevisions():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            return jsonify(status="success", message="Fetched Successfully for '{0}'-'{1}'".format(from_date, to_date), revisions=revision_list, from_date=from_date, to_date=to_date)
        else:
            cursor.close()
            return jsonify(status="failure", message="There are no Uploads for state {0} for the month '{1}'-'{2}'".format(state_name, from_date, to_date)) 

    except Exception as e:
        log_error("fetchmonthrevisions", e)
        cursor.close()
        return jsonify(message="There is some problem in fetching the revisions! Please contact SRLDC IT", status="failure")
    

@app.route('/api/fetchmonthlyrevisionsdata', methods=['POST'])
@jwt_required()
@token_required
def fetchMonthlyRevisionsData():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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

            cursor.close()
            # print(len(file_data), len(file_data[0]))
            return jsonify(status="success", data=file_data, time=uploaded_time, from_date=from_date,to_date=to_date, revision=revision_no, role=uploaded_by)
        else:
            cursor.close()
            return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
            

        # return jsonify(message="Fetched Successfully")

    except Exception as e:
        log_error("fetchmonthlyrevisionsdata", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")


@app.route('/api/uploadyearahead', methods=['POST'])
@jwt_required()
@token_required
def uploadYearAheadDataAndFile():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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

            directory_path = os.path.join(shared_drive_path,"YEAR_AHEAD_FORECAST_FILES", from_date+"-"+ to_date, state_name)

            cursor.execute("select * from year_ahead_file_uploads where from_date = to_date('{0}', 'DD/MM/YYYY') and to_date = to_date('{1}','DD/MM/YYYY') and state_id = {2}".format(fromDate,toDate,  state))

            existing_revs = cursor.fetchall()


            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)

            # Get the current revision number for the state and increment it
            filename = f"{from_date}_{to_date}_{state_name}_rev{len(existing_revs)}.xlsx"

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
                        conn.commit()
                        cursor.close()
                        # cursor.execute("update file_contents set file_data =  '{0}' where state_id = {1} and upload_date = to_date('{2}', 'YYYY-MM-DD')".format( data, state, disabledDate))
                        return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs)), "status": "success"})

                    else:
                        cursor.execute("insert into year_ahead_file_uploads (state_id, from_date,to_date, upload_time, file_name, revision_no, uploaded_by, file_data) values({0}, to_date('{1}', 'DD/MM/YYYY'),to_date('{2}','DD/MM/YYYY'), to_timestamp('{3}', 'YYYY-MM-DD HH24:MI:SS'), '{4}', {5}, '{6}', '{7}')".format(state, fromDate,toDate, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file_path, len(existing_revs), role, data))
                        conn.commit()
                        cursor.close()
                        # cursor.execute("insert into file_contents (state_id, upload_date, file_data) values({0}, to_date('{1}', 'YYYY-MM-DD'), '{2}')".format(state, disabledDate, data))
                        return jsonify({'message': 'Data and file uploaded successfully. Uploaded with Revision-{0}'.format(len(existing_revs)), "status":"success"})
            # file.save("D:\\forecast_excel_store\\"+file_name)
            # print("file saved successfully")
            # Process the form data and uploaded file as needed
            # You can access 'name' and 'email' here

            # return jsonify({'message': 'Data and file uploaded successfully'})
        else:
            return jsonify({'error': 'Invalid file type'})

    except Exception as e:
        log_error("uploadyearahead", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")





@app.route('/api/fetchyearlyrevisionsdata', methods=['POST'])
@jwt_required()
@token_required
def fetchYearlyRevisionsData():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            # print(len(file_data), len(file_data[0]))
            cursor.c
            return jsonify(status="success", data=file_data, time=uploaded_time, from_date=from_date,to_date=to_date, revision=revision_no, role=uploaded_by)
            
        else:
            return jsonify(status="failure", message="There is a Problem in fetching the data, Please contact SRLDC IT!")
            

        return jsonify(message="Fetched Successfully")
    
    except Exception as e:
        log_error("fetchyearlyrevisionsdata", e)
        cursor.close()
        return jsonify(message="There is some problem in fetching the revisions data! Please contact SRLDC IT", status="failure")



@app.route('/api/fetchyearrevisions', methods=['POST'])
@jwt_required()
@token_required
def fetchYearRevisions():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
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
            cursor.close()
            return jsonify(status="success", message="Fetched Successfully for '{0}'-'{1}'".format(from_date, to_date), revisions=revision_list, from_date=from_date, to_date=to_date)
        else:
            cursor.close()
            return jsonify(status="failure", message="There are no Uploads for state {0} for the year '{1}'-'{2}'".format(state_name, from_date, to_date))    
    
    except Exception as e:
        log_error("fetchyearrevisions", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")






@app.route('/api/uploadstatus')
@jwt_required()
@token_required
def scatterPlotUploadStatus():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        # Day Ahead Data Processing
        end_date = datetime.now() + timedelta(days=1)
        start_date = end_date - timedelta(days=30)

        sql_query = """
                    WITH min_revision AS (
                    SELECT 
                        state_id, 
                        upload_date, 
                        MIN(revision_no) AS min_revision_no
                    FROM 
                        file_uploads
                    GROUP BY 
                        state_id, 
                        upload_date
                )
                SELECT 
                    states.state_name,
                    COALESCE(file_uploads.upload_date, %s) AS upload_date,
                    COALESCE(min_uploads.upload_time, NULL) AS upload_time,
                    CASE
                        WHEN min_uploads.upload_time IS NULL THEN 2  -- Not Uploaded
                        WHEN min_uploads.upload_time < (file_uploads.upload_date - INTERVAL '1 day' + INTERVAL '10 hours') THEN 1  -- Proper Upload before 10 AM on the previous day
                        ELSE 0  -- Late Upload
                    END AS upload_status_code,
                    COUNT(file_uploads.state_id) AS upload_count
                FROM 
                    states
                LEFT JOIN 
                    file_uploads ON states.state_id = file_uploads.state_id
                    AND file_uploads.upload_date BETWEEN %s AND %s
                LEFT JOIN (
                    SELECT 
                        file_uploads.state_id, 
                        file_uploads.upload_date, 
                        file_uploads.upload_time
                    FROM 
                        file_uploads
                    INNER JOIN min_revision ON 
                        file_uploads.state_id = min_revision.state_id
                        AND file_uploads.upload_date = min_revision.upload_date
                        AND file_uploads.revision_no = min_revision.min_revision_no
                ) AS min_uploads ON 
                    file_uploads.state_id = min_uploads.state_id 
                    AND file_uploads.upload_date = min_uploads.upload_date
                WHERE 
                    states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')
                GROUP BY 
                    states.state_name, 
                    file_uploads.upload_date,
                    min_uploads.upload_time  
                ORDER BY
                    states.state_name,
                    upload_date DESC;
        """
        cursor.execute(sql_query, (end_date, start_date, end_date))
        results = cursor.fetchall()

        day_data = []
        date_range = [end_date - timedelta(days=i) for i in range(30)]
        state_names = set(result[0] for result in results)

        for state_name in state_names:
            state_data = {"name": state_name, "data": []}
            for date in date_range:
                date_str = date.strftime('%Y-%m-%d')
                found_result = False
                for result in results:
                    if result[0] == state_name and result[1].strftime("%Y-%m-%d") == date_str:
                        upload_count = result[4]
                        upload_time = result[2].strftime("%Y-%m-%d %H:%M:%S") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break
                if not found_result:
                    upload_count = 0
                    upload_time = None
                    upload_status_code = 2  # Not Uploaded
                state_data["data"].append({
                    'x': date_str, 
                    'y': upload_status_code, 
                    'upload_time': upload_time, 
                    'upload_count': upload_count
                })
            day_data.append(state_data)

        day_dates = {
            "start_date": (start_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d')
        }


        # for i in day_data:
        #     print(i["name"])

        #######################################################################################################################################
        #######################################################################################################################################
        # Week Ahead Data Processing
                


        # Week Ahead Data Processing
        # Calculate date ranges
        today = datetime.now()
        # Get the start of this week (Monday)
        this_week_start = today - timedelta(days=today.weekday())

        # Setting date ranges
        start_date = this_week_start - timedelta(weeks=2)  # Start date two weeks before this week
        end_date = this_week_start + timedelta(weeks=3) - timedelta(days=1)  # End date two weeks after this week

        # Adjusting end_date to ensure it ends on the last day of the intended week
        if end_date.weekday() != 6:  # Check if end_date is not a Sunday
            end_date = end_date - timedelta(days=end_date.weekday() + 1)  # Adjust to the last Sunday before or on end_date

        sql_query = """
            WITH min_revision AS (
                SELECT 
                    state_id, 
                    from_date, 
                    MIN(revision_no) AS min_revision_no
                FROM 
                    week_ahead_file_uploads
                WHERE
                    from_date BETWEEN %s AND %s
                GROUP BY 
                    state_id, 
                    from_date
            ), min_uploads AS (
                SELECT 
                    fu.state_id, 
                    fu.from_date, 
                    fu.upload_time,
                    fu.revision_no
                FROM 
                    week_ahead_file_uploads fu
                INNER JOIN min_revision mr ON
                    fu.state_id = mr.state_id
                    AND fu.from_date = mr.from_date
                    AND fu.revision_no = mr.min_revision_no
            )
            SELECT 
                states.state_name,
                COALESCE(mu.from_date, %s) AS week_start_date,
                COALESCE(mu.upload_time, NULL) AS upload_time,
                CASE
                    WHEN mu.upload_time IS NULL THEN 2  -- Not Uploaded
                    WHEN mu.upload_time < DATE_TRUNC('week', mu.from_date - INTERVAL '1 week')  + INTERVAL '1 day' THEN 1  -- Uploaded on time, before the first working day of the week
                    ELSE 0  -- Late Upload
                END AS upload_status_code,
                COUNT(mu.state_id) AS upload_count
            FROM 
                states
            LEFT JOIN 
                min_uploads mu ON states.state_id = mu.state_id
            WHERE 
                states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')
            GROUP BY 
                states.state_name, 
                mu.from_date,
                mu.upload_time  
            ORDER BY
                states.state_name,
                mu.from_date DESC;
        """
        cursor.execute(sql_query, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        results = cursor.fetchall()


        cursor.execute("SELECT state_name FROM states WHERE username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')")
        all_states = [row[0] for row in cursor.fetchall()]

        week_range = sorted([(start_date + timedelta(weeks=i)).date() for i in range(5)], reverse=True)  # Generate Mondays for 6 weeks

        week_data = []
        for state_name in all_states:
            state_data = {"name": state_name, "data": []}
            for week_start in week_range:
                week_start_date = week_start
                week_end_date = week_start_date + timedelta(days=6)  # End on Sunday
                week_range_str = f"{week_start_date.strftime('%Y-%m-%d')} to {week_end_date.strftime('%Y-%m-%d')}"

                upload_count = 0
                upload_status_code = 2  # Default to Not Uploaded
                upload_time = None
                found_result = False
                for result in results:
                    if result[0] == state_name and result[1] == week_start_date:
                        upload_count = result[4]
                        upload_time = result[2].strftime("%Y-%m-%d %H:%M:%S") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break

                if not found_result:
                    upload_count = 0
                    upload_status_code = 2  # Not Uploaded
                state_data["data"].append({'x': week_range_str, 'y': upload_status_code, 'upload_time': upload_time, 'upload_count': upload_count})
            week_data.append(state_data)

        week_dates = {
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d')
        }






        #######################################################################################################################################
        #######################################################################################################################################
        # Month Ahead Data Processing

        today = datetime.now()
        start_of_current_month = today.replace(day=1)
        month_ranges = [subtract_months(start_of_current_month, i) for i in range(1, 4)]

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
            WHERE states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')
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

        cursor.execute("SELECT state_name FROM states WHERE username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')")
        all_states = [row[0] for row in cursor.fetchall()]

        month_data = []
        for state_name in all_states:
            state_data = {"name": state_name, "data": []}
            for month_start in month_ranges:
                last_day_of_month = monthrange(month_start.year, month_start.month)[1]
                month_end = month_start.replace(day=last_day_of_month)
                month_range_str = f"{month_start.strftime('%Y-%m-%d')} to {month_end.strftime('%Y-%m-%d')}"

                upload_count = 0
                upload_status_code = 2  # Default to Not Uploaded
                upload_time = None
                found_result = False
                for result in results:
                    if result[0] == state_name and result[1] == month_start:
                        upload_count = result[4]
                        upload_time = result[2].strftime("%Y-%m-%d %H:%M:%S") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break

                if not found_result:
                    upload_count = 0
                state_data["data"].append({'x': month_range_str, 'y': upload_status_code, 'upload_time': upload_time, 'upload_count': upload_count})
            month_data.append(state_data)

        month_dates = {
            "start_date": month_ranges[-1].strftime('%Y-%m-%d'),
            "end_date": (start_of_current_month - timedelta(days=1)).strftime('%Y-%m-%d')
        }
        cursor.close()
        return jsonify(day=day_data, week=week_data, month=month_data, day_dates=day_dates, week_dates=week_dates, month_dates=month_dates, status="success")
    
    except Exception as e:
        # print(error)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        log_error("uploadstatus", e)
        cursor.close()
        # return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
        return jsonify(message="There is a problem, please contact SRLDC IT!", status="failure")




@app.route('/api/mapechart', methods=['POST'])
@jwt_required()
@token_required
def mapeChart():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        params = request.get_json()
        print(params)

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

        print(len(actual_data))

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

            print(actual_day_df)
            

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

        cursor.close()

        return jsonify(status="success", data=final_data, title="MAPE for the data between {0} and {1} for {2}".format(from_date, to_date, state_name ))

    except Exception as e:
        log_error("mapechart", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")

    
    



@app.route('/api/dayrangestatus', methods=['POST'])
@jwt_required()
@token_required
def dayRangeStatus():
    try:
        # Retrieve date range from request
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        params = request.get_json()
        print(params)

        start_date = datetime.strptime(params["params"]["fromDate"], '%d/%m/%Y')
        end_date = datetime.strptime(params["params"]["toDate"], '%d/%m/%Y')

        # SQL query to fetch data within the specified date range
        sql_query = """
                    WITH min_revision AS (
                    SELECT 
                        state_id, 
                        upload_date, 
                        MIN(revision_no) AS min_revision_no
                    FROM 
                        file_uploads
                    GROUP BY 
                        state_id, 
                        upload_date
                )
                SELECT 
                    states.state_name,
                    COALESCE(file_uploads.upload_date, %s) AS upload_date,
                    COALESCE(min_uploads.upload_time, NULL) AS upload_time,
                    CASE
                        WHEN min_uploads.upload_time IS NULL THEN 2  -- Not Uploaded
                        WHEN min_uploads.upload_time < (file_uploads.upload_date - INTERVAL '1 day' + INTERVAL '10 hours') THEN 1  -- Proper Upload before 10 AM on the previous day
                        ELSE 0  -- Late Upload
                    END AS upload_status_code,
                    COUNT(file_uploads.state_id) AS upload_count
                FROM 
                    states
                LEFT JOIN 
                    file_uploads ON states.state_id = file_uploads.state_id
                    AND file_uploads.upload_date BETWEEN %s AND %s
                LEFT JOIN (
                    SELECT 
                        file_uploads.state_id, 
                        file_uploads.upload_date, 
                        file_uploads.upload_time
                    FROM 
                        file_uploads
                    INNER JOIN min_revision ON 
                        file_uploads.state_id = min_revision.state_id
                        AND file_uploads.upload_date = min_revision.upload_date
                        AND file_uploads.revision_no = min_revision.min_revision_no
                ) AS min_uploads ON 
                    file_uploads.state_id = min_uploads.state_id 
                    AND file_uploads.upload_date = min_uploads.upload_date
                WHERE 
                    states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')
                GROUP BY 
                    states.state_name, 
                    file_uploads.upload_date,
                    min_uploads.upload_time  
                ORDER BY
                    states.state_name,
                    upload_date DESC;
        """
        cursor.execute(sql_query, (end_date, start_date, end_date))
        results = cursor.fetchall()

        day_data = []
        date_range = [end_date - timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        state_names = set(result[0] for result in results)

        for state_name in state_names:
            state_data = {"name": state_name, "data": []}
            for date in date_range:
                date_str = date.strftime('%Y-%m-%d')
                found_result = False
                for result in results:
                    if result[0] == state_name and result[1].strftime("%Y-%m-%d") == date_str:
                        upload_count = result[4]
                        upload_time = result[2].strftime("%Y-%m-%d %H:%M:%S") if result[2] is not None else None
                        upload_status_code = result[3]
                        found_result = True
                        break
                if not found_result:
                    upload_count = 0
                    upload_time = None
                    upload_status_code = 2  # Not Uploaded
                state_data["data"].append({
                    'x': date_str, 
                    'y': upload_status_code, 
                    'upload_time': upload_time, 
                    'upload_count': upload_count
                })
            day_data.append(state_data)

        day_dates = {
            "start_date": (start_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d')
        }

        return jsonify(day=day_data, status="success")

    except Exception as e:
        log_error("dayrangestatus", e)
        cursor.close()
        # return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
        return jsonify(message="There is a problem, please contact SRLDC IT!", status="failure")





@app.route('/api/weekrangestatus', methods=['POST'])
@jwt_required()
@token_required
def weekRangeStatus():
    try:
        conn = psycopg2.connect(
        database="demand_forecast_states", user='prasadbabu', 
        password='BabuPrasad#123', host='10.0.100.79', port='5432'
        )
        cursor = conn.cursor()
        # Retrieve date range from request
        params = request.get_json()
        # print(params)
        # Parse start and end dates from the JSON input
        # Parse start and end dates from the JSON input
        # Parse start and end dates from the JSON input
        custom_start_date = datetime.strptime(params["params"]["fromDate"], '%d/%m/%Y').date()
        custom_end_date = datetime.strptime(params["params"]["toDate"], '%d/%m/%Y').date()

        # Adjust start date to the start of the week (Monday)
        week_range = []
        week_start = custom_start_date - timedelta(days=custom_start_date.weekday())  # Start of the week
        while week_start <= custom_end_date:
            week_range.append(week_start)
            week_start += timedelta(weeks=1)

        week_range = sorted(week_range, reverse=True)

        # SQL query for fetching data within the custom date range
        sql_query = """
            WITH min_revision AS (
                SELECT 
                    state_id, 
                    from_date, 
                    MIN(revision_no) AS min_revision_no
                FROM 
                    week_ahead_file_uploads
                WHERE
                    from_date BETWEEN %s AND %s
                GROUP BY 
                    state_id, 
                    from_date
            ), min_uploads AS (
                SELECT 
                    fu.state_id, 
                    fu.from_date, 
                    fu.upload_time,
                    fu.revision_no
                FROM 
                    week_ahead_file_uploads fu
                INNER JOIN min_revision mr ON
                    fu.state_id = mr.state_id
                    AND fu.from_date = mr.from_date
                    AND fu.revision_no = mr.min_revision_no
            )
            SELECT 
                states.state_name,
                mu.from_date AS week_start_date,
                mu.upload_time,
                CASE
                    WHEN mu.upload_time IS NULL THEN 2  -- Not Uploaded
                    WHEN mu.upload_time < DATE_TRUNC('week', mu.from_date - INTERVAL '1 week')  + INTERVAL '1 day' THEN 1  -- Uploaded before the Monday of the previous week
                    ELSE 0  -- Late Upload
                END AS upload_status_code
            FROM 
                states
            LEFT JOIN 
                min_uploads mu ON states.state_id = mu.state_id
            WHERE 
                states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')
            GROUP BY 
                states.state_name, 
                mu.from_date,
                mu.upload_time  
            ORDER BY
                states.state_name,
                mu.from_date DESC;
        """
        cursor.execute(sql_query, (custom_start_date.strftime('%Y-%m-%d'), custom_end_date.strftime('%Y-%m-%d')))
        results = cursor.fetchall()

        # Fetch state names
        cursor.execute("SELECT state_name FROM states WHERE username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')")
        all_states = [row[0] for row in cursor.fetchall()]

        # Initialize data structure for states
        week_data = [{"name": state_name, "data": []} for state_name in all_states]

        # Process each state and week range
        # Process each state and week range
        for state in week_data:
            for week_start in week_range:
                week_end = week_start + timedelta(days=6)  # End of the week
                # Find relevant upload data for the state and week
                upload_info = next((item for item in results if item[0] == state["name"] and item[1] is not None and week_start <= item[1] <= week_end), None)
                if upload_info:
                    upload_status_code = upload_info[3]
                    upload_time = upload_info[2].strftime('%Y-%m-%d %H:%M:%S') if upload_info[2] else None
                    upload_count = 1  # Assuming at least one upload exists
                else:
                    upload_status_code = 2  # Not Uploaded
                    upload_time = None
                    upload_count = 0
                # Append data for the week
                state["data"].append({
                    "x": f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}",
                    "y": upload_status_code,
                    "upload_time": upload_time,
                    "upload_count": upload_count
                })

        return jsonify(week=week_data, status="success")

    except Exception as e:
        log_error("weekrangestatus", e)
        cursor.close()
        # return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
        return jsonify(message="There is a problem, please contact SRLDC IT!", status = "failure")




@app.route('/api/monthrangestatus', methods=['POST'])
@jwt_required()
@token_required
def monthRangeStatus():
    try:
        # Get the current date
        today = datetime.now()

        # Retrieve date range from request
        params = request.get_json()
        print(params)

        start_date = datetime.strptime(params["params"]["fromDate"], '%d/%m/%Y')
        end_date = datetime.strptime(params["params"]["toDate"], '%d/%m/%Y')

        # Calculate the start of the first month in the custom range
        start_of_first_month = start_date.replace(day=1)
        end_of_last_month = end_date.replace(day=1)

        # Create list of start dates for each month in the custom range
        month_ranges = []
        current_month = start_of_first_month
        while current_month <= end_of_last_month:
            month_ranges.append(current_month)
            # Move to the next month
            next_month = (current_month.month % 12) + 1
            next_year = current_month.year + (current_month.month // 12)
            current_month = current_month.replace(year=next_year, month=next_month, day=1)

        # SQL query to fetch upload counts by state and month within the custom date range
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
            WHERE states.username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')
            GROUP BY 
                states.state_name, 
                month_start_date,
                month_ahead_file_uploads.upload_time,
                month_ahead_file_uploads.from_date
            ORDER BY
                states.state_name,
                month_start_date DESC
        """
        cursor.execute(sql_query, (end_date, end_date, start_date, end_date))
        results = cursor.fetchall()

        # Fetch all states
        cursor.execute("SELECT state_name FROM states WHERE username NOT IN ('admin', 'pgcil_sr_1', 'pgcil_sr_2', 'sr_internal')")
        all_states = [row[0] for row in cursor.fetchall()]

        # Data structure for JSON output
        data = []
        for state_name in all_states:
            state_data = {"name": state_name, "data": []}
            for month_start in month_ranges:
                # Get the last day of the current month
                last_day_of_month = monthrange(month_start.year, month_start.month)[1]
                month_end = month_start.replace(day=last_day_of_month)
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
        return jsonify(month=month_data, status="success")

    except Exception as e:
        log_error("monthrangestatus", e)
        cursor.close()
        # return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
        return jsonify(message="There is a problem, please contact SRLDC IT!")

    
# Special /data endpoint only accessible by script token
@app.route('/api/data', methods=['POST'])
@jwt_required()
@token_required
def get_data():
    data = request.get_json()
    state_id = data.get('state')
    input_from_date = data.get('from_date')
    input_to_date = data.get('to_date')

    conn = psycopg2.connect(
    database="demand_forecast_states", user='prasadbabu', 
    password='BabuPrasad#123', host='10.0.100.79', port='5432'
    )

    cursor = conn.cursor()

    print(f"State ID: {state_id}, From Date: {input_from_date}, To Date: {input_to_date}")

    if not (state_id and input_from_date and input_to_date):
        return jsonify({'error': 'Missing data for state_id, from_date, or to_date'}), 400

    try:


        # Updated SQL query to filter by state_id, from_date, and to_date
        query = """
        SELECT
          state_id,
          from_date,
          to_date,
          revision_no,
          upload_time,
          file_data
        FROM (
          SELECT
            state_id,
            from_date,
            to_date,
            revision_no,
            upload_time,
            file_data,
            ROW_NUMBER() OVER (PARTITION BY state_id, from_date, to_date ORDER BY upload_time DESC) as rn
          FROM
            week_ahead_file_uploads
          WHERE state_id = %s AND from_date >= %s AND to_date <= %s
        ) sub
        WHERE sub.rn = 1;
        """

        cursor.execute(query, (state_id, input_from_date, input_to_date))
        records = cursor.fetchall()

        df_list = []

        results = []
        columns = ['Date', 'Block', 'Period', 'Forcasted Demand_MW (A)', 'From its own Sources Excl. Renewable_THERMAL_MW', 'From its own Sources Excl. Renewable_GAS_MW','From its own Sources Excl. Renewable_HYDRO_MW', 'From its own Sources Excl. Renewable_TOTAL (B)_MW', 'From Renewable Sources_SOLAR_MW', 'From Renewable Sources_WIND_MW', 'From Renewable Sources_Other RES (biomass)_MW', 'From Renewable Sources_TOTAL (C)_MW', 'From ISGS & Other LTA & MTOA (D)_MW', 'From Bilateral Transaction (Advance+ FCFS) (E)_MW', 'Total Availability  (F)= (B+C+D+E)_MW', 'Gap between Demand & Availability (G) = (A)-(F)  Surplus(-) / Deficit (+)_MW' , 'Proposed Procurement_Under Bilateral Transaction (Day Ahead+ Contingency) (H)_MW', 'Proposed Procurement_Through Power Exchange (I)_MW', 'Shortages after day ahead procurement from market (J) =(G)-(H+I)  Surplus(-) / Deficit (+)_MW', 'Relief through planned restrictions/ rostering/ power cuts (K)_MW','Additional Load shedding proposed (L) = (J)-(K) Surplus(-) / Deficit (+)_MW', 'Reactive Power Forecast_MVar' ]

        for record in records:
            from_date = record[1]  # From Date
            to_date = record[2]    # To Date
            
            # Generate the Date column based on from_date and to_date
            date_range = generate_date_range(from_date, to_date)

            # Ensure the generated date list has the correct length to match the rows
            if len(date_range) != len(record[5]):
                raise ValueError(f"Generated date range length {len(date_range)} does not match file data length {len(record[5])}")

            # Replace "Invalid Date" with the actual date range
            file_data = record[5]
            for i, row in enumerate(file_data):
                row[0] = date_range[i]  # Assign the correct date to the first column
            
            result = {
                "State ID": record[0],
                "From Date": from_date.isoformat(),
                "To Date": to_date.isoformat(),
                "Revision No": record[3],
                "Upload Time": record[4].isoformat(),
                "File Data": file_data
            }

            # Create DataFrame from the updated File Data
            df_file_data = pd.DataFrame(result["File Data"], columns=columns)
            df_list.append(df_file_data)

        if not df_list:
            return jsonify({'error': 'No data present for this period'}), 500


        final_df = pd.concat(df_list, ignore_index=True)
        final_df['Date'] = pd.to_datetime(final_df['Date'], dayfirst = True)
        df_json = final_df.to_json(orient='records', date_format='iso')  # 'records' is good for row-wise format

        cursor.close()
        conn.close()

        return jsonify(df_json)

    except Exception as e:
        print(f"Database connection or SQL execution error: {e}")
        log_error("data query", e)
        return jsonify({'error': 'Database query failed'}), 500

    




##################### LINEFLOWS REPORT



@app.route("/api/reports/lineflows", methods=["POST"])
@jwt_required()
@token_required
def displayLineFlows():
    try:
        input_dat = request.get_json()
        start_date = datetime.strptime(input_dat['params']['fromDate'].replace('"', ''), '%d/%m/%Y').date()
        end_date = datetime.strptime(input_dat['params']['toDate'].replace('"', ''), '%d/%m/%Y').date()


        # Get columns data
        cur.execute("""
            SELECT col_name, out_mwh_columns.formula as formula, col_seq_no, item, col_type, out_mwh_columns.startdatetime as startdatetime, out_mwh_columns.enddatetime as enddatetime
            FROM out_mwh_config join out_mwh_columns on out_mwh_config.id = out_mwh_columns.item_fk_id
            WHERE item = 'LFL_MWH' AND out_mwh_columns.startdatetime <= %s;
        """, (end_date,))
        columns_data = cur.fetchall()
        columns_df = pd.DataFrame(columns_data, columns=['col_name', 'formula', 'col_seq_no', 'item', 'col_type', 'startdatetime', 'enddatetime'])

        # Regular expression pattern
        pattern = r"[-+]?[A-Za-z0-9]+-[A-Za-z0-9]+\s*"
        for i, col in columns_df.iterrows():
            if col['formula']:
                matches = re.findall(pattern, col['formula'])
                if col['col_type'] in ['SINGLE', 'FREQ'] and len(matches) >= 1:
                    columns_df.at[i, 'neg_factor'] = -1 if col['formula'][0] == '-' else 1
                    columns_df.at[i, 'formula'] = matches[0]
                else:
                    columns_df.at[i, 'neg_factor'] = 1

        columns_df = columns_df.sort_values('col_seq_no').copy()

        # print(columns_df)

        # Get fict computed list
        cur.execute("""
            SELECT DISTINCT short_location, startdate, time, mwh
            FROM fict_computation
            WHERE startdate BETWEEN %s AND %s;
        """, (start_date, end_date))
        fict_computed_list = pd.DataFrame(cur.fetchall(), columns=['short_location', 'startdate', 'time', 'mwh'])

        # print(fict_computed_list.head())

        # Get NPC meter data
        cur.execute("""
            SELECT DISTINCT startdate, time, meterno, mwh
            FROM npcmeterdata
            WHERE startdate BETWEEN %s AND %s;
        """, (start_date, end_date))
        queryset_npc = pd.DataFrame(cur.fetchall(), columns=['startdate', 'time', 'meterno', 'mwh'])

        # Get replaced meter data
        cur.execute("""
            SELECT DISTINCT find_meterno, startdate, time, mwh
            FROM replaced_meter_data
            WHERE startdate BETWEEN %s AND %s;
        """, (start_date, end_date))
        replaced_query_set = pd.DataFrame(cur.fetchall(), columns=['find_meterno', 'startdate', 'time', 'mwh'])

        # Get fict meters locations
        cur.execute("""
            SELECT short_location
            FROM create_fictmeter
            WHERE end_date_time >= CURRENT_TIMESTAMP OR end_date_time IS NULL;
        """)
        fict_meters_locations = [loc[0] for loc in cur.fetchall()]

        # Get real meter data
        cur.execute("""
            SELECT meter_number, short_location, start_date_time, end_date_time
            FROM create_meter;
        """)
        realmeter_obj = pd.DataFrame(cur.fetchall(), columns=['meter_number', 'short_location', 'start_date_time', 'end_date_time'])        

        # print(realmeter_obj.head())

            # folder creation
        # directory=create_folder(start_date,end_date)
        entity_df=generate_dataframe_forrange(start_date,end_date)

        for _,col in columns_df.iterrows():
            # below is to check whether column is Single fict like (AP-NEW)
            if col['col_type'] in ['SINGLE'] :
                # this column is there but no fict formula so just keep the column in output csv
                if col['formula']!= None and col['formula']!='' and len(col['formula']) > 0 :
                    # checking fict meter first
                    full_data_df = fict_computed_list[(fict_computed_list["short_location"] == col["formula"]) & (fict_computed_list["startdate"].between(start_date, end_date, inclusive="both"))][["startdate", "time", "mwh"]]
                    full_data_df.rename(columns={'startdate': 'DATE', 'time': 'TIME', 'mwh': 'mwh1'}, inplace=True)

                    if not full_data_df.empty:
                        #replace None with --
                        full_data_df.fillna('--',inplace=True)
                        entity_df=pd.merge(entity_df, full_data_df, on=['DATE', 'TIME'], how='left')
                        entity_df.rename(columns={'mwh1':col['col_name']} , inplace=True)
                    elif col['formula'] in fict_meters_locations:
                        # fict meter but not computed
                        entity_df=_column(entity_df , col['col_name'] )
                    else:
                        # if it is real meter but replaced for particular week
                        # replaced_meter_data_df=pd.DataFrame(replaced_queryset.filter(find_meterno=col['outmwhcolumns__formula']).values(**{'DATE':F('startdate'),'TIME':F('time'),'mwh1':F('mwh') }),columns=['DATE','TIME','mwh1'] )
                        replaced_meter_data_df = replaced_query_set[(replaced_query_set["find_meterno"] == col["formula"]) & (replaced_query_set["startdate"].between(start_date, end_date, inclusive="both"))][["startdate", "time", "mwh"]]
                        replaced_meter_data_df.rename(columns={'startdate': 'DATE', 'time': 'TIME', 'mwh': 'mwh1'}, inplace=True)

                        # first get the meterno corresponding short location
                        # meterno_obj=realmeter_obj.filter( Q(short_location=col['outmwhcolumns__formula']) ,( Q(end_date_time__range=[start_date,end_date] )| Q(end_date_time__isnull=True) ) )
                        # realmeter_obj['end_date_time'] = realmeter_obj['end_date_time'].dt.date
                        
                        meterno_obj = realmeter_obj[(realmeter_obj["short_location"] == col['formula']) & ((realmeter_obj["end_date_time"].between(pd.to_datetime(start_date).tz_localize('UTC'), pd.to_datetime(end_date).tz_localize('UTC'), inclusive="both")) | (realmeter_obj["end_date_time"].isnull()) )]

                        real_meter_data_df=pd.DataFrame([],columns=['DATE','TIME'])


                        for m, mtr in meterno_obj.iterrows():
                            # temp_multi_real_df=pd.DataFrame( queryset_npc.filter(meterno=mtr.meter_number).values(**{'DATE':F('startdate'),'TIME':F('time'),'mwh1':F('mwh') }) ,columns=['DATE','TIME','mwh1'])
                            
                            temp_multi_real_df = queryset_npc[queryset_npc["meterno"] == mtr["meter_number"]][["startdate", "time", "mwh"]]
                            temp_multi_real_df.rename(columns={'startdate': 'DATE', 'time': 'TIME', 'mwh': 'mwh1'}, inplace=True)

                            temp_multi_real_df=check_start_enddate_col(temp_multi_real_df ,mtr["start_date_time"] , mtr["end_date_time"],'mwh1')

                            real_meter_data_df=pd.concat([real_meter_data_df,temp_multi_real_df])
                        
                        replaced_meter_data_df.set_index(['DATE', 'TIME'], inplace=True)
                        real_meter_data_df.set_index(['DATE', 'TIME'], inplace=True)

                        if not real_meter_data_df.empty:
                            # Update values in real_meter_data_df with corresponding values from replaced_meter_data_df based on the index (DATE, TIME)
                            real_meter_data_df.update(replaced_meter_data_df)
                            # Reset the index to columns
                            real_meter_data_df.reset_index(inplace=True)
                            
                            # print("ENTITY_DF")
                            # print(entity_df.head())
                            # print("REAL_METER_DF")
                            # print(real_meter_data_df.head())

                            entity_df=pd.merge(entity_df, real_meter_data_df[["DATE", "TIME", "mwh1"]], on=['DATE', 'TIME'], how='left')
                            entity_df.rename(columns={'mwh1':col['col_name']} , inplace=True)
                        elif not replaced_meter_data_df.empty:
                            # if real meter data not present but replaced meter data presents then updat entity_df with only replaced duration
                            # Reset the index to columns
                            replaced_meter_data_df.reset_index(inplace=True)

                            # print("ENTITY_DF")
                            # print(entity_df.head())
                            # print("REPLACED_METER_DF")
                            # print(replaced_meter_df.head())

                            entity_df=pd.merge(entity_df, replaced_meter_data_df, on=['DATE', 'TIME'], how='left')
                            entity_df.rename(columns={'mwh1':col['col_name']} , inplace=True)
                        else:
                            entity_df=_column(entity_df , col['col_name'] )
                    
                    # finally multiplying with negative factor
                    entity_df[col['col_name']]=(entity_df[col['col_name']]) * int(col['neg_factor']) 

                else: 
                    # this else no fict formula but to keep the column in output file to match the srpc format
                    entity_df=_column(entity_df , col['col_name'] )

            elif col['col_type'] in ['MULTI'] :
                short_locations=set(split_string(col['formula']))
                multi_df=generate_dataframe_forrange(start_date,end_date)


                for loct in short_locations:
                    modified_loc=loct.replace('(','').replace(')','')
                    # fist check if it is fict meter else real meter
                    # multi_fict_data_df=pd.DataFrame( fict_computed_list.filter(short_location= modified_loc , startdate__range=[start_date,end_date]).values(**{'DATE':F('startdate'),'TIME':F('time'), loct:F('mwh') } ) , columns=['DATE','TIME',loct])
                    multi_fict_data_df = fict_computed_list[(fict_computed_list["short_location"] == modified_loc) & (fict_computed_list["startdate"].between(start_date, end_date, inclusive="both"))]
                    multi_fict_data_df.rename(columns={'startdate': 'DATE', 'time': 'TIME', 'mwh': loct}, inplace=True)

                    if not multi_fict_data_df.empty:
                        multi_fict_data_df.fillna('--',inplace=True)
                        multi_df=pd.merge(multi_df, multi_fict_data_df, on=['DATE', 'TIME'], how='inner')

                    elif modified_loc in fict_meters_locations:
                        multi_df=_column(multi_df , loct )

                    else:
                        # if it is real meter but replaced for particular week
                        # replaced_meter_data_df=pd.DataFrame(replaced_queryset.filter(find_meterno=modified_loc).values(**{'DATE':F('startdate'),'TIME':F('time'),loct:F('mwh') }),columns=['DATE','TIME',loct] )

                        replaced_meter_data_df = replaced_query_set[(replaced_query_set["find_meterno"] == modified_loc) ][["startdate", "time", "mwh"]]
                        replaced_meter_data_df.rename(columns={'startdate': 'DATE', 'time': 'TIME', 'mwh': loct}, inplace=True)

                        # meterno_obj=realmeter_obj.filter( Q(short_location=modified_loc) , ( Q(end_date_time__range=[start_date,end_date] )| Q(end_date_time__isnull=True) ) )

                        meterno_obj = realmeter_obj[(realmeter_obj["short_location"] == modified_loc) & ((realmeter_obj["end_date_time"].between(pd.to_datetime(start_date).tz_localize('UTC'), pd.to_datetime(end_date).tz_localize('UTC'), inclusive="both")) | (realmeter_obj["end_date_time"].isnull()) )]


                        real_meter_data_df=pd.DataFrame([],columns=['DATE','TIME'])

                        for m, mtr in meterno_obj.iterrows():
                            # temp_multi_real_df=pd.DataFrame( queryset_npc.filter(meterno=mtr.meter_number).values(**{'DATE':F('startdate'),'TIME':F('time'),'mwh1':F('mwh') }) ,columns=['DATE','TIME','mwh1'])
                            
                            temp_multi_real_df = queryset_npc[queryset_npc["meterno"] == mtr["meter_number"]][["startdate", "time", "mwh"]]
                            temp_multi_real_df.rename(columns={'startdate': 'DATE', 'time': 'TIME', 'mwh': loct}, inplace=True)

                            temp_multi_real_df=check_start_enddate_col(temp_multi_real_df ,mtr["start_date_time"] , mtr["end_date_time"],loct)

                            real_meter_data_df=pd.concat([real_meter_data_df,temp_multi_real_df])
                        
                        replaced_meter_data_df.set_index(['DATE', 'TIME'], inplace=True)
                        real_meter_data_df.set_index(['DATE', 'TIME'], inplace=True)

                        if not real_meter_data_df.empty:
                            # Update values in real_meter_data_df with corresponding values from replaced_meter_data_df based on the index (DATE, TIME)
                            real_meter_data_df.update(replaced_meter_data_df)
                            # Reset the index to columns
                            real_meter_data_df.reset_index(inplace=True)

                            multi_df=pd.merge(multi_df, real_meter_data_df[["DATE", "TIME", loct]], on=['DATE', 'TIME'], how='left')
                        elif not replaced_meter_data_df.empty:
                            # if real meter data not present but replaced meter data presents then updat entity_df with only replaced duration
                            # Reset the index to columns
                            replaced_meter_data_df.reset_index(inplace=True)

                            multi_df=pd.merge(multi_df, replaced_meter_data_df, on=['DATE', 'TIME'], how='left')   
                        else:  
                            multi_df=_column(multi_df , loct )

                if not multi_df.empty:
                    multi_df[col['col_name']] = multi_df.apply(calculate_formula,args=(short_locations, col['formula']), axis=1)
                else: 
                    multi_df=_column(multi_df , col['col_name'] )

                multi_df.drop(columns=short_locations,inplace=True)
                entity_df=pd.merge(entity_df, multi_df, on=['DATE', 'TIME'], how='left')


            else:
                pass
            
            #skip if col_type is DATE,TIME and TOTAL
            if col['col_type'] not in ['DATE','TIME','TOTAL']:
                # if startdatetime is greater than current date then putting -- as mwh1 else original data 
                new_frame_df=entity_df.copy()
                new_frame_df['DATETIME'] = pd.to_datetime(new_frame_df['DATE'].astype(str) + ' ' + new_frame_df['TIME'].astype(str) ,  errors='coerce')
                new_frame_df['DATETIME'] = new_frame_df['DATETIME'].apply(lambda x: x.tz_localize(None))

                temp_timestamp=pd.to_datetime(col['startdatetime']).tz_convert(None)
                temp_endtimestamp=pd.to_datetime(col['enddatetime'],errors='coerce')
                
                # temp_timestamp = temp_timestamp.apply(lambda x: x.tz_localize(None))
                # temp_endtimestamp = temp_endtimestamp.apply(lambda x: x.tz_localize(None))
            
                # print(new_frame_df.dtypes)

                if pd.isnull(temp_endtimestamp):
                    # Handle the invalid timestamps by replacing them with a default value
                    default_endtimestamp = pd.to_datetime('2050-01-01')
                else:
                    default_endtimestamp = temp_endtimestamp.tz_convert(None)

                record_dt_time_condition=new_frame_df['DATETIME'].apply(lambda dt: dt >= temp_timestamp and dt <= default_endtimestamp )

                new_frame_df.loc[~(record_dt_time_condition), col['col_name']] = '--'
                new_frame_df.drop(columns=['DATETIME'],inplace=True)
                entity_df=new_frame_df.copy()

        entity_df=entity_df.fillna('--')
        new_frame_df=entity_df.copy()

        if not new_frame_df.empty:
            new_frame_df.set_index(['DATE', 'TIME'], inplace=True)
            # Specify columns to include in calculations
            columns_to_include = new_frame_df.columns.difference(['DATE', 'TIME'])

            new_frame_df[new_frame_df.columns[2:]] = new_frame_df[new_frame_df.columns[2:]].apply(pd.to_numeric, errors='coerce')

            # Apply the function column-wise on the selected columns
            result_df = new_frame_df[columns_to_include].apply(calculate_column_stats, axis=0)
            try:
                # to rearrange the column order
                result_df = result_df[entity_df.columns[2:]]
            except Exception as e: 
                extractdb_errormsg(e)
            # Transpose the result DataFrame
            result_df = result_df.T
            result_df.reset_index(inplace=True)
            result_df.rename( columns={'Pos_Sum':'Export (MU)','Pos_Max':'Maximum Power Flow (MW)','Neg_Sum':'Import (MU)','Neg_Max':'Maximum Power Flow (MW)(I)' ,'index':'NAME OF THE LINE'},inplace=True ) 
        else:
            result_df=pd.DataFrame(['No data found , Please check'])

        filename='line_flows_'+start_date.strftime('%d-%m-%y')+'.xlsx'
        
        entity_df.set_index('DATE', inplace=True)

        df = entity_df
        df.columns = [col[:-2] if col.endswith('.1') else col for col in df.columns]
        df.drop(columns=['TIME'], inplace=True)
        df = df.applymap(lambda x: 0 if isinstance(x, str) else x)
        def calculate_positive_negative_sum(df, column_name):
            positive_sum = df[df[column_name] > 0][column_name].groupby(level=0).sum()
            negative_sum = df[df[column_name] < 0][column_name].groupby(level=0).sum()
            return positive_sum, negative_sum
        df2=pd.DataFrame()
        positive_sums = {}
        negative_sums = {}
        all_dates = df.index.unique()

        for column_name in df.columns:
            positive_sum, negative_sum = calculate_positive_negative_sum(df, column_name)
            positive_sum = positive_sum.reindex(all_dates, fill_value=0)
            negative_sum = negative_sum.reindex(all_dates, fill_value=0)
            df2[column_name + ' imp'] = positive_sum
            df2[column_name + ' exp'] = negative_sum
        df2= df2.div(1000)
        interreg=["RGDM-CHNDPR imp","RGDM-CHNDPR exp","765KV RCR-SLPR I&II imp","765KV RCR-SLPR I&II exp","HVDC GAJUWAKA imp","HVDC GAJUWAKA exp","HVDC TAL-KLR imp","HVDC TAL-KLR exp","765KV KDG-KLPR I&II imp","765KV KDG-KLPR I&II exp","ANG-SKLM imp","ANG-SKLM exp","WAR-NZB imp","WAR-NZB exp","RGH-PUG imp","RGH-PUG exp","220KV AMBWDI-XLDM imp","220KV AMBWDI-XLDM exp","220KV AMBWDI-PONDA imp","220KV AMBWDI-PONDA exp","765KV WAR-WRNGL I&II.1 imp","765KV WAR-WRNGL I&II.1 exp"]
        column_map ={"BHADRAVATHI IMP":"RGDM-CHNDPR imp","BHADRAVATHI EXP":"RGDM-CHNDPR exp","RCR-SOLPR IMP":"765KV RCR-SLPR I&II imp","RCR-SLPR EXP":"765KV RCR-SLPR I&II exp","GAZUWAKA IMP":"HVDC GAJUWAKA imp","GAZUWAKA EXP":"HVDC GAJUWAKA exp","TAL-KOLAR":"HVDC TAL-KLR imp","TAL-KOLAR EXP":"HVDC TAL-KLR exp","KUDGI-KOLAPUR IMP":"765KV KDG-KLPR I&II imp","KUDGI-KOLAPUR EXP":"765KV KDG-KLPR I&II exp","Angul-Srikakulam IMP":"ANG-SKLM imp","Angul-Srikakulam EXP":"ANG-SKLM exp","765kV Wardha-Nizamabad 1 & 2 IMP":"WAR-NZB imp","765kV Wardha-Nizamabad 1 & 2 EXP":"WAR-NZB exp","Raighar-Pugalur HVDC IMP":"RGH-PUG imp","Raighar-Pugalur HVDC EXP":"RGH-PUG exp","Ambewadi-Xeldom IMP":"220KV AMBWDI-XLDM imp","Ambewadi-Xeldom EXP":"220KV AMBWDI-XLDM exp","Ambewadi-Ponda IMP":"220KV AMBWDI-PONDA imp","Ambewadi-Ponda EXP":"220KV AMBWDI-PONDA exp","765KV WAR-WRNGL I&II IMP":"765KV WAR-WRNGL I&II imp","765KV WAR-WRNGL I&II EXP":"765KV WAR-WRNGL I&II exp"}

        # Load the workbook and select the desired sheet
        wb = openpyxl.load_workbook(r"\\fileserver\common\Prasad\Lineflows Report work\LineFlows.xlsx")
        sheet = wb['SUMMARY']

        # Clear the contents of the range A2:W32
        for row in sheet.iter_rows(min_row=2, max_row=32, min_col=1, max_col=23):  # A2:W32 is 2nd row to 32nd, and columns A to W (23 columns)
            for cell in row:
                cell.value = None

        # Assuming df2 is your DataFrame, converting the index to datetime
        index_datetime = pd.to_datetime(df2.index)

        # Writing dates to column A starting from row 2
        for row_num, date in enumerate(index_datetime.strftime('%d-%m-%Y'), start=2):
            sheet.cell(row=row_num, column=1, value=date)

        # Prepare JSON output
        json_output = []

        # Assuming column_map is a dictionary that maps your output columns to DataFrame columns
        for output_column, df_column in column_map.items():
            try:
                # Find the column index for the output column in the first row
                output_column_index = None
                for col_num, cell in enumerate(sheet[1], start=1):  # Sheet row 1
                    if cell.value == output_column:
                        output_column_index = col_num
                        break
                
                if output_column_index is None:
                    continue  # Skip if the column wasn't found
                
                # Writing data from the DataFrame to the corresponding column
                data = df2[df_column].values.tolist()
                for row_num, value in enumerate(data, start=2):
                    sheet.cell(row=row_num, column=output_column_index, value=value if pd.notna(value) else None)

                # Prepare the JSON output data
                data_entries = [{'x': date.strftime('%Y-%m-%d'), 'y': value if pd.notna(value) else ''} for date, value in zip(df2.index, df2[df_column])]
                json_output.append({
                    'name': df_column,
                    'data': data_entries
                })
            except Exception as e:
                print(e)
                continue

        # Save the workbook with a timestamped name
        file_name = r"\\fileserver\common\Prasad\Lineflows Report work\lineflows_report_{0}.xlsx".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
        wb.save(file_name)
        wb.close()

        # Return the response in the same format as the original
        return jsonify({
            'status': 'success',
            "message": "Report generated successfully!",
            "file_link": file_name,
            "data": json_output,
            "title": "Lineflows for the period between {0} and {1}".format(input_dat['params']['fromDate'], input_dat['params']['toDate'])
        }), 200



    except Exception as e:
        log_error("displaylineflows", e)
        cursor.close()
        return jsonify(message="There is some problem in uploading the file! Please contact SRLDC IT", status="failure")
        # return jsonify({"status": "failure", "error": str(e), "file": fname, "line": exc_tb.tb_lineno}), 500


        

@app.route("/api/reports/downloadlineflows", methods=["POST"])
@jwt_required()
@token_required
def downloadLineFlows():
    try:
        # Generate a unique filename with a timestamp
        download_link_json = request.get_json()
        download_link = download_link_json['downloadLink']

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'lineflows_report_{timestamp}.xlsx'
        file_path = download_link

        # Example logic for saving the Excel file
        # wb.save(file_path)
        # wb.close()

        # Directly send the file in the response
        return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        log_error("downloadlineflows", e)
        cursor.close()
        return jsonify(message="There is some problem in downloading the file! Please contact SRLDC IT", status="failure")
        # return jsonify({'status': 'failure', 'error': str(e)}), 500





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)






