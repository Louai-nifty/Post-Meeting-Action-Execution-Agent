from services.extraction_service import extraction_func
from state import AgentState
from utils.loggings import get_logger
from database.db import get_client

logger = get_logger(__name__)
supabase = get_client()

async def extraction_node(state: AgentState):
    try:
        meeting_title = state.meeting_title
        raw_transcript = state.raw_transcript
        meeting_date = state.meeting_date
        meeting_type = state.meeting_type
        meeting_attendees = state.meeting_attendees
        call_owner_email = state.call_owner_email

        logger.info("Begin extracting the meeting information")
        
        extracted_data = await extraction_func(
            transcript=raw_transcript,
            meeting_date=meeting_date,
            meeting_type=meeting_type
        )

        logger.info(f"Successfully extracted data from meeting: {meeting_title}")
        
        return {
            "extracted_data": extracted_data
        }
    except Exception as e:
        logger.error(f"Extraction node failed with error: {str(e)}", exc_info=True)
        raise e