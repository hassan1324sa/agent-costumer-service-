# Agent Customer Service

This repository contains the code for an agent-based customer service system. The project leverages various AI agents, a Telegram bot, and a FastAPI backend to provide automated customer support and booking functionalities.

## Features

- **Intelligent Agents**: Utilizes RAG (Retrieval-Augmented Generation), booking, and routing agents to handle diverse customer queries.
- **Telegram Bot Integration**: Provides a conversational interface for users via Telegram.
- **FastAPI Backend**: A robust and scalable API built with FastAPI, handling requests and orchestrating agent interactions.
- **Modular Structure**: Organized into `agents`, `bot`, `controllers`, `models`, `routers`, and `stores` for clear separation of concerns.
- **Dockerized Environment**: Includes `docker-compose.yml` for easy setup and deployment using Docker.

## Project Structure

```
agent-customer-service-/
├── docker/
│   └── docker-compose.yml
├── src/
│   ├── agents/
│   │   ├── bookingAgent.py
│   │   ├── ragAgent.py
│   │   └── routerAgent.py
│   ├── assets/
│   ├── bot/
│   │   └── telegramBot.py
│   ├── controllers/
│   │   ├── baseController.py
│   │   ├── bookingController.py
│   │   └── dataController.py
│   ├── helpers/
│   │   ├── config.py
│   │   └── jsonEncoder.py
│   ├── main.py
│   ├── models/
│   │   ├── baseDataModel.py
│   │   ├── bookingModel.py
│   │   ├── dataModdel.py
│   │   └── dbSchemes/
│   │       ├── booking.py
│   │       └── data.py
│   │       └── retrieveDocs.py
│   │   └── enums/
│   │       ├── dataBaseEunm.py
│   │       └── responseEnum.py
│   ├── routers/
│   │   ├── base.py
│   │   ├── booking.py
│   │   └── data.py
│   └── stores/
│       ├── llms/
│       │   └── provider.py
│       └── vectordb/
│           ├── providers/
│           │   └── QdrantDB.py
│           └── vecotrDBInterface.py
│           └── vectorDBProviderFactory.py
└── README.md
```

## Setup and Installation

To get this project up and running, follow these steps:

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### 1. Clone the repository

```bash
git clone https://github.com/hassan1324sa/agent-customer-service-.git
cd agent-customer-service-
```

### 2. Set up environment variables

Create a `.env` file in the root directory and add necessary environment variables, such as API keys for LLMs, database connection strings, and Telegram bot token. An example `.env.example` might be provided later.

```ini
# Example .env content (adjust as per your actual configuration)
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
DATABASE_URL=sqlite:///./sql_app.db
```

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

This command will build the Docker images and start the services defined in `docker-compose.yml`.

### 4. Manual Installation (Alternative)

If you prefer to run without Docker, you can set up a virtual environment and install dependencies manually.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

*(Note: `requirements.txt` will be generated in the next step.)*

## Usage

Once the services are running, the Telegram bot will be active and the FastAPI endpoints will be accessible. Interact with the bot via Telegram to utilize the customer service agents. The API documentation will be available at `/docs` or `/redoc` if enabled in `main.py`.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. (Note: `LICENSE` file not currently in repo, consider adding one.)

## Contact

For any questions or suggestions, please contact [hassan1324sa](https://github.com/hassan1324sa).
