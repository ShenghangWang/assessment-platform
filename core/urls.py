from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('p/<slug:slug>/', views.landing, name='landing'),
    path('p/<slug:slug>/quiz/', views.quiz_view, name='quiz'),
    path('p/<slug:slug>/submit/', views.submit_view, name='submit'),
    path('attempt/<int:attempt_id>/result/', views.result_view, name='result'),
    path('attempt/<int:attempt_id>/paywall/', views.paywall_view, name='paywall'),
    path('attempt/<int:attempt_id>/unlock/', views.unlock_view, name='unlock'),
    path('attempt/<int:attempt_id>/report/', views.report_view, name='report'),
]
