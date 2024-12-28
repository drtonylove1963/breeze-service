from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(prefix="/families", tags=["Families"])

@router.post("/create")
async def create_family(people_ids: List[str]):
    """
    Create a new family by linking multiple people together.
    
    Parameters:
    - **people_ids**: List of Breeze person IDs to add to the family
    
    Returns:
        Family creation confirmation
    """
    return breeze_api.create_family(people_ids)

@router.post("/add")
async def add_to_family(people_ids: List[str], target_person_id: str):
    """
    Add people to an existing family.
    
    Parameters:
    - **people_ids**: List of Breeze person IDs to add to the family
    - **target_person_id**: ID of a person in the target family
    
    Returns:
        Family addition confirmation
    """
    return breeze_api.add_to_family(people_ids, target_person_id)

@router.post("/destroy")
async def destroy_family(people_ids: List[str]):
    """
    Destroy a family connection between people.
    
    Parameters:
    - **people_ids**: List of Breeze person IDs whose family to destroy
    
    Returns:
        Family destruction confirmation
    """
    return breeze_api.destroy_family(people_ids)

@router.post("/remove")
async def remove_from_family(people_ids: List[str]):
    """
    Remove people from their current family.
    
    Parameters:
    - **people_ids**: List of Breeze person IDs to remove from their family
    
    Returns:
        Family removal confirmation
    """
    return breeze_api.remove_from_family(people_ids)
