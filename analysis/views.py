# analysis/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Conversation, ConversationAnalysis
from .serializers import ConversationSerializer, ConversationAnalysisSerializer
from .analyzer import perform_analysis # Import your logic
from .tasks import analyze_conversation_async

class ConversationUploadView(generics.CreateAPIView):
    """Upload chat JSON and create Conversation with nested Messages."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class AnalysisReportView(generics.ListAPIView):
    """List all conversation analysis results."""
    queryset = ConversationAnalysis.objects.all().order_by('-created_at')
    serializer_class = ConversationAnalysisSerializer

class SingleAnalysisView(generics.RetrieveAPIView):
    """Fetch a single analysis report by ID."""
    queryset = ConversationAnalysis.objects.all()
    serializer_class = ConversationAnalysisSerializer

class AnalysisTriggerView(APIView):
    """Trigger async analysis for a specific conversation."""
    def post(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {"error": "conversation_id is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if not Conversation.objects.filter(id=conversation_id).exists():
            return Response(
                {"error": f"Conversation {conversation_id} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        task = analyze_conversation_async.delay(conversation_id)        
        return Response({
            "message": "Analysis queued",
            "task_id": task.id,
            "conversation_id": conversation_id
        }, status=status.HTTP_202_ACCEPTED)