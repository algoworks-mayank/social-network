# Social Network API

## Installation Steps

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd socialnetwork
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Apply migrations:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. Access the API at `http://localhost:8000/api/`.

## API Endpoints

- `POST /api/signup/`: Signup a new user.
- `POST /api/login/`: Login a user and get a JWT token.
- `POST /api/token-refresh/`: Refresh JWT token.
- `GET /api/search/`: Search users by email or name.
- `POST /api/friend-request/`: Send a friend request (max 3 requests per minute).
- `PUT /api/friend-request/<id>/`: Accept or reject a friend request.
- `GET /api/friends/`: List friends.
- `GET /api/pending-requests/`: List pending friend requests.
