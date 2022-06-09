from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.ProcedureView.as_view(), name="homepage"),
    path('register/', SignUpView, name="register"),
    path("question/<int:pk>/", views.AddQuestion.as_view(), name="add_question"),
    path("tag/<slug:slug>", views.TagView.as_view(), name="tag_detail"),
    path("<slug:slug>/", views.ProcedureDetailView.as_view(), name="procedure_detail"),


]
