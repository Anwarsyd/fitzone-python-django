from .models import Program, Trainer

def footer_content(request):
    programs = Program.objects.all()[:4]
    trainers = Trainer.objects.all()[:4]
    context = {
        'footer_programs': programs,
        'footer_trainers': trainers
    }
    return context