from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Dict, Any, List
import re

def validate_name(cls, v: str) -> str:
    if not v:
        return ""
    v = v.strip()
    if len(v) < 2:
        raise ValueError("Name must be at least 2 characters long")
    if not re.match(r"^[A-Za-z\s\-']+$", v):
        raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
    lower_v = v.lower()
    if lower_v in ['test', 'asdf', 'qwer', 'admin', 'dummy', 'null']:
        raise ValueError("Please provide a valid name")
    return v

def validate_phone(cls, v: str) -> str:
    if not v:
        return ""
    # Strip spaces, hyphens, and the +91 prefix for validation
    digits = re.sub(r'[\s\-()]', '', v)
    if digits.startswith('+91'):
        digits = digits[3:]
    elif digits.startswith('91') and len(digits) == 12:
        digits = digits[2:]
        
    if len(digits) != 10:
        raise ValueError("Phone number must be exactly 10 digits (excluding +91)")
    
    if len(set(digits)) == 1:
        raise ValueError("Phone number cannot be all identical digits")
    
    if digits in ['1234567890', '0987654321', '9876543210', '0123456789']:
        raise ValueError("Please provide a valid phone number")
        
    return f"+91 {digits}" # standardize storage

def validate_email_domain(cls, v: EmailStr) -> EmailStr:
    email_str = str(v).strip().lower()
    dummy_domains = ['test.com', 'example.com', 'dummy.com', 'a.com']
    domain = email_str.split('@')[1]
    if domain in dummy_domains or email_str in ['test@test.com', 'example@example.com']:
        raise ValueError("Please provide a valid email address")
    return v

class ScoreRequest(BaseModel):
    campaign_source: str = Field(..., description="'ad_1', 'ad_2', or 'ad_3'")
    assessment_answers: Dict[str, Any]
    selected_songs: List[str] = Field(default_factory=list, description="List of 5 selected songs from the setlist feature")

class LeadEmailRequest(BaseModel):
    campaign_source: str = Field(..., description="'ad_1', 'ad_2', or 'ad_3'")
    email: EmailStr
    name: str = ""
    phone: str = ""
    assessment_answers: Dict[str, Any]
    selected_songs: List[str] = Field(default_factory=list, description="List of 5 selected songs from the setlist feature")

    _validate_email = field_validator('email')(validate_email_domain)
    _validate_name = field_validator('name')(validate_name)
    _validate_phone = field_validator('phone')(validate_phone)

class BookingRequest(BaseModel):
    lead_id: str
    name: str
    phone: str
    time_slot: str
    email: EmailStr # Ensure email is validated when booking is submitted

    _validate_name = field_validator('name')(validate_name)
    _validate_phone = field_validator('phone')(validate_phone)
    _validate_email = field_validator('email')(validate_email_domain)

class SendResultRequest(BaseModel):
    lead_id: str
    email: EmailStr
    name: str = ""
    phone: str = ""
    
    _validate_email = field_validator('email')(validate_email_domain)
