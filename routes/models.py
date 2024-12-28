from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Person(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None

class Event(BaseModel):
    id: str
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Contribution(BaseModel):
    date: Optional[str] = None

class FormField(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[str] = None

class FormEntry(BaseModel):
    id: str
    form_id: str
    created_on: Optional[str] = None
    person_id: Optional[str] = None
    response: Optional[Dict[str, Any]] = None

class VolunteerRole(BaseModel):
    id: Optional[str] = None
    name: str
    quantity: Optional[int] = None

class Volunteer(BaseModel):
    person_id: str
    role_ids: Optional[List[str]] = None
