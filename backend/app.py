from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import logging
from .letter_agent import LetterGenerationAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Letter Generation API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the letter generation agent
try:
    letter_agent = LetterGenerationAgent()
    logger.info("Letter generation agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize letter agent: {e}")
    letter_agent = None

# Pydantic models for request/response
class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    conversation_id: str
    success: bool
    error: Optional[str] = None

# Store conversation sessions (in production, use Redis or database)
conversations = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Letter Generation API is running", "status": "healthy"}

@app.post("/chat", response_model=MessageResponse)
async def chat_endpoint(request: MessageRequest):
    """
    Main chat endpoint for letter generation
    """
    try:
        if not letter_agent:
            raise HTTPException(status_code=500, detail="Letter generation service unavailable")
        
        # Get or create conversation
        conversation_id = request.conversation_id or "default"
        
        if conversation_id not in conversations:
            conversations[conversation_id] = LetterGenerationAgent()
        
        agent = conversations[conversation_id]
        
        # Process the message
        logger.info(f"Processing message for conversation {conversation_id}: {request.message}")
        
        # Run the agent (this might take some time)
        response = await asyncio.to_thread(agent.run, request.message)
        
        logger.info(f"Generated response for conversation {conversation_id}")
        
        return MessageResponse(
            response=response,
            conversation_id=conversation_id,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return MessageResponse(
            response="I apologize, but I encountered an error processing your request. Please try again.",
            conversation_id=request.conversation_id or "default",
            success=False,
            error=str(e)
        )

@app.post("/new-conversation")
async def new_conversation():
    """
    Create a new conversation session
    """
    try:
        import uuid
        conversation_id = str(uuid.uuid4())
        conversations[conversation_id] = LetterGenerationAgent()
        
        return {
            "conversation_id": conversation_id,
            "message": "New conversation started",
            "success": True
        }
    except Exception as e:
        logger.error(f"Error creating new conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to create new conversation")

@app.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation session
    """
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation deleted", "success": True}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

@app.get("/conversations")
async def list_conversations():
    """
    List all active conversations
    """
    return {
        "conversations": list(conversations.keys()),
        "total": len(conversations)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)