# GenAI_test_task

A Django-based API for managing user registration, balance, and currency exchange functionality. The API allows users to register, check their balance, exchange currencies, and view transaction history.

## Features

- **User Registration**: Allows users to create an account with a username and password.
- **Balance Management**: Each user has a balance, which can be checked and used for currency exchanges.
- **Currency Exchange**: Users can exchange currencies (USD, EUR, etc.) and check current exchange rates.
- **Transaction History**: Users can view their currency exchange transaction history, optionally filterable by currency code or date.
  
<br><br>

## Installation

### 1. Clone the repository
```bash
https://github.com/oksanamazurak/GenAI_test_task.git
```

### 2. Navigate to the cloned directory and create a virtual environment
```bash
cd GenAI_test_task
python -m venv venv
```

### 3. Activate the virtual environment

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install all required dependencies
```bash
pip install -r requirements.txt
```

### 5. Navigate to the test-task directory
```bash
cd test-task
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Start the development server
```bash
python manage.py runserver
```
---

## API Endpoints

### **POST** `/register/`  
Register a new user.

### **GET** `/balance/`  
Get user balance. **JWT token required.**

### **POST** `/currency/`  
Get currency exchange rate. **JWT token required.**

### **GET** `/history/`  
Get exchange history. **JWT token required.**

### **POST** `/token/`  
Get JWT token using username and password.
<br><br>

---

## API Documentation with Swagger

You can view the interactive API documentation using Swagger by navigating to the `/swagger` endpoint.
<br><br>

---

## Running Tests

### 1. Navigate to the directory containing the manage.py file
```bash
cd test-task
```

### 2. Run the test suite using the following command
```bash
python manage.py test
```

