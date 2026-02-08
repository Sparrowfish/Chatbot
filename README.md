# HR Chatbot with Ollama

A simple HR chatbot built with Ollama (Llama 3.1), FastAPI, and vanilla JavaScript.

## Prerequisites

- Python 3.8+
- Ollama installed

## Setup Instructions

### 1. Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

### 2. Download the Model

```bash
ollama pull llama3.1:8b
```

### 3. Install Python Dependencies

```bash
cd hr-chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start the Backend Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Open the Frontend

Simply open `index.html` in your web browser, or use a simple HTTP server:

```bash
python -m http.server 3000
```

Then visit `http://localhost:3000`

## Testing

1. Make sure Ollama is running (it should auto-start)
2. Start the backend: `python main.py`
3. Open `index.html` in your browser
4. Try asking: "What is the PTO policy?" or "How do I request time off?"

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Main chat endpoint
- `GET /health` - Check Ollama connection

### Example Chat Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How many PTO days do I get?",
    "history": []
  }'
```

## Next Steps

1. **Add RAG for Company Documents**: Integrate ChromaDB to answer questions based on your actual HR policies
2. **Add Function Calling**: Connect to your HRIS API to check real PTO balances
3. **Authentication**: Add employee login/SSO
4. **Database**: Store conversation history
5. **Deploy**: Containerize with Docker and deploy to your infrastructure

## Troubleshooting

**"Connection refused" error:**
- Make sure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`

**Slow responses:**
- The 8B model should be fast. If slow, check your system resources
- Consider using a smaller model or deploying to a GPU server

**CORS errors:**
- Make sure the backend is running on port 8000
- Update the API_URL in index.html if using a different port
