from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from llm.models import MeetingExtraction

class AgentState(BaseModel):
    meeting_id: str = Field(description="Unique identifier for the meeting")
    raw_transcript: str = Field(description="Raw transcript of the meeting")
    meeting_title: str = Field(description="Title of the meeting")
    meeting_date: str = Field(description="Date of the meeting")
    meeting_type: str = Field(description="Type of the meeting")
    meeting_attendees: List[str] = Field(description="List of attendees")
    call_owner_email: EmailStr
    extracted_data: Optional[MeetingExtraction] = Field(default=None, description="Extracted meeting intelligence from Phase 2")
    status: Optional[str] = Field(default="ingested", description="Current workflow state")