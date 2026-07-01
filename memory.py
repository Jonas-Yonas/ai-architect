from models import Conversation

# Simple in-memory storage for conversation history (will reset when server restarts)
conversations = {}


def get_conversation(session_id: str) -> Conversation:
    """Get or create a conversation for this session."""
    if session_id not in conversations:
        conversations[session_id] = Conversation()
    return conversations[session_id]


def add_message(session_id: str, role: str, content: str):
    """Add a message to the conversation history."""
    conv = get_conversation(session_id)
    conv.messages.append({"role": role, "content": content})
