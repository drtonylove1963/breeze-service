from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from pyBreezeChMS.breeze.breeze import BreezeApi
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Breeze API
breeze_api = BreezeApi(
    breeze_url=os.getenv('breeze_url'),
    api_key=os.getenv('api_key')
)

app = FastAPI(
    title="Breeze ChMS API",
    description="""
    API wrapper for Breeze Church Management System.
    This API wrapper allows churches to build custom functionality integrated with Breeze ChMS.
    """,
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
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
    name: Optional[str] = None
    person_id: Optional[str] = None
    uid: Optional[str] = None
    processor: Optional[str] = None
    method: Optional[str] = None
    funds_json: Optional[str] = None
    amount: Optional[float] = None
    group: Optional[str] = None
    batch_number: Optional[str] = None
    batch_name: Optional[str] = None

class Tag(BaseModel):
    id: str
    name: str
    created_on: Optional[str] = None
    folder_id: Optional[str] = None

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

# Create routers with tags
people_router = APIRouter(prefix="/people", tags=["People"])
events_router = APIRouter(prefix="/events", tags=["Events"])
contributions_router = APIRouter(prefix="/contributions", tags=["Contributions"])
campaigns_router = APIRouter(prefix="/campaigns", tags=["Campaigns"])
tags_router = APIRouter(prefix="/tags", tags=["Tags"])
forms_router = APIRouter(prefix="/forms", tags=["Forms"])
volunteers_router = APIRouter(prefix="/volunteers", tags=["Volunteers"])
profile_router = APIRouter(prefix="/profile", tags=["Profile"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {"message": "Breeze ChMS API is running"}

# People endpoints
@people_router.get("/", response_model=List[Person])
async def get_people(limit: Optional[int] = None, offset: Optional[int] = None, details: bool = False):
    """
    List people from your database.

    Parameters:
    - **limit**: Number of people to return. If None, will return all people
    - **offset**: Number of people to skip before beginning to return results. Can be used with limit for pagination
    - **details**: Option to return all information (slower) or just names

    Returns:
        JSON response. For example:
        ```json
        [
            {
                "id": "157857",
                "first_name": "Thomas",
                "last_name": "Anderson",
                "path": "img/profiles/generic/blue.jpg"
            },
            {
                "id": "157859",
                "first_name": "Kate",
                "last_name": "Austen",
                "path": "img/profiles/upload/2498d7f78s.jpg"
            }
        ]
        ```
    """
    try:
        return breeze_api.get_people(limit=limit, offset=offset, details=details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@people_router.get("/{person_id}", response_model=Dict)
async def get_person_details(person_id: str):
    """
    Retrieve the details for a specific person by their ID.

    Parameters:
    - **person_id**: Unique ID for a person in Breeze database

    Returns:
        JSON response with person details
    """
    try:
        return breeze_api.get_person_details(person_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Person not found: {str(e)}")

@people_router.post("/", response_model=Dict)
async def add_person(first_name: str, last_name: str, fields_json: Optional[str] = None):
    """
    Add a new person to the database.

    Parameters:
    - **first_name**: The first name of the person
    - **last_name**: The last name of the person
    - **fields_json**: Optional JSON string representing an array of fields to update.
        Each array element must contain field id, field type, response, and in some cases, more information.

    Example fields_json:
    ```json
    [
        {
            "field_id": "929778337",
            "field_type": "email",
            "response": "true",
            "details": {
                "address": "tony@starkindustries.com",
                "is_private": 1
            }
        }
    ]
    ```

    Note: Use get_profile_fields() to get field information or get_person_details() 
    to see fields that already exist for a person.

    Returns:
        JSON response equivalent to get_person_details()
    """
    try:
        return breeze_api.add_person(first_name, last_name, fields_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@people_router.put("/{person_id}", response_model=Dict)
async def update_person(person_id: str, fields_json: str):
    """
    Updates the details for a specific person in the database.

    Parameters:
    - **person_id**: Unique id for a person in Breeze database
    - **fields_json**: JSON string representing an array of fields to update.
        Each array element must contain field id, field type, response,
        and in some cases, more information.

    Example fields_json:
    ```json
    [
        {
            "field_id": "929778337",
            "field_type": "email",
            "response": "true",
            "details": {
                "address": "tony@starkindustries.com",
                "is_private": 1
            }
        }
    ]
    ```

    Note: Use get_profile_fields() to get field information or
    use get_person_details() to see fields that already exist for a specific person.

    Returns:
        JSON response equivalent to get_person_details(person_id)
    """
    try:
        return breeze_api.update_person(person_id, fields_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Profile endpoints
@profile_router.get("/fields", response_model=List[Dict])
async def get_profile_fields():
    """
    List profile fields from your database.

    Returns:
        JSON response containing all available profile fields and their details. For example:
        ```json
        [
            {
                "id": "929778337",
                "name": "Email",
                "type": "email"
            },
            {
                "id": "929778338",
                "name": "Phone",
                "type": "phone"
            }
        ]
        ```
    """
    try:
        return breeze_api.get_profile_fields()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Events endpoints
@events_router.get("/", response_model=List[Event])
async def get_events(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Retrieve all events for a given date range.

    Parameters:
    - **start_date**: Start date (defaults to first day of current month)
    - **end_date**: End date (defaults to last day of current month)

    Returns:
        JSON response with list of events
    """
    try:
        return breeze_api.get_events(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@events_router.post("/", response_model=Dict)
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
    - **start_date**: Start datetimestamp (epoch time)
    - **end_date**: End datetimestamp (epoch time)
    - **all_day**: Boolean indicating if event is all day
    - **description**: Description of event
    - **category_id**: Which calendar your event is on (defaults to primary)
    - **event_id**: Series ID

    Returns:
        JSON response with created event details
    """
    try:
        return breeze_api.add_event(name, start_date, end_date, all_day, description, category_id, event_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@events_router.post("/{event_instance_id}/check-in/{person_id}")
async def event_check_in(person_id: str, event_instance_id: str):
    """
    Check in a person to an event.

    Parameters:
    - **person_id**: ID for a person in Breeze database
    - **event_instance_id**: ID for event instance to check into

    Returns:
        JSON response confirming check-in
    """
    try:
        return breeze_api.event_check_in(person_id, event_instance_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@events_router.delete("/{event_instance_id}/check-out/{person_id}")
async def event_check_out(person_id: str, event_instance_id: str):
    """
    Remove the attendance for a person checked into an event.

    Parameters:
    - **person_id**: Breeze ID for a person in Breeze database
    - **event_instance_id**: ID for event instance to check out (delete)

    Returns:
        True if check-out succeeds; False if check-out fails
    """
    try:
        return breeze_api.event_check_out(person_id, event_instance_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contributions endpoints
@contributions_router.post("/", response_model=str)
async def add_contribution(contribution: Contribution):
    """
    Add a contribution to Breeze.

    Parameters:
    - **date**: Date of transaction in DD-MM-YYYY format (e.g., 24-5-2015)
    - **name**: Name of person that made the transaction (e.g., John Doe)
    - **person_id**: The Breeze ID of the donor. If unknown, use UID instead
    - **uid**: Unique ID from the giving platform when Breeze ID is unknown
    - **processor**: Name of payment processor (e.g., SimpleGive, BluePay, Stripe)
    - **method**: Payment method (Check, Cash, Credit/Debit Online, etc.)
    - **funds_json**: JSON string for splitting fund giving
    - **amount**: Total amount given (must match sum in funds_json)
    - **group**: For creating new batch with grouped contributions
    - **batch_number**: Batch number for import
    - **batch_name**: Name of the batch

    Example funds_json:
    ```json
    [
        {
            "id": "12345",
            "name": "General Fund",
            "amount": "100.00"
        },
        {
            "name": "Missions Fund",
            "amount": "150.00"
        }
    ]
    ```

    Returns:
        Payment ID
    """
    try:
        return breeze_api.add_contribution(
            date=contribution.date,
            name=contribution.name,
            person_id=contribution.person_id,
            uid=contribution.uid,
            processor=contribution.processor,
            method=contribution.method,
            funds_json=contribution.funds_json,
            amount=contribution.amount,
            group=contribution.group,
            batch_number=contribution.batch_number,
            batch_name=contribution.batch_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@contributions_router.get("/", response_model=List[Dict])
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
    - **start_date**: Find contributions given on or after this date (YYYY-MM-DD)
    - **end_date**: Find contributions given on or before this date (YYYY-MM-DD)
    - **person_id**: ID of person's contributions to fetch
    - **include_family**: Include family members of person_id (requires person_id)
    - **amount_min**: Contribution amounts equal or greater than
    - **amount_max**: Contribution amounts equal or less than
    - **method_ids**: List of payment method IDs
    - **fund_ids**: List of fund IDs
    - **envelope_number**: Envelope number
    - **batches**: List of batch numbers
    - **forms**: List of form IDs

    Returns:
        List of matching contributions
    """
    try:
        return breeze_api.list_contributions(
            start_date=start_date,
            end_date=end_date,
            person_id=person_id,
            include_family=include_family,
            amount_min=amount_min,
            amount_max=amount_max,
            method_ids=method_ids,
            fund_ids=fund_ids,
            envelope_number=envelope_number,
            batches=batches,
            forms=forms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Forms endpoints
@forms_router.get("/{form_id}/entries", response_model=List[FormEntry])
async def list_form_entries(form_id: str, details: bool = False):
    """
    Get entries for a specific form.

    Parameters:
    - **form_id**: The ID of the form
    - **details**: Option to return all information (slower) or just names

    Returns:
        JSON response. For example:
        ```json
        [
            {
                "id": "11",
                "form_id": "15326",
                "created_on": "2021-03-09 13:04:02",
                "person_id": null,
                "response": {
                    "45": {
                        "id": "13",
                        "oid": "1512",
                        "first_name": "Zoe",
                        "last_name": "Washburne",
                        "created_on": "2021-03-09 13:04:03"
                    },
                    "46": "zwashburne@test.com",
                    "47": "Red"
                }
            }
        ]
        ```
    """
    try:
        return breeze_api.list_form_entries(form_id, details)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@forms_router.get("/{form_id}/fields", response_model=List[FormField])
async def list_form_fields(form_id: str):
    """
    List all fields for a specific form.
    
    Parameters:
    - **form_id**: The ID of the form
    
    Returns:
        List of form fields with their properties
    """
    try:
        return breeze_api.list_form_fields(form_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@forms_router.delete("/entries/{entry_id}")
async def remove_form_entry(entry_id: str):
    """
    Remove a specific form entry.
    
    Parameters:
    - **entry_id**: The ID of the form entry to remove
    
    Returns:
        Success or failure message
    """
    try:
        return breeze_api.remove_form_entry(entry_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Volunteers endpoints
@volunteers_router.get("/{instance_id}", response_model=List[Volunteer])
async def list_volunteers(instance_id: str):
    """
    List all volunteers for a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    
    Returns:
        List of volunteers and their roles
    """
    try:
        return breeze_api.list_volunteers(instance_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@volunteers_router.post("/{instance_id}")
async def add_volunteer(instance_id: str, person_id: str):
    """
    Add a volunteer to a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **person_id**: The ID of the person to add as volunteer
    
    Returns:
        Success or failure message
    """
    try:
        return breeze_api.add_volunteer(instance_id, person_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@volunteers_router.delete("/{instance_id}/{person_id}")
async def remove_volunteer(instance_id: str, person_id: str):
    """
    Remove a volunteer from a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **person_id**: The ID of the person to remove
    
    Returns:
        Success or failure message
    """
    try:
        return breeze_api.remove_volunteer(instance_id, person_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@volunteers_router.put("/{instance_id}/{person_id}")
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
    try:
        return breeze_api.update_volunteer(instance_id, person_id, role_ids_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@volunteers_router.get("/{instance_id}/roles", response_model=List[VolunteerRole])
async def list_volunteer_roles(instance_id: str, show_quantity: bool = False):
    """
    List all volunteer roles for a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **show_quantity**: Whether to include quantity information
    
    Returns:
        List of volunteer roles
    """
    try:
        return breeze_api.list_volunteer_roles(instance_id, show_quantity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@volunteers_router.post("/{instance_id}/roles")
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
    try:
        return breeze_api.add_volunteer_role(instance_id, name, quantity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@volunteers_router.delete("/{instance_id}/roles/{role_id}")
async def remove_volunteer_role(instance_id: str, role_id: str):
    """
    Remove a volunteer role from a specific instance.
    
    Parameters:
    - **instance_id**: The ID of the instance
    - **role_id**: The ID of the role to remove
    
    Returns:
        Success or failure message
    """
    try:
        return breeze_api.remove_volunteer_role(instance_id, role_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include all routers
app.include_router(people_router)
app.include_router(events_router)
app.include_router(contributions_router)
app.include_router(campaigns_router)
app.include_router(tags_router)
app.include_router(forms_router)
app.include_router(volunteers_router)
app.include_router(profile_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
