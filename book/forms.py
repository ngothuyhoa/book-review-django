from django import forms
from .models import Review, Comment, Buy


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        review = super(ReviewForm, self).save(commit=False)
        review.book = self.book
        review.user = self.user
        review.save()

    class Meta:
        model = Review
        fields = ['description']
        labels = {
            "description": "Review"
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.review = kwargs.pop('review', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.review = self.review
        comment.user = self.user
        comment.save()

    class Meta:
        model = Comment
        fields = ['description']
        widgets = {
            'description': forms.Textarea(
            attrs={
                'rows': '4',
                'class': 'textarea form-control',
            })
        }


class BuyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        buy = super(BuyForm, self).save(commit=False)
        buy.book = self.book
        buy.user = self.user
        buy.save()

    class Meta:
        model = Buy
        fields = ['name', 'phone', 'address', 'note']
        widgets = {
            'note': forms.Textarea(
            attrs={
                'rows': '4',
                'class': 'textarea form-control',
            })
        }