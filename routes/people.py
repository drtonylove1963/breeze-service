from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from .models import Person

router = APIRouter(prefix="/people", tags=["People"])

@router.get("/", response_model=List[dict])
async def get_people(limit: Optional[int] = None, offset: Optional[int] = None, details: bool = False):
    """
    List people from your database.
    
    Parameters:
    - **limit**: Number of people to return. If None, will return all people
    - **offset**: Number of people to skip before beginning to return results
    - **details**: Option to return all information (slower) or just names
    
    Returns:
        List of people
    """
    return breeze_api.get_people(limit, offset, details)

@router.get("/{person_id}", response_model=dict)
async def get_person_details(person_id: str):
    """
    Retrieve the details for a specific person by their ID.
    
    Parameters:
    - **person_id**: Unique ID for a person in Breeze database
    
    Returns:
        Person details
    """
    return breeze_api.get_person_details(person_id)

@router.get("/profile/fields")
async def get_profile_fields():
    """
    List profile fields from your database.
    
    Returns:
        List of profile fields
    """
    return breeze_api.get_profile_fields()

@router.post("/add")
async def add_person(first_name: str, last_name: str, fields_json: Optional[str] = None):
    """
    Add a new person to the database.
    
    Parameters:
    - **first_name**: The first name of the person
    - **last_name**: The last name of the person
    - **fields_json**: Optional JSON string representing fields to update
    
    Returns:
        Created person details
    """
    return breeze_api.add_person(first_name, last_name, fields_json)

@router.put("/{person_id}/update")
async def update_person(person_id: str, fields_json: str):
    """
    Updates the details for a specific person in the database.
    
    Parameters:
    - **person_id**: Unique id for a person in Breeze database
    - **fields_json**: JSON string representing fields to update
    
    Returns:
        Updated person details
    """
    return breeze_api.update_person(person_id, fields_json)
