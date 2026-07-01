import os
import google.generativeai as genai
from dotenv import load_dotenv
from models import ArchitecturePlan  # Our strict schema

# Load the secret key from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_available_model():
    """
    Find the best available Gemini model for structured architecture generation.
    """

    # List all available models from the API
    models = genai.list_models()

    # Priority order: best to worst
    preferred_models = [
        "models/gemini-2.0-flash",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "models/gemini-1.0-pro",
    ]

    # Try to find a preferred model that supports generateContent
    for preferred in preferred_models:
        for model in models:
            if (
                model.name == preferred
                and "generateContent" in model.supported_generation_methods
            ):
                print(f"Using model: {preferred}")
                return genai.GenerativeModel(preferred)

    # Fallback: use any model that supports generateContent
    for model in models:
        if "generateContent" in model.supported_generation_methods:
            print(f"⚠️ Using fallback model: {model.name}")
            return genai.GenerativeModel(model.name)

    raise Exception("No suitable Gemini model found!")


# 1. Pick the best available model automatically.
# Priority: Gemini 2.0 Flash → Gemini 1.5 Flash → Gemini 1.5 Pro → Fallback
model = get_available_model()


def generate_architecture(user_description: str) -> ArchitecturePlan:
    """
    This function takes a user's idea and forces Gemini to return a strict ArchitecturePlan.
    """

    # 2. The Prompt (The "Art" of this project).
    # Notice we give it a ROLE, a TASK, and strict RULES.
    prompt = f"""
    You are a Senior Solutions Architect with 20 years of experience.

    A developer wants to build: {user_description}

    Your job is to give them a battle-tested, modern architecture.

    RULES:
    - Be specific. Say "Next.js 14" not just "React".
    - Recommend the absolute best practice stack for this specific project.
    - The 'first_phase_tasks' must be concrete (e.g., "Setup JWT authentication").

    Return the architecture strictly in the requested JSON format.
    """

    # 3. The Critical Piece: Enforcing Structured Output.
    # We pass our Pydantic model here. Gemini converts its response into our exact JSON shape.
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",  # Force JSON
            response_schema=ArchitecturePlan,  # Force our specific schema
        ),
    )

    # 4. Parse it into our Python object.
    # This validates that the AI didn't mess up the format.
    return ArchitecturePlan.model_validate_json(response.text)


# --- Quick manual test (we'll run this in Step 6) ---
if __name__ == "__main__":
    test_input = "I want to build a marketplace for local farmers to sell produce."

    result = generate_architecture(test_input)

    print("Architecture Generated Successfully!")
    print(result)
