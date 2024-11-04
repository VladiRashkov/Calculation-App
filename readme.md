# Web Application for Computation API
## Overview
This project is a web application that provides an HTTP API for performing calculations based on user-uploaded CSV files. The application utilizes FastAPI for the backend, React for the frontend, and SQLite as the database with SQLAlchemy for ORM. The application is containerized using Docker and can be easily deployed with Docker Compose.

## Requirements
Docker Desktop: Ensure you have Docker Desktop installed and running on your machine. You can download it from Docker's official website.
## Getting Started
To get started with this application, follow these steps:


Ensure that Docker Desktop is running. Use the following command to build the containers and start the application:

docker-compose up --build

This command will build the necessary Docker images and start the application, including both the FastAPI backend and the React frontend.

Access the Application

Once the application is running, you can access the frontend in your web browser at http://localhost:3000. The backend API can be accessed at http://localhost:8000/api/compute.

## Features
Authorization: The API requires authorization to access the /api/compute endpoint.
File Upload: Accepts CSV files containing calculations

(NOTE: the feature is available only http://localhost:8000/api/compute on the backend. The feature hasn't been implemented on the front end part).
Calculations: Supports the following operations: addition (+), subtraction (-), multiplication (*), and division (/).
Results Storage: Calculation results and requests are stored in an SQLite database.
Admin UI: A simple interface to browse request and result entries.

## Input Format
(A CSV file can be found in the project for testing)
The application accepts CSV files with the following format:


Copy code
A|O|B
1|+|2
3|*|4
5|-|6
8|/|4
Where:

A is the left operand
O is the operator
B is the right operand
Calculation Example
For the input:


Copy code
A|O|B
1|+|2
3|*|4
5|-|6
8|/|4
The application calculates:


Copy code
(1 + 2) + (3 * 4) + (5 - 6) + (8 / 4) = 16.0
The result is stored in the database.

## Testing
The application includes unit tests for the calculation functionality. You can run the tests using:
