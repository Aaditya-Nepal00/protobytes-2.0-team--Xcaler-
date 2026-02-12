# Projects API

## Endpoints

### List Projects
**GET** `/api/projects`

Response:
```json
[
  {
    "id": "project-id",
    "title": "Infrastructure Project",
    "description": "Project description",
    "status": "active",
    "budget": 1000000,
    "location": "Location"
  }
]
```

### Get Project Details
**GET** `/api/projects/{id}`

Response:
```json
{
  "id": "project-id",
  "title": "Infrastructure Project",
  "description": "Project description",
  "status": "active",
  "budget": 1000000,
  "location": "Location",
  "startDate": "2024-01-01",
  "endDate": "2024-12-31"
}
```

### Create Project
**POST** `/api/projects`

Request:
```json
{
  "title": "New Project",
  "description": "Description",
  "budget": 500000,
  "location": "Location"
}
```

Response:
```json
{
  "message": "Project created",
  "id": "project-id"
}
```

### Update Project
**PUT** `/api/projects/{id}`

Request:
```json
{
  "title": "Updated Title",
  "status": "completed"
}
```

### Delete Project
**DELETE** `/api/projects/{id}`

## Status Values

- `planning` - Planning phase
- `active` - Currently under way
- `completed` - Finished
- `on-hold` - Temporarily suspended

## Query Parameters

- `status` - Filter by status
- `location` - Filter by location
- `page` - Pagination page (default: 1)
- `limit` - Items per page (default: 20)
