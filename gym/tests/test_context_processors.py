import pytest
from django.test import RequestFactory
from gym.context_processors import footer_content
from gym.tests.factories import ProgramFactory, TrainerFactory


@pytest.mark.django_db
class TestFooterContextProcessor:
    def test_footer_content_returns_correct_keys(self):
        """Test footer_content returns correct context keys"""
        request = RequestFactory().get('/')
        context = footer_content(request)
        
        assert 'footer_programs' in context
        assert 'footer_trainers' in context

    def test_footer_content_limits_programs(self):
        """Test footer_content returns max 4 programs"""
        # Create 6 programs
        for i in range(6):
            ProgramFactory()
        
        request = RequestFactory().get('/')
        context = footer_content(request)
        
        # Should return only 4
        assert len(context['footer_programs']) == 4

    def test_footer_content_limits_trainers(self):
        """Test footer_content returns max 4 trainers"""
        # Create 6 trainers
        for i in range(6):
            TrainerFactory()
        
        request = RequestFactory().get('/')
        context = footer_content(request)
        
        # Should return only 4
        assert len(context['footer_trainers']) == 4

    def test_footer_content_empty_data(self):
        """Test footer_content with no data"""
        request = RequestFactory().get('/')
        context = footer_content(request)
        
        assert len(context['footer_programs']) == 0
        assert len(context['footer_trainers']) == 0

    def test_footer_content_partial_data(self):
        """Test footer_content with less than 4 items"""
        # Create 2 programs and 3 trainers
        ProgramFactory()
        ProgramFactory()
        TrainerFactory()
        TrainerFactory()
        TrainerFactory()
        
        request = RequestFactory().get('/')
        context = footer_content(request)
        
        assert len(context['footer_programs']) == 2
        assert len(context['footer_trainers']) == 3