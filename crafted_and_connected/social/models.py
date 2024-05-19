from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

# Define your choices for categories and subcategories
CATEGORY_CHOICES = [
    ('paper', 'Изделия от хартия'),
    ('wax', 'Изделия от восък'),
    ('wood', 'Изделия от дърво'),
    ('ceramic', 'Керамични изделия'),
    ('tapestry', 'Гоблени'),
    ('painting', 'Картини'),
    ('jewelry', 'Бижута'),
    ('knit', 'Плетива'),
    ('other', 'Други'),
]

SUBCATEGORY_CHOICES = {
    'paper': [
        ('cards', 'Картички'),
        ('decorations', 'Декорации'),
        ('quilling', 'Квилинг'),
        ('other', 'Други'),
    ],
    'wax': [
        ('candles', 'Свещи'),
        ('other', 'Други'),
    ],
    'wood': [
        ('decorations', 'Декорации'),
        ('tables_and_chairs', 'Маси и столове'),
        ('frames', 'Рамки'),
        ('other', 'Други'),
    ],
    'ceramic': [
        ('cups', 'Чаши'),
        ('plates', 'Чинии'),
        ('decorations', 'Декорации'),
        ('other', 'Други'),
    ],
    'tapestry': [
        ('finished', 'Готови'),
        ('patterns', 'Схеми'),
        ('stamped', 'Щампирани'),
        ('other', 'Други'),
    ],
    'painting': [
        ('portrait', 'Портретна живопис'),
        ('landscape', 'Пейзажна живопис'),
        ('still_life', 'Натюрморт'),
        ('abstract', 'Абстрактна живопис'),
        ('historical', 'Исторически живопис'),
        ('religious', 'Религиозна живопис'),
        ('allegory', 'Алегория'),
        ('other', 'Други'),
    ],
    'jewelry': [
        ('earrings', 'Обеци'),
        ('necklaces', 'Колиета'),
        ('bracelets', 'Гривни'),
        ('other', 'Други'),
    ],
    'knit': [
        ('clothes', 'Дрехи'),
        ('toys', 'Играчки'),
        ('accessories', 'Аксесоари'),
        ('decorations', 'Декорации'),
        ('other', 'Други'),
    ],
    'other': [
        ('other', 'Други'),
    ]
}


class Post(models.Model):
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
        if self.category not in SUBCATEGORY_CHOICES or \
                self.subcategory not in dict(SUBCATEGORY_CHOICES[self.category]).keys():
            raise ValueError('Invalid subcategory for the selected category.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    # Other fields...

    def __str__(self):
        return f'Comment by {self.user} on {self.post.title}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)

    # Other fields...

    def __str__(self):
        return f'Like by {self.user} on {self.post.title}'
