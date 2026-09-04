from datetime import date

def build_extraction_prompt(transcript: str, meeting_date: date, meeting_type: str) -> tuple[str, str]:
    """Returns (system_prompt, user_prompt) for Phase 2 extraction."""
    
    system = """You are a meeting intelligence extractor. Your job is to analyze sales meeting transcripts and extract structured business outcomes.

Rules:
- Be precise. Extract only what was actually said or clearly implied.
- Distinguish between what WE promised to do vs. what THE CLIENT promised to do.
- Infer deadlines from context: "by next Tuesday" = calculate from meeting_date. "soon" = 2 business days. "end of month" = last business day.
- Flag ambiguity. If you're unsure whether something is a real commitment, note it in confidence_notes.
- Ignore pleasantries, scheduling small talk, and technical digressions unless they contain commitments.
- Consolidate duplicates. If the same item is mentioned multiple times, extract it once and note frequency."""

    user = f"""Meeting Type: {meeting_type}
Meeting Date: {meeting_date.isoformat()}

Transcript:
---
{transcript}
---

Extract all action items, commitments, decisions, open questions, and objections. Return structured data only."""

    return system, user