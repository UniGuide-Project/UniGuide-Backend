from django.urls import path
from .views import (
    SubjectListView, SubjectDetailView, SubjectCreateView,
    SubjectUpdateView, SubjectDeleteView,
    QuestionListView, QuestionDetailView, QuestionDetailAdminView,
    QuestionCreateView, QuestionUpdateView, QuestionDeleteView,
    ChoiceListView, ChoiceCreateView, ChoiceUpdateView, ChoiceDeleteView,
    CheckAnswersView, StartTestView, UserStatisticsView,
)

app_name = 'quizzes'

urlpatterns = [
    # Fanlar
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
    # Savollar
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/create/', QuestionCreateView.as_view(), name='question_create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('questions/<int:pk>/admin/', QuestionDetailAdminView.as_view(), name='question_detail_admin'),
    path('questions/<int:pk>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    # Variantlar
    path('choices/', ChoiceListView.as_view(), name='choice_list'),
    path('choices/create/', ChoiceCreateView.as_view(), name='choice_create'),
    path('choices/<int:pk>/update/', ChoiceUpdateView.as_view(), name='choice_update'),
    path('choices/<int:pk>/delete/', ChoiceDeleteView.as_view(), name='choice_delete'),
    # Test tekshirish, boshlash va statistika
    path('test/check/', CheckAnswersView.as_view(), name='check_answers'),
    path('test/start/', StartTestView.as_view(), name='start_test'),
    path('test/statistics/', UserStatisticsView.as_view(), name='user_statistics'),
]
