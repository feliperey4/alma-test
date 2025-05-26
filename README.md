# Leads Management API

<!-- TOC -->
* [To run the application locally, follow these steps:](#to-run-the-application-locally-follow-these-steps)
  * [1. Prerequisites:](#1-prerequisites)
  * [2. Environment Setup:](#2-environment-setup)
  * [3. Build and run the images:](#3-build-and-run-the-images)
  * [4. Use the Application:](#4-use-the-application)
    * [Public API](#public-api)
    * [Internal API](#internal-api)
  * [5. Stopping the Application:](#5-stopping-the-application)
  * [Troubleshooting](#troubleshooting)
* [Usage Flow](#usage-flow)
  * [1. Create Lead](#1-create-lead)
  * [2. Register a New User](#2-register-a-new-user)
  * [3. Login User](#3-login-user)
  * [4. List Leads](#4-list-leads)
  * [5. Update Lead Status](#5-update-lead-status)
  * [6. Download CV/resume](#6-download-cvresume)
<!-- TOC -->

## To run the application locally, follow these steps:
### 1. Prerequisites:
- Docker and Docker Compose: Ensure you have Docker and Docker Compose installed on your system. 
You can download them from the official Docker website.
- Clone this project.

### 2. Environment Setup:
`.env` file: This file will hold the environment variables required by the application. 
Populate it with the following content, modifying values as needed:
```
AUTH_SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com # replace with your actual Gmail address
SMTP_PASSWORD=your_app_password # Replace with your Gmail app password. 
ATTORNEY_EMAIL=attorney@example.com
```
**Important notes on email:**  For `SMTP_USERNAME` and `SMTP_PASSWORD`, 
you'll likely need to use an "App Password" instead of your regular Gmail password.  
You can generate one in your Google account settings under "Security" -> "2-Step Verification" -> "App passwords".  If you are not using Gmail, adapt `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, and `SMTP_PASSWORD` to your email provider's settings.

### 3. Build and run the images:
The application uses a PostgreSQL database and a service with FastAPI. Running the following command will build and run all.
```
docker-compose build
docker-compose up
```

This command builds the application image and starts the application container. The application will be accessible at http://localhost:8000.

You can use http://0.0.0.0:8000/api-doc to check the endpoint documentation and test the application.

### 4. Use the Application:
#### Public API
Creating leads is possible without authentication.
Simply fill out a form with email, first name, last name, and CV/Resume, then submit it using `POST /leads/`.
#### Internal API
Before using this API, you must create a new user with `POST /internal/register`.
Once you have a username and password, use the login endpoint `POST /internal/login` to receive a JWT token for authenticated lead endpoints.

**Note**: see [Usage Flow](#usage-flow). 

### 5. Stopping the Application:
To stop the running containers, use:
```
docker-compose down
```


### Troubleshooting
- Database Connection Issues: If the application container fails to start due to database connection errors, ensure that the database container is running (docker-compose ps) and that the DATABASE_URL in your .env file matches the database settings in docker-compose.yml.
- Port Conflicts: If you have another service running on port 8000 or 5432, you'll need to either stop that service or modify the port mappings in docker-compose.yml. For example, to run the app on port 8001, change the ports section of the app service to - "8001:8000".
- Email Sending: Verify that the SMTP_* settings in your .env file are correct. Test your email configuration separately if necessary.


# Usage Flow

## 1. Create Lead

```bash
curl -X POST \
  http://localhost:8000/leads/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'email=test@example.com' \
  -F 'f_name=John' \
  -F 'l_name=Doe' \
  -F 'CV=@/path/to/your/resume.pdf' # Replace with the actual path to your CV file
```

## 2. Register a New User

```bash
curl -X POST \
  http://localhost:8000/internal/auth/register \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "myuser",
    "password": "mypassword"
  }'
```

## 3. Login User

```bash
curl -X POST \
  http://localhost:8000/internal/auth/login \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "myuser",
    "password": "mypassword"
  }'
```
*Note: This will return a JSON object containing the `access_token`. You will need this token for subsequent authenticated requests.*

## 4. List Leads

```bash
curl -X GET \
  "http://localhost:8000/internal/leads/?email=test@example.com&state=new" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" 
```
*You can adjust the query parameters (`email`, `f_name`, `l_name`, `state`) to filter the results. Replace YOUR_ACCESS_TOKEN with the token obtained from the login step*

## 5. Update Lead Status

```bash
curl -X PATCH \
  "http://localhost:8000/internal/leads/LEAD_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "status": "REACHED_OUT" 
  }'
```
*This will update the status of the specified lead. Replace LEAD_ID with the actual ID of the lead and YOUR_ACCESS_TOKEN with your token.*

## 6. Download CV/resume
```bash
curl -X GET \
  "http://localhost:8000/internal/leads/LEAD_ID/cv-download" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o downloaded_cv.pdf 
```
*This will download the CV associated with the specified lead ID to a file named `downloaded_cv.pdf`. Replace YOUR_ACCESS_TOKEN with the token obtained from the login step*
