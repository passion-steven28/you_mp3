from django import forms

class YouTubeURLForm(forms.Form):
    url = forms.URLField(
        label='YouTube URL',
        widget=forms.URLInput(
            attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }
        )
    )