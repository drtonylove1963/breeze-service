from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/")
async def list_campaigns():
    """
    List all campaigns.
    
    Returns:
        List of campaigns
    """
    return breeze_api.list_campaigns()

@router.get("/{campaign_id}/pledges")
async def list_pledges(campaign_id: str):
    """
    List pledges within a campaign.
    
    Parameters:
    - **campaign_id**: ID number of a campaign
    
    Returns:
        List of pledges
    """
    return breeze_api.list_pledges(campaign_id)
