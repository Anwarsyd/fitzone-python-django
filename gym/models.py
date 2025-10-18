from django.db import models

# Create your models here.
class Slider(models.Model):
    caption = models.CharField(max_length=50)
    slogan = models.CharField(max_length=120)
    image = models.ImageField(upload_to='sliders/')
    
    def __str__(self):
        return self.caption[:20]
    
    class Meta:
        verbose_name_plural = 'Sliders'
        
class Program(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    features = models.ManyToManyField('Feature',blank=True)
    thumbnail = models.ImageField(upload_to='programs/')
    cover = models.ImageField(upload_to='programs/')
    image1 = models.ImageField(upload_to='programs/', blank = True , null = True)
    image2 = models.ImageField(upload_to='programs/', blank = True , null = True)
    duration = models.CharField(max_length=50, help_text="e.g., 3 months, 6 weeks")
    price = models.DecimalField(max_digits=8, decimal_places=2, null = True,blank = True)
    
    def __str__(self):
        return self.title
    
class Feature(models.Model):
    title = models.CharField(max_length=120)
    
    def __str__(self):
        return self.title
    
class Specialization(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Specializations'

class Trainer(models.Model):
    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="trainers/")
    bio = models.TextField(help_text="Trainer biography")
    experience = models.TextField(help_text="Years and type of experience")
    certifications = models.ManyToManyField('Specialization', related_name='trainers')
    twitter = models.CharField(max_length=120,blank = True,null = True)
    facebook = models.CharField(max_length=120,blank = True,null = True)
    instagram = models.CharField(max_length=120,blank = True,null = True)
    
    def __str__(self):
        return self.name
    
class Faq(models.Model):
    question = models.CharField(max_length=120)
    answer = models.TextField()
    
    def __str__(self):
        return self.question
    
class Gallery(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/")
    category = models.CharField(max_length=50, choices=[
        ('gym', 'Gym Equipment'),
        ('classes', 'Classes'),
        ('facility', 'Facility'),
        ('events', 'Events'),
    ], default='facility')
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    program = models.CharField(max_length=120)
    testimonial = models.TextField()
    image = models.ImageField(upload_to="testimonials/")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    
    def __str__(self):
        return f"{self.name} - {self.program}"
    
