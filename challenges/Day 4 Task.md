# Day 4: Multi-Agent Active Recall Coach

# Project Overview: 
For Day 4, I moved beyond single-agent logic and built a sophisticated Multi-Agent System. The goal was to create an "Active Recall Coach" that helps me learn by teaching. Instead of one AI doing everything, I architected a team of specialized agents (Router, Teacher, Quiz Master, Student) that seamlessly hand off the conversation to one another while preserving context.

File Structure & Logic: I organized the code into a modular structure under src/ to handle the complexity of multiple personas:

1. tutor_content.json:

- Acts as the "Knowledge Base" for the application.
- Contains structured lessons on "Variables", "Loops", and "Functions", including summaries for learning and specific questions for quizzing.

2. content_manager.py:

- A helper module that loads the JSON content.
- It allows the agents to dynamically fetch lesson details by topic ID, ensuring the logic remains separate from the data.

3. agent_tutor.py:

- Consists of the Multi-Agent Orchestration Logic.
The Router: A main receptionist agent that listens to user intent and routes the call.

Specialized Personas: Defined three distinct agent classes:

- LearnAgent (Matthew): Patiently explains concepts.
- QuizAgent (Alicia): Strictly tests knowledge.
- TeachBackAgent (Ken): A "confused student" who asks the user to explain concepts back to verify mastery.

Agent Handoffs: Implemented a switch_mode_tool that returns a new Agent instance. The system automatically transfers the live session to the new agent.

Context Preservation: When switching agents, the code explicitly copies self.chat_ctx so the new agent knows exactly what was just discussed.

Linkedin:[https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7399038398784708608-KxYP?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]
