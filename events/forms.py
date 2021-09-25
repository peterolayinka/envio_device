from django import forms
from django.forms.models import BaseModelFormSet

from .models import Reading


class ReadingForm(forms.ModelForm):
    device_id = forms.UUIDField()
    customer_id = forms.UUIDField()

    class Meta:
        model = Reading
        fields = ["timestamp", "reading"]

    def clean_device_id(self, **kwargs):
        from .services import DeviceService

        if self.cleaned_data.get("device_id"):
            device_service = DeviceService()
            device = device_service.set_device(self.cleaned_data["device_id"])
            return device

    def clean_customer_id(self, **kwargs):
        from .services import DeviceService

        if self.cleaned_data.get("customer_id"):
            device_service = DeviceService()
            customer = device_service.set_customer(self.cleaned_data["customer_id"])
            return customer

    def clean(self):
        if (
            self.cleaned_data.get("device_id")
            and self.cleaned_data["device_id"].customer
            and self.cleaned_data["device_id"].customer
            != self.cleaned_data["customer_id"]
        ):
            raise forms.ValidationError(
                {
                    "device_id": "Device ID can't be shared across customers, a device can only be assigned to one customer"
                }
            )

        elif (
            self.cleaned_data.get("device_id")
            and self.cleaned_data.get("customer_id")
            and not self.cleaned_data["device_id"].customer
        ):
            self.cleaned_data["device_id"].customer = self.cleaned_data["customer_id"]
            self.cleaned_data["device_id"].save()

    def save(self, commit=True):
        instance = super(ReadingForm, self).save(commit=False)
        instance.device = self.cleaned_data.get("device_id")
        instance.customer = self.cleaned_data.get("customer_id")
        if commit:
            instance.save()
        return instance


class ReadingFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(ReadingFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


ReadingFormSetFactory = forms.modelformset_factory(
    Reading, form=ReadingForm, formset=ReadingFormSet
)


class UUIDForm(forms.Form):
    id = forms.UUIDField()
