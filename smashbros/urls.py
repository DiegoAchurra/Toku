from django.urls import path

from clash.views import index_view, battle_simulation_view, send_battle_email_view

urlpatterns = [
    path('', index_view, name='index'),  # Simple landing page
    path('battle-simulation/', battle_simulation_view, name='battle_simulation'),  # Battle simulation page
    path('send-battle-email/', send_battle_email_view, name='send_battle_email'),  # URL for sending the email
]
