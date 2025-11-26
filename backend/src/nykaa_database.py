# nykaa_database.py
from dataclasses import dataclass
from typing import List, Optional

# --- COMMON INSTRUCTIONS ---
COMMON_INSTRUCTIONS = """
You are a professional Sales Development Representative for Nykaa.
Be warm, engaging, and genuinely interested in understanding the prospect's needs.
Focus on qualification and building rapport rather than being pushy.
Use the FAQ data to answer questions accurately - never make up information about products or pricing.
"""

# --- FAQ DATA STRUCTURE ---
@dataclass
class FAQItem:
    question: str
    answer: str
    keywords: List[str]  # For simple keyword matching

# --- NYKAA FAQ DATABASE ---
FAQ_DATA = [
    FAQItem(
        question="What does Nykaa do?",
        answer="Nykaa is an omnichannel beauty, wellness, and fashion retailer offering 100,000+ products from 2400+ brands. We operate online at Nykaa.com and have 100+ physical stores across India. We serve personal shoppers, professionals, and beauty enthusiasts.",
        keywords=["what do you do", "who are you", "what is nykaa", "business", "company"]
    ),
    FAQItem(
        question="Is there a free tier or trial?",
        answer="For personal shoppers, you can browse and shop on Nykaa.com anytime without membership. For beauty professionals, we offer Nykaa PRO membership - a professional program with exclusive benefits. Apply at nykaa.com/pro-intro with business proof (business card, salon license, etc).",
        keywords=["free", "trial", "membership", "paid", "cost", "pricing"]
    ),
    FAQItem(
        question="Who is Nykaa for?",
        answer="Nykaa is for everyone! We serve: (1) Personal beauty shoppers - men and women looking for makeup, skincare, wellness. (2) Beauty professionals - makeup artists, beauticians, hair stylists, salon owners. (3) Fashion enthusiasts. (4) Wellness seekers. We have curated collections for all customer types.",
        keywords=["who is this for", "target", "audience", "customer", "suitable"]
    ),
    FAQItem(
        question="What brands do you carry?",
        answer="We carry 2400+ brands across luxury, mainstream, and Indian brands. Luxury: MAC, Dior, HUDA Beauty, Charlotte Tilbury. Popular: Lakme, Maybelline, L'Oreal. Nykaa's own brands: Nykaa Cosmetics, Nykaa Naturals, Kay Beauty. We stock everything from budget-friendly to premium.",
        keywords=["brands", "products", "what do you sell", "catalog", "inventory"]
    ),
    FAQItem(
        question="What is Nykaa PRO?",
        answer="Nykaa PRO is an exclusive membership program for beauty professionals. Benefits include: 100+ professional-relevant brands, always-on exclusive offers, GST tax benefits, 100% authentic products sourced directly from brands, masterclasses and educational content, and priority customer support.",
        keywords=["pro", "professional", "membership", "exclusive", "benefits"]
    ),
    FAQItem(
        question="How do I become a Nykaa PRO member?",
        answer="Visit nykaa.com/pro-intro and sign up with your professional credentials. Required documents: 1 government-issued ID + 1 business proof (business card, salon license, academy registration, etc). Nykaa verifies within 72 hours. Once approved, you get access to PRO pricing and exclusive offers on the app.",
        keywords=["join pro", "apply", "register", "professional member", "how to sign up"]
    ),
    FAQItem(
        question="What are your delivery times?",
        answer="We offer fast delivery - typically within 3 days. Free shipping available on most orders. We also offer Cash on Delivery (COD) as a payment option for your convenience.",
        keywords=["delivery", "shipping", "how long", "when will i get", "faster", "cod"]
    ),
    FAQItem(
        question="Do you have physical stores?",
        answer="Yes! Nykaa has 100+ stores across India in major cities. We offer three store formats: (1) Nykaa Luxe - international luxury brands, (2) Nykaa On Trend - popular curated items, (3) Beauty Kiosks - convenient local shopping. Find your nearest store on Nykaa.com.",
        keywords=["store", "physical", "offline", "location", "retail", "near me"]
    ),
    FAQItem(
        question="Is everything on Nykaa authentic?",
        answer="Yes, 100% guaranteed authentic. All products are sourced directly from brands. We have strict quality verification processes and authentication systems to ensure all items are genuine. Your trust is our priority.",
        keywords=["authentic", "genuine", "fake", "real", "quality", "trust"]
    ),
    FAQItem(
        question="Do you have men's products?",
        answer="Yes! Nykaa Man is our dedicated men's grooming store with a full range: shaving creams, razors, beard trimmers, hair care products, skincare for men, wellness items, and gift collections. Available online and in select stores.",
        keywords=["men", "male", "men's grooming", "men's products", "beard", "shaving"]
    ),
    FAQItem(
        question="What about wellness products?",
        answer="We have a comprehensive wellness section including: supplements, vitamins, Ayurvedic products, herbal skincare, wellness-focused bath products, fitness accessories, and health items. All 100% authentic from trusted brands.",
        keywords=["wellness", "health", "supplement", "vitamin", "ayurvedic", "herbal"]
    ),
    FAQItem(
        question="How do I track my order?",
        answer="Once you place an order on Nykaa.com or our app, you'll receive order confirmation and tracking details via email and SMS. You can also track orders directly on the app or website under 'My Orders'. Our delivery partners provide real-time updates.",
        keywords=["track", "order status", "tracking", "where is my order", "delivery"]
    ),
    FAQItem(
        question="What about returns and exchanges?",
        answer="We have a customer-friendly return and exchange policy. Terms vary by product category. Visit Nykaa.com/returns for detailed policy or contact our customer service team. We want you to be completely satisfied with your purchase.",
        keywords=["return", "exchange", "refund", "policy", "not satisfied", "damaged"]
    ),
    FAQItem(
        question="Do you have skincare for specific concerns?",
        answer="Yes! We have curated skincare ranges for: acne-prone skin, sensitive skin, dry skin, oily skin, aging concerns, dark spots, hyperpigmentation, and more. Browse by concern on Nykaa.com or speak with our beauty advisors in-store.",
        keywords=["skincare", "skin type", "acne", "sensitive", "dry", "oily", "concern"]
    ),
    FAQItem(
        question="Are there current promotions or discounts?",
        answer="Yes! We run regular promotions including seasonal sales, festival offers, category discounts, and bundle deals. Check Nykaa.com or the app for current offers. Subscribers get early access to sales. Download the Nykaa app for the best deals.",
        keywords=["discount", "sale", "offer", "promotion", "coupon", "deal", "price"]
    ),
]

# --- SEARCH FUNCTION ---
def find_faq_answer(user_question: str) -> Optional[str]:
    """
    Simple keyword-based FAQ search.
    Returns the answer if a match is found, else None.
    """
    user_question_lower = user_question.lower()
    
    for faq in FAQ_DATA:
        for keyword in faq.keywords:
            if keyword in user_question_lower:
                return faq.answer
    
    return None

# --- HELPER CLASS FOR UI/VOICE ---
class FakeDB:
    """Fake database for potential menu/activity systems."""
    
    async def get_faq(self) -> List[FAQItem]:
        return FAQ_DATA
    
    async def search_faq(self, query: str) -> Optional[str]:
        return find_faq_answer(query)