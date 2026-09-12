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
                call_data['call_owner_email'] = field.value
            if field.label == "meeting title":
                call_data['meeting_title'] = field.value
            if field.label == "meeting type":
                call_data['meeting_type'] = field.value
            if field.label == "meeting url":
                call_data['recording_url'] = field.value
            if field.label == "meeting date":
                call_data['meeting_date'] = field.value
            if field.label == "meeting attendees":
                call_data['attendees_list'] = field.value
            if field.label == "meeting transcript":
                call_data['raw_transcript'] = field.value


        insert_res = supabase.table('meetings').insert(call_data).execute()
        meeting_id = None
        if insert_res.data and len(insert_res.data) > 0:
            meeting_id = insert_res.data[0].get("meeting_id") or insert_res.data[0].get("id")
        
        if not meeting_id:
            query_res = supabase.table('meetings').select("meeting_id").eq("call_owner_email", call_data.get('call_owner_email')).execute()
            if query_res.data and len(query_res.data) > 0:
                meeting_id = query_res.data[0].get("meeting_id")

        meeting_id_str = str(meeting_id) if meeting_id else "meeting_thread"

        await agent.ainvoke({
            "meeting_id": meeting_id_str,
            "raw_transcript": call_data.get('raw_transcript', ''),
            "meeting_title": call_data.get('meeting_title', ''),
            "meeting_date": call_data.get('meeting_date', ''),
            "meeting_type": call_data.get('meeting_type', ''),
            "meeting_attendees": call_data.get('attendees_list', []),
            "call_owner_email": call_data.get('call_owner_email', ''),
        },
            config={"configurable": {"thread_id": meeting_id_str}}
        )
    except Exception as e:
        logger.error(f"Agent run failed: {str(e)}", exc_info=True)