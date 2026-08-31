from pydantic import BaseModel
from typing import Any, List


# This model was supposed to have the payload from Fathom but it was replaced by TallyWebhookPayload, due to the incapability to replicate a real sales call

class FormFields(BaseModel):
    key: Any
    label: Any
    type: Any
    value: Any

class FormData(BaseModel):
    formName: str
    submissionPdfUrl: str
    fields: List[FormFields]

class FathomWebhook(BaseModel):
    data: FormData
    