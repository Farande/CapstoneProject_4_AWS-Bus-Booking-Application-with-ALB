# AWS Bus Booking Application with ALB

## Project Overview

The Bus Booking Application is a web-based application developed using Python Flask and MySQL. It allows users to register, log in, view available buses, search buses by route, book seats, and view their booking history.

The application is deployed on Amazon Web Services (AWS) using Amazon EC2, Amazon RDS, and an Application Load Balancer (ALB).

The project demonstrates how a Flask application can be deployed across multiple EC2 instances while using a centralized MySQL database hosted on Amazon RDS.

---

## Features

### User Features

* User registration
* User login and logout
* View available buses
* Search buses by source and destination
* View available seats
* Book a bus seat
* View booking history

### Admin Features

* Admin login
* View available buses
* View customer bookings
* View user booking information
* Monitor booking details

---

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

### Backend

* Python
* Flask
* PyMySQL
* Werkzeug

### Database

* MySQL
* Amazon RDS

### AWS Services

* Amazon EC2
* Amazon RDS
* Application Load Balancer
* Amazon VPC
* Security Groups

---

## AWS Architecture


                         Internet
                            |
                            |
                  Application Load Balancer
                            |
                    BusBooking-ALB-SG
                            |
                  ---------------------
                  |                   |
                  |                   |
              EC2 Instance 1      EC2 Instance 2
              Flask App           Flask App
                  |                   |
                  |                   |
                  -----------+---------
                             |
                             |
                       Amazon RDS
                       MySQL Database
                             |
                       BusBooking-RDS-SG


Both EC2 instances run the same Flask application and connect to the same Amazon RDS MySQL database.

---

## AWS Security Group Flow


Internet
   |
   | HTTP :80
   v
ALB Security Group
BusBooking-ALB-SG
   |
   | HTTP :5000
   v
EC2 Security Group
BusBooking-EC2-SG
   |
   | MySQL :3306
   v
RDS Security Group
BusBooking-RDS-SG


### Security Group Rules

#### ALB Security Group

| Type | Port | Source    |
| ---- | ---: | --------- |
| HTTP |   80 | 0.0.0.0/0 |

#### EC2 Security Group

| Type       | Port | Source            |
| ---------- | ---: | ----------------- |
| SSH        |   22 | My IP             |
| Custom TCP | 5000 | BusBooking-ALB-SG |

Port 5000 can temporarily be opened to your own IP for direct Flask testing.

#### RDS Security Group

| Type         | Port | Source            |
| ------------ | ---: | ----------------- |
| MySQL/Aurora | 3306 | BusBooking-EC2-SG |

The RDS database should not be exposed to the public internet.

---

## Project Structure


bus_bookings/
├─ app.py
├─ db.py
├─ data.py
├─ auth_utils.py
├─ ai_widget.py
├─ aws_utils.py
├─ requirements.txt
├─ index.html
├─ routes/
│ ├─ admin.py
│ ├─ analytics.py
│ ├─ assistant.py
│ ├─ auth.py
│ ├─ booking.py
│ ├─ buses.py
│ ├─ complaints.py
│ ├─ feedback.py
│ ├─ history.py
│ ├─ home.py
│ ├─ lost_found.py
│ ├─ notifications.py
│ ├─ status.py
│ └─ ticket.py
├─ templates/
│ ├─ admin.html
│ ├─ analytics.html
│ ├─ assistant.html
│ ├─ booking.html
│ ├─ buses.html
│ ├─ complaints.html
│ ├─ feedback.html
│ ├─ history.html
│ ├─ login.html
│ ├─ lost_found.html
│ ├─ notifications.html
│ ├─ register.html
│ ├─ status.html
│ └─ ticket.html
├─ static/
│ └─ style.css
│ └─ Shared CSS styling
├─ test_routes.py
├─ venv/
└─ pycache/

## Database Structure

The application uses Amazon RDS MySQL.

Database name:


BusBookingDB


Main tables:


Users
Buses
Bookings


### Users

Stores registered user information.


user_id
name
email
password
role
created_at


### Buses

Stores bus and route information.


bus_id
bus_number
bus_name
source
destination
departure_time
arrival_time
total_seats
available_seats
created_at


### Bookings

Stores user booking information.


booking_id
user_id
bus_id
seat_number
booking_date
status


The `Bookings` table has relationships with the `Users` and `Buses` tables.

---

## Example Bus Data

The project can contain sample buses such as:

