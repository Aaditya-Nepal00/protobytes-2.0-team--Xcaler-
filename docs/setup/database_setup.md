# Database Schema

## Overview

Project Sachet uses PostgreSQL with SQLAlchemy ORM. This document outlines the complete database schema.

## Tables

### Users
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(120) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Projects
```sql
CREATE TABLE projects (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'planning',
    budget FLOAT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tenders
```sql
CREATE TABLE tenders (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    budget FLOAT,
    deadline TIMESTAMP,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Corruption Reports
```sql
CREATE TABLE corruption_reports (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'submitted',
    severity VARCHAR(50),
    reported_by VARCHAR(36) REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Laws
```sql
CREATE TABLE laws (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    category VARCHAR(100),
    simplified TEXT,
    source VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Budget
```sql
CREATE TABLE budgets (
    id VARCHAR(36) PRIMARY KEY,
    year INTEGER,
    sector VARCHAR(100),
    allocation FLOAT,
    spent FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Forum Threads
```sql
CREATE TABLE forum_threads (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    author_id VARCHAR(36) REFERENCES users(id),
    votes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Forum Comments
```sql
CREATE TABLE forum_comments (
    id VARCHAR(36) PRIMARY KEY,
    thread_id VARCHAR(36) REFERENCES forum_threads(id),
    content TEXT,
    author_id VARCHAR(36) REFERENCES users(id),
    votes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationships

- **Users** → **Corruption Reports** (1:M)
- **Users** → **Forum Threads** (1:M)
- **Users** → **Forum Comments** (1:M)
- **Forum Threads** → **Forum Comments** (1:M)

## Indexes

For performance optimization:
- `users.email` - UNIQUE INDEX
- `projects.status` - INDEX
- `tenders.status` - INDEX
- `corruption_reports.status` - INDEX
- `forum_threads.author_id` - INDEX

---

See [Environment Setup](environment_setup.md) for database configuration.
