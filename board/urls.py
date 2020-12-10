from django.urls import path
from .views import *

app_name='board'

urlpatterns = [
    path('', BoardListView.as_view(), name='list'),
    path('grid/', board_grid, name='grid'),
    path('add/', BoardCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', BoardDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BoardUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BoardDeleteView.as_view(), name='delete'),
]