| Bus                 | Source | Destination | Departure |
| ------------------- | ------ | ----------- | --------- |
| Shivneri Express    | Pune   | Mumbai      | 06:00     |
| Maharashtra Travels | Pune   | Nashik      | 08:00     |
| City Express        | Nashik | Mumbai      | 10:00     |
| Royal Travels       | Pune   | Nagpur      | 20:00     |

---

## Local Setup

### 1. Clone the Repository


git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git


Move into the project:


cd bus_bookings


---

### 2. Create a Virtual Environment


python3 -m venv venv


Activate it:

#### Linux/macOS


source venv/bin/activate


#### Windows


venv\Scripts\activate


---

### 3. Install Dependencies


pip install -r requirements.txt


---

## Requirements File

The `requirements.txt` file contains:


Flask
PyMySQL
Werkzeug


Install them using:


pip install -r requirements.txt


---

## Database Configuration

Update the database configuration in `app.py`:


DB_HOST = "foodorderdb.c9c6mkwkmeli.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "PASSWORD"
DB_NAME = "BusBookingDB"
DB_PORT = 3306




---

## Running the Application

Activate the virtual environment:


source venv/bin/activate


Run Flask:


python3 app.py


The application runs on:


http://127.0.0.1:5000


For an EC2 deployment, Flask listens on:


0.0.0.0:5000


---

# AWS Deployment

## Step 1: Create Amazon RDS

Create an Amazon RDS MySQL database.

Recommended configuration:


DB Identifier: bus-booking-db
Engine: MySQL
Database: BusBookingDB
Username: admin
Port: 3306


Configure the RDS security group so that only the EC2 security group can connect to port 3306.

---

## Step 2: Create EC2 Instance

Launch an Ubuntu EC2 instance.

Install Python:


sudo apt update
sudo apt install python3 python3-pip python3-venv -y


Clone or copy the project:


cd ~
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd bus_bookings


Create the virtual environment:


python3 -m venv venv


Activate it:


source venv/bin/activate


Install dependencies:


pip install -r requirements.txt


---

## Step 3: Configure RDS Connection

Update the Flask application with the RDS connection details.

Example:


DB_HOST = "foodorderdb.c9c6mkwkmeli.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "PASSWORD"
DB_NAME = "BusBookingDB"
DB_PORT = 3306


Test the application:


python3 app.py


---

## Step 4: Test Flask on EC2

Flask should display:


Running on http://0.0.0.0:5000


For direct testing, use the EC2 instance's **Public IPv4 address**, not its private IP address.

Example:


http://EC2-PUBLIC-IP:5000


Do not use:


http://172.31.x.x:5000


because `172.31.x.x` is a private VPC address.

---

## Step 5: Create a Second EC2 Instance

Launch another EC2 instance using the same application configuration.

Install Python:


sudo apt update
sudo apt install python3 python3-pip python3-venv -y


Deploy the same Flask application:


cd ~
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd bus_bookings
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Configure both EC2 instances to connect to the same RDS database.

---

# Application Load Balancer

Create an Application Load Balancer to distribute incoming requests between the EC2 instances.

### Load Balancer


Name: BusBooking-ALB
Scheme: Internet-facing
IP Address Type: IPv4


### Listener


Protocol: HTTP
Port: 80


### Target Group


Name: BusBooking-TG
Target Type: Instances
Protocol: HTTP
Port: 5000
Health Check Path: /


Register both EC2 instances with the target group.

Example:


EC2-1 → Port 5000 → Healthy
EC2-2 → Port 5000 → Healthy


---

## Accessing the Application

After the Application Load Balancer is configured, use the ALB DNS name:


http://YOUR-ALB-DNS-NAME


The user does not need to access the EC2 instances directly.

The final request flow is:


Browser
   |
   v
ALB
   |
   +------> EC2 Instance 1
   |
   +------> EC2 Instance 2
              |
              v
          RDS MySQL


---

# Application Flow

### User Registration


User
 ↓
Registration Page
 ↓
Flask Application
 ↓
Users Table
 ↓
Registration Complete


### Login


User
 ↓
Login Page
 ↓
Flask
 ↓
RDS MySQL
 ↓
Validate Credentials
 ↓
Dashboard / Bus List


### Bus Search


Source + Destination
        ↓
      Flask
        ↓
    RDS MySQL
        ↓
 Available Buses


### Bus Booking


Select Bus
    ↓
Select Seat
    ↓
Flask Application
    ↓
Create Booking
    ↓
Update Available Seats
    ↓
RDS MySQL
    ↓
Booking History


---

# Admin Flow


