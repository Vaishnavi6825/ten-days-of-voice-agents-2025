# Day 1: The Intelligent Coffee Barista

## 📌 Project Overview  
For Day 2, I built a context-aware **Coffee Shop Voice Agent** capable of handling complex drink orders, modifiers, menu filtering, and checkout logic. The agent simulates a real café ordering system and stores completed transactions in a JSON file.

---

## 📁 File Structure & Logic

### `src/database.py`
- Acts as the café **Knowledge Base**.  
- Contains:
  - `MenuItem` class  
  - Lists of Drinks, Milk Options, Syrups, Extras  
- Includes helper functions for filtering and searching by ID.

### `src/order.py`
- Manages **State & Cart Logic**.
- Defines:
  - `OrderedDrink` — tracks size, milk, syrups, and modifiers  
  - `OrderState` — manages the cart  
- Supports:
  - Add/remove items  
  - Update selections  
  - Clear cart  

### `src/agent_barista.py`
- Contains the **Main Agent**.
- Features:
  - `order_drink_tool`: Maps spoken user requests to menu items.
  - `finalize_order_tool`: Saves completed cart to `coffee_orders.json`.

---

## 🌟 What I Learned
- Clear separation of **data**, **state**, and **agent logic**.
- Using `function_tool` calls to manipulate Python data from voice.
- Persisting real POS-style transactions in JSON.

🔗 **LinkedIn Post:**  
https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7398424685899599873-UX7i
