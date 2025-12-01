# ---
# FILE 2: backend/src/fraud_database.py
# Handles mock database loading and saving

import json
import os
from typing import Optional, List
from Day5.fraud_case import FraudCase

FRAUD_DB_FILE = "fraud_cases.json"

# Mock fraud cases database
MOCK_FRAUD_CASES = [
    {
        "case_id": "FRAUD_001",
        "userName": "John Doe",
        "securityIdentifier": "12345",
        "cardEnding": "**** 4242",
        "transactionName": "Amazon Electronics",
        "transactionAmount": 50000.00,
        "transactionTime": "2024-11-25 03:45 AM",
        "transactionCategory": "e-commerce",
        "transactionSource": "amazon.com",
        "merchantLocation": "USA",
        "securityQuestion": "What is your pet's name?",
        "securityAnswer": "fluffy",
        "status": "pending_review",
        "outcome_note": "",
        "timestamp": ""
    },
    {
        "case_id": "FRAUD_002",
        "userName": "Sarah Smith",
        "securityIdentifier": "67890",
        "cardEnding": "**** 8888",
        "transactionName": "DuoLingo Premium",
        "transactionAmount": 12000.00,
        "transactionTime": "2024-11-24 11:20 PM",
        "transactionCategory": "subscription",
        "transactionSource": "duolingo.com",
        "merchantLocation": "USA",
        "securityQuestion": "What city were you born in?",
        "securityAnswer": "mumbai",
        "status": "pending_review",
        "outcome_note": "",
        "timestamp": ""
    },
    {
        "case_id": "FRAUD_003",
        "userName": "Raj Kumar",
        "securityIdentifier": "11111",
        "cardEnding": "**** 5555",
        "transactionName": "Alibaba Shopping",
        "transactionAmount": 35000.00,
        "transactionTime": "2024-11-25 02:15 AM",
        "transactionCategory": "e-commerce",
        "transactionSource": "alibaba.com",
        "merchantLocation": "China",
        "securityQuestion": "What is your mother's maiden name?",
        "securityAnswer": "sharma",
        "status": "pending_review",
        "outcome_note": "",
        "timestamp": ""
    }
]

def initialize_fraud_database():
    """Initialize the fraud database JSON file with mock data if it doesn't exist"""
    if not os.path.exists(FRAUD_DB_FILE):
        with open(FRAUD_DB_FILE, "w") as f:
            json.dump(MOCK_FRAUD_CASES, f, indent=4)
    return load_all_fraud_cases()

def load_all_fraud_cases() -> List[FraudCase]:
    """Load all fraud cases from database"""
    try:
        with open(FRAUD_DB_FILE, "r") as f:
            data = json.load(f)
            return [FraudCase.from_dict(case) for case in data]
    except Exception as e:
        print(f"Error loading fraud cases: {e}")
        return []

def find_fraud_case_by_username(username: str) -> Optional[FraudCase]:
    """Find a fraud case by username"""
    cases = load_all_fraud_cases()
    for case in cases:
        if case.userName.lower() == username.lower():
            return case
    return None

def update_fraud_case(case_id: str, status: str, outcome_note: str) -> bool:
    """Update a fraud case status and outcome note"""
    cases = load_all_fraud_cases()
    
    for case in cases:
        if case.case_id == case_id:
            case.status = status
            case.outcome_note = outcome_note
            
            # Save back to file
            with open(FRAUD_DB_FILE, "w") as f:
                json.dump([c.to_dict() for c in cases], f, indent=4)
            return True
    
    return False

def get_fraud_case_by_id(case_id: str) -> Optional[FraudCase]:
    """Get a specific fraud case by ID"""
    cases = load_all_fraud_cases()
    for case in cases:
        if case.case_id == case_id:
            return case
    return None
