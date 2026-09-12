from datetime import date, datetime
from typing import Union
from llm.models import MeetingExtraction
from llm.provider import llm_client
from prompts.extraction import extraction_prompt


async def extraction_func(
    transcript: str,
    meeting_date: Union[date, str],
    meeting_type: str
) -> MeetingExtraction:
    """
    Phase 2 Extraction Service: Extracts structured meeting intelligence
    (action items, commitments, decisions, open questions, objections, sentiment, confidence notes)
    from raw meeting transcript using the LLM client.
    """
    if isinstance(meeting_date, str):
        try:
            meeting_date = date.fromisoformat(meeting_date)
        except ValueError:
            meeting_date = datetime.fromisoformat(meeting_date).date()

    system_prompt, user_prompt = extraction_prompt(
        transcript=transcript,
        meeting_date=meeting_date,
        meeting_type=meeting_type
    )

    extracted_data: MeetingExtraction = await llm_client.structured_call(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        output_schema=MeetingExtraction
    )

    return extracted_data


# Alias for explicit service naming convention
extract_meeting_intelligence = extraction_func