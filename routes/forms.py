from fastapi import APIRouter, HTTPException
from typing import List
from .models import FormField, FormEntry
from .dependencies import breeze_api

router = APIRouter()

@router.get("/api/forms/list_form_fields", response_model=List[FormField], tags=["Forms"])
async def list_form_fields(form_id: str):
    """
    List all fields for a specific form.
    
    Parameters:
    - **form_id**: The ID of the form
    
    Returns:
        List of form fields with their properties
    """
    return breeze_api.list_form_fields(form_id)

@router.get("/api/forms/list_form_entries", response_model=List[FormEntry], tags=["Forms"])
async def list_form_entries(form_id: str, details: bool = False):
    """
    List all entries for a specific form.
    
    Parameters:
    - **form_id**: The ID of the form
    - **details**: Option to return all information (slower) or just basic info
    
    Returns:
        List of form entries
    """
    return breeze_api.list_form_entries(form_id, details)

@router.delete("/api/forms/remove_form_entry", tags=["Forms"])
async def remove_form_entry(entry_id: str):
    """
    Remove a specific form entry.
    
    Parameters:
    - **entry_id**: The ID of the form entry to remove
    
    Returns:
        Success or failure message
    """
    return breeze_api.remove_form_entry(entry_id)
