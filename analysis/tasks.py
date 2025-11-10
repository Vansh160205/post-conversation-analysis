
from celery import shared_task
from .models import Conversation
from .analyzer import perform_analysis

@shared_task
def run_daily_analysis():
    """
    Celery task: Runs analysis on all unprocessed conversations
    """
    unprocessed = Conversation.objects.filter(analysis__isnull=True)
    
    count = 0
    for convo in unprocessed:
        try:
            perform_analysis(convo.id)
            count += 1
        except Exception as e:
            print(f"Failed to analyze conversation {convo.id}: {e}")
    
    return f"Successfully analyzed {count} conversations"


@shared_task
def analyze_conversation_async(conversation_id):
    analysis = perform_analysis(conversation_id)
    if not analysis:
        return {"status": "failure", "conversation_id": conversation_id}
    return {"status": "success", "conversation_id": conversation_id, "analysis_id": analysis.id}