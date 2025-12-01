# Day 2: Health & Wellness Voice Companion

## 📌 Project Overview
For Day 3, I created an empathetic **Health & Wellness Companion** that tracks mood, goals, and activities — and remembers them using persistent JSON storage. The agent opens with supportive context based on the user's previous mood.

---

## 📁 File Structure & Logic

### `src/database_wellness.py`
- Contains:
  - Exercise, Nutrition, Mindfulness activity lists  
  - Unit definitions (mins, reps, steps)

### `src/agent_wellness.py`
- Loads `wellness_log.json` on startup.
- Injects last known mood into the system prompt.
- Defines `save_daily_checkin` tool to record:
  - Timestamp  
  - Mood  
  - Goals  
- Writes persistent records to disk.

### `src/order_wellness.py`
- Data models for wellness entries.
- `WellnessLog` + `WellnessState` to maintain session logs.

### `wellness_log.json`
- Long-term memory file.

---

## 🌟 What I Learned
- Implementing **AI memory** using JSON.  
- Designing **empathetic prompts** for wellness.  
- Structuring domain-specific logic.

🔗 **LinkedIn Post:**  
https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7398658949828415488-gY2Y
