# FILE 1: backend/src/fraud_case.py
# Defines the structure of a fraud case

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class FraudCase:
    """Represents a fraud case in the database"""
    case_id: str
    userName: str
    securityIdentifier: str
    cardEnding: str
    transactionName: str
    transactionAmount: float
    transactionTime: str
    transactionCategory: str
    transactionSource: str
    merchantLocation: str
    securityQuestion: str
    securityAnswer: str
    status: str = "pending_review"  # pending_review, confirmed_safe, confirmed_fraud, verification_failed
    outcome_note: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create FraudCase from dictionary"""
        return cls(**data)