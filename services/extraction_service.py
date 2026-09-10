from llm.models import ExtractedDataSchema
from prompts.extraction import extraction_prompt


async def extraction_func(
    transcript: str,
    meeting_date: str,
    meeting_type: str
):
    system_prompt, user_prompt = extraction_prompt(
        transcript=transcript,
        meeting_date=meeting_date,
        meeting_type=meeting_type
    )
    response = await llm.models.call_llm(
        system=system_prompt,
        user=user_prompt
        output_schema=ExtractedDataSchema
    )
    return response
    