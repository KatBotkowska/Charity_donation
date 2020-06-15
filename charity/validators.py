import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate


class SimilarOldPasswordValidator(object):
    def validate(self, password, user=None):
        if authenticate(username=user.username, password=password):
            raise ValidationError(_(self.get_help_text()), code='the_same_password')

    def get_help_text(self):
        return 'Nowe hasło musi byc różne od starego'


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _(self.get_help_text()),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Hasło musi zawierać co najmniej 1 cyfrę, 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _(self.get_help_text()),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Hasło musi zawierać co najmniej 1 wielką literę, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _(self.get_help_text()),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Hasło musi zawierać co najmniej 1 małą literę, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _(self.get_help_text()),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Hasło musi zawierać co najmniej 1 symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
