# Agentic Customer Support Bot

## 📄 Description

This project is a Python-based customer support bot that answers queries based on a provided document. It features an "agentic" workflow, allowing it to refine its answers based on simulated user feedback. The bot is built with a local Hugging Face transformer model for question-answering and uses semantic search to find relevant information.

## ✨ Features

* **Document Training:** Learns from any provided `.txt` file to build its knowledge base.
* **Semantic Search:** Uses `sentence-transformers` to find the most relevant document section for a user's query.
* **Extractive Question Answering:** Employs a Hugging Face `transformer` model (`distilbert`) to extract precise answers from the text.
* **Agentic Feedback Loop:** Simulates user feedback and automatically adjusts its response strategy to provide more detail when needed.
* **Robustness:** Gracefully handles out-of-scope questions by checking relevance scores.
* **API & Front End:** A simple Flask API and HTML/CSS/JS front end are included to make the bot interactive.
* **Logging:** Logs all major decisions and actions to `support_bot_log.txt` for transparency and debugging.

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd <your-project-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ How to Run

To interact with the bot, run the Flask web application:

```bash
flask --app app run --port 5002
