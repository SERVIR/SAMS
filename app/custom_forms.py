from django import forms

ROLE_CHOICES = [
    ('SERVIR SCO', 'SERVIR SCO'),
    ('USAID', 'USAID'),
    ('Support Team', 'Support Team'),
    ('Hub Staff', 'Hub Staff'),
    ('AST team', 'AST team'),
    ('Other collaborator', 'Other collaborator'),
]


class UserRoleForm(forms.Form):
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    other_explanation = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Please explain why you are requesting access to the system',
        'rows': 3,
    }))
