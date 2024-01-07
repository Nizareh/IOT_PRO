from django.core.mail import send_mail
from django.db import models

# Create your models here.
from django.db import models
class Dht11(models.Model):
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.temp)

    def save(self, *args, **kwargs):
        try:
            if self.temp is not None and self.temp > 40:
                from DHT.views import sendtele
                sendtele()
                send_mail(
                    "température dépasse la normale," + str(self.temp),
                    "anomalie dans la machine le," + str(self.dt),
                    "nizarnejjari220@gmail.com",
                    ["saadlcf1999@gmail.com"],
                    fail_silently=False,
                )

            return super().save(*args, **kwargs)

        except Exception as e:
            import logging
            logging.error(f"An error occurred in save method: {e}")

            
class Member(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    country=models.CharField(max_length=100)






        


