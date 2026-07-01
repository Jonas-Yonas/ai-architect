# 🏗️ AI Software Architect

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-orange.svg)](https://openrouter.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An AI agent that generates complete, production-ready project architectures from a single sentence. Built with ReAct pattern, FastAPI, and OpenRouter.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Why This Project](#why-this-project)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [What Makes This Unique](#what-makes-this-unique)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**AI Software Architect** is a ReAct (Reasoning + Acting) agent that acts as your personal Senior Solutions Architect.

Tell it what you want to build, and it will:

1. 🧠 **Think** about the best approach
2. 🔧 **Use tools** to research current best practices
3. 📝 **Generate** a complete architecture plan
4. 📁 **Scaffold** the actual project files on your computer

**Stop wasting hours researching tech stacks. Let the AI architect build your project foundation in minutes.**

---

## Why This Project

### The Problem

Developers spend countless hours:
- Researching tech stacks
- Debating architecture decisions
- Setting up project structures
- Writing boilerplate code
- Creating Dockerfiles and READMEs

### The Solution

```bash
User: "Build a blog platform using the latest best practices"
↓ (5 seconds)
AI Architect: Generates architecture + Creates all files
↓
Developer: `npm install && npm run dev`
↓
🚀 Working project in minutes!
```

---

## Features

### 🤖 ReAct Agent
- Implements the ReAct (Reasoning + Acting) pattern
- Thinks step-by-step before answering
- Uses tools to gather current information
- Shows its reasoning process transparently

### 🛠️ Tools
- **Web Search**: Researches current best practices
- **Time & Date**: Knows when it is
- **Package Versioning**: Gets the latest npm versions

### 📁 Project Scaffolding
Generates complete project structures including:
- `package.json` with all dependencies
- `Dockerfile` for containerization
- `.env.example` for environment variables
- `README.md` with setup instructions
- Starter code (Next.js pages, Express routes)
- Database models (MongoDB/PostgreSQL)

### 💾 Memory
- Session-based conversation history
- Project-aware follow-up questions
- Maintains context across requests

### 🔌 API-First Design
- RESTful API with FastAPI
- Automatic Swagger/OpenAPI documentation
- Ready for integration with other tools

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     AI SOFTWARE ARCHITECT                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  User: "Build a blog platform"                                 │
│       ↓                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ReAct Loop                           │   │
│  │                                                         │   │
│  │  1. THINK: "I need current best practices"              │   │
│  │       ↓                                                 │   │
│  │  2. DECIDE: "I'll search the web"                       │   │
│  │       ↓                                                 │   │
│  │  3. ACT: search_web("best blog platform 2026")          │   │
│  │       ↓                                                 │   │
│  │  4. OBSERVE: "Results: Next.js 14 is popular..."        │   │
│  │       ↓                                                 │   │
│  │  5. REPEAT: Until enough info                           │   │
│  │       ↓                                                 │   │
│  │  6. ANSWER: Generate architecture + Scaffold            │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│       ↓                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Output                              │   │
│  │                                                         │   │
│  │  ├── Architecture JSON (validated with Pydantic)        │   │
│  │  ├── Scaffolded Project (actual files on disk)          │   │
│  │  ├── Reasoning Log                                      │   │
│  │  └── Tools Used                                         │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core language |
| **FastAPI** | REST API framework |
| **Pydantic** | Data validation & schemas |
| **Uvicorn** | ASGI server |

### AI/LLM
| Technology | Purpose |
|------------|---------|
| **OpenRouter** | Unified LLM API |
| **Gemini 2.5 Flash** | Primary model |
| **ReAct Pattern** | Agent architecture |

### Deployment
| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **.env** | Configuration management |

---

## Getting Started

### Prerequisites

- Python 3.10+
- OpenRouter API key ([Get it free here](https://openrouter.ai/))
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-architect.git
cd ai-architect

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env with your OpenRouter API key

# 5. Run the server
uvicorn main:app --reload
```

### Environment Variables

```env
# .env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=google/gemini-2.5-flash
```

---

## Usage

### API Endpoints

#### 1. Generate Architecture

```bash
POST /architect
Content-Type: application/json

{
  "session_id": "user123",
  "description": "Build a blog platform with user comments"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "project_type": "Blog Platform",
    "primary_language": "TypeScript",
    "frontend": "Next.js 14",
    "backend": "Node.js with Express",
    "database": "PostgreSQL",
    "caching": "Redis",
    "folder_structure_hint": "src/{components,pages,api,utils}",
    "first_phase_tasks": [
      "Setup JWT authentication",
      "Create CRUD API for blog posts",
      "Implement user comments functionality"
    ],
    "reasoning": "Selected Next.js for SSR/SSG benefits..."
  }
}
```

#### 2. Scaffold Project

```bash
POST /scaffold
Content-Type: application/json

{
  "session_id": "user123",
  "project_name": "awesome-blog"
}
```

**Response:**

```json
{
  "success": true,
  "project_name": "awesome-blog",
  "path": "generated_projects/awesome-blog",
  "folders_created": [...],
  "files_created": [...],
  "message": "Project scaffolded successfully!"
}
```

### Interactive Documentation

Visit `http://localhost:8000/docs` for the Swagger UI.

### Example Workflow

```bash
# 1. Generate architecture
curl -X POST http://localhost:8000/architect \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test123", "description": "Build an e-learning platform"}'

# 2. Scaffold the project
curl -X POST http://localhost:8000/scaffold \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test123", "project_name": "my-elearning"}'

# 3. Check generated files
ls generated_projects/my-elearning/
```

---

## Project Structure

```
ai-architect/
├── 📁 src/                          # Source code
│   ├── architect_agent_openrouter.py # ReAct agent implementation
│   ├── scaffolder.py                # Project scaffolding engine
│   ├── models.py                    # Pydantic schemas
│   ├── memory.py                    # Session management
│   └── main.py                      # FastAPI application
│
├── 📁 generated_projects/           # Scaffolded projects
├── 📁 venv/                         # Virtual environment
├── 📄 .env                          # Environment variables (gitignored)
├── 📄 .env.example                  # Environment variables template
├── 📄 .gitignore                    # Git ignore file
├── 📄 requirements.txt              # Python dependencies
└── 📄 README.md                     # This file
```

---

## What Makes This Unique

| Feature | ChatGPT/DeepSeek | AI Software Architect |
|---------|------------------|----------------------|
| **Advice** | Text only | ✅ **Structured JSON** |
| **Memory** | Session only | ✅ **Project-aware** |
| **Folders** | Suggests structure | ✅ **Actually creates** |
| **Files** | Code blocks | ✅ **Writes to disk** |
| **Dependencies** | Tells you | ✅ **package.json** |
| **Docker** | Tells you | ✅ **Dockerfile** |
| **Docs** | Tells you | ✅ **README.md** |
| **API** | Web UI only | ✅ **REST API** |
| **Tools** | ❌ None | ✅ **Web search** |
| **Reasoning** | ❌ Hidden | ✅ **Shows process** |

---

## Roadmap

### ✅ Completed
- [x] ReAct agent pattern
- [x] Web search tool
- [x] Project scaffolding
- [x] Conversation memory
- [x] API with Swagger docs
- [x] Environment-based configuration

### 🔜 In Progress
- [ ] RAG + Vector Database (Chroma)
- [ ] Long-term memory
- [ ] Hybrid search (keyword + semantic)

### 📅 Planned
- [ ] Multi-agent systems
- [ ] Code execution tool
- [ ] Frontend dashboard
- [ ] Deployment automation
- [ ] Testing suite

---

## Learning Journey

This project was built as part of my Agentic AI learning roadmap:

| Week | Topic | Status |
|------|-------|--------|
| 1-2 | Fundamentals, API calls, Prompt engineering | ✅ |
| 3-4 | ReAct Agent, Tools, Autonomy | ✅ |
| 5-6 | RAG, Memory, Chroma, Retrieval | 🎯 |
| 7-8 | LangChain/LlamaIndex, Plan-and-execute | 🔜 |
| 9-10 | Multi-Agent Systems, CrewAI | 🔜 |

---

## Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Connect With Me

- [LinkedIn](https://linkedin.com/in/yonas-gashaw)
- [GitHub](https://github.com/jonas-yonas)

---

## Acknowledgments

- [OpenRouter](https://openrouter.ai/) for LLM access
- [FastAPI](https://fastapi.tiangolo.com/) for the beautiful framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) for the AI model

---

**⭐ Star this repo if you found it useful!**

Made with ❤️ by Yonas  G.