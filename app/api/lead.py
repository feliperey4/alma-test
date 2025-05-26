"""
Written by Felipe Rey
"""
import io
from typing import *

from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.user import get_current_user
from app.database import LeadState, get_db, User
from app.service.lead_service import LeadService

lead_route = APIRouter(tags=['Lead'])


# API schema

class LeadCreate(BaseModel):
    email: EmailStr
    f_name: str
    l_name: str

class LeadUpdate(BaseModel):
    state: LeadState

class LeadResponse(BaseModel):
    id: int
    email: str
    f_name: str
    l_name: str
    cv_name: str
    state: LeadState

    class Config:
        from_attributes = True


# Endpoints - Public

@lead_route.post("/leads/", status_code=204)
async def create_lead(
        email: str = Form(...),
        f_name: str = Form(...),
        l_name: str = Form(...),
        cv: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Create a new lead that will be processed by an attorney.
    """
    # Validate file type (optional)
    if not cv.filename.lower().endswith(('.pdf', '.doc', '.docx')):
        raise HTTPException(status_code=400,
                            detail="Invalid file type. Please upload PDF, DOC, or DOCX files.")
    # Read file content
    cv_content = await cv.read()
    # Create lead data
    await LeadService.create_lead(email, f_name, l_name, cv.filename ,cv_content, db)
    return Response(status_code=204)

# ======================================================
# Endpoints - Protect

@lead_route.patch("/internal/leads/{lead_id}", status_code=204)
async def update_lead(
        lead_id: int,
        lead_update: LeadUpdate,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user) # validate JWT
):
    """
    Update the state of a lead.
    """
    updated_lead = LeadService.update_lead(db, lead_id, lead_update.state)
    if not updated_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return Response(status_code=204)



@lead_route.get("/internal/leads/", response_model=List[LeadResponse])
async def list_leads(
    email: Optional[str] = None,
    f_name: Optional[str] = None,
    l_name: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user) # validate JWT
):
    """
    Get a list of leads.
    """
    return LeadService.get_leads(db, email=email, f_name=f_name, l_name=l_name, state=state)


@lead_route.get("/internal/leads/{lead_id}/cv-download")
async def download_cv(
        lead_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user) # validate JWT
):
    """
    Download the CV of a lead.
    """
    lead = LeadService.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return StreamingResponse(
        io.BytesIO(lead.cv_content),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={lead.cv_name}"}
    )