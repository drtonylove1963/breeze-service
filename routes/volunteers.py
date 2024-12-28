from fastapi import APIRouter, HTTPException
from typing import List
from .models import VolunteerRole, Volunteer
from .dependencies import breeze_api

router = APIRouter(prefix="/api/volunteers", tags=["Volunteers"])

@router.get("/list")
async def list_volunteers(instance_id: str):
    """
    List all volunteers for a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    
    Returns:
        List of volunteers and their roles
    """
    return breeze_api.list_volunteers(instance_id)

@router.post("/add")
async def add_volunteer(instance_id: str, person_id: str):
    """
    Add a volunteer to a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **person_id**: The ID of the person to add as volunteer
    
    Returns:
        Success or failure message
    """
    return breeze_api.add_volunteer(instance_id, person_id)

@router.delete("/remove")
async def remove_volunteer(instance_id: str, person_id: str):
    """
    Remove a volunteer from a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **person_id**: The ID of the person to remove
    
    Returns:
        Success or failure message
    """
    return breeze_api.remove_volunteer(instance_id, person_id)

@router.put("/update")
async def update_volunteer(instance_id: str, person_id: str, role_ids_json: str):
    """
    Update a volunteer's roles for a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **person_id**: The ID of the person to update
    - **role_ids_json**: JSON string containing role IDs
    
    Returns:
        Updated volunteer information
    """
    return breeze_api.update_volunteer(instance_id, person_id, role_ids_json)

@router.get("/list_roles", response_model=List[VolunteerRole])
async def list_volunteer_roles(instance_id: str, show_quantity: bool = False):
    """
    List all volunteer roles for a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **show_quantity**: Whether to include quantity information
    
    Returns:
        List of volunteer roles
    """
    return breeze_api.list_volunteer_roles(instance_id, show_quantity)

@router.post("/add_role")
async def add_volunteer_role(instance_id: str, name: str, quantity: int = 1):
    """
    Add a new volunteer role to a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **name**: Name of the role
    - **quantity**: Number of volunteers needed for this role
    
    Returns:
        Created role information
    """
    return breeze_api.add_volunteer_role(instance_id, name, quantity)

@router.delete("/remove_role")
async def remove_volunteer_role(instance_id: str, role_id: str):
    """
    Remove a volunteer role from a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **role_id**: The ID of the role to remove
    
    Returns:
        Success or failure message
    """
    return breeze_api.remove_volunteer_role(instance_id, role_id)
