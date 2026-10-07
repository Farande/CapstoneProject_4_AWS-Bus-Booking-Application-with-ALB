# AWS Bus Booking Application with ALB

## 1. Project Title and Objective

**Project Title:** AWS Bus Booking Application with Application Load Balancer (ALB)

**Objective:**
This project is a web-based bus booking application built with **Python Flask** and **MySQL**. Users can register, log in, view available buses, search buses by route, book seats and view their booking history. Administrators can view buses and customer bookings.

The application is deployed on AWS across **two Amazon EC2 instances** behind an **Application Load Balancer**, with a centralized **Amazon RDS MySQL** database. The project demonstrates how a database-backed Flask application can be deployed for availability and scalability using core AWS networking and security features.

### Features

**User features**
- Registration, login and logout
- View available buses and seats
- Search buses by source and destination
- Book a bus seat
- View booking history
- Live bus status

**Admin features**
- Admin login
- View buses, customer bookings and user booking information

**Additional modules** (in `routes/`): analytics, assistant, complaints, feedback, lost and found, notifications, ticket.

---

## 2. AWS Services Used

| Service | Purpose |
|---|---|
| **Amazon EC2** | Two Ubuntu instances run the Flask application |
| **Amazon RDS (MySQL)** | Central database (`BusBookingDB`) shared by both instances |
| **Application Load Balancer** | Distributes incoming HTTP traffic across the EC2 instances |
| **Target Group** | Registers both instances and performs health checks on port 5000 |
| **Amazon VPC** | Private networking for EC2 and RDS |
| **Security Groups** | Restricts traffic: Internet to ALB, ALB to EC2, EC2 to RDS |

**Other technologies:** Python, Flask, PyMySQL, Werkzeug, HTML, CSS, JavaScript, Jinja2

---

## 3. Architecture / Workflow

### Architecture

```
                         Internet
                            |
                            v
                Application Load Balancer
                  (BusBooking-ALB-SG)
                            |
                  +---------+---------+
                  |                   |
                  v                   v
            EC2 Instance 1      EC2 Instance 2
              Flask App           Flask App
                  |                   |
                  +---------+---------+
                            |
                            v
                  Amazon RDS (MySQL)
                    BusBookingDB
                  (BusBooking-RDS-SG)
```

Both EC2 instances run the same Flask application and connect to the same RDS database.

### Security Group Flow

```
Internet --HTTP :80--> BusBooking-ALB-SG
                            |
                            | HTTP :5000
                            v
                       BusBooking-EC2-SG
                            |
                            | MySQL :3306
                            v
                       BusBooking-RDS-SG
```

| Security Group | Type | Port | Source |
|---|---|---:|---|
| BusBooking-ALB-SG | HTTP | 80 | 0.0.0.0/0 |
| BusBooking-EC2-SG | SSH | 22 | My IP |
| BusBooking-EC2-SG | Custom TCP | 5000 | BusBooking-ALB-SG |
| BusBooking-RDS-SG | MySQL/Aurora | 3306 | BusBooking-EC2-SG |

The RDS database is **not** exposed to the public internet. Port 5000 can temporarily be opened to your own IP for direct Flask testing.

### Application Flow

```
Register / Login  ->  Flask  ->  RDS (Users)
Search Buses      ->  Flask  ->  RDS (Buses)  ->  Available buses
Select Bus + Seat ->  Flask  ->  Create booking + update available seats  ->  RDS  ->  Booking history
Admin Login       ->  Admin dashboard  ->  View buses, bookings and users
```

### Database Structure

Database name: `BusBookingDB`

| Table | Columns |
|---|---|
| **Users** | user_id, name, email, password, role, created_at |
| **Buses** | bus_id, bus_number, bus_name, source, destination, departure_time, arrival_time, total_seats, available_seats, created_at |
| **Bookings** | booking_id, user_id, bus_id, seat_number, booking_date, status |

`Bookings` has relationships with both `Users` and `Buses`.

### Project Structure

```
bus_bookings/
├── app.py
├── db.py
├── data.py
├── auth_utils.py
├── ai_widget.py
├── aws_utils.py
├── requirements.txt
├── index.html
├── routes/          # admin, auth, booking, buses, history, status, ticket, ...
├── templates/       # HTML pages (login, register, buses, booking, history, ...)
├── static/          # style.css
├── Screenshot/      # Project screenshots
└── test_routes.py
```

---

## 4. Implementation Steps

1. **Build the Flask application** with registration, login, bus search, seat booking, booking history and admin views.
2. **Create the RDS MySQL database** (`BusBookingDB`) with the `Users`, `Buses` and `Bookings` tables.
3. **Create the security groups** (`BusBooking-ALB-SG`, `BusBooking-EC2-SG`, `BusBooking-RDS-SG`) with the rules above.
4. **Launch the first EC2 instance** (Ubuntu), install Python, clone the project, create a virtual environment and install the dependencies.
5. **Configure the RDS connection** and test Flask directly at `http://EC2-PUBLIC-IP:5000`.
6. **Launch the second EC2 instance** with the identical application and database configuration.
7. **Create the target group** `BusBooking-TG` (HTTP, port 5000, health check path `/`) and register both instances.
8. **Create the Application Load Balancer** `BusBooking-ALB` (internet-facing, IPv4, HTTP listener on port 80) forwarding to the target group.
9. **Verify** that both targets are **Healthy**, then open the application through the ALB DNS name.
10. **Run the testing checklist** below.

