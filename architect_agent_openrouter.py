# ============================================================
# CLEAN AGENT - CONFIGURATION FROM .env
# ============================================================

import json
import re
import requests
from typing import Dict, Optional, Any
from models import ArchitecturePlan
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURATION FROM .env
# ============================================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")

if not OPENROUTER_API_KEY:
    raise Exception("OPENROUTER_API_KEY not found in .env file")


# ============================================================
# OPENROUTER API CALL (USING .env CONFIG)
# ============================================================
def call_openrouter(prompt: str, max_tokens: int = 2000) -> str:
    """
    Call OpenRouter API using the model from .env.
    """
    print(f"📤 Using model: {OPENROUTER_MODEL}")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Architect",
        },
        json={
            "model": OPENROUTER_MODEL,  # ← FROM .env
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": max_tokens,
        },
        timeout=60,
    )

    if response.status_code != 200:
        error_data = response.json()
        error_msg = error_data.get("error", {}).get("message", "Unknown error")
        raise Exception(f"OpenRouter API error: {error_msg}")

    result = response.json()
    return result["choices"][0]["message"]["content"]


# ============================================================
# TOOL 1: Web Search
# ============================================================
def search_web(query: str) -> str:
    """Search the web for current information."""
    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            result = data.get("AbstractText", "")
            if not result:
                related = data.get("RelatedTopics", [])
                if related:
                    result = related[0].get("Text", "No results found.")
            return result if result else "No search results found."
        else:
            return f"Search failed with status: {response.status_code}"
    except Exception as e:
        return f"Search error: {str(e)}"


