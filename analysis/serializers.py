# analysis/serializers.py
from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis

class MessageSerializer(serializers.ModelSerializer):
    message = serializers.CharField(source='text')  # Map message -> text

    class Meta:
        model = Message
        fields = ['sender', 'message']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, write_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # This logic handles creating the Conversation AND its nested Messages
        # Handles nested message creation from uploaded JSON
        messages_data = validated_data.pop('messages',[])
        conversation = Conversation.objects.create(**validated_data)
        for message_data in messages_data:
            Message.objects.create(conversation=conversation, **message_data)
        return conversation

class ConversationAnalysisSerializer(serializers.ModelSerializer):
    # Include conversation ID for context
    conversation_id = serializers.ReadOnlyField(source='conversation.id')

    class Meta:
        model = ConversationAnalysis
        # List all fields you defined in the model
        fields = [
            'id', 'conversation_id', 'clarity_score', 'relevance_score', 
            'accuracy_score', 'completeness_score', 'sentiment', 
            'empathy_score', 'response_time_avg', 'resolution_rate', 
            'escalation_need', 'fallback_frequency', 'overall_score', 'created_at'
        ]