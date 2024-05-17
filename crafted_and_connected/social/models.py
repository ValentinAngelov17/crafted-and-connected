from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.IntegerField(help_text="Delivery time in days")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @staticmethod
    def create_predefined_categories():
        categories = {
            'Изделия от хартия': ['Картички', 'Декорации', 'Квилинг', 'Други'],
            'Изделия от восък': ['Свещи'],
            'Изделия от дърво': ['Декорации', 'Маси и столове', 'Рамки', 'Други'],
            'Керамични изделия': ['Чаши', 'Чинии', 'Декорации', 'Други'],
            'Гоблени': ['Готови', 'Схеми', 'Щампирани'],
            'Картини': ['Портретна живопис', 'Пейзажна живопис', 'Натюрморт', 'Абстрактна живопис',
                        'Исторически живопис', 'Религиозна живопис', 'Алегория'],
            'Бижута': ['Обеци', 'Колиета', 'Гривни'],
            'Плетива': ['Дрехи', 'Играчки', 'Аксесоари', 'Декорации', 'Други'],
            'Други': []
        }

        for category_name, subcategory_names in categories.items():
            category, created = Category.objects.get_or_create(name=category_name)
            for subcategory_name in subcategory_names:
                Subcategory.objects.create(name=subcategory_name, category=category)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    # Other fields...

    def __str__(self):
        return f'Comment by {self.user} on {self.post.title}'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    # Other fields...

    def __str__(self):
        return f'Like by {self.user} on {self.post.title}'
