import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from architect_agent_openrouter import generate_architecture
from memory import get_conversation, add_message
from scaffolder import scaffold_project
from models import ArchitecturePlan

app = FastAPI(title="AI Software Architect")


# --- Request/Response Models ---
class UserRequest(BaseModel):
    session_id: str
    description: str


class ScaffoldRequest(BaseModel):
    session_id: str
    project_name: str = None


class UserResponse(BaseModel):
    success: bool
    data: dict
    history: list


# --- Endpoint 1: Get Architecture ---
@app.post("/architect", response_model=UserResponse)
async def get_architecture(request: UserRequest):
    try:
        conv = get_conversation(request.session_id)
        architecture_plan = generate_architecture(request.description, conv.messages)

        add_message(request.session_id, "user", request.description)
        add_message(request.session_id, "assistant", architecture_plan.json())

        return UserResponse(
            success=True, data=architecture_plan.dict(), history=conv.messages
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI failed: {str(e)}")


# --- Endpoint 2: Scaffold Project (NEW!) ---
@app.post("/scaffold")
async def scaffold(request: ScaffoldRequest):
    """
    Generate actual project files from the last architecture plan.
    This is what makes our system unique — we create real code!
    """
    try:
        conv = get_conversation(request.session_id)

        # Find the last assistant message with architecture data
        last_plan = None
        for msg in reversed(conv.messages):
            if msg["role"] == "assistant":
                try:
                    data = json.loads(msg["content"])
                    last_plan = ArchitecturePlan(**data)
                    break
                except:  # noqa: E722
                    continue

        if not last_plan:
            raise HTTPException(
                status_code=400,
                detail="No architecture plan found. Please run /architect first.",
            )

        # Generate the project files
        result = scaffold_project(last_plan, request.project_name)

        return {
            "success": True,
            "project_name": request.project_name
            or last_plan.project_type.replace(" ", "-"),
            "path": result["path"],
            "folders_created": result["folders_created"],
            "files_created": result["files_created"],
            "message": f"✅ Project scaffolded successfully! Check: {result['path']}",
        }

    except Exception as e:
        print(f"❌ Scaffolding error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scaffolding failed: {str(e)}")


# --- Health Check ---
@app.get("/")
def root():
    return {
        "message": "AI Architect is running!",
        "endpoints": {
            "POST /architect": "Get architecture recommendations",
            "POST /scaffold": "Generate actual project files",
        },
    }
