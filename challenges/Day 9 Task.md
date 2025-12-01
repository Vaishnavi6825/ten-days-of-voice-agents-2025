Day 10: Squid Game Improv Battle Agent 🦑

Project Overview

For the Grand Finale (Day 10), I built a Voice-First Improv Game Master inspired by the high-stakes world of Squid Game. The goal was to move beyond standard conversational bots and create an interactive "Director" that guides players through theatrical scenarios, critiques their acting, and manages a multi-round game flow.

Instead of a passive assistant, this agent acts as the enigmatic "Front Man." It sets the scene ("You are a Red Guard..."), demands a performance, and provides dynamic, character-driven feedback—ranging from dark amusement to harsh critique—before moving the narrative forward.

File Structure & Logic

I organized the code to separate the game state management from the improvisational logic:

- agent.py (Main Agent)

Host Persona: Defines the strict, high-stakes personality of the Game Master. The agent is instructed to be mysterious, commanding, and sometimes theatrically critical.

Stateful Game Engine: Implements a custom ImprovisationContext class to track the game state across phases (intro → awaiting_improv → reacting → done). It manages round progression (1 through 3) and handles logic for "Early Exits" if a player wants to quit.

Dynamic Reaction Tool: Unlike static responses, the agent uses the LLM to analyze the user's voice input text and generate specific feedback. It references exact lines the user said (e.g., "I liked how you threatened the contestant...") to make the experience feel deeply responsive.

- improv_sessions.json

Session Persistence: Acts as the game ledger.

Real-Time Logging: Every time a round completes, the system records the scenario, the user's improvised dialogue, and the host's reaction. This proves the agent maintains long-term memory of the session's narrative arc.
