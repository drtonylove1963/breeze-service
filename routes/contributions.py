from fastapi import APIRouter, HTTPException
from typing import List, Optional
from .models import Contribution

router = APIRouter(prefix="/contributions", tags=["Contributions"])

@router.post("/add")
async def add_contribution(contribution: Contribution):
    """
    Add a contribution to Breeze.
    
    Parameters:
    - **contribution**: Contribution object with all necessary details
    
    Returns:
        Payment ID
    """
    return breeze_api.add_contribution(contribution)

@router.get("/list")
async def list_contributions(
    start_date: str,
    end_date: str,
    person_id: Optional[str] = None,
    include_family: bool = False,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None,
    method_ids: Optional[List[str]] = None,
    fund_ids: Optional[List[str]] = None,
    envelope_number: Optional[str] = None,
    batches: Optional[List[str]] = None,
    forms: Optional[List[str]] = None
):
    """
    Retrieve a list of contributions based on various filters.
    
    Parameters:
    - **start_date**: Find contributions given on or after this date
    - **end_date**: Find contributions given on or before this date
    - **person_id**: ID of person's contributions to fetch
    - **include_family**: Include family members of person_id
    - **amount_min**: Contribution amounts equal or greater than
    - **amount_max**: Contribution amounts equal or less than
    - **method_ids**: List of payment method IDs
    - **fund_ids**: List of fund IDs
    - **envelope_number**: Envelope number
    - **batches**: List of batch numbers
    - **forms**: List of form IDs
    
    Returns:
        List of contributions
    """
    return breeze_api.list_contributions(
        start_date, end_date, person_id, include_family,
        amount_min, amount_max, method_ids, fund_ids,
        envelope_number, batches, forms
    )
