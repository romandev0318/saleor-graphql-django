from datetime import date

from django import forms
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy

from ...cart.models import Cart
from ...core.utils import format_money
from ...core.utils.taxes import display_gross_prices
from ...discount.models import NotApplicable, Voucher
from ...shipping.models import ShippingMethodCountry
from ...shipping.utils import get_taxed_shipping_price


class AnonymousUserShippingForm(forms.ModelForm):
    """Additional shipping information form for users who are not logged in."""

    user_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'shipping email'}),
        label=pgettext_lazy('Address form field label', 'Email'))

    class Meta:
        model = Cart
        fields = ['user_email']


class AnonymousUserBillingForm(forms.ModelForm):
    """Additional billing information form for users who are not logged in."""

    user_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'billing email'}),
        label=pgettext_lazy('Address form field label', 'Email'))

    class Meta:
        model = Cart
        fields = ['user_email']


class AddressChoiceForm(forms.Form):
    """Choose one of user's addresses or to create new one."""

    NEW_ADDRESS = 'new_address'
    CHOICES = [
        (NEW_ADDRESS, pgettext_lazy(
            'Shipping addresses form choice', 'Enter a new address'))]

    address = forms.ChoiceField(
        label=pgettext_lazy('Shipping addresses form field label', 'Address'),
        choices=CHOICES, initial=NEW_ADDRESS, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        addresses = kwargs.pop('addresses')
        super().__init__(*args, **kwargs)
        address_choices = [(address.id, str(address)) for address in addresses]
        self.fields['address'].choices = self.CHOICES + address_choices


class BillingAddressChoiceForm(AddressChoiceForm):
    """Choose one of user's addresses, a shipping one or to create new."""

    NEW_ADDRESS = 'new_address'
    SHIPPING_ADDRESS = 'shipping_address'
    CHOICES = [
        (NEW_ADDRESS, pgettext_lazy(
            'Billing addresses form choice', 'Enter a new address')),
        (SHIPPING_ADDRESS, pgettext_lazy(
            'Billing addresses form choice', 'Same as shipping'))]

    address = forms.ChoiceField(
        label=pgettext_lazy('Billing addresses form field label', 'Address'),
        choices=CHOICES, initial=SHIPPING_ADDRESS, widget=forms.RadioSelect)


class ShippingCountryMethodChoiceField(forms.ModelChoiceField):
    """Shipping method country choice field.

    Uses a radio group instead of a dropdown and includes estimated shipping
    prices.
    """

    taxes = None
    widget = forms.RadioSelect()

    def label_from_instance(self, obj):
        """Return a friendly label for the shipping method."""
        price = get_taxed_shipping_price(obj.price, self.taxes)
        if display_gross_prices():
            price = price.gross
        else:
            price = price.net
        price_html = format_money(price)
        label = mark_safe('%s %s' % (obj.shipping_method, price_html))
        return label


class CartShippingMethodForm(forms.ModelForm):
    """Cart shipping method form."""

    shipping_method = ShippingCountryMethodChoiceField(
        queryset=ShippingMethodCountry.objects.select_related(
            'shipping_method').order_by('price').all(),
        label=pgettext_lazy(
            'Shipping method form field label', 'Shipping method'),
        required=True)

    class Meta:
        model = Cart
        fields = ['shipping_method']

    def __init__(self, *args, **kwargs):
        taxes = kwargs.pop('taxes')
        super().__init__(*args, **kwargs)
        method_field = self.fields['shipping_method']
        method_field.taxes = taxes

        country_code = self.instance.shipping_address.country.code
        if country_code:
            queryset = method_field.queryset
            method_field.queryset = queryset.unique_for_country_code(
                country_code)

        if self.initial.get('shipping_method') is None:
            self.initial['shipping_method'] = method_field.queryset.first()

        method_field.empty_label = None


class CartNoteForm(forms.ModelForm):
    """Save note in cart."""

    note = forms.CharField(
        max_length=250, required=False, strip=True, label=False,
        widget=forms.Textarea({'rows': 3}))

    class Meta:
        model = Cart
        fields = ['note']


class VoucherField(forms.ModelChoiceField):

    default_error_messages = {
        'invalid_choice': pgettext_lazy(
            'Voucher form error', 'Discount code incorrect or expired')}


class CartVoucherForm(forms.ModelForm):
    """Apply voucher to a cart form."""

    voucher = VoucherField(
        queryset=Voucher.objects.none(),
        to_field_name='code',
        help_text=pgettext_lazy(
            'Checkout discount form label for voucher field',
            'Gift card or discount code'),
        widget=forms.TextInput)

    class Meta:
        model = Cart
        fields = ['voucher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voucher'].queryset = Voucher.objects.active(
            date=date.today())

    def clean(self):
        from .utils import get_voucher_discount_for_cart
        cleaned_data = super().clean()
        if 'voucher' in cleaned_data:
            voucher = cleaned_data['voucher']
            try:
                discount_amount = get_voucher_discount_for_cart(
                    voucher, self.instance)
                cleaned_data['discount_amount'] = discount_amount
            except NotApplicable as e:
                self.add_error('voucher', smart_text(e))
        return cleaned_data

    def save(self, commit=True):
        voucher = self.cleaned_data['voucher']
        self.instance.voucher_code = voucher.code
        self.instance.discount_name = voucher.name
        self.instance.discount_amount = self.cleaned_data['discount_amount']
        return super().save(commit)
