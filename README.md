## To run the application locally, follow these steps:
1. Prerequisites:
- Docker and Docker Compose: Ensure you have Docker and Docker Compose installed on your system. 
You can download them from the official Docker website.
- Clone this project.

2. Environment Setup:
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

3. Build and run the images:
The application uses a PostgreSQL database and a service with FastAPI. Running the following command will build and run all.
```
docker-compose build
docker-compose up
```

This command builds the application image and starts the application container. The application will be accessible at http://localhost:8000.

You can use http://0.0.0.0:8000/api-doc to check the endpoint documentation and test the application.

4. Stopping the Application:
To stop the running containers, use:
```
docker-compose down
```


### Troubleshooting
- Database Connection Issues: If the application container fails to start due to database connection errors, ensure that the database container is running (docker-compose ps) and that the DATABASE_URL in your .env file matches the database settings in docker-compose.yml.
- Port Conflicts: If you have another service running on port 8000 or 5432, you'll need to either stop that service or modify the port mappings in docker-compose.yml. For example, to run the app on port 8001, change the ports section of the app service to - "8001:8000".
- Email Sending: Verify that the SMTP_* settings in your .env file are correct. Test your email configuration separately if necessary.