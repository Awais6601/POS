from django import forms
from .models import Medicine,Order,Transaction
from datetime import date

class MedicineForm(forms.ModelForm):
    # Fields for the Medicine model
    manufacture_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, date.today().year + 1))
    )
    expiry_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(date.today().year, date.today().year + 20))
    )
    purchasing_date = forms.DateField(
        initial=date.today,
        widget=forms.SelectDateWidget(years=range(1900, date.today().year + 1))
    )

    class Meta:
        model = Medicine
        fields = ['Product_name', 'purchasing_date', 'manufacture_date', 'expiry_date', 'Product_price', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'product', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data['product']

        if quantity > product.quantity:
            raise forms.ValidationError(f"Available quantity is only {product.quantity}.")
        
        return quantity
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['income', 'expense']

    def clean(self):
        cleaned_data = super().clean()
        income = cleaned_data.get('income')
        expense = cleaned_data.get('expense')

        # Ensure at least one of income or expense is entered
        if not income and not expense:
            raise forms.ValidationError('You must enter either income or expense.')
        return cleaned_data