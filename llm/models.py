from pydantic import BaseModel, Field
from typing import Literal, List
from datetime import date

class ExtractedActionItem(BaseModel):
    description: str = Field(description="What needs to be done")
    owner: str = Field(description="Who is responsible (name or 'us'/'them')")
    deadline: str | None = Field(description="Deadline as stated or inferred. ISO 8601 if possible, original text if ambiguous")
    deadline_confidence: Literal["explicit", "inferred", "ambiguous"] = Field(description="How the deadline was determined")
    category: Literal["action_item", "our_commitment", "their_commitment", "decision", "open_question", "objection"]

class MeetingExtraction(BaseModel):
    meeting_summary: str = Field(description="Concise summary of what was discussed")
    action_items: List[ExtractedActionItem] = Field(default_factory=list)
    key_decisions: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    objections: List[str] = Field(default_factory=list)
    sentiment: Literal["positive", "neutral", "concerned", "negative"] = Field(description="Overall meeting tone")
    confidence_notes: List[str] = Field(default_factory=list, description="Any ambiguous items the human should review")