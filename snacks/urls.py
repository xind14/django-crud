from django.urls import path
from .views import SnackListView, SnackDetailView, AboutPageView, SnackCreateView, SnackDeleteView, SnackUpdateView

urlpatterns = [
  path('', SnackListView.as_view(), name='snack_list'),
  path('about/', AboutPageView.as_view(), name='about'),
  path('<int:pk>/', SnackDetailView.as_view(), name='snack_detail'),
  path('<int:pk>/update/', SnackUpdateView.as_view(), name='snack_update'),
  path('create/', SnackCreateView.as_view(), name='snack_create'),
  path('<int:pk>/delete/', SnackDeleteView.as_view(), name='snack_delete'),
]