Admin Login
     ↓
Admin Dashboard
     ↓
View Buses
     ↓
View Bookings
     ↓
View User Information


---

# Health Check

The Application Load Balancer uses:

GET /


as the health-check endpoint.

The Flask application responds through:


@app.route("/")
def index():
    return render_template("index.html")


If the application is running correctly, the target should become:


Healthy


in the target group.

---

# Testing Checklist

### Application

* [ ] Home page loads
* [ ] User registration works
* [ ] User login works
* [ ] Bus list displays
* [ ] Bus search works
* [ ] Seat booking works
* [ ] Booking history displays
* [ ] Admin login works
* [ ] Admin dashboard displays

### Database

* [ ] EC2 can connect to RDS
* [ ] Users are stored in RDS
* [ ] Buses are stored in RDS
* [ ] Bookings are stored in RDS
* [ ] Available seat count is updated

### AWS

* [ ] EC2-1 is running
* [ ] EC2-2 is running
* [ ] Both EC2 instances run Flask
* [ ] RDS is available
* [ ] ALB is active
* [ ] Target group is healthy
* [ ] ALB can reach both EC2 instances
* [ ] RDS accepts connections only from EC2 security group

---

# Important Security Notes

Do not upload the following information to GitHub:

```text
AWS Access Keys
AWS Secret Keys
RDS Password
Database Credentials
Private SSH Keys
.env files containing passwords
```

Use environment variables for sensitive configuration.

# Screenshots

For the GitHub project documentation, include screenshots of the important parts of the deployment.

Recommended screenshots:

1. Application home page

<img width="1366" height="768" alt="Screenshot (722)" src="https://github.com/user-attachments/assets/bf40112f-9186-4f9b-a60d-b8a76bc38294" />

2 User registration page

<img width="1366" height="768" alt="Screenshot (723)" src="https://github.com/user-attachments/assets/f5e88992-0b33-4347-966f-43991b090e8c" />

3 Login page

<img width="1366" height="768" alt="Screenshot (724)" src="https://github.com/user-attachments/assets/e8c27eb7-66a8-4644-ac4c-099ac176b357" />

4. Bus listing page
   <img width="1366" height="768" alt="Screenshot (725)" src="https://github.com/user-attachments/assets/193cdd4a-8156-433c-91e6-49c491703d21" />

5. Bus booking page
   <img width="1366" height="768" alt="Screenshot (727)" src="https://github.com/user-attachments/assets/0601f1b7-fa38-450f-8240-c29360aa8ffe" />

6. Booking history
<img width="1366" height="768" alt="Screenshot (733)" src="https://github.com/user-attachments/assets/585a62df-1371-489e-87ad-e6a2ff8bd84a" />

7. EC2 instances
<img width="1366" height="768" alt="Screenshot (728)" src="https://github.com/user-attachments/assets/74a7cf6e-ba09-4b6a-826c-fd7b90033efc" />

8. EC2 security group
<img width="1366" height="768" alt="Screenshot (729)" src="https://github.com/user-attachments/assets/1e08db99-e3d6-4b08-b8a5-5baa6d6b06a2" />

9. RDS database
<img width="1366" height="768" alt="Screenshot (730)" src="https://github.com/user-attachments/assets/351a5fae-2742-44e6-a50c-f4d72b6b26f1" />

10. Application Load Balancer
<img width="1366" height="768" alt="Screenshot (731)" src="https://github.com/user-attachments/assets/346b19af-2116-4136-9913-9f4587e3c3ea" />


---

# What This Project Demonstrates

This project demonstrates practical knowledge of:

* Python Flask web development
* MySQL database integration
* Amazon RDS
* Amazon EC2
* Application Load Balancer
* Target Groups
* Security Groups
* AWS networking
* Multi-instance application deployment
* Database-backed web applications
* Basic cloud deployment and scalability

---

# Future Improvements

Possible future improvements include:

* Online payment integration
* Email booking confirmation
* Password reset
* Better seat-selection interface
* Admin bus management
* Route management
* Booking cancellation
* HTTPS using an SSL/TLS certificate
* Domain name integration
* Auto Scaling Group
* CI/CD pipeline
* CloudWatch monitoring
* Improved database security
* Environment-based configuration

---

# Conclusion

The Bus Booking Application is a Flask-based web application deployed on AWS using EC2, RDS, and an Application Load Balancer.

The project provides a practical example of deploying a database-driven application in the cloud, using multiple EC2 instances for application availability and Amazon RDS for centralized database management.
