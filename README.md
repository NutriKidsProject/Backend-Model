# NutriKids - Cloud Computing

This repository contains the cloud infrastructure and deployment code for NutriKids, a mobile application designed to help parents monitor and improve their children's nutritional status.

## How to install .venv
```
#install .venv
python3 -m venv .venv
# Menginstal dependencies
RUN pip install --no-cache-dir -r requirements.txt
```

## Project Overview

NutriKids utilizes machine learning to predict a child's nutritional status based on their height, weight, age, and gender. It then provides personalized food recommendations to help parents make informed decisions about their children's diet.

## Cloud Architecture

NutriKids leverages Google Cloud Platform's serverless services for scalability, reliability, and cost-effectiveness. The core components of the cloud architecture include:

* **Cloud Run:**  Hosts and scales the application backend and machine learning model.
* **Cloud Storage:** Stores the machine learning model and supporting data files.
* **Firestore:**  Serves as the database for storing prediction results and user information.
* **Firebase Authentication:**  Provides secure user authentication for the mobile app.

## Cloud Computing Engineer's Role

As the Cloud Computing Engineer on this project, We was responsible for:

* Designing and implementing the cloud architecture.
* Deploying the application backend and machine learning model to Cloud Run.
* Setting up and managing the Cloud Storage bucket for storing project assets.
* Integrating Firestore as the database for the application.
* Configuring Firebase Authentication for secure user login.
* Ensuring the scalability, security, and performance of the cloud infrastructure.

## Deployment

The application is deployed on Cloud Run and can be accessed at:
https://nutrikids-service-873608920687.asia-southeast2.run.app/

## API Endpoint

**POST /predict**

This endpoint accepts a JSON payload with the following parameters:

* `tb` (height in cm)
* `bb` (weight in kg)
* `usia` (age in years)
* `jenis_kelamin` (gender - "Laki-laki" or "Perempuan")

Example Input :
{
  "tb": 110,
  "bb": 15,
  "usia": 6,
  "jenis_kelamin": "Laki-laki" 
}

Response :
{
    "bmi": 12.4,
    "description": "Child has lower weight than recommended.",
    "firestore_status": "Data saved to Firestore with ID: JF5iDnFOf1vTGlN68i7L",
    "prediction": "Gizi Kurang",
    "recommendations": [
        {
            "Caloric Value": 330,
            "Protein": 40.0,
            "food": "soy flour low fat"
        },
        {
            "Caloric Value": 363,
            "Protein": 13.3,
            "food": "spaghetti cooked"
        },
        {
            "Caloric Value": 970,
            "Protein": 15.2,
            "food": "potato chips barbecue"
        },
        {
            "Caloric Value": 1036,
            "Protein": 13.9,
            "food": "corn chips barbecue"
        },
        {
            "Caloric Value": 446,
            "Protein": 15.4,
            "food": "bacon meatless"
        }
    ]
}


It returns a JSON response with the predicted nutritional status, food recommendations, and other relevant information.
