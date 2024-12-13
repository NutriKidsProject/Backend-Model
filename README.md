# NutriKids - Cloud Computing

This repository contains the cloud infrastructure and deployment code for NutriKids, a mobile application designed to help parents monitor and improve their children's nutritional status.

## Project Overview

NutriKids utilizes machine learning to predict a child's nutritional status based on their height, weight, age, and gender. It then provides personalized food recommendations to help parents make informed decisions about their children's diet.

## Cloud Architecture

NutriKids leverages Google Cloud Platform's serverless services for scalability, reliability, and cost-effectiveness. The core components of the cloud architecture include:

* **Cloud Run:**  Hosts and scales the application backend and machine learning model.
* **Cloud Storage:** Stores the machine learning model and supporting data files.
* **Firestore:**  Serves as the database for storing prediction results and user information.
* **Firebase Authentication:**  Provides secure user authentication for the mobile app.

## Cloud Computing Engineer's Role

As the Cloud Computing Engineer on this project, I was responsible for:

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

It returns a JSON response with the predicted nutritional status, food recommendations, and other relevant information.
