# Day 3: Multi-Agent Active Recall Coach

## 📌 Project Overview
I built a **multi-agent orchestration system** that teaches, quizzes, and tests concept mastery using active recall. The system routes control between Teacher, Quiz Master, and Teach-Back personas.

---

## 📁 File Structure & Logic

### `tutor_content.json`
- Knowledge Base for lessons:
  - Variables  
  - Loops  
  - Functions  
- Includes summaries and quiz pools.

### `src/content_manager.py`
- Loads lesson data.
- Provides dynamic fetch helpers.

### `src/agent_tutor.py`
Contains 4 agents:
- **Router Agent:** Detects intent and routes conversation.
- **LearnAgent (Matthew):** Explains concepts patiently.
- **QuizAgent (Alicia):** Strict tester.
- **TeachBackAgent (Ken):** Confused student asking user to explain concepts.

### Key Features
- Dynamic mode switching via `switch_mode_tool`
- Context preservation using shared `chat_ctx`

---

## 🌟 What I Learned
- How to build **multi-agent** voice systems.  
- Clean architecture for switching personas.  
- Using JSON + routing logic for dynamic teaching.

🔗 **LinkedIn Post:**  
https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7399038398784708608-KxYP

