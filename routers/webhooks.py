from fastapi import APIRouter, BackgroundTasks, Request
from database.db import get_client
from fastapi.responses import JSONResponse
from models.fathom import FathomWebhook
from utils.loggings import get_logger


router = APIRouter()
supabase = get_client()
logger = get_logger(__name__)


@router.post("/webhooks/meeting-completed")
async def handle_zoom_webhook(request: Request, background_tasks: BackgroundTasks, payload: FathomWebhook):
    try:
        agent = request.app.state.agent
        background_tasks.add_task(process_webhook, agent, payload)
        return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Webhook received successfully."}
    )
    except Exception as e:
        return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(e)}
    )


async def process_webhook(agent, payload: FathomWebhook):
    """This BG method is for processing the webhook comming from Tally(supposed to be Fathom)."""
    try:
        logger.info(f"Processing Fathom webhook...")
        
        fields = payload.data.fields
        call_data = {}
        for field in fields:
            if field.label == "call owner":
                call_data['call_owner'] = field.value
            if field.label == "meeting title":
                call_data['meeting_title'] = field.value
            if field.label == "meeting type":
                call_data['meeting_type'] = field.value
            if field.label == "meeting url":
                call_data['meeting_url'] = field.value
            if field.label == "meeting date":
                call_data['meeting_date'] = field.value
            if field.label == "meeting attendees":
                call_data['meeting_attendees'] = field.value
            if field.label == "meeting transcript":
                call_data['meeting_transcript'] = field.value


        return response
    except Exception as e:
        print(e)