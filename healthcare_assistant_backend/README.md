
# 🩺 AI-Powered Healthcare Appointment Assistant (Text-Based)

An **AI-driven healthcare appointment assistant** built for the **AWS AI Agent Hackathon**, designed to help patients book, cancel, and check appointments through **natural language text**.
The backend is powered by **Flask**, **Amazon Bedrock (Claude 3 Sonnet)**, and **AWS DynamoDB** — making the system intelligent, accessible, and scalable.

---

## 🚀 Project Overview

This project demonstrates how AI can simplify healthcare interactions by enabling **text-based appointment management**.
Patients can simply type messages like:

> “Book an appointment with Dr. Lee tomorrow at 10 AM.”

The assistant interprets the intent, processes it using **Amazon Bedrock**, stores the data in **AWS DynamoDB**, and returns a confirmation — all automatically.

---

## 🧱 Tech Stack

| Layer                      | Technology                                         |
| -------------------------- | -------------------------------------------------- |
| **Frontend**               | Web-based Text Interface (React or HTML/JS client) |
| **Backend**                | Flask (Python 3.12)                                |
| **AI Model**               | Amazon Bedrock – Claude 3 Sonnet                   |
| **Database**               | AWS DynamoDB                                       |
| **SDK**                    | boto3                                              |
| **Environment Management** | Conda                                              |
| **Hosting Options**        | AWS Elastic Beanstalk / EC2 / ECS Fargate          |

---

## 🧩 Architecture Overview

```
💬 User Input (Text)
   ↓
🧠 Amazon Bedrock → Understands intent (book/cancel/check)
   ↓
⚙️ Flask Backend → Processes intent
   ↓
🗂️ AWS DynamoDB → Stores or retrieves appointment data
   ↓
💬 Flask → Returns confirmation or appointment summary
```

---

## 📁 Project Structure

```
healthcare_assistant_backend/
│
├── app.py                           # Flask main server
├── requirements.txt                  # Dependencies
├── .env                              # Environment variables (AWS creds)
└── services/
    ├── bedrock_service.py            # Amazon Bedrock integration
    └── dynamodb_service.py           # DynamoDB booking logic
```

---

## 🧠 Phase 1 — Flask Backend Setup

In **Phase 1**, the foundational Flask server was created to serve as the backend for the AI-powered appointment system.
This phase focused on environment setup, dependency management, and AWS SDK connectivity.

### 🔧 Key Objectives

* Created and activated a dedicated **Conda environment**.
* Installed core dependencies: `flask`, `boto3`, `requests`, and `python-dotenv`.
* Configured AWS credentials locally using `aws configure`.
* Built and verified the Flask server with test endpoints.

### 🧪 Verification Endpoints

| Endpoint    | Description                         |
| ----------- | ----------------------------------- |
| `/`         | Confirms Flask server is running.   |
| `/aws-test` | Validates AWS connection using STS. |

Example response:

```json
{
  "AWS Test": "Connection successful ✅",
  "Account": "123456789012",
  "UserArn": "arn:aws:iam::123456789012:user/monika"
}
```

### ✅ Outcome

* Flask backend was running locally on `http://localhost:5000`.
* AWS SDK (`boto3`) connectivity verified.
* Environment ready for AI and database integration.

---

## 🧠 Phase 2 — AI and Database Integration

In **Phase 2**, the Flask backend was enhanced with **AI intent detection** (Amazon Bedrock) and **data persistence** (DynamoDB).
The `/chat` endpoint was introduced to process text messages, interpret user intent, and perform real appointment actions.

### 🔧 Key Objectives

* Integrated **Amazon Bedrock (Claude 3 Sonnet)** to extract intent and entities.
* Connected **AWS DynamoDB** to store and manage appointments.
* Implemented `/chat` endpoint for end-to-end AI-driven appointment handling.

### 🧩 Flow

```
User → /chat → Bedrock → Flask Logic → DynamoDB → Response
```

### ⚙️ Example Request

```bash
POST /chat
Content-Type: application/json

{
  "message": "Book an appointment with Dr. Lee tomorrow at 10 AM"
}
```

### ⚙️ Example Response

```json
{
  "reply": "✅ Appointment booked with Dr. Lee on 2025-10-13 at 10:00 AM.",
  "ai_output": {
    "intent": "book_appointment",
    "doctor": "Dr. Lee",
    "date": "2025-10-13",
    "time": "10:00 AM"
  }
}
```

### ✅ Outcome

* The system can **understand natural language input** via Bedrock.
* Appointments are **created, cancelled, or listed** dynamically using DynamoDB.
* Backend fully operational and ready for frontend integration.

---

## 🧾 Environment Setup

```bash
# 1️⃣ Create environment
conda create -n AWSHackathon python=3.11

# 2️⃣ Activate environment
conda activate AWSHackathon

# 3️⃣ Install dependencies
pip install flask boto3 requests python-dotenv

# 4️⃣ Run Flask server
python app.py
```

Server runs on:
👉 `http://127.0.0.1:5000/`

---

## 🔐 AWS Services & Permissions

Ensure the IAM role or user has the following permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "dynamodb:*",
    "sts:GetCallerIdentity"
  ],
  "Resource": "*"
}
```

Region used: `us-east-1`

---

## 🧾 Example DynamoDB Schema

| Attribute        | Type   | Description                     |
| ---------------- | ------ | ------------------------------- |
| `appointment_id` | String | Unique identifier               |
| `user_id`        | String | User who booked the appointment |
| `doctor_name`    | String | Doctor's name                   |
| `date`           | String | Appointment date                |
| `time`           | String | Appointment time                |
| `status`         | String | Booked/Cancelled                |
| `created_at`     | String | Timestamp                       |

---

## 🌟 Next Steps (Phase 3)

* Add a **React or HTML-based text interface** for patient interaction.
* Enable **voice accessibility** using Amazon **Transcribe** (speech → text) and **Polly** (text → speech).
* Deploy to **AWS Elastic Beanstalk** or **ECS Fargate** for scalability.
* Integrate **Amazon QuickSight** dashboards for analytics (appointments per doctor, time-slot trends, etc.).

---

## 🏁 Hackathon Impact Statement

This project empowers patients — including those with accessibility challenges — to easily manage medical appointments using **AI-powered, natural language interaction**.
By leveraging **Amazon Bedrock** and **AWS serverless technologies**, it delivers a secure, scalable, and inclusive healthcare experience.

---

Would you like me to now extend this README with a **Phase 3 section** (frontend + accessibility + deployment) to make it fully end-to-end and ready for your AWS Hackathon submission?
