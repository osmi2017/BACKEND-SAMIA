from re import A
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.core.signals import request_finished
from django.template.loader import render_to_string
from django.urls import reverse
from quickstart.models import Notifications
import traceback


from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Modification de mot de passe {title}".format(title="pour SAMIA"),
        # message:
        email_plaintext_message,
        # from:
        "support.appinov@snedai.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


@receiver(request_finished)
def send_mail_mission(sender,**kwargs): 
       
        try:
            notification = Notifications.objects.latest('id_notifications')
            #print('''1111111111111111111111111''')
            print(notification.id_notifications)
            if notification.sent =='no':
                ##print('''1111111111111111111111111''')
                print(notification.id_notifications)
                
                context = {
                    'id': notification.id_notifications,
                    'A' : notification.A,
                    'cc': notification.cc,
                    'message':notification.message,
                    'prochaine_action':notification.prochaine_action,
                }
                email_html_message = render_to_string('email/lancement_mission.html', context)
                email_plaintext_message = render_to_string('email/lancement_mission.txt', context)

                msg = EmailMultiAlternatives(
                    # title:
                    "Lancement de mission ",
                    # message:
                    email_plaintext_message,
                    # from:
                    "support.appinov@snedai.com",
                    # to:
                    [context['A']]
                )
                msg.attach_alternative(email_html_message, "text/html")
                ##print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                msg.send()
                obj = Notifications.objects.get(pk=int(notification.id_notifications))
                
                obj.sent = "yes"
                
                obj.save()
                print("sento")
        except Exception as e:
            print('Email not sent')
            print(e)
            trace_back = traceback.format_exc()
            message = str(e)+ " " + str(trace_back)
            print(message)

