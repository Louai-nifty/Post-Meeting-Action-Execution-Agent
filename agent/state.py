from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class AgentState(BaseModel):
    meeting_id: str = Field(description="Unique identifier for the meeting")
    raw_transcript: str = Field(description="Raw transcript of the meeting")
    meeting_title: str = Field(description="Title of the meeting")
    meeting_date: str = Field(description="Date of the meeting")
    meeting_type: str = Field(description="Type of the meeting")
    meeting_attendees: List[str] = Field(description="List of attendees")
    call_owner_email: EmailStr