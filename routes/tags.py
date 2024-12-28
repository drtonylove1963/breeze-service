from fastapi import APIRouter, HTTPException
from typing import Optional
from .models import Tag

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/")
async def get_tags(folder: Optional[str] = None):
    """
    List all tags, optionally filtered by folder.
    
    Parameters:
    - **folder**: If set, only return tags in this folder ID
    
    Returns:
        List of tags
    """
    return breeze_api.get_tags(folder)

@router.get("/folders")
async def get_tag_folders():
    """
    List all tag folders.
    
    Returns:
        List of tag folders
    """
    return breeze_api.get_tag_folders()

@router.post("/assign")
async def assign_tag(person_id: str, tag_id: str):
    """
    Assign a tag to a person.
    
    Parameters:
    - **person_id**: An existing person's user ID
    - **tag_id**: The ID number of the tag to assign
    
    Returns:
        Success or failure message
    """
    return breeze_api.assign_tag(person_id, tag_id)

@router.delete("/unassign")
async def unassign_tag(person_id: str, tag_id: str):
    """
    Remove a tag from a person.
    
    Parameters:
    - **person_id**: An existing person's user ID
    - **tag_id**: The ID number of the tag to remove
    
    Returns:
        Success or failure message
    """
    return breeze_api.unassign_tag(person_id, tag_id)
