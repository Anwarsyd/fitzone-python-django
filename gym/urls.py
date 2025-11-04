from django.urls import path
from . import views
app_name = "gym"
urlpatterns = [
    path('',views.HomeView.as_view(),name = 'index'),
    path('programs/',views.ProgramListView.as_view(),name='programs'),
    path('programs/<int:pk>/',views.ProgramDetailsView.as_view(),name='program_details'),
    path('faqs/',views.FaqsView.as_view(),name="faqs")
]
