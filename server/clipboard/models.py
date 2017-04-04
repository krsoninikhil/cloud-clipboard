from django.db import models

class Clip(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE,
                                  related_name='clips')
    text = models.TextField()
    device = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ('created_at',)

