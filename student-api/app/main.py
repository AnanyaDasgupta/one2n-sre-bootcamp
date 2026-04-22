from fastapi import FastAPI  # Import the FastAPI framework for building the web API

app = FastAPI()  # Create an instance of the FastAPI application

@app.get("/")  # Define a GET endpoint at the root path "/"
def hello():  # Function to handle requests to the root endpoint
    return {"message": "Hello, World!"}  # Return a JSON response with a greeting message

@app.get("/healthcheck")  # Define a GET endpoint at "/healthcheck" for health monitoring
def healthcheck():  # Function to handle health check requests
    return {"status": "ok"}  # Return a JSON response indicating the service is healthy