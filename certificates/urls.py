from django.urls import path
from .views import (
    CertSubjectListView, CertSubjectDetailView, CertSubjectCreateView,
    CertSubjectUpdateView, CertSubjectDeleteView,
    CertQuestionListView, CertQuestionDetailView, CertQuestionDetailAdminView,
    CertQuestionCreateView, CertQuestionUpdateView, CertQuestionDeleteView,
    CertChoiceListView, CertChoiceCreateView, CertChoiceUpdateView, CertChoiceDeleteView,
    CertStartTestView, CertCheckAnswersView, CertUserStatisticsView,
)

app_name = 'certificates'

urlpatterns = [
    # Fanlar
    path('cert/subjects/', CertSubjectListView.as_view(), name='cert_subject_list'),
    path('cert/subjects/create/', CertSubjectCreateView.as_view(), name='cert_subject_create'),
    path('cert/subjects/<int:pk>/', CertSubjectDetailView.as_view(), name='cert_subject_detail'),
    path('cert/subjects/<int:pk>/update/', CertSubjectUpdateView.as_view(), name='cert_subject_update'),
    path('cert/subjects/<int:pk>/delete/', CertSubjectDeleteView.as_view(), name='cert_subject_delete'),

    # Savollar
    path('cert/questions/', CertQuestionListView.as_view(), name='cert_question_list'),
    path('cert/questions/create/', CertQuestionCreateView.as_view(), name='cert_question_create'),
    path('cert/questions/<int:pk>/', CertQuestionDetailView.as_view(), name='cert_question_detail'),
    path('cert/questions/<int:pk>/admin/', CertQuestionDetailAdminView.as_view(), name='cert_question_detail_admin'),
    path('cert/questions/<int:pk>/update/', CertQuestionUpdateView.as_view(), name='cert_question_update'),
    path('cert/questions/<int:pk>/delete/', CertQuestionDeleteView.as_view(), name='cert_question_delete'),

    # Variantlar
    path('cert/choices/', CertChoiceListView.as_view(), name='cert_choice_list'),
    path('cert/choices/create/', CertChoiceCreateView.as_view(), name='cert_choice_create'),
    path('cert/choices/<int:pk>/update/', CertChoiceUpdateView.as_view(), name='cert_choice_update'),
    path('cert/choices/<int:pk>/delete/', CertChoiceDeleteView.as_view(), name='cert_choice_delete'),

    # Test boshlash, tekshirish va statistika
    path('cert/test/start/', CertStartTestView.as_view(), name='cert_start_test'),
    path('cert/test/check/', CertCheckAnswersView.as_view(), name='cert_check_answers'),
    path('cert/test/statistics/', CertUserStatisticsView.as_view(), name='cert_user_statistics'),
]
