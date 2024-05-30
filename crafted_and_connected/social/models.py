from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings


# Define your choices for categories and subcategories


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('paper', _('Изделия от хартия')),
        ('wax', _('Изделия от восък')),
        ('wood', _('Изделия от дърво')),
        ('ceramics', _('Керамични изделия')),
        ('tapestry', _('Гоблени')),
        ('paintings', _('Картини')),
        ('jewelry', _('Бижута')),
        ('knitting', _('Плетива')),
        ('other', _('Други')),
    ]

    SUBCATEGORY_CHOICES = {
        'paper': [
            ('cards', _('Картички')),
            ('decorations', _('Декорации')),
            ('quilling', _('Квилинг')),
            ('other', _('Други')),
        ],
        'wax': [
            ('candles', _('Свещи')),
            ('other', _('Други')),
        ],
        'wood': [
            ('decorations', _('Декорации')),
            ('tables_and_chairs', _('Маси и столове')),
            ('frames', _('Рамки')),
            ('other', _('Други')),
        ],
        'ceramics': [
            ('cups', _('Чаши')),
            ('plates', _('Чинии')),
            ('decorations', _('Декорации')),
            ('other', _('Други')),
        ],
        'tapestry': [
            ('finished', _('Готови')),
            ('patterns', _('Схеми')),
            ('stamped', _('Щампирани')),
            ('other', _('Други')),
        ],
        'paintings': [
            ('portrait', _('Портретна живопис')),
            ('landscape', _('Пейзажна живопис')),
            ('still_life', _('Натюрморт')),
            ('abstract', _('Абстрактна живопис')),
            ('historical', _('Исторически живопис')),
            ('religious', _('Религиозна живопис')),
            ('allegory', _('Алегория')),
            ('other', _('Други')),
        ],
        'jewelry': [
            ('earrings', _('Обеци')),
            ('necklaces', _('Колиета')),
            ('bracelets', _('Гривни')),
            ('other', _('Други')),
        ],
        'knitting': [
            ('clothes', _('Дрехи')),
            ('toys', _('Играчки')),
            ('accessories', _('Аксесоари')),
            ('decorations', _('Декорации')),
            ('other', _('Други')),
        ],
        'other': []
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField()  # Number of days
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50)
    photos = models.ImageField(upload_to='post_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def save(self, *args, **kwargs):
        if self.category not in self.SUBCATEGORY_CHOICES or \
                self.subcategory not in dict(self.SUBCATEGORY_CHOICES[self.category]).keys():
            raise ValueError('Invalid subcategory for the selected category.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category)

    def get_subcategory_display(self):
        subcategories = dict(self.SUBCATEGORY_CHOICES.get(self.category, []))
        return subcategories.get(self.subcategory)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Other fields...

    def __str__(self):
        return f'Comment by {self.user} on {self.post.title}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)

    # Other fields...

    def __str__(self):
        return f'Like by {self.user} on {self.post.title}'
