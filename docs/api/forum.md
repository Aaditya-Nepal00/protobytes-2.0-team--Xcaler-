# Forum API

## Endpoints

### List Forum Threads
**GET** `/api/forum/threads`

Query Parameters:
- `sort` - Sort by (newest, popular, active)
- `category` - Filter by category
- `page` - Pagination

Response:
```json
[
  {
    "id": "thread-id",
    "title": "Thread Title",
    "content": "Thread content",
    "author": "author-name",
    "votes": 42,
    "commentCount": 15,
    "createdAt": "2024-01-15"
  }
]
```

### Create Thread
**POST** `/api/forum/threads`

Headers:
```
Authorization: Bearer <token>
```

Request:
```json
{
  "title": "New Discussion",
  "content": "Thread content"
}
```

Response:
```json
{
  "id": "thread-id",
  "message": "Thread created"
}
```

### Get Thread Details
**GET** `/api/forum/threads/{threadId}`

Response:
```json
{
  "id": "thread-id",
  "title": "Thread Title",
  "content": "Content",
  "author": "author-name",
  "votes": 42,
  "comments": [
    {
      "id": "comment-id",
      "content": "Comment text",
      "author": "commenter-name",
      "votes": 5
    }
  ],
  "createdAt": "2024-01-15"
}
```

### Post Comment
**POST** `/api/forum/threads/{threadId}/comments`

Headers:
```
Authorization: Bearer <token>
```

Request:
```json
{
  "content": "Comment text"
}
```

### Vote on Thread/Comment
**POST** `/api/forum/threads/{threadId}/vote`

Request:
```json
{
  "vote": 1  // 1 for upvote, -1 for downvote
}
```

## Moderation

- Comments can be flagged as inappropriate
- Threads can be pinned by moderators
- Users can be muted for violations
