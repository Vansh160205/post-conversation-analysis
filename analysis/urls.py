# analysis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.ConversationUploadView.as_view(), name='conversation-upload'),
    path('analyse/', views.AnalysisTriggerView.as_view(), name='analysis-trigger'),
    path('reports/<int:pk>/', views.SingleAnalysisView.as_view(), name='single-report'),
    path('reports/', views.AnalysisReportView.as_view(), name='analysis-reports'),
]