from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
import mysql.connector, joblib


app = Flask(__name__)
app.secret_key = 'pollution' 

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='pollution'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']

        if password == c_password:
            query = "SELECT email FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])

            if email not in email_data_list:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)

                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email in email_data_list:
            query = "SELECT * FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password == password__data[0][3]:
                session["user_email"] = email
                session["user_id"] = password__data[0][0]
                session["user_name"] = password__data[0][1]

                return redirect("/home")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')



@app.route('/home')
def home():
    return render_template('home.html')


########################################################################################################################
############################################## PREDICTION SECTION #####################################################
########################################################################################################################


import joblib
import pandas as pd
import numpy as np

class AQIPredictor:
    def __init__(self, model_path):
        # Load artifacts
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(r'models\label_encoder.joblib')
        self.feature_columns = joblib.load(r'models\feature_columns.joblib')
        self.medians = joblib.load(r'models\imputation_medians.joblib')
        
        # Create city columns template
        self.city_columns = [col for col in self.feature_columns if col.startswith('City_')]

    def preprocess_input(self, input_data):
        # Create DataFrame
        df = pd.DataFrame([input_data])
        
        # Feature engineering
        df['PM_combined'] = df['PM2.5'] * df['PM10']
        df['NH3_log'] = np.log1p(df['NH3'])
        
        # One-hot encode city
        city = df['City'].iloc[0]
        df = pd.get_dummies(df, columns=['City'])
        for col in self.city_columns:
            df[col] = 1 if col == f'City_{city}' else 0
        
        # Impute missing values
        numeric_cols = [col for col in self.feature_columns if col not in self.city_columns]
        df[numeric_cols] = df[numeric_cols].fillna(pd.Series(self.medians, index=numeric_cols))
        
        # Ensure column order matches training data
        return df[self.feature_columns]

    def predict(self, input_data):
        # Validate input
        required_fields = ['City', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 
                          'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene']
        if not all(field in input_data for field in required_fields):
            raise ValueError("Missing required fields in input data")
            
        # Preprocess
        processed_data = self.preprocess_input(input_data)
        
        # Predict
        prediction = self.model.predict(processed_data)
        
        # Decode label
        return self.label_encoder.inverse_transform(prediction)[0]



def prediction_func(City, PM2, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene):

    input_data = {
        'City': City,
        'PM2.5': PM2 ,
        'PM10': PM10,
        'NO': NO,
        'NO2': NO2,
        'NOx': NOx,
        'NH3': NH3,
        'CO': CO,
        'SO2': SO2,
        'O3': O3,
        'Benzene': Benzene,
        'Toluene': Toluene
    }

    # Initialize predictor with your best model
    predictor = AQIPredictor(r'models\xgb_model.joblib')

    # Get prediction
    prediction = predictor.predict(input_data)
    return prediction


@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        City = request.form["City"]
        PM2 = float(request.form["PM2"])
        PM10 = float(request.form["PM10"])
        NO = float(request.form["NO"])
        NO2 = float(request.form["NO2"])
        NOx = float(request.form["NOx"])
        NH3 = float(request.form["NH3"])
        CO = float(request.form["CO"])
        SO2 = float(request.form["SO2"])
        O3 = float(request.form["O3"])
        Benzene = float(request.form["Benzene"])
        Toluene = float(request.form["Toluene"])

        result = prediction_func(City, PM2, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene)
        
        return render_template('prediction.html', result = result)   
    return render_template('prediction.html')




if __name__ == '__main__':
    app.run(debug = True)