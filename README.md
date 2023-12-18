# Events Application

## Introduction
This FastAPI application is designed to manage events and send reminders. It allows users to create events, sign up for reminders, and handles the automatic sending of reminder emails.

Tools and packages used in this project:

- [FastAPI](https://fastapi.tiangolo.com//): a micro web framework written in Python
- [Docker](https://www.docker.com/): a set of platform as a service products that uses OS-level virtualization to deliver software in packages called containers

## Features
- Create and manage events.
- Sign up for event reminders.
- Automatic reminder notifications via email.


## Installation

### Setup
You need to install the followings:

- Python 3.10
- Docker

### Running
1. Clone the repository:
   ```bash
   $git clone https://github.com/Avichai96/AlfaBet.git
2. Setup database 
    ```bash
    $docker compose up
3. Switch to `app` dir
4. Run Tests
    ```bash
    $pytest
5. Run Application
    ```bash
    $python3 app/main.py
6. Visit http://127.0.0.1:8080/docs/ to check API docs. 



## API Endpoints

### Events

| Endpoint            | HTTP Method | Description                 |
|---------------------|-------------|-----------------------------|
| `/events/`          | `GET`       | List all events.            |
| `/events/`          | `POST`      | Create a new event.         |
| `/events/bath/`     | `POST`      | Create a new batch events.  |
| `/events/bath/`     | `PUT`       | Update a batch events.      |
| `/events/bath/`     | `DELETE`    | Delete a batch events.      |
| `/events/{event_id}`| `GET`       | Retrieve a specific event.  |
| `/events/{event_id}`| `PUT`       | Update a specific event.    | 
| `/events/{event_id}`| `DELETE`    | Delete a specific event.    |

### Reminders

| Endpoint                              | HTTP Method | Description                      |
|---------------------------------------|-------------|----------------------------------|
| `/reminders/`                         | `GET`       | List all reminders.              |
| `/reminders/signup-for-reminder/`     | `POST`      | Sign up for a new reminder.      |
| `/reminders/unsubscribe/`             | `POST`      | Unsubscribe from reminder.       |
