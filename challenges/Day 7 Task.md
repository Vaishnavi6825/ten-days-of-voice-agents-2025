# Title: Day 7 - FreshMart Express: Context-Aware Grocery Agent

- Description: A conversational grocery assistant that uses natural language understanding to manage a shopping cart. This agent supports "Recipe Bundling," allowing users to add multiple related items based on a single intent (e.g., "I want to make a sandwich").

Key Features:

- Recipe-to-Cart Logic: Maps high-level intents ("Breakfast", "Pasta") to specific lists of product IDs using a dictionary-based recipe catalog.

- Structured Data: Uses Pydantic models (CartItem, OrderData) to ensure strict validation of prices, quantities, and order totals.

- State Management: Persistent CartState class tracks user sessions, updates quantities, and calculates dynamic totals in real-time.

- Smart Filtering: Backend logic to filter inventory by category, brand, and dietary tags.

Linkedin:[https://www.linkedin.com/posts/kiruthika-m-66b1a5254_murfaivoiceagentschallenge-10daysofaivoiceagents-activity-7400165833005522944-KTqe?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD6tG3MBYWx9mOEBXuTEYqfqcrMbrpxUBwE]
