from django.core.exceptions import ImproperlyConfigured

try:
    from captcha.fields import ReCaptchaField as CaptchaField
except ImportError:
    try:
        from captcha.fields import CaptchaField
    except ImportError:
        raise ImportError(
            "To use the captcha contact form, you need to have "
            "django-recaptcha or django-simple-captcha installed."
        )


class CaptchaFormMixin(object):
    def _reorder_fields(self, ordering):
        """
        Test that the 'captcha' field is really present.
        This could be broken by a bad FLUENT_COMMENTS_FIELD_ORDER configuration.
        """
        if 'captcha' not in ordering:
            raise ImproperlyConfigured(
                "When using 'FLUENT_COMMENTS_FIELD_ORDER', "
                "make sure the 'captcha' field included too to use '{}' form. ".format(
                    self.__class__.__name__
                )
            )
        super(CaptchaFormMixin, self)._reorder_fields(ordering)

        # Avoid making captcha required for previews.
        if self.is_preview:
            self.fields.pop('captcha')
