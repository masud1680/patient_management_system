from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


# when  registration from created it's send a vierfation email for token

@receiver(post_save, sender=User)
def send_verify_email(sender, instance, created, **kwargs):
    
    if created:
        
        token = default_token_generator.make_token(instance)
        activation_url = f'{settings.FONTEND_URL}/activate/{instance.id}/{token}/'
        
        subject = "Active Your Account."
        message = f"Hi, {instance.first_name} {instance.last_name}. \n\n Please active your account by clicking this link : \n {activation_url} \n\n Thank You."
        recipient_list = [instance.email]
        
        
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send {instance.email} : {str(e)}")
        
        
@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        
        user_group , created = Group.objects.get_or_create(name='patient')
        instance.groups.add(user_group)   
        instance.save()   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        