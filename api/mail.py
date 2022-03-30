from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def asmr_mail(subject_, message_, recipient_):
    subject = subject_
    message = message_
    recepient = recipient_
    try:
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    except:
        print("cant send message")

def new_register_mail(user, role):
    message = "Hi " + user + ",\nYou've registered in the ASMR Online Medical COnsulation Service.\n"
    if(role == 2):
        message += "Since you've registered as a doctor, you will need to wait for your account to be activated by the admin before being allowed to use ther service to the fullest\n"

    message += "Hope you have a nice time using our service\n\n"
    message += "Thanks and regards\nASMR Team"
    return message

def doctor_accepted(user):
    message = "Hi " + user + ",\nYou've registered in the ASMR Online Medical COnsulation Service.\n"
    message += "You account has been approved by the admin, please continue to login and use the service\n"

    message += "Hope you have a nice time using our service\n\n"
    message += "Thanks and regards\nASMR Team"
    return message

def doctor_removed(user):
    message = "Hi " + user   + ",\nYou've been removed from the ASMR Online Medical COnsulation Service.\n"
    message += "You account has been deleted by the admin, please register again and contact teh amdin to login and use the service\n"

    message += "Hope you have a nice time using our service\n\n"
    message += "Thanks and regards\nASMR Team"
    return message