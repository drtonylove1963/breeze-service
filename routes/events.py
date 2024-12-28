from fastapi import APIRouter, HTTPException
from typing import List, Optional
from .models import Event

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=List[dict])
async def get_events(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Retrieve all events for a given date range.
    
    Parameters:
    - **start_date**: Start date (defaults to first day of current month)
    - **end_date**: End date (defaults to last day of current month)
    
    Returns:
        List of events
    """
    return breeze_api.get_events(start_date, end_date)

@router.post("/add")
async def add_event(
    name: str,
    start_date: str,
    end_date: Optional[str] = None,
    all_day: Optional[bool] = None,
    description: Optional[str] = None,
    category_id: Optional[str] = None,
    event_id: Optional[str] = None
):
    """
    Add event for a given date range.
    
    Parameters:
    - **name**: Name of event
    - **start_date**: Start datetimestamp
    - **end_date**: End datetimestamp
    - **all_day**: Boolean indicating if event is all day
    - **description**: Description of event
    - **category_id**: Which calendar your event is on
    - **event_id**: Series ID
    
    Returns:
        Created event details
    """
    return breeze_api.add_event(name, start_date, end_date, all_day, description, category_id, event_id)

@router.post("/check-in")
async def event_check_in(person_id: str, event_instance_id: str):
    """
    Check in a person to an event.
    
    Parameters:
    - **person_id**: ID for a person in Breeze database
    - **event_instance_id**: ID for event instance
    
    Returns:
        Check-in confirmation
    """
    return breeze_api.event_check_in(person_id, event_instance_id)

@router.delete("/check-out")
async def event_check_out(person_id: str, event_instance_id: str):
    """
    Remove the attendance for a person checked into an event.
    
    Parameters:
    - **person_id**: ID for a person in Breeze database
    - **event_instance_id**: ID for event instance
    
    Returns:
        Check-out confirmation
    """
    return breeze_api.event_check_out(person_id, event_instance_id)
