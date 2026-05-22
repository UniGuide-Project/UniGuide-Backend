from django.urls import path
from .views import (
    UniversityListView,
    UniversityPaginatedListView,
    UniversityDetailView,
    UniversityCreateView,
    UniversityUpdateView,
    UniversityDeleteView,
    FacultyListView,
    FacultyDetailView,
    FacultyCreateView,
    FacultyUpdateView,
    FacultyDeleteView,
)

app_name = 'universities'

urlpatterns = [
    # --- Universitetlar ---
    path('universities/', UniversityListView.as_view(), name='university_list'),
    path('universities/paginated/', UniversityPaginatedListView.as_view(), name='university_list_paginated'),
    path('universities/create/', UniversityCreateView.as_view(), name='university_create'),
    path('universities/<int:pk>/', UniversityDetailView.as_view(), name='university_detail'),
    path('universities/<int:pk>/update/', UniversityUpdateView.as_view(), name='university_update'),
    path('universities/<int:pk>/delete/', UniversityDeleteView.as_view(), name='university_delete'),

    # --- Fakultetlar ---
    path('faculties/', FacultyListView.as_view(), name='faculty_list'),
    path('faculties/create/', FacultyCreateView.as_view(), name='faculty_create'),
    path('faculties/<int:pk>/', FacultyDetailView.as_view(), name='faculty_detail'),
    path('faculties/<int:pk>/update/', FacultyUpdateView.as_view(), name='faculty_update'),
    path('faculties/<int:pk>/delete/', FacultyDeleteView.as_view(), name='faculty_delete'),
]
