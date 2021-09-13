from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm
from mainapp.models import ProductCategory, Product


class ShopUserRegisterForm(ShopUserEditForm):  # Наследуемся от ShopUserEditFor

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'is_active', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_staff'].widget.attrs.update({'class': 'form-check-input'})


class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='Скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ()  # кортеж с исключенными из отображения полями

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})


class ProductEditForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
