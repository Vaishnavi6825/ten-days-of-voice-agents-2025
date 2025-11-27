# Day 5: Nykaa Voice SDR & Lead Capture Agent 🛍️

## Project Overview
For Day 5, I built a specialized **Sales Development Representative (SDR)** voice agent for **Nykaa for Business**. The goal was to replace static lead forms with a dynamic, conversational AI that can answer complex queries and capture business leads automatically.

Instead of a generic chatbot, this agent ("Nia") acts as a Corporate Gifting Specialist. He uses RAG (Retrieval-Augmented Generation) to answer policy questions and a custom toolset to extract and save lead details.

## File Structure & Logic
I organized the code into a modular structure under `src/` to separate data, logic, and agent behavior:

1. **`nykaa_database.py`**:
   - Acts as the **Knowledge Base** (RAG source).
   - Contains structured text on Nykaa's corporate gifting policies, bulk discounts, shipping tiers, and Prive loyalty benefits.

2. **`nykaa_order.py`**:
   - Defines the **Data Structure** for a lead.
   - Uses Python `dataclasses` to enforce a schema (Name, Email, Role, Use Case, Team Size) ensuring that the data saved is always clean and structured.

3. **`agent_sdr.py` (Main Agent)**:
   - **Persona Logic:** Defines "Nia", the professional and stylish SDR persona.
   - **Lead Capture Tool:** A custom function `save_lead_to_database` that the LLM calls when it detects the user is done. It extracts entities from the conversation history and maps them to the JSON schema.
   - **JSON Storage:** Automatically creates a `leads/` directory and saves every conversation as a timestamped JSON file.

Linkedin:[https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7399324907211251712-a4D5?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]
