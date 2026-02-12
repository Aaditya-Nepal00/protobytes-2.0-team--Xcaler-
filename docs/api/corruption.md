# Corruption Reporting API

## Endpoints

### Submit Corruption Report
**POST** `/api/corruption/report`

Request:
```json
{
  "title": "Report Title",
  "description": "Detailed description",
  "severity": "high",
  "projectId": "project-id"
}
```

Response:
```json
{
  "message": "Report submitted",
  "reportId": "report-id"
}
```

### Get All Reports
**GET** `/api/corruption/reports`

Query Parameters:
- `status` - Filter by status
- `severity` - Filter by severity
- `page` - Pagination

Response:
```json
[
  {
    "id": "report-id",
    "title": "Report Title",
    "status": "investigating",
    "severity": "high",
    "submittedDate": "2024-01-15"
  }
]
```

### Track Report Status
**GET** `/api/corruption/track/{reportId}`

Response:
```json
{
  "reportId": "report-id",
  "status": "investigating",
  "updates": [
    "Report received",
    "Investigation started"
  ],
  "lastUpdated": "2024-01-20"
}
```

## Severity Levels

- `low` - Minor issue
- `medium` - Moderate concern
- `high` - Serious violation
- `critical` - Emergency level

## Report Status

- `submitted` - Initial submission
- `investigating` - Under investigation
- `resolved` - Investigation complete
- `closed` - Case closed

## Encryption

All reports are encrypted end-to-end. Submission is anonymous by default, with optional identity disclosure.
