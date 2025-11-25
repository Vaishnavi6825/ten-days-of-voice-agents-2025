# Day 3: Health & Wellness Voice Companion

Project Overview: For Day 3, I built an empathetic "Health & Wellness Companion." The goal was to create an agent that doesn't just talk, but remembers. It tracks mood and goals, persists that data to a JSON file, and uses that history to inform the next conversation.

File Structure & Logic: I created a specific set of files for the wellness domain under src/:

database_wellness.py:

- Consists of the wellness activities list (Exercises, Nutrition, Mindfulness).
- Defines units like "mins" or "steps" for accurate logging.

agent_wellness.py:

- Consists of the core intelligence and Persistence Layer.
- Memory Injection: On startup, the code reads wellness_log.json to see the user's last mood and injects it into the system prompt (e.g., "Welcome back, I hope you are feeling better than yesterday").
- Data Saving: It defines the save_daily_checkin tool. When the user shares their mood and goals, the agent automatically writes this structured data (Timestamp + Mood + Goals) into the JSON file.

order_wellness.py:

- Consists of the Data Models and State Management.
- It defines the WellnessLog class (to structure a specific activity entry) and the WellnessState class (to manage the collection of logs during the session).

wellness_log.json:
This is the storage file where the agent persists the conversation history, allowing for long-term memory across different sessions.

What I Learned:

- How to implement Data Persistence in a voice agent (saving mood/goals to JSON).
- How to give an AI "Long-term Memory" by reading past JSON files before the session starts and dynamically updating the context.
- How to prompt engineering for empathy (creating a supportive, non-medical tone).

LinkedIn: [https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7398658949828415488-gY2Y?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]
