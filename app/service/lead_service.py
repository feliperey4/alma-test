"""
Written by Felipe Rey
"""
from typing import Optional, List

from sqlalchemy.orm import Session

from app.database import LeadState, Lead
from app.service.email_utils import send_lead_confirmation_email, send_attorney_notification_email


class LeadService:

    @classmethod
    async def create_lead(
            cls,
            email: str,
            f_name: str,
            l_name: str,
            cv_name: str,
            cv_content: bytes,
            db: Session
    ):
        # Save to database
        cls._create_lead(
            db=db,
            email=email,
            f_name=f_name,
            l_name=l_name,
            cv_name=cv_name,
            cv_content=cv_content,
        )

        # Send emails
        full_name = f"{f_name} {l_name}"
        await send_lead_confirmation_email(email, full_name)
        await send_attorney_notification_email(email, full_name)

    @classmethod
    def update_lead(
            cls,
            db: Session,
            lead_id: int,
            new_state: LeadState) -> Optional[Lead]:
        return cls._update_lead(db, lead_id, new_state)

    @classmethod
    def get_leads(
            cls,
            db: Session,
            email: Optional[str] = None,
            f_name: Optional[str] = None,
            l_name: Optional[str] = None,
            state: Optional[str] = None
    ) -> List[Lead]:
        return cls._get_leads(db, email, f_name, l_name, state)

    @classmethod
    def get_lead(cls, db: Session, lead_id: int) -> Optional[Lead]:
        return db.query(Lead).filter(Lead.id == lead_id).first()

    @classmethod
    def _create_lead(
            cls,
            db: Session,
            email: str,
            f_name: str,
            l_name: str,
            cv_name: str,
            cv_content: bytes,
    ):
        # Save to database
        db_lead = Lead(
            email=email,
            f_name=f_name,
            l_name=l_name,
            cv_name=cv_name,
            cv_content=cv_content,
            state=LeadState.PENDING
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead

    @classmethod
    def _update_lead(cls, db: Session, lead_id: int, state: LeadState) -> Optional[Lead]:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if lead:
            lead.state = state
            db.commit()
            db.refresh(lead)
        return lead

    @classmethod
    def _get_leads(
            cls,
            db: Session,
            email: Optional[str] = None,
            f_name: Optional[str] = None,
            l_name: Optional[str] = None,
            state: Optional[str] = None
    ) -> List[Lead]:
        query = db.query(Lead)

        if email:
            query = query.filter(Lead.email == email)
        if f_name:
            query = query.filter(Lead.f_name == f_name)
        if l_name:
            query = query.filter(Lead.l_name == l_name)
        if state:
            query = query.filter(Lead.state == state)

        return query.all()


