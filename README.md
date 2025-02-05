# paraprofessional-assessment-db
# Paraprofessional Assessment Database and Dashboard

## Overview
This repository hosts the SQL schema, dummy data scripts, and integration code for a comprehensive pre-employment assessment designed for paraprofessionals in education and healthcare. The assessment uses validated instruments to measure key competencies including emotional regulation, communication skills, and basic literacy and numeracy. Data from survey responses is stored in a cloud-based SQL database and visualized via an interactive Tableau dashboard, which is embedded in a WordPress site.

## Components

### 1. SQL Database
- **Schema (`schema.sql`):** Defines a `survey_results` table that captures:
  - **Role:** Administrator, Professional Counselor/Teacher, Paraprofessional, or No Experience.
  - **Demographics:** Gender and Education level.
  - **Survey Responses:** Scores for DERS Overall, NONACCEPTANCE, GOALS, IMPULSE, AWARENESS, STRATEGIES, and CLARITY.
  - **Timestamp:** Records the submission time.

- **Data Insertion (`insert_dummy_data.sql`):** Populates the database with records that represent:
  - **520 records for women** and **194 records for men**.
  - **Role distribution:** 10 Administrators, 36 Teachers, and 28 Paraprofessionals.
  - **Education details:** Administrators include 2 with doctorates and 8 with master’s degrees; 36% of Teachers have master’s degrees (with the remainder holding bachelor’s degrees); Paraprofessionals have a gender distribution of 85% women.

### 2. Python API Integration
- **Flask Application (`app.py`):** 
  - Connects to the cloud-hosted SQL database using SQLAlchemy.
  - Provides a `/submit` endpoint that accepts POST requests from Forminator forms.
  - Inserts new survey responses into the `survey_results` table, enabling real-time data updates.

### 3. Dashboard Integration
- **Tableau Dashboard:**
  - Connects directly to the SQL database to visualize survey data.
  - Displays metrics such as normal distribution curves for subscale scores by gender, demographic breakdowns, and key performance indicators.
  - Designed to be embedded on a WordPress site via an iframe, offering live updates as new survey data is received.

## Deployment
- **SQL Database:** Hosted on a cloud service (e.g., ElephantSQL or Heroku Postgres).
- **Python API:** Deployed on a platform like Heroku or PythonAnywhere.
- **Tableau Dashboard:** Published on Tableau Public or your organization's Tableau Server and embedded in your WordPress site.

## Setup and Usage
1. **Clone this Repository:**
   ```bash
   git clone https://github.com/yourusername/paraprofessional-assessment-db.git
   cd paraprofessional-assessment-db

---

This README explains the purpose of the repository, details the database schema and data insertion process, describes the Python API integration, and outlines how the Tableau dashboard is configured and deployed.
