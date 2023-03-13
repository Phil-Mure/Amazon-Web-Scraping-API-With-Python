from django.db import models

class ReactUrl(models.Model):
    url = models.URLField(max_length=25500, default='https://www.amazon.com/Lenovo-Chromebook-11-6-Inch-Processor-82HG0006US/dp/B08T6N')