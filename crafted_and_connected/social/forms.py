
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'price', 'delivery_time', 'category', 'subcategory', 'photos']

    category = forms.ChoiceField(choices=Post.CATEGORY_CHOICES, required=True)
    subcategory = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # Set the initial choices for category and subcategory
        self.fields['category'].choices = [('', 'Избери категория')] + list(Post.CATEGORY_CHOICES)
        self.fields['subcategory'].choices = [('', 'Избери подкатегория')]

        # Set labels for fields
        self.fields['category'].label = 'Категория'
        self.fields['subcategory'].label = 'Подкатегория'
        self.fields['title'].label = "Заглавие:"
        self.fields['description'].label = "Описание:"
        self.fields['price'].label = "Цена:"
        self.fields['delivery_time'].label = "Време за доставка(дни)"
        self.fields['photos'].label = "Качване на снимка:"

        # Set choices for subcategory based on the selected category or instance category
        if 'category' in self.data:
            category = self.data.get('category')
            self.fields['subcategory'].choices = ([('', 'Избери подкатегория')]
                                                  + list(Post.SUBCATEGORY_CHOICES.get(category, [])))
        elif self.instance.pk:
            category = self.instance.category
            self.fields['subcategory'].choices = ([('', 'Избери подкатегория')]
                                                  + list(Post.SUBCATEGORY_CHOICES.get(category, [])))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Добави коментар...'}, )
        }
