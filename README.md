# Air Quality Index Prediction System

This project is a web application that predicts Air Quality Index (AQI) using machine learning models with a Flask backend and modern frontend technologies.

## Features

- **User Authentication**: Secure signup/login system with session management
- **AQI Prediction**: Machine learning model to predict air quality category
- **Responsive UI**: Clean, mobile-friendly interface using Bootstrap
- **Database Integration**: MySQL database for user management
- **Model Serving**: Integration of trained XGBoost model for predictions

## Technology Stack

### Frontend
- HTML5, CSS3
- Bootstrap 5
- JavaScript (with potential for React.js integration)

### Backend
- Python 3.10
- Flask web framework
- MySQL database

### Machine Learning
- XGBoost classifier
- Scikit-learn for preprocessing
- Pandas and NumPy for data handling
- Joblib for model serialization

## Installation Guide

### Prerequisites
- Python 3.10
- MySQL Server
- Node.js (for potential React frontend)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/air-quality-prediction.git
   cd air-quality-prediction
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up MySQL database:
   - Create a database named `pollution`
   - Create a table using this SQL:
     ```sql
     CREATE TABLE users (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         email VARCHAR(255) UNIQUE NOT NULL,
         password VARCHAR(255) NOT NULL
     );
     ```

5. Configure database credentials in `app.py`:
   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="your_username",
       password="your_password",
       port="3306",
       database='pollution'
   )
   ```

6. Run the Flask application:
   ```bash
   python app.py
   ```

### Frontend Setup (Optional React Conversion)
1. Create React app:
   ```bash
   npx create-react-app frontend
   cd frontend
   ```

2. Install Bootstrap:
   ```bash
   npm install bootstrap
   ```

3. Integrate with Flask backend by adding proxy to `package.json`:
   ```json
   "proxy": "http://localhost:5000"
   ```

4. Start React development server:
   ```bash
   npm start
   ```

## Usage

1. Access the application at `http://localhost:5000`
2. Register a new account or login with existing credentials
3. Navigate to the prediction page
4. Enter air quality parameters:
   - City name
   - PM2.5, PM10 levels
   - NO, NO2, NOx concentrations
   - NH3, CO, SO2, O3 levels
   - Benzene and Toluene measurements
5. Submit the form to get AQI prediction

## Project Structure

```
air-quality-prediction/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── models/                # Machine learning models
│   ├── xgb_model.joblib
│   ├── label_encoder.joblib
│   ├── feature_columns.joblib
│   └── imputation_medians.joblib
├── templates/             # HTML templates
│   ├── index.html
│   ├── about.html
│   ├── register.html
│   ├── login.html
│   ├── home.html
│   └── prediction.html
├── static/                # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── README.md              # This documentation
```

## Machine Learning Approach

The prediction system uses an XGBoost classifier with the following workflow:

1. **Input Processing**:
   - Combine PM features: `PM2.5 * PM10`
   - Logarithmic transformation: `log1p(NH3)`
   - One-hot encoding for city names

2. **Feature Engineering**:
   - Missing value imputation with feature medians
   - Ensure consistent feature columns with training data

3. **Prediction**:
   - XGBoost model classifies air quality into categories
   - Label encoder converts numerical predictions to human-readable categories

## Future Enhancements

1. Integrate React.js for a more dynamic frontend
2. Add real-time air quality data visualization
3. Implement historical prediction storage
4. Add location-based services for automatic parameter detection
5. Include multiple model comparison and selection
6. Implement admin dashboard for data management

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Publication

This project is published under the  Journal of Emerging Technologies and Innovative Research (ISSN : 2349-5162) - see the [http://www.jetir.org/view?paper=JETIR2504575](LICENSE) file for details.
