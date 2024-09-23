## Running the Application

## Required Software

1. Python
2. Node.js
3. Docker and Docker Compose
4. [Poetry](https://python-poetry.org/docs/#installation)
5. Postgres libpq header files (e.g. `apt install libpq-dev` on Ubuntu, `brew install postgresql` on macOS)

### First-Time Setup

1. Run `make init`


### Running the Application
1. Run `make run` or `docker compose up --build` to start the backend application and database.
2. In another terminal, `cd` into `frontend` and run `npm run dev` to start the frontend application.
