# Day 8: Zathura Voice Game Master & Stateful RPG Engine 🎲🪐

Project Overview
For Day 8, I built an immersive Voice Game Master inspired by the retro-sci-fi world of Zathura. The goal was to move beyond simple Q&A bots and create a Stateful RPG Engine that remembers player choices, tracks inventory, and narrates a branching storyline.

Instead of a standard assistant, this agent acts as the "Game Board" itself. It uses Deepgram Aura for high-speed, dramatic narration and Google Gemini to improvise complex scenarios involving meteor showers, Zorgon aliens, and malfunctioning robots.

- File Structure & Logic
I organized the code to separate the storytelling logic from the state management:

- zathura_agent.py (Main Agent):

Game Master Persona: Defines the strict rules of the universe (Retro-futuristic 1950s aesthetic).

High-Level API: Uses LiveKit's VoicePipelineAgent to manage the conversation flow using Deepgram (STT/TTS) and Google Gemini (LLM).

- Custom Tool: Implements log_checkpoint, a function tool that the LLM autonomously triggers to save the player's progress (Location, Inventory, Health) whenever a major event occurs.

zathura_journal.json:

Acts as the Save File.

Automatically updates in real-time as the user plays. If the user finds a "Gold Card" or gets injured by a robot, this file records that state, proving the agent has "memory" beyond just the chat context.

Linkedin:[https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7400480486776692736-_AEd?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]
