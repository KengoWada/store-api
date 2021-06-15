from cerberus import Validator
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class CustomValidator(Validator):

    def _validate_is_url(self, is_url, field, value):
        """
        Test if a value follows the email regex given.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        validate = URLValidator()
        try:
            validate(value)
        except ValidationError:
            self._error(field, 'Invalid URL')


def validate_create_product(data):
    schema = {
        'name': {'type': 'string', 'maxlength': 255, 'required': True},
        'description': {'type': 'string', 'required': True},
        'price': {'type': 'integer', 'required': True},
        'quantity': {'type': 'integer', 'required': True},
        'images': {
            'type': 'list',
            'empty': False,
            'required': True,
            'maxlength': 5,
            'schema': {'type': 'string', 'is_url': True, 'required': True}
        },
    }

    v = CustomValidator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}


def validate_update_product(data):
    schema = {
        'name': {'type': 'string', 'maxlength': 255, 'required': False},
        'description': {'type': 'string', 'required': False},
        'price': {'type': 'integer', 'required': False},
        'images': {
            'type': 'list',
            'empty': False,
            'required': False,
            'maxlength': 5,
            'schema': {'type': 'string', 'is_url': True, 'required': True}
        },
    }

    v = CustomValidator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}


def validate_patch_product(data):
    schema = {
        'discount_product': {
            'type': 'dict',
            'schema': {
                'discount_price': {'type': 'integer', 'required': True},
            },
            'required': True,
            'excludes': ['remove_product_discount', 'add_product_stock', 'remove_product_stock'],
        },
        'remove_product_discount': {
            'type': 'string',
            'empty': True,
            'required': True,
            'excludes': ['discount_product', 'add_product_stock', 'remove_product_stock'],
        },
        'add_product_stock': {
            'type': 'dict',
            'schema': {
                'increment_by': {'type': 'integer', 'min': 1, 'required': True}
            },
            'required': True,
            'excludes': ['discount_product', 'remove_product_discount', 'remove_product_stock'],
        },
        'remove_product_stock': {
            'type': 'dict',
            'schema': {
                'decrement_by': {'type': 'integer', 'min': 1, 'required': True}
            },
            'required': True,
            'excludes': ['discount_product', 'remove_product_discount', 'add_product_stock'],
        },
    }

    v = Validator(schema)
    v.validate(data)

    if v.errors:
        return {'is_valid': False, 'errors': v.errors}

    return {'is_valid': True}
