# My Social Network

My Social Network is a web-based social networking platform designed to connect users, facilitate communication, and share updates in real-time.

## Technologies

- **Backend:**
  - FastAPI
  - PostgreSQL
  - SQLAlchemy
  - Redis
  - Alembic
  - OAuth2
  - WebSockets

- **Frontend:**
  - HTML/CSS
  - Bootstrap
  - JavaScript

## Functionality

My Social Network offers the following features:

### Authorization System

- User registration and secure authentication using OAuth2.

### Posts Page

- View posts from subscribed users.

### Follow and Unfollow Page

- Follow and unfollow other users to customize your news feed.

### Create Post Page

- Share your own posts and updates with your followers.

### Chats Page

- Create chat rooms.
- Add other users to the chat.
- Exit chat rooms.

### Real-time Communication

- Users can communicate in chat rooms in real-time.

## Screenshots

Add screenshots of your project here to showcase its user interface and functionality.

[Insert Screenshots Here]


## Installation

To install and run My Social Network without Docker, follow these steps:

1. **Clone the Project:**

   - Clone the project repository to your local machine:

     ```bash
     git clone 
     cd my-social-network
     ```

2. **Set up the Backend(without Docker):**

   - Ensure you have Python 3.10+ installed.
   - Create a virtual environment and activate it:

     ```bash
     python -m venv myenv
     source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
     ```

   - Install the required Python packages:

     ```bash
     pip install -r requirements.txt
     ```

   - Configure your database connection in the `config.py` file.

   - Apply database migrations using Alembic:

     ```bash
     alembic upgrade head
     ```

   - Run the FastAPI application:

     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8000 --reload
     ```
3. Open your web browser and access the application at `http://localhost:8000`.

