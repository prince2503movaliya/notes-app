
from django.urls import path
from .views import note_list, note_detail, note_create, note_update, note_delete, toggle_pin

urlpatterns = [
    path('', note_list, name='note_list'),
    path('note/<int:id>/', note_detail, name='note_detail'),
    path('create/', note_create, name='note_create'),
    path('edit/<int:id>/', note_update, name='note_update'),
    path('delete/<int:id>/', note_delete, name='note_delete'),
    path('pin/<int:id>/', toggle_pin, name='note_pin'),
]
