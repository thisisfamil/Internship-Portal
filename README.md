# Mini Internship Portal

A small internship portal built with Python and FastAPI.  
Users can submit applications with their CVs, and admins can manage and review the applications.

---

## Features

- User application submission with CV upload  
- Admin panel to view applicants, see details, and download CVs  
- PostgreSQL database for data storage  

---

## Technologies Used

- Python 3.13  
- FastAPI  
- PostgreSQL  
- psycopg2  
- python-dotenv  

---

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/thisisfamil/Internship-Portal.git
cd Internship-Portal
```
# 2. Create and activate a virtual environment:
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Install dependencies:
pip install -r requirements.txt 

# 4. Create a .env file in the project root and add your database credentials:
HOST=***
PORT=***
DATABASE=***
USER=***
PASSWORD=***

# 5. Run the server: 
uvicorn main:app --reload

---

## Author

**Famil Eyvazli**
GitHub Profile: https://github.com/thisisfamil