---

## 5. Screenshots

### Landing Home Page
![Landing home Page](Screenshot/Landing%20home%20Page.png)

### User Registration
![User Registration](Screenshot/User%20Registration.png)

### User Login
![user login](Screenshot/user%20login.png)

### Bus Search and Routes
![Bus Search and Routes](Screenshot/Bus%20Search%20and%20Routes.png)

### Seat Selection and Booking
![Seat Selection and Booking](Screenshot/Seat%20Selection%20and%20Booking.png)

### Live Bus Status
![Live Bus Status](Screenshot/Live%20Bus%20Status.png)

### EC2 Instance (Application Server)
![EC2 Instance Application Server](Screenshot/EC2%20Instance%20%28Application%20Server%29.png)

### EC2 Security Group
![EC2 security group](Screenshot/EC2%20security%20grp.png)

### RDS MySQL Database (Connectivity)
![RDS MySQL Database Connectivity](Screenshot/RDS%20MySQL%20Database%20%28Connectivity%29.png)

---

## 6. How to Run or Deploy the Project

### Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/Farande/CapstoneProject_4_AWS-Bus-Booking-Application-with-ALB.git
cd CapstoneProject_4_AWS-Bus-Booking-Application-with-ALB
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

`requirements.txt` contains `Flask`, `PyMySQL` and `Werkzeug`.

**4. Configure the database connection**

```python
DB_HOST = "foodorderdb.c9c6mkwkmeli.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "YOUR-PASSWORD"
DB_NAME = "BusBookingDB"
DB_PORT = 3306
```

> Do not commit real values. Read them from environment variables instead.

**5. Run Flask**

```bash
python3 app.py
```

Open `http://127.0.0.1:5000`. On EC2, Flask listens on `0.0.0.0:5000`.

### Deploy on AWS

1. **RDS:** Create a MySQL database named `BusBookingDB` (user `admin`, port 3306). Allow port 3306 only from `BusBooking-EC2-SG`.
2. **EC2 instance 1:** Launch Ubuntu, then run:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv -y
   git clone https://github.com/Farande/CapstoneProject_4_AWS-Bus-Booking-Application-with-ALB.git
   cd bus_bookings
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python3 app.py
   ```
3. **Test directly** with the instance's **public IPv4** address: `http://EC2-PUBLIC-IP:5000`. Do not use the private `172.31.x.x` address.
4. **EC2 instance 2:** Repeat step 2 with the same configuration and the same RDS database.
5. **Target group:** `BusBooking-TG`, target type Instances, HTTP, port 5000, health check path `/`. Register both instances.
6. **Load balancer:** `BusBooking-ALB`, internet-facing, IPv4, HTTP listener on port 80 forwarding to `BusBooking-TG`.
7. **Access** the application at `http://YOUR-ALB-DNS-NAME`.

### Health Check

The ALB calls `GET /`, which the Flask application serves with:

```python
@app.route("/")
def index():
    return render_template("index.html")
```

When it responds correctly, each target shows as **Healthy**.

### Testing Checklist

**Application**
- [ ] Home page loads
- [ ] Registration and login work
- [ ] Bus list and search work
- [ ] Seat booking works
- [ ] Booking history displays
- [ ] Admin login and dashboard work

**Database**
- [ ] EC2 can connect to RDS
- [ ] Users, buses and bookings are stored
- [ ] Available seat count is updated

**AWS**
- [ ] Both EC2 instances are running Flask
- [ ] RDS is available
- [ ] ALB is active and the target group is healthy
- [ ] RDS accepts connections only from the EC2 security group

### Security Notes

Never upload the following to GitHub:

```text
AWS Access Keys
AWS Secret Keys
RDS password and database credentials
Private SSH keys (.pem)
.env files containing passwords
```

Use environment variables for sensitive configuration, and add `.env`, `*.pem`, `venv/` and `__pycache__/` to `.gitignore`.

---

## 7. Key Learnings

- **Load balancing:** An ALB with a target group spreads traffic across several EC2 instances and removes unhealthy ones from rotation, improving availability.
- **Layered security groups:** Chaining security groups (Internet to ALB, ALB to EC2, EC2 to RDS) means each tier is reachable only from the tier in front of it.
- **Private database access:** Keeping RDS closed to the public internet and allowing only the application's security group greatly reduces the attack surface.
- **Stateless application servers:** Because both instances share one RDS database, any instance can serve any request, which makes horizontal scaling possible.
- **Health checks:** A simple `/` endpoint lets the target group verify each instance, and Flask must listen on `0.0.0.0`, not just `127.0.0.1`.
- **Public vs private IPs:** Direct testing uses the EC2 public IPv4 address, while `172.31.x.x` addresses only work inside the VPC.
- **Secrets management:** Database credentials should live in environment variables or a secrets service, never in source code or Git.
- **Troubleshooting:** Most connectivity problems come from security group rules, so checking them first saves time.

---

