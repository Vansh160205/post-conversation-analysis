# analysis/analyzer.py
from django.utils import timezone
from datetime import timedelta
from .models import Conversation, Message, ConversationAnalysis
import re

def perform_analysis(conversation_id):
    """
    Performs comprehensive analysis on a conversation.
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        messages = conversation.messages.all().order_by('created_at')
        
        if not messages.exists():
            return None
        
        # Separate messages
        user_messages = [m for m in messages if m.sender == 'user']
        ai_messages = [m for m in messages if m.sender == 'ai']
        
        if not user_messages or not ai_messages:
            return None
        
        # ============ ANALYSIS LOGIC ============
        
        # 1. CLARITY SCORE (5.0 max)
        clarity = calculate_clarity(ai_messages)
        
        # 2. RELEVANCE SCORE (5.0 max)
        relevance = calculate_relevance(user_messages, ai_messages)
        
        # 3. ACCURACY SCORE (5.0 max)
        accuracy = calculate_accuracy(ai_messages)
        
        # 4. COMPLETENESS SCORE (5.0 max)
        completeness = calculate_completeness(ai_messages)
        
        # 5. SENTIMENT ANALYSIS
        sentiment = detect_sentiment(user_messages)
        
        # 6. EMPATHY SCORE (5.0 max, only if negative sentiment)
        empathy = calculate_empathy(ai_messages, sentiment)
        
        # 7. RESPONSE TIME (in seconds)
        avg_response_time = calculate_response_time(messages)
        
        # 8. RESOLUTION RATE (Boolean)
        resolved = detect_resolution(user_messages, ai_messages)
        
        # 9. ESCALATION NEED (Boolean)
        escalation = detect_escalation_need(user_messages, ai_messages, sentiment, resolved)
        
        # 10. FALLBACK FREQUENCY (Count)
        fallback_count = count_fallbacks(ai_messages)
        
        # 11. OVERALL SCORE (Average of key metrics)
        overall = calculate_overall_score(clarity, relevance, accuracy, completeness, empathy)
        
        # ============ SAVE TO DATABASE ============
        analysis, created = ConversationAnalysis.objects.update_or_create(
            conversation=conversation,
            defaults={
                'clarity_score': clarity,
                'relevance_score': relevance,
                'accuracy_score': accuracy,
                'completeness_score': completeness,
                'sentiment': sentiment,
                'empathy_score': empathy,
                'response_time_avg': avg_response_time,
                'resolution_rate': resolved,
                'escalation_need': escalation,
                'fallback_frequency': fallback_count,
                'overall_score': overall,
            }
        )
        
        return analysis
    
    except Conversation.DoesNotExist:
        return None
    except Exception as e:
        print(f"Analysis error for conversation {conversation_id}: {e}")
        return None


# ========== HELPER FUNCTIONS ==========

def calculate_clarity(ai_messages):
    """
    Clarity based on:
    - Message length (not too short, not too long)
    - Sentence structure
    - Technical jargon usage
    """
    score = 5.0
    
    for msg in ai_messages:
        text = msg.text.strip()
        word_count = len(text.split())
        
        # Too short responses (< 5 words)
        if word_count < 5:
            score -= 0.5
        
        # Too long responses (> 100 words) without structure
        if word_count > 100 and '.' not in text[:-1]:
            score -= 0.3
        
        # Check for unclear phrases
        unclear_phrases = ['maybe', 'might', 'possibly', 'not sure', 'i think']
        if any(phrase in text.lower() for phrase in unclear_phrases):
            score -= 0.2
    
    return max(1.0, min(5.0, score))


def calculate_relevance(user_messages, ai_messages):
    """
    Relevance based on topic consistency
    """
    score = 5.0
    
    # Extract keywords from user messages
    user_keywords = set()
    for msg in user_messages:
        words = re.findall(r'\w+', msg.text.lower())
        user_keywords.update(words)
    
    # Check if AI responses contain user keywords
    for ai_msg in ai_messages:
        ai_words = set(re.findall(r'\w+', ai_msg.text.lower()))
        
        # If no common keywords, reduce relevance
        common = user_keywords.intersection(ai_words)
        if len(common) < 2:
            score -= 0.5
    
    return max(1.0, min(5.0, score))


def calculate_accuracy(ai_messages):
    """
    Accuracy check (mock logic - can be enhanced with fact-checking APIs)
    """
    score = 5.0
    
    # Penalize uncertain language
    uncertain_phrases = [
        'i am not sure', 'i cannot verify', 'i might be wrong',
        'i don\'t have that information', 'i cannot confirm'
    ]
    
    for msg in ai_messages:
        text = msg.text.lower()
        if any(phrase in text for phrase in uncertain_phrases):
            score -= 0.5
    
    return max(1.0, min(5.0, score))


def calculate_completeness(ai_messages):
    """
    Completeness based on answer depth
    """
    score = 5.0
    
    for msg in ai_messages:
        word_count = len(msg.text.split())
        
        # Very short answers indicate incomplete responses
        if word_count < 10:
            score -= 0.4
        
        # Questions in AI response indicate incomplete answer
        if '?' in msg.text:
            score -= 0.3
    
    return max(1.0, min(5.0, score))


def detect_sentiment(user_messages):
    """
    Sentiment analysis: positive, neutral, negative
    """
    positive_words = [
        'thanks', 'thank you', 'great', 'awesome', 'perfect', 'excellent',
        'good', 'helpful', 'appreciate', 'love', 'happy', 'resolved'
    ]
    
    negative_words = [
        'bad', 'terrible', 'worst', 'angry', 'frustrated', 'sad', 'disappointed',
        'useless', 'horrible', 'awful', 'hate', 'poor', 'unacceptable'
    ]
    
    pos_count = 0
    neg_count = 0
    
    for msg in user_messages:
        text = msg.text.lower()
        pos_count += sum(1 for word in positive_words if word in text)
        neg_count += sum(1 for word in negative_words if word in text)
    
    if pos_count > neg_count and pos_count > 0:
        return "positive"
    elif neg_count > pos_count and neg_count > 0:
        return "negative"
    else:
        return "neutral"


def calculate_empathy(ai_messages, sentiment):
    """
    Empathy score (only relevant for negative sentiment)
    """
    if sentiment != "negative":
        return 0.0
    
    empathy_phrases = [
        'i understand', 'i apologize', 'i\'m sorry', 'i appreciate your patience',
        'i can imagine', 'that must be frustrating', 'i hear you', 'let me help'
    ]
    
    score = 0.0
    for msg in ai_messages:
        text = msg.text.lower()
        empathy_count = sum(1 for phrase in empathy_phrases if phrase in text)
        score += min(empathy_count * 1.5, 5.0)
    
    return min(score, 5.0)


def calculate_response_time(messages):
    """
    Calculate average response time between user and AI messages
    """
    if len(messages) < 2:
        return 0.0
    
    response_times = []
    prev_msg = None
    
    for msg in messages:
        if prev_msg and prev_msg.sender == 'user' and msg.sender == 'ai':
            time_diff = (msg.created_at - prev_msg.created_at).total_seconds()
            response_times.append(time_diff)
        prev_msg = msg
    
    if response_times:
        return sum(response_times) / len(response_times)
    return 0.0


def detect_resolution(user_messages, ai_messages):
    """
    Check if issue was resolved
    """
    if not user_messages:
        return False
    
    last_user_msg = user_messages[-1].text.lower()
    
    resolution_indicators = [
        'thanks', 'thank you', 'resolved', 'solved', 'fixed', 'worked',
        'perfect', 'got it', 'understood', 'clear now'
    ]
    
    return any(indicator in last_user_msg for indicator in resolution_indicators)


def detect_escalation_need(user_messages, ai_messages, sentiment, resolved):
    """
    Determine if escalation to human is needed
    """
    # Escalate if negative sentiment and not resolved
    if sentiment == "negative" and not resolved:
        return True
    
    # Escalate if too many fallbacks
    fallback_count = count_fallbacks(ai_messages)
    if fallback_count > 2:
        return True
    
    # Escalate if user explicitly asks
    escalation_keywords = ['speak to human', 'talk to agent', 'real person', 'manager', 'supervisor']
    for msg in user_messages:
        if any(keyword in msg.text.lower() for keyword in escalation_keywords):
            return True
    
    return False


def count_fallbacks(ai_messages):
    """
    Count how many times AI used fallback responses
    """
    fallback_phrases = [
        'i don\'t know', 'i am unable to', 'i cannot help', 'i don\'t understand',
        'not sure', 'cannot assist', 'beyond my capability'
    ]
    
    count = 0
    for msg in ai_messages:
        text = msg.text.lower()
        if any(phrase in text for phrase in fallback_phrases):
            count += 1
    
    return count


def calculate_overall_score(clarity, relevance, accuracy, completeness, empathy):
    """
    Overall satisfaction score (weighted average)
    """
    weights = {
        'clarity': 0.25,
        'relevance': 0.25,
        'accuracy': 0.30,
        'completeness': 0.20,
    }
    
    overall = (
        clarity * weights['clarity'] +
        relevance * weights['relevance'] +
        accuracy * weights['accuracy'] +
        completeness * weights['completeness']
    )
    
    return round(overall, 2)