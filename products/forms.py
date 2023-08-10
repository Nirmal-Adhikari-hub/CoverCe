from django import forms
from .models import Product, ProductAttachment
from django.forms import inlineformset_factory, modelformset_factory


input_css_class = "form-control"
# input_css_class = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class ProductForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":
    #                                                      "from-control"}))
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductUpdateForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":
    #                                                      "from-control"}))
    class Meta:
        model = Product
        fields = ['image', 'name', 'handle', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductAttachmentForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={"class":
    #                                                      "from-control"}))
    class Meta:
        model = ProductAttachment
        fields = ['file', 'name', 'is_free', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class            


ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    fields=['file', 'name', 'is_free', 'active'],
    extra = 0,
    can_delete=True
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    formset=ProductAttachmentModelFormSet,
    fields=['file', 'name', 'is_free', 'active'],
    extra = 0,
    can_delete=True
)