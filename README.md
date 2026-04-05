# Industrial Machine Fault Diagnosis Environment

This is a reinforcement-learning-style environment for machine condition diagnosis, fully compatible with OpenEnv and Hugging Face Spaces.

## Architecture
The system is built as a RESTful API with FastAPI and follows the standard environment abstraction:
- **`my_env.py`**: Contains the `FaultEnv` class simulating the machine logic and calculating rewards.
- **`models.py`**: Defines Pydantic models mapping to Observations, Actions, and Step results.
- **`server.py`**: Exposes the environment as a web API (`/reset`, `/step`, `/state`).
- **`inference.py`**: Simulates an agent interaction using OpenAI's GPT models.

## API Endpoints
- `POST /reset`: Resets the environment and returns the initial observation.
- `POST /step`: Takes an action and returns the new observation, reward, done flag, and info.
- `GET /state`: Retrieves internal simulation state.

## How to Run Locally
Ensure Python 3.10+ is installed.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 7860
   ```
3. Run inference in another terminal window:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   python inference.py
   ```

## How to Run Docker
Containerized version ready for isolated testing.
```bash
docker build -t fault-env .
docker run -p 7860:7860 fault-env
```

## How to Deploy on Hugging Face Spaces
This project is fully designed to run seamlessly on Hugging Face Spaces using the Docker template.
1. Create a new Space on Hugging Face.
2. Select **Docker** as the Space SDK.
3. Choose the "Blank" Docker template.
4. Upload all the files from this directory to the Space.
5. Hugging Face Spaces will automatically build the `Dockerfile` and expose port `7860`.
