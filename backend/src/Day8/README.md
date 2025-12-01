# Day 8: Zathura Voice Game Master & RPG Engine

## 📌 Project Overview
A stateful sci-fi RPG inspired by Zathura.  
The agent narrates events, tracks inventory, saves checkpoints, and evolves the storyline based on user actions.

---

## 📁 File Structure

### `zathura_agent.py`
- Game Master persona  
- Runs via `VoicePipelineAgent`  
- Deepgram Aura for narration  
- Gemini for story generation  
- Implements `log_checkpoint` tool to save:
  - Health  
  - Inventory  
  - Location  

### `zathura_journal.json`
- Real-time save file  
- Stores player progress  

---

## 🌟 What I Learned
- Voice-first game engines  
- Story state persistence  
- Checkpoint-saving logic  

🔗 **LinkedIn Post:**  
https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7400480486776692736-_AEd

