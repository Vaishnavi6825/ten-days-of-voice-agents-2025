# Day 5: Fraud Alert Agent

## 📌 Project Overview
A secure **Fraud Detection Voice Agent** for "SecureBank."  
The agent verifies identity, reads suspicious transactions, and updates fraud case status.

---

## 📁 File Structure

### `src/fraud_case.py`
- `FraudCase` model:
  - User  
  - Merchant  
  - Amount  
  - Status  

### `src/fraud_database.py`
- Reads/writes to mock JSON DB  
- Handles transaction lookup and updates  

### `src/agent_fraud.py`
- Persona: “Alex” — calm fraud specialist  
- Flow:
  - Identity verification  
  - Transaction explanation  
  - Status update via tools  

### Scenarios Tested
- John → Safe (answer: *max*)  
- Sarah → Fraud victim (answer: *london*)  

---

## 🌟 What I Learned
- Secure voice workflows  
- Identity verification flows  
- Real-time database updates  

🔗 **LinkedIn Post:**  
https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7399738557604745216-PVVt

