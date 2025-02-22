# Algorithmen und Datenstrukturen RAG-Chatbot Backend

## Setup

1. **Set up Development Environment:**
    Run the following `make` command to initialize your development environment. This command will:

    - **Create a Python virtual environment:** Isolates project dependencies in a `.venv` directory within your project.
    - **Install Python dependencies:** Installs all required Python packages listed in `requirements.txt` into the virtual environment.
    - **Start PostgreSQL Database (using Docker Compose):** Launches a PostgreSQL database in a Docker container using the configuration in `docker-compose.yml`.

    ```bash
    make setup
    ```

2. **Activate the Virtual Environment:**
    Before running the application, activate the virtual environment.

    - If you use direnv, just do:
        ```bash
        direnv allow
        ```
    - or activate it manually:
        ```bash
        source .venv/bin/activate
        ```

3. **Start the FastAPI Application:**
    Run the backend application in development mode with automatic code reloading using `make run`:

    ```bash
    make run
    ```

4. **Accessing API Endpoints:**
    The backend currently provides the following main API endpoints:

    - `POST /chat/start`: Starts a new chat session, the json-body must contain an `initial_message`, returns a `chat_id`.
    - `POST /chat/{chat_id}/message`: Sends a user message to a specific chat session.
    - `GET /chat/{chat_id}/poll`: Polls for new chatbot messages in a specific chat session.

    See the "API Endpoints" section below for more details and example `curl` commands.

5. **Stopping the Database (when done developing):**
    When you are finished with development and want to stop the PostgreSQL database running in Docker, use:

    ```bash
    make docker-down
    ```

6. **Cleaning Up the Environment (Optional):**
    To stop the database, remove the virtual environment, and clean up build artifacts, you can use:

    ```bash
    make clean
    ```
    This command will also stop the Docker database container.

## Configuration

Application settings are managed through a combination of:

- **`config.py`:** Contains default settings and defines the structure of the configuration using Pydantic Settings. Key settings like the database URL (for the Docker Compose setup), default LLM model name, etc., are defined here.
- **`.env` file:** Environment variables are loaded from a `.env` file in the project root (if it exists). This is the recommended way to store sensitive configuration like API keys.

## API Endpoints

Here are example `curl` commands to interact with the main API endpoints.

1. **Start a New Chat Session (`POST /chat/start`):**

    ```bash
    curl -X POST \
         -H "Content-Type: application/json" \
         -d '{"initial_message": "Hello, I have a question about..."}' \
         http://127.0.0.1:8000/chat/start
    ```

    **Response:**
    ```json
    {"chat_id": "your-chat-id"}
    ```

2. **Poll for Messages (`GET /chat/{chat_id}/poll`):**

    ```bash
    curl http://127.0.0.1:8000/chat/{your-chat-id}/poll
    ```

    **Response:**
    ```json
    {
      "messages": [
        {
          "text": "Chatbot response message 1...",
          "is_user": false
        },
        ...
      ],
      "status": "generating"  // or "done" when all messages are generated
    }
    ```

3. **Send another User Message (`POST /chat/{chat_id}/message`):**

    ```bash
    curl -X POST \
         -H "Content-Type: application/json" \
         -d '{"user_message": "Your user question here"}' \
         http://127.0.0.1:8000/chat/{your-chat-id}/message
    ```

    **Response:**
    ```json
    {"status": "message_sent"}
    ```

