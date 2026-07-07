# Programming Basics AI Chatbot

> An AI-powered programming tutor built with **FastAPI** and the **OpenAI API**, providing real-time streaming responses and contextual conversations.

![Python](https://img.shields.io/badge/Python-3.10.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

# Overview & Features

Learning to program can be overwhelming for beginners because many explanations assume prior knowledge. This project aims to provide an AI assistant capable of explaining programming topics in plain language with practical examples.

Instead of focusing solely on AI integration, the project builds a complete web application with:

- 💬 Real-time AI responses using streaming
- 🧠 Conversation history for contextual responses
- 📚 Custom system prompt specialized for programming education
- 📝 Markdown rendering for formatted code and explanations
- 📊 Token counting for prompt, completion, and total usage
- 🔄 Conversation reset functionality
- 📱 Responsive chat interface built with Tailwind CSS
- ⚡ REST API built with FastAPI

---

# System Architecture

```text
                    User
                      │
                      ▼
             Web Chat Interface
         (HTML + JavaScript + Tailwind)
                      │
          POST /send_message
                      │
                      ▼
                 FastAPI Backend
                      │
               Chat Service Layer
                      │
      Conversation History + Prompt
                      │
                      ▼
                 OpenAI API
                      │
            Streaming Completion
                      │
                      ▼
          Server-Sent Events (SSE)
                      │
                      ▼
             Live Chat Response
```

---

# Technologies

### Backend

- Python
- FastAPI
- Uvicorn

### AI

- OpenAI API
- Prompt Engineering
- Streaming Chat Completions

### Frontend

- HTML
- JavaScript
- Tailwind CSS
- Font Awesome
- Marked.js

### Utilities

- python-dotenv
- TikToken
- Server-Sent Events (SSE)

---

# AI Pipeline

1. The user submits a programming question through the chat interface.

2. The FastAPI backend receives the request through the `/send_message` endpoint.

3. The user's message is appended to the conversation history alongside the system prompt.

4. The complete conversation context is sent to the OpenAI API.

5. Responses are streamed token-by-token using **Server-Sent Events (SSE)** instead of waiting for the entire response.

6. The frontend updates the interface in real time as each token is received.

7. Once generation is complete, the application calculates:

   - Prompt tokens
   - Completion tokens
   - Total token usage

8. The assistant response is stored in the conversation history so future messages remain contextual.

---

# Project Structure

```text
ai-chatbot/
│
├── main.py              # FastAPI application and UI
├── routes.py            # API endpoints
├── chat.py              # OpenAI communication logic
├── sys_msg.py           # System prompt
├── static/
│   └── styles.css
├── requirements.txt
└── .gitignore
```

---

# Screenshots

- Home screen
- Active conversation
- Toast Notification
- Token usage example

---

# Requirements

- Python **3.10.10**
- OpenAI API Key
- pip

> **Note:** This project was developed and tested using **Python 3.10.10**. Compatibility with Python 3.11+ has not been verified, and some dependencies may fail to install or behave unexpectedly.

---

# Installation

Clone the repository

```bash
git clone https://github.com/suselyt/ai-chatbot.git
cd ai-chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
API_KEY=your_openai_api_key
BASE_URL=your_openai_endpoint
```

Run the application

```bash
uvicorn main:app --reload
```

Open your browser and navigate to:

```text
http://localhost:8000
```

---

# Future Improvements

- User authentication
- Persistent chat history using a database
- Docker support
- Unit and integration testing
- Conversation export
- Support for multiple AI models
- Syntax highlighting for code snippets
- Dark/Light mode
- Rate limiting and API protection
- Conversation analytics dashboard

---

# Lessons Learned

This project helped me to practice the following:

- Designing REST APIs using FastAPI
- Integrating Large Language Models through the OpenAI API
- Implementing real-time communication using Server-Sent Events (SSE)
- Managing conversation context for multi-turn interactions
- Prompt engineering for specialized AI assistants
- Tracking token consumption with TikToken
- Structuring Python applications into modular components
- Connecting frontend and backend systems through asynchronous APIs

---

# Portfolio Highlights

This project demonstrates experience with:

- 🤖 AI Application Development
- 🧠 Large Language Models (LLMs)
- 🐍 Python
- ⚡ FastAPI
- 🌐 REST APIs
- 💬 Streaming Responses (SSE)
- 📝 Prompt Engineering
- 📊 Token Management
- 🔗 Frontend–Backend Integration

---

# Author

**Susely T.**

GitHub: https://github.com/suselyt

---

## License

This project is intended for educational and portfolio purposes.
