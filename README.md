# AI Voice Agents Challenge - Starter Repository

Welcome to the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai)!

## About the Challenge

We just launched **Murf Falcon** – the consistently fastest TTS API, and you're going to be among the first to test it out in ways never thought before!

**Build 10 AI Voice Agents over the course of 10 Days** along with help from our devs and the community champs, and win rewards!

### How It Works

- One task to be provided everyday along with a GitHub repo for reference
- Build a voice agent with specific personas and skills
- Post on GitHub and share with the world on LinkedIn!

## Repository Structure

This is a **monorepo** that contains both the backend and frontend for building voice agent applications. It's designed to be your starting point for each day's challenge task.

```
ten-days-of-voice-agents-2025/
├── backend/                    # LiveKit Agents backend with Murf Falcon TTS
│   ├── src/
│   │   ├── agent.py           # Main agent implementation
│   │   └── ...
│   ├── .env.example           # Environment template
│   ├── .venv/                 # Python virtual environment
│   ├── pyproject.toml         # Python dependencies
│   └── README.md              # Backend docs
├── frontend/                   # React/Next.js UI for voice interaction
│   ├── app/
│   ├── components/
│   ├── .env.local             # LiveKit configuration
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend docs
├── challenges/                 # Daily challenge tasks
│   ├── Day 1 Task.md
│   ├── Day 2 Task.md
│   └── ...
├── start_app.sh               # Convenience script to run all services
└── README.md                  # This file
```

### Backend

The backend is based on [LiveKit's agent-starter-python](https://github.com/livekit-examples/agent-starter-python) with modifications to integrate **Murf Falcon TTS** for ultra-fast, high-quality voice synthesis.

**Features:**

- Complete voice AI agent framework using LiveKit Agents
- Murf Falcon TTS integration for fastest text-to-speech
- LiveKit Turn Detector for contextually-aware speaker detection
- Background voice cancellation
- Integrated metrics and logging
- Complete test suite with evaluation framework
- Production-ready Dockerfile

[→ Backend Documentation](./backend/README.md)

### Frontend

The frontend is based on [LiveKit's agent-starter-react](https://github.com/livekit-examples/agent-starter-react), providing a modern, beautiful UI for interacting with your voice agents.

**Features:**

- Real-time voice interaction with LiveKit Agents
- Camera video streaming support
- Screen sharing capabilities
- Audio visualization and level monitoring
- Light/dark theme switching
- Highly customizable branding and UI

[→ Frontend Documentation](./frontend/README.md)

## Quick Start

### Prerequisites

Make sure you have the following installed:

- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- [LiveKit CLI](https://docs.livekit.io/home/cli/cli-setup) (optional but recommended)
- [LiveKit Server](https://docs.livekit.io/home/self-hosting/local/) for local development

### 1. Clone the Repository

```bash
git clone <https://github.com/Vaishnavi6825/ten-days-of-voice-agents-2025.git>
cd falcon-tdova-nov25-livekit
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Copy environment file and configure
cp .env.example .env.local

# Edit .env.local with your credentials:
# - LIVEKIT_URL
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET
# - MURF_API_KEY (for Falcon TTS)
# - GOOGLE_API_KEY (for Gemini LLM)
# - DEEPGRAM_API_KEY (for Deepgram STT)

# Download required models
uv run python src/agent.py download-files
```

For LiveKit Cloud users, you can automatically populate credentials:

```bash
lk cloud auth
lk app env -w -d .env.local
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Copy environment file and configure
cp .env.example .env.local

# Edit .env.local with the same LiveKit credentials
```

### 4. Run the Application

#### Install livekit server

```bash
brew install livekit
```

You have two options:

#### Option A: Use the convenience script (runs everything)

```bash
# From the root directory
chmod +x start_app.sh
./start_app.sh
```

This will start:

- LiveKit Server (in dev mode)
- Backend agent (listening for connections)
- Frontend app (at http://localhost:3000)

#### Option B: Run services individually

```bash
# Terminal 1 - LiveKit Server
livekit-server --dev

# Terminal 2 - Backend Agent
cd backend
uv run python src/agent.py dev

# Terminal 3 - Frontend
cd frontend
pnpm dev
```

Then open http://localhost:3000 in your browser!

## Daily Challenge Tasks

Each day, you'll receive a new task that builds upon your voice agent. The tasks will help you:

- Implement different personas and conversation styles
- Add custom tools and capabilities
- Integrate with external APIs
- Build domain-specific agents (customer service, tutoring, etc.)
- Optimize performance and user experience

**Stay tuned for daily task announcements!**

## Documentation & Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Original Backend Template](https://github.com/livekit-examples/agent-starter-python)
- [Original Frontend Template](https://github.com/livekit-examples/agent-starter-react)

## Testing

The backend includes a comprehensive test suite:

```bash
cd backend
uv run pytest
```
# 📋 10-Day Challenge Progress

## Day 1: Getting Started ✅

Task: Get Your Starter Voice Agent Running<br>
Objective: Successfully deploy a working voice agent and have a real conversation with it.<br>

What I Built:

-✅ Cloned and set up the starter repository <br>
-✅ Configured all environment variables (LiveKit, Murf, Deepgram, Gemini) <br>
-✅ Successfully ran the backend agent with Murf Falcon TTS <br>
-✅ Launched the frontend interface <br>
-✅ Had my first conversation with the voice agent <br>
-✅ Verified audio quality and response times <br>

Key Learnings:

-Understanding the LiveKit Agents framework<br>
-Setting up Murf Falcon TTS for ultra-low latency<br>
-Configuring real-time audio streaming pipeline<br>
---

| Component | Technology |
|-----------|-----------|
| **TTS** | Murf Falcon (Ultra-fast text-to-speech) |
| **STT** | Deepgram (Speech-to-text) |
| **LLM** | Google Gemini (Conversational AI) |
| **Framework** | LiveKit Agents |
| **Backend** | Python 3.9+ |
| **Frontend** | React, Next.js, TypeScript |
| **Styling** | Tailwind CSS |
| **Real-time** | WebRTC, LiveKit SDK |

Built for the AI Voice Agents Challenge by murf.ai
Linkedin : [https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-murfaivoiceagentschallenge-activity-7397979490313756672-S7uD?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]

---
