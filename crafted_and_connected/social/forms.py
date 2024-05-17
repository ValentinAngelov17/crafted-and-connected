from django import forms
from .models import Post, Subcategory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'price', 'delivery_time', 'category', 'subcategory', 'photos']
        widgets = {
            'subcategory': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['price'].required = True
        self.fields['delivery_time'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True
        self.fields['photos'].required = True

        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')
