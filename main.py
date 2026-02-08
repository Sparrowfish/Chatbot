from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Optional
import json

app = FastAPI(title="HR Chatbot API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama
llm = Ollama(
    model="llama3.1:8b",
    temperature=0.7,
)

# HR-specific system prompt
HR_SYSTEM_PROMPT = """You are an AI assistant for an HR system. Your role is to help employees with:
1. Answering questions about company policies, benefits, and procedures
2. Helping with PTO (Paid Time Off) requests and balance inquiries
3. Assisting with onboarding processes
4. Providing general HR support

Be professional, helpful, and concise. If you need specific employee information to complete a task, 
ask for it. If you don't know something, admit it and suggest they contact HR directly.

Current conversation:
{chat_history}

Employee: {question}
HR Assistant:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=HR_SYSTEM_PROMPT
)

chain = LLMChain(llm=llm, prompt=prompt)


class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    

@app.get("/")
def read_root():
    return {"status": "HR Chatbot API is running", "model": "llama3.1:8b"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    """
    try:
        # Format chat history
        chat_history = ""
        for msg in request.history[-5:]:  # Keep last 5 messages for context
            role = "Employee" if msg.role == "user" else "HR Assistant"
            chat_history += f"{role}: {msg.content}\n"
        
        # Get response from LLM
        response = chain.run(
            chat_history=chat_history,
            question=request.message
        )
        
        return ChatResponse(response=response.strip())
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Check if Ollama is running and model is available"""
    try:
        test_response = llm.invoke("Hello")
        return {"status": "healthy", "ollama": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
