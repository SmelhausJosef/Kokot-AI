from django import forms

from .models import Budget
from construction.models import Order


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["order", "name", "excel_file"]

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields["order"].queryset = Order.objects.filter(
                construction__organization=organization
            )
