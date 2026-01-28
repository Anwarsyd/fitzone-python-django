import pytest
from django.urls import reverse, resolve
from gym import views


class TestGymURLs:
    """Test URL patterns for gym app"""

    def test_home_url(self):
        """Test home URL resolves correctly"""
        url = reverse('gym:index')
        assert url == '/'
        assert resolve(url).func.view_class == views.HomeView

    def test_programs_url(self):
        """Test programs list URL resolves correctly"""
        url = reverse('gym:programs')
        assert url == '/programs/'
        assert resolve(url).func.view_class == views.ProgramListView

    def test_program_details_url(self):
        """Test program details URL resolves correctly"""
        url = reverse('gym:program_details', kwargs={'pk': 1})
        assert url == '/programs/1/'
        assert resolve(url).func.view_class == views.ProgramDetailsView

    def test_faqs_url(self):
        """Test FAQs URL resolves correctly"""
        url = reverse('gym:faqs')
        assert url == '/faqs/'
        assert resolve(url).func.view_class == views.FaqsView

    def test_trainers_url(self):
        """Test trainers list URL resolves correctly"""
        url = reverse('gym:trainers')
        assert url == '/trainers/'
        assert resolve(url).func.view_class == views.TrainersView

    def test_trainer_details_url(self):
        """Test trainer details URL resolves correctly"""
        url = reverse('gym:trainer_details', kwargs={'pk': 1})
        assert url == '/trainers/1/'
        assert resolve(url).func.view_class == views.TrainerDetailsView

    def test_gallery_url(self):
        """Test gallery URL resolves correctly"""
        url = reverse('gym:gallery')
        assert url == '/gallery/'
        assert resolve(url).func.view_class == views.GalleryListView

    def test_contact_url(self):
        """Test contact URL resolves correctly"""
        url = reverse('gym:contact')
        assert url == '/contact/'
        assert resolve(url).func.view_class == views.ContactView