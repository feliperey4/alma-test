"""
Written by Felipe Rey
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .api.lead import lead_route
from .api.user import user_route
from .database import engine, Base


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lead Management API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(lead_route)
app.include_router(user_route)


# endpoints to test and API documentation

@app.get("/api-doc", include_in_schema=False)
async def api_doc_stoplight():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>API documentation</title>
    </head>
    <body>
        <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
            <elements-api
               apiDescriptionUrl="/openapi.json"
               router="hash"
               hideSchemas="true"
               layout="responsive"/>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/submit", response_class=HTMLResponse, include_in_schema=False)
def submit_form():
    html = """
<!DOCTYPE html>
<html>
<head>
  <title>Submit Lead</title>
</head>
<body>
  <h2>Submit Your Information</h2>
  <form action="/leads/" method="post" enctype="multipart/form-data">
    <label>First Name:</label><br />
    <input type="text" name="f_name" required><br />

    <label>Last Name:</label><br />
    <input type="text" name="l_name" required><br />

    <label>Email:</label><br />
    <input type="email" name="email" required><br />

    <label>CV / Resume:</label><br />
    <input type="file" name="cv" accept=".pdf,.doc,.docx" required><br /><br />

    <button type="submit">Submit</button>
  </form>
</body>
</html>
"""
    return HTMLResponse(content=html)