# Project: Textualize

### Brief Description

Textualize is a cloud-based project designed to provide an API service that can:

  * Summarize long text into shorter content.
  * Upload images with metadata (title and description) to cloud storage.
  * Manage user data and authentication using a database.

This project uses Python Flask for the Machine Learning model, Express.js for the main backend, and various Google Cloud Platform (GCP) services for deployment.

### Key Features

  1. **Summarize Endpoint (Flask)**:
     - Summarizes text longer than 10 words.
     - Returns an error message if the text is fewer than 10 words.
  
  2. **Upload Endpoint (Express.js)**:
     - Uploads image files to Google Cloud Storage.
     - Stores metadata (image URL, title, description) in MySQL.
  
  3. **Items Endpoint (Express.js)**:
     - Fetches all image data and metadata from the database.
     - Supports data retrieval by user ID.
  
  4. **Authentication Endpoint (Express.js)**:
     - **Register**: Register a new user.
     - **Login**: Authenticate a user.
     - **Logout**: Remove user session.

### Technologies Used

  * **Backend**:
    - Python Flask
    - Express.js (Node.js)
  
  * **Database**:
    - Google Cloud SQL (MySQL)
  
  * **File Storage**:
    - Google Cloud Storage
  
  * **Deployment**:
    - Docker, Docker Hub
    - Google Cloud Run

### Installation and Setup

#### 1. Running the Flask API

  1. Clone the repository.
  2. Navigate to the Flask project directory.
  3. Install dependencies: 

        `pip install -r requirements.txt`

  4. Run the local server:

        `python app.py`

#### 2. Running the Express.js API

  1. Navigate to the Express project directory.
  2. Install dependencies:

        `npm install`

  3. Run the local server:

        `npm start`

#### 3. Deployment with Docker

  1. Build Docker image: 

        `docker build -t <image-name> .`

  2. Push image to Docker Hub: 

        `docker push <dockerhub-username>/<image-name>`

  3. Deploy to Google Cloud Run:
     * Open Google Cloud Console.
     * Choose Cloud Run, create a new service, and use the image from Docker Hub.

### API Endpoints

#### 1. Summarize Endpoint (Flask)
  - **URL**: `/summarize`
  - **Method**: POST
  - **Request Body**:

        {
      "text": "<long text>"
    }

  - **Success Response**:

        {
      "status": "success",
      "summary": "<text summary>"
    }

  - **Error Response**:

        {
      "status": "error",
      "message": "Text must be more than 10 words."
    }

#### 2. Upload Endpoint (Express.js)

  - **URL**: `/upload`
  - **Method**: POST
  - **Request Body**:
    - Form Data:
      - `file`: image file
      - `title`: string
      - `description`: string
  - **Success Response**:

        {
      "status": "success",
      "data": {
        "url": "<public image URL>",
        "title": "<title>",
        "description": "<description>"
      }
    }

#### 3. Items Endpoint (Express.js)

  - **URL**: `/items`
  - **Method**: GET
  - **Success Response**:

        {
      "status": "success",
      "data": [
        {
          "id": 1,
          "url": "<public URL>",
          "title": "<title>",
          "description": "<description>"
        }
      ]
    }

#### 4. Authentication Endpoint (Express.js)

  - **Register**:

    - **URL**: `/register`
    - **Method**: POST
    - **Request Body**:

                {
          "email": "<email>",
          "username": "<username>",
          "password": "<password>",
          "confirm_password": "<confirm password>"
        }

  - **Login**:

    - **URL**: `/login`
    - **Method**: POST
    - **Request Body**:

                {
          "username": "<username>",
          "password": "<password>"
        }

  - **Logout**:

    - **URL**: `/logout`
    - **Method**: POST

### Database Structure

  * **Table**: `items`
    - Columns:
      - `id` (integer, primary key, auto increment)
      - `url` (string, public image URL)
      - `title` (string)
      - `description` (string)
  * **Table**: `users`
    - Columns:
      - `id` (integer, primary key, auto increment)
      - `email` (string, unique)
      - `username` (string, unique)
      - `password` (hashed string)

### Additional Documentation

  * API Documentation: [Postman Documentation](https://documenter.getpostman.com)