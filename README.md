# Number Plate Recognition System

## Overview

The Number Plate Recognition System is a project designed to recognize vehicle number plates using Optical Character Recognition (OCR) combined with a Convolutional Neural Network (CNN) model. The project includes a database for storing company and number plate details, a web application for managing these records, and a machine learning model for character recognition in number plate images.

## Project Structure

The project is organized into the following main components:

### 1. Database Setup (`Number_plate_DB.ipynb`)

This component involves setting up a MySQL database to store information about companies and their associated number plates. The database consists of two main tables:

- **company_master**: Stores details like company name, email, and password.
- **Numberplate**: Stores number plate information linked to each company.

### 2. Web Application (`OCR_app/`)

A Flask-based web application that allows companies to log in, add, manage, and delete number plates. The app includes:

- **Login Page :-** for company accounts.
- **Forgot Password:-** for changing password with 2FA(ie. Email ID OTP Validation)
- **Dashboard:-** for managing number plate entries.
- **Display of Number Plates :-** Display of Existing Number Plates with option to edit and delete and search functionality also added.
- **Bulk Upload :-** Option to upload number Plate details in Bulk using Excel file
- **Single Upload :-** Add a single Number Plate at A Time

### 3. OCR Model (`OCR_CNN_Model.ipynb`)

This module contains the code for a TensorFlow-based CNN model that recognizes alphanumeric characters from number plate images. The model is trained on a dataset of characters and is used for identifying text in the number plate images.

#### Model Explanation

**Overview:**
`model_alpha` is a Convolutional Neural Network (CNN) designed to recognize characters from images of number plates.

**Layers:**

1. **First Layer:**
   - **Conv2D:** Detects features using 32 filters.
   - **BatchNormalization:** Keeps the data stable.
   - **MaxPooling2D:** Reduces the size of the data.

2. **Second Layer:**
   - **Conv2D:** Uses 64 filters to detect more features.
   - **BatchNormalization:** Keeps the data stable.
   - **MaxPooling2D:** Further reduces the size of the data.

3. **Third Layer:**
   - **Conv2D:** Uses 128 filters for even more features.
   - **BatchNormalization:** Keeps the data stable.
   - **MaxPooling2D:** Reduces the size again.

4. **Fourth Layer:**
   - **Conv2D:** Uses another 128 filters.
   - **BatchNormalization:** Keeps the data stable.

5. **Global Average Pooling:**
   - **GlobalAveragePooling2D:** Simplifies the data by averaging.

6. **Dense Layers:**
   - **Dense:** 128 units to process the data.
   - **Dropout:** 50% chance to ignore some data to prevent overfitting.
   - **Dense:** 36 units to classify the characters (digits and letters).

**Compilation:**
- **Optimizer:** Adam, which helps the model learn.
- **Loss Function:** Sparse Categorical Crossentropy, which measures how well the model is doing.
- **Metrics:** Accuracy, to see how often the model is correct.


### 4. Number Plate Processing (`Number_plate_detection.ipynb`)
**Pre-Processing:**
- This component is responsible for processing images of number plates.
- It extracts the plate from the image.
- It separates each character by first resizing the image to a specific size and finding contours.

**OCR Model Prediction:**
- The trained OCR model is loaded and compiled.
- Each individual character is identified using the trained CNN model and converted to text.

**Post-Processing:**
- For each character, the best predicted number and alphabet are considered.
- All the possible combinations of numbers and alphabets are used to check if there is an existing number plate in the database.




## How It Works

1. **Database Setup**: The MySQL database is initialized with the necessary tables to store company and number plate details.
2. **Web Application**: Companies use the Flask web application to log in and manage their number plate records.
3. **OCR Model**: The CNN model is trained to recognize characters and is then used to process images of number plates.
4. **Number Plate Processing**: Images are processed to extract and recognize number plates, and the results are verified against the database.