# ============================================================
# TOOL 2: Get Current Time
# ============================================================
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# TOOL 3: Get Latest Package Version
# ============================================================
def get_latest_version(package: str) -> str:
    """Get the latest version of an npm package."""
    try:
        response = requests.get(
            f"https://registry.npmjs.org/{package}/latest", timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return f"{package}: {data.get('version', 'unknown')}"
        else:
            return f"Could not find package: {package}"
    except Exception as e:
        return f"Version check failed: {str(e)}"


# ============================================================
# THE REACT AGENT CLASS
# ============================================================
class ReactArchitectAgent:
    """
    Implements the ReAct pattern: Reason → Act → Observe → Repeat
    """

    def __init__(self):
        self.max_iterations = 3

        self.tools = {
            "search_web": {
                "fn": search_web,
                "description": "Search the web for current information. Use this for: latest versions, best practices, new technologies.",
            },
            "get_time": {
                "fn": get_current_time,
                "description": "Get the current date and time.",
            },
            "get_latest_version": {
                "fn": get_latest_version,
                "description": "Get the latest version of an npm package. Use this to recommend current versions.",
            },
        }

    def generate_architecture(
        self, user_description: str, history: list = None
    ) -> ArchitecturePlan:
        """Main entry point - runs the ReAct loop."""
        print(f"\n{'=' * 60}")
        print("🤖 AGENT STARTING")
        print(f"📝 Query: {user_description}")
        print(f"🧠 Model: {OPENROUTER_MODEL}")
        print(f"{'=' * 60}\n")

        history_context = ""
        if history:
            history_context = "\nPrevious conversation:\n"
            for msg in history[-4:]:
                history_context += f"{msg['role']}: {msg['content']}\n"

        final_result = self._react_loop(user_description, history_context)

        print(f"\n{'=' * 60}")
        print("✅ AGENT FINISHED")
        print(f"💭 Reasoning: {final_result.get('reasoning', 'N/A')[:100]}...")
        print(f"🔧 Tools Used: {final_result.get('tools_used', [])}")
        print(f"{'=' * 60}\n")

        try:
            return ArchitecturePlan(**final_result)
        except Exception as e:
            print(f"❌ Error parsing result: {e}")
            return ArchitecturePlan(
                project_type="Error Generating Architecture",
                primary_language="Unknown",
                frontend="Unknown",
                backend="Unknown",
                database="Unknown",
                caching=None,
                folder_structure_hint="src/{components,pages,api,utils}",
                first_phase_tasks=[f"Error: {str(e)}", "Please try again"],
                reasoning="Failed to parse result",
            )

    def _react_loop(self, query: str, history: str) -> Dict[str, Any]:
        """The core ReAct loop."""
        scratchpad = []
        tools_used = []
        tool_results = []

        for iteration in range(self.max_iterations):
            print(f"\n🔄 Iteration {iteration + 1}/{self.max_iterations}")

            # Step 1: THINK
            thought_prompt = self._build_thought_prompt(
                query,
                history,
                scratchpad,
                tool_results,
                is_final=(iteration == self.max_iterations - 1),
            )

            print("💭 Thinking...")
            thought = call_openrouter(thought_prompt, max_tokens=1000)
            print(f"🧠 Thought: {thought[:200]}...")

            scratchpad.append(f"Thought: {thought}")

            # Step 2: DECIDE
            tool_decision = self._extract_tool_decision(thought)

            if not tool_decision and iteration < self.max_iterations - 1:
                print("No tool call detected, continuing...")
                continue

            if tool_decision:
                # Step 3: ACT
                tool_name = tool_decision.get("name")
                tool_args = tool_decision.get("args", [])

                print(f"🔧 Using tool: {tool_name}({', '.join(tool_args)})")

                if tool_name in self.tools:
                    try:
                        result = self.tools[tool_name]["fn"](*tool_args)
                        print(f"📊 Result: {result[:150]}...")

                        tool_results.append(
                            {"tool": tool_name, "args": tool_args, "result": result}
                        )
                        tools_used.append(tool_name)
                        scratchpad.append(
                            f"Action: {tool_name}({', '.join(tool_args)})"
                        )
                        scratchpad.append(f"Observation: {result}")
                    except Exception as e:
                        error_msg = f"Tool error: {str(e)}"
                        print(f"❌ {error_msg}")
                        tool_results.append(
                            {"tool": tool_name, "args": tool_args, "result": error_msg}
                        )
            else:
                print("No more tools needed, generating final answer...")
                break

        # Step 4: ANSWER
        print("\n📝 Generating final architecture...")
        final_prompt = self._build_final_prompt(
            query, history, scratchpad, tool_results, tools_used
        )

        final_response = call_openrouter(final_prompt, max_tokens=1500)

        try:
            json_match = re.search(r"\{[\s\S]*\}", final_response)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return json.loads(final_response)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            return self._fallback_response(query, tools_used)

    def _build_thought_prompt(
        self,
        query: str,
        history: str,
        scratchpad: list,
        tool_results: list,
        is_final: bool,
    ) -> str:
        """Build the prompt for the 'Think' step."""
        tools_description = "\n".join(
            [f"- {name}: {info['description']}" for name, info in self.tools.items()]
        )

        scratchpad_text = "\n".join(scratchpad) if scratchpad else "No thoughts yet."

        if is_final:
            instruction = "This is your LAST iteration. You must provide the final architecture NOW."
        else:
            instruction = (
                "Decide if you need to use a tool or if you have enough information."
            )

        return f"""
You are a Senior Solutions Architect with 20 years of experience.

USER REQUEST: {query}

{history}

CONTEXT:
{scratchpad_text}

TOOL RESULTS:
{json.dumps(tool_results, indent=2) if tool_results else "No tools used yet."}

AVAILABLE TOOLS:
{tools_description}

YOUR TASK:
{instruction}

1. If you need more information, specify which tool to use and with what arguments.
   Format: "I need to use search_web with args: ['latest Next.js version']"

2. If you have enough information, say "NO MORE TOOLS NEEDED" and prepare your final answer.

Remember: You are a Senior Architect. Give specific, actionable advice.
"""

    def _extract_tool_decision(self, thought: str) -> Optional[Dict]:
        """Extract tool decisions from the agent's thought."""
        tool_patterns = {
            "search_web": r"(?:search|look up|find|get info about|what is|current)['\"]?\s*(?:for)?\s*['\"]?([^'\"]+)",
            "get_latest_version": r"(?:version of|latest|current version of)['\"]?\s*['\"]?([a-z-]+)",
            "get_time": r"(?:time|date|now|current time)",
        }

        for tool_name, pattern in tool_patterns.items():
            match = re.search(pattern, thought, re.IGNORECASE)
            if match:
                if tool_name == "get_time":
                    return {"name": tool_name, "args": []}
                else:
                    arg = match.group(1).strip()
                    if arg:
                        return {"name": tool_name, "args": [arg]}

        return None

    def _build_final_prompt(
        self,
        query: str,
        history: str,
        scratchpad: list,
        tool_results: list,
        tools_used: list,
    ) -> str:
        """Build the final prompt to generate the architecture."""
        scratchpad_text = "\n".join(scratchpad)

        return f"""
You are a Senior Solutions Architect with 20 years of experience.

USER REQUEST: {query}

{history}

AGENT'S THOUGHT PROCESS:
{scratchpad_text}

TOOLS USED AND RESULTS:
{json.dumps(tool_results, indent=2) if tool_results else "No tools were needed."}

TOOLS USED: {tools_used if tools_used else "None"}

YOUR FINAL TASK:
Based on your thinking and any information you gathered, provide the FINAL architecture recommendation.

Return ONLY valid JSON (no markdown, no explanations) in this exact format:
{{
    "project_type": "string",
    "primary_language": "string",
    "frontend": "string",
    "backend": "string",
    "database": "string",
    "caching": "string or null",
    "folder_structure_hint": "string",
    "first_phase_tasks": ["string", "string", "string"],
    "reasoning": "Explain WHY you chose this architecture, referencing your research",
    "tools_used": ["list", "of", "tools", "you", "used"]
}}

Remember: Be specific. Say "Next.js 14" not just "React". Give actionable tasks.
"""

    def _fallback_response(self, query: str, tools_used: list) -> Dict:
        """Fallback if JSON parsing fails."""
        return {
            "project_type": "Architecture Generation",
            "primary_language": "JavaScript",
            "frontend": "Next.js 14",
            "backend": "Node.js with Express",
            "database": "PostgreSQL",
            "caching": "Redis",
            "folder_structure_hint": "src/{components,pages,api,utils}",
            "first_phase_tasks": [
                "Set up project structure",
                "Implement authentication",
                "Create core features",
            ],
            "reasoning": "Generated from fallback due to parsing error",
            "tools_used": tools_used,
        }


# ============================================================
# MAIN FUNCTION
# ============================================================
def generate_architecture(
    user_description: str, history: list = None
) -> ArchitecturePlan:
    """Generate architecture using the ReAct agent."""
    agent = ReactArchitectAgent()
    return agent.generate_architecture(user_description, history)


# ============================================================
# QUICK TEST
# ============================================================
if __name__ == "__main__":
    print("Testing the ReAct agent...")
    print("=" * 60)
    result = generate_architecture("Build a blog platform with user comments")
    print("\n" + "=" * 60)
    print("RESULT:")
    print(json.dumps(result.dict(), indent=2))
