# Day 4: Nykaa Voice SDR

## 📌 Project Overview
Built a professional **Sales Development Representative Voice Agent** for Nykaa for Business.   
It answers corporate gifting queries using RAG and automatically captures leads.

---

## 📁 File Structure

### `nykaa_database.py`
- Acts as the Knowledge Base.
- Contains structured data:
  - Gifting policies  
  - Bulk pricing  
  - Shipping tiers  
  - Prive loyalty perks  

### `nykaa_order.py`
- Defines `Lead` structure using Pydantic/dataclasses.
- Validates user info:
  - Name  
  - Email  
  - Role  
  - Use Case  
  - Team Size  

### `agent_sdr.py`
- Persona: “Nia” — Corporate Gifting Specialist.  
- Uses Gemini + RAG for accuracy.  
- Implements `save_lead_to_database` tool:
  - Extracts entities  
  - Auto-saves JSON leads with timestamps  

---

## 🌟 What I Learned
- RAG pipelines for business queries  
- Professional persona engineering  
- Automated JSON-based CRM logic  

🔗 **LinkedIn Post:**  
https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7399324907211251712-a4D5
