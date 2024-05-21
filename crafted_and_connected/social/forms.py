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
        self.fields['category'].choices = Post.CATEGORY_CHOICES
        self.fields['subcategory'].choices = []

        if 'category' in self.data:
            try:
                category = self.data.get('category')
                self.fields['subcategory'].choices = Post.SUBCATEGORY_CHOICES.get(category, [])
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            category = self.instance.category
            self.fields['subcategory'].choices = Post.SUBCATEGORY_CHOICES.get(category, [])


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Добави коментар...'})
        }
