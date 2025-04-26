# Store Monitoring System

This project is a backend system designed to monitor and report the uptime and downtime of stores. It provides APIs to generate comprehensive reports based on predefined data sources, ensuring accurate monitoring of store activity during business hours.

---

## Features

1. **Dynamic Report Generation**
   - Generate reports on store uptime and downtime based on data ingested into the system.
   - Reports include detailed metrics for the last hour, day, and week.

2. **APIs for Report Management**
   - Trigger report generation asynchronously.
   - Fetch the status of a report or download the generated report in CSV format.

3. **Business Hour Consideration**
   - Uptime and downtime are calculated only during business hours of the store.
   - Handles missing business hours and timezones with default values.

4. **Data Extrapolation**
   - Interpolates uptime/downtime data for periods without direct observations, ensuring accurate reporting.

---

## API Documentation

### 1. **Trigger Report**
Endpoint: `/trigger_report/`  
Method: `POST`

Description: Triggers the report generation process.

**Request Body:** None  

**Response:**
```json
{
    "report_id": "unique-report-id"
}
```

- `report_id`: A unique identifier for the generated report, which can be used to fetch its status.

---

### 2. **Get Report**
Endpoint: `/get_report/<report_id>/`  
Method: `GET`

Description: Fetches the status of the report or downloads the generated CSV report.

**Path Parameter:**
- `report_id`: The unique identifier of the report (received from `/trigger_report/`).

**Response:**
- If the report is still being generated:
  ```json
  {
      "status": "Running"
  }
  ```

- If the report is completed:
  - The generated CSV file is returned as a download.

- If the report generation failed or the report ID is invalid:
  ```json
  {
      "error": "Report not found"
  }
  ```

---

## Setup Instructions

### 1. **Environment Setup**
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- Apply database migrations:
  ```bash
  python manage.py migrate
  ```

- Start the development server:
  ```bash
  python manage.py runserver
  ```

### 2. **Database**
- Populate the database with initial data from CSV files.

### 3. **Run the Application**
- Use the APIs to generate and fetch reports.

---

## Example Workflow

1. **Trigger a Report**
   - Send a `POST` request to `/api/trigger_report/`.
   - Receive a `report_id` in the response.

2. **Check Report Status**
   - Use the `report_id` to send a `GET` request to `/api/get_report/<report_id>/`.
   - If the report is ready, the CSV file will be returned as a downloadable response.

---

## Improvements
- Implement asynchronous tasks using Celery to improve performance during report generation.
- Add authentication to secure API endpoints.
- Optimize data processing for large datasets.

---

## Notes
- Ensure the necessary data files are loaded into the database before triggering reports.
- Default values are used for missing timezone or business hour data.

---
