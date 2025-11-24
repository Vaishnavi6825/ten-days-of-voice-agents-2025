# Day 2: The Intelligent Coffee Barista

Project Overview: For Day 2, I moved beyond simple conversation and built a context-aware Coffee Shop Agent capable of handling complex orders, menus, and business logic. I also implemented a checkout system that saves finalized orders to a JSON file.

File Structure & Logic: I organized the code into three specific modules under src/:

database.py:

Consists of the "Knowledge Base" for the shop.
It contains the MenuItem class and raw data lists for Drinks, Milk Options, and Extras.
It includes helper functions to filter and find items by ID.

order.py:

Consists of the State Management logic.
It defines the OrderedDrink class (tracking size/milk/syrups) and the OrderState class (managing the cart).
It handles the logic of adding items, removing items, and clearing the cart.

agent_barista.py:

Consists of the main Agent definition and Tool declarations.
It defines the order_drink_tool to intelligently map spoken requests to menu items.
JSON Feature: I implemented a finalize_order_tool. When the user says "That's all," this tool captures the entire cart state and exports it to coffee_orders.json, simulating a real Point-of-Sale (POS) system.

What I Learned:

How to separate data, state, and agent logic into different files.
How to use function_tools to manipulate Python objects based on voice.
How to persist transaction data by writing complex objects to a local JSON file.

LinkedIn: [https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7398424685899599873-UX7i?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]
