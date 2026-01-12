from django import forms

from accounts.services import get_construction_manager_queryset

from .models import Construction, ContractForWork, Order


class ConstructionForm(forms.ModelForm):
    class Meta:
        model = Construction
        fields = ["name", "location"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["construction", "name", "managers"]
        widgets = {"managers": forms.CheckboxSelectMultiple}

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields["construction"].queryset = Construction.objects.filter(organization=organization)
            self.fields["managers"].queryset = get_construction_manager_queryset(organization)


class ContractForWorkForm(forms.ModelForm):
    class Meta:
        model = ContractForWork
        fields = [
            "contract_number",
            "contractor_share",
            "contract_signed",
            "day_after_due",
            "start_contract",
            "end_contract",
            "is_social_house",
            "tax_reverse_charge",
            "warranty_period",
        ]
        widgets = {
            "contract_signed": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "start_contract": forms.DateInput(attrs={"type": "date"}),
            "end_contract": forms.DateInput(attrs={"type": "date"}),
        }
