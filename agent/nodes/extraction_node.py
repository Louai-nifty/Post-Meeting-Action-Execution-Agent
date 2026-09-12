from agent.state import AgentState
from services.extraction_service import extraction_func
from utils.loggings import get_logger
from database.db import get_client

logger = get_logger(__name__)
supabase = get_client()

async def extraction_node(state: AgentState | dict) -> dict:
    """
    LangGraph Node for Phase 2: Intelligent Extraction & Structuring.
    Calls extraction_service to produce structured meeting intelligence and updates AgentState.
    """
    try:
        # Handle state as object or dict seamlessly
        meeting_title = getattr(state, "meeting_title", None) or state.get("meeting_title")
        raw_transcript = getattr(state, "raw_transcript", None) or state.get("raw_transcript")
        meeting_date = getattr(state, "meeting_date", None) or state.get("meeting_date")
        meeting_type = getattr(state, "meeting_type", None) or state.get("meeting_type")

        logger.info(f"Begin extracting meeting intelligence for: '{meeting_title}'")
        
        extracted_data = await extraction_func(
            transcript=raw_transcript,
            meeting_date=meeting_date,
            meeting_type=meeting_type
        )

        logger.info(f"Successfully extracted intelligence for meeting: '{meeting_title}'")
        
        return {
            "extracted_data": extracted_data,
            "status": "extracted"
        }
    except Exception as e:
        logger.error(f"Extraction node failed for meeting '{meeting_title}': {str(e)}", exc_info=True)
        raise e