# Number Plate Recognition System

## Overview

The Number Plate Recognition System is a project designed to recognize vehicle number plates using Optical Character Recognition (OCR) combined with a Convolutional Neural Network (CNN) model. The project includes a database for storing company and number plate details, a web application for managing these records, and a machine learning model for character recognition in number plate images.

## Project Structure

The project is organized into the following main components:

### 1. Database Setup (`Number_plate_DB/`)

This component involves setting up a MySQL database to store information about companies and their associated number plates. The database consists of two main tables:

- **company_master**: Stores details like company name, email, and password.
- **Numberplate**: Stores number plate information linked to each company.

### 2. Web Application (`OCR_app/`)

A Flask-based web application that allows companies to log in, add, manage, and delete number plates. The app includes:

- **Login and registration forms** for company accounts.
- **Dashboard** for managing number plate entries.
- **Templates and static files** for rendering the web pages.

### 3. OCR Model (`OCR_CNN_Model/`)

This module contains the code for a TensorFlow-based CNN model that recognizes alphanumeric characters from number plate images. The model is trained on a dataset of characters and is used for identifying text in the number plate images.

### 4. Number Plate Processing (`Numberplate_processing/`)

This component is responsible for processing images of number plates. It extracts the plate from the image, recognizes individual characters using the trained CNN model, and checks if the recognized number plate exists in the database.

### 5. Utility Functions (`utils/`)

Helper functions for database operations, including connecting to the database, executing SQL queries, and fetching data.

## How It Works

1. **Database Setup**: The MySQL database is initialized with the necessary tables to store company and number plate details.
2. **Web Application**: Companies use the Flask web application to log in and manage their number plate records.
3. **OCR Model**: The CNN model is trained to recognize characters and is then used to process images of number plates.
4. **Number Plate Processing**: Images are processed to extract and recognize number plates, and the results are verified against the database.
