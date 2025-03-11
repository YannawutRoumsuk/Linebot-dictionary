# Linebot Dictionary

A LINE chatbot that provides dictionary definitions using FastAPI and LINE Messaging API.

## Features
- Receive and respond to text messages via LINE
- Fetch word definitions from an online dictionary API
- Deployable to AWS Lambda

---

## Prerequisites

Ensure you have the following installed:
- **Python 3.10+**
- **pip** (Python package manager)
- **virtualenv** (optional but recommended)
- **Git**
- **LINE Developer Account** (to get API credentials)

---

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/YannawutRoumsuk/Linebot-dictionary.git
cd Linebot-dictionary
```

### 2. Create a virtual environment (optional but recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

---

## Configuration

### 1. Create a `.env` file in the `app_fast-api` directory
Add the following environment variables:
```env
ACCESS_TOKEN=your_line_access_token
CHANNEL_SECRET=your_line_channel_secret
```
Replace `your_line_access_token` and `your_line_channel_secret` with actual values from your LINE Developer Console.

---

## Running the Application Locally (For `app_fast-api` Only)

### 1. Navigate to `app_fast-api`
```sh
cd app_fast-api
```

### 2. Start FastAPI Server
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Expose the local server using ngrok
If testing locally with LINE, install **ngrok** and run:
```sh
ngrok http 8000
```
Copy the HTTPS URL from ngrok and update your **LINE webhook URL** in the LINE Developer Console.

---

## Deployment to AWS Lambda

### 1. Navigate to `app_lambda-function`
```sh
cd app_lambda-function
```

### 2. Install AWS CLI (if not installed)
```sh
pip install awscli
```

### 3. Configure AWS Credentials
```sh
aws configure
```
Provide your **AWS Access Key ID** and **Secret Access Key**.

### 4. Package the application for AWS Lambda
Use the following script to zip the function and dependencies:
```sh
pip install -r requirements.txt -t ./package
cd package
zip -r ../function.zip .
cd ..
zip -g function.zip lambda_handler.py
```

### 5. Deploy to AWS Lambda
```sh
aws lambda create-function --function-name linebot-dictionary \
    --runtime python3.10 \
    --role arn:aws:iam::your-account-id:role/lambda-role \
    --handler lambda_handler.lambda_handler \
    --zip-file fileb://function.zip
```
Replace `your-account-id` with your actual AWS account ID and `lambda-role` with the correct IAM role.

### 6. Set up API Gateway for Lambda

#### a. Create an API Gateway
- Go to **AWS Management Console** → **API Gateway**
- Click **Create API** → **HTTP API**
- Click **Add Integration** → **Lambda Function**
- Select your function (`linebot-dictionary`) and click **Create**

#### b. Deploy API
- Click **Deploy API** and note the endpoint URL
- Use this URL as the webhook URL in LINE Developer Console

---

## Testing the API

### 1. Test using cURL (For `app_fast-api` on local machine)
```sh
curl -X POST "http://127.0.0.1:8000/callback" -H "Content-Type: application/json" -d '{"events": [{"message": {"text": "hello"}}]}'
```

### 2. Test on AWS Lambda via API Gateway
Invoke the API using:
```sh
curl -X POST "https://your-api-gateway-url/callback" -H "Content-Type: application/json" -d '{"events": [{"message": {"text": "hello"}}]}'
```
Replace `your-api-gateway-url` with the actual API Gateway URL.

---

## License
This project is licensed under the MIT License.

