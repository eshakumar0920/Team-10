# Team-10 Senior Design Project: Campus Event App

A web application that allows students to create and join events on campus.

### Setup Instructions

#### Prerequisites
- Python 3.8+
- PostgreSQL

#### Database Setup
1. Create a PostgreSQL database:
```sql
CREATE DATABASE events_db;
CREATE USER eventadmin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE events_db TO eventadmin;
GRANT ALL ON SCHEMA public TO eventadmin;
