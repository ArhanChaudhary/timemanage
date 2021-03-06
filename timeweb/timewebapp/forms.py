from django import forms
from .models import TimewebModel, SettingsModel
from django.utils.translation import ugettext_lazy as _
from colorfield.widgets import ColorWidget
class DateInput(forms.DateInput):
    input_type = 'date'

class TimewebForm(forms.ModelForm):
    class Meta:
        model = TimewebModel
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "Ex: Reading book, English essay, Math homework"}),
            'assignment_date': DateInput(),
            'x': DateInput(),
            'blue_line_start': forms.HiddenInput(),
            'skew_ratio': forms.HiddenInput(),
            'fixed_mode': forms.HiddenInput(),
            'dynamic_start': forms.HiddenInput(),
            'mark_as_done': forms.HiddenInput(),
            'needs_more_info': forms.HiddenInput(),
            'tags': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'unit': forms.TextInput(attrs={"placeholder": "Ex: Chapter, Paragraph, Question"}),
            'works': forms.NumberInput(attrs={"min":"0","step":"0.01"}),
            'y': forms.NumberInput(attrs={"min":"1"}),
            'ctime': forms.NumberInput(attrs={"min":"0"}),
            'description': forms.Textarea(attrs={"rows": "1"}),
            'funct_round': forms.NumberInput(attrs={"min":"0"}),
            'min_work_time': forms.NumberInput(attrs={"min":"0"}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter an assignment name"),
                'max_length': _("This assignment's name is too long (>%(n)d characters)") % {"n": TimewebModel.name.field.max_length},
                'invalid': _("This assignment's name is invalid"),
            },
            'assignment_date': {
                'required': _('Please enter an assignment date'),
                'invalid': _('The assignment date is out of range or invalid'),
            },
            'x': {
                'invalid': _('The due date is out of range or invalid'),
            },
            'unit': {
                'required': _("Please enter a name"),
                'max_length': _("This field's name is too long (>%(n)d characters)") % {"n": TimewebModel.unit.field.max_length},
                'invalid': _("This field's value is invalid"),
            },
            'y': {
                'required': _("Please enter a value"),
                'max_digits': _("This field can only have %(n)d digits before and %(n2)d digits after its decimal point") % {"n": TimewebModel.y.field.max_digits - TimewebModel.y.field.decimal_places, "n2": TimewebModel.y.field.decimal_places},
                'max_decimal_places': _("This field's value has too many decimal places (>%(n)d decimal places)") % {"n": TimewebModel.y.field.decimal_places},
                'max_whole_digits': _("This field's value has too many digits before its decimal point (>%(n)d digits)")% {"n": TimewebModel.y.field.max_digits - TimewebModel.y.field.decimal_places},
            },
            'works': {
                'required': _("Please enter a value"),
                'invalid': _("This field's value is invalid"),
            },
            'ctime': {
                'required': _("Please enter a value"),
                'max_digits': _("This field's value is too long (>%(n)d digits)") % {"n": TimewebModel.ctime.field.max_digits},
                'max_decimal_places': _("This field's value has too many decimal places (>%(n)d decimal places)") % {"n": TimewebModel.ctime.field.decimal_places},
                'max_whole_digits': _("This field's value has too many digits before its decimal point (>%(n)d digits)") % {"n": TimewebModel.ctime.field.max_digits - TimewebModel.ctime.field.decimal_places},
                'invalid': _("This field's value is invalid"),
            },
            'funct_round': {
                'max_digits': _("This field can only have %(n)d digits before and %(n2)d digits after its decimal point") % {"n": TimewebModel.funct_round.field.max_digits - TimewebModel.funct_round.field.decimal_places, "n2": TimewebModel.funct_round.field.decimal_places},
                'max_decimal_places': _("This field's value has too many digits after its decimal point (>%(n)d digits)") % {"n": TimewebModel.funct_round.field.decimal_places},
                'max_whole_digits': _("This field's value has too many digits before its decimal point (>%(n)d digits)") % {"n": TimewebModel.funct_round.field.max_digits - TimewebModel.funct_round.field.decimal_places},
                'invalid': _("This field's value is invalid"),
            },
            'min_work_time': {
                'max_digits': _("This field can only have %(n)d digits before and %(n2)d digits after its decimal point") % {"n": TimewebModel.min_work_time.field.max_digits - TimewebModel.min_work_time.field.decimal_places, "n2": TimewebModel.min_work_time.field.decimal_places},
                'max_decimal_places': _("The minimum work time has too many decimal places (>%(n)d decimal places)") % {"n": TimewebModel.min_work_time.field.decimal_places},
                'max_whole_digits': _("The minimum work time has too many digits before its decimal point (>%(n)d digits)") % {"n": TimewebModel.min_work_time.field.max_digits - TimewebModel.min_work_time.field.decimal_places},
                'invalid': _("The minimum work time is invalid"),
            },
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    def clean(self):
        cleaned_data = super().clean()
        x = cleaned_data.get("x")
        assignment_date = cleaned_data.get("assignment_date")
        works = cleaned_data.get("works")
        y = cleaned_data.get("y")
        try:
            if works >= y >= 1:
                self.add_error("works",
                    forms.ValidationError(_("This field's value of %(value)g cannot be %(equal_to_or_greater_than)s the above field's value of %(y)g"),code='invalid',params={
                        'value': works,
                        'y': y,
                        'equal_to_or_greater_than': "equal to" if works == y else "greater than",
                    })
                )
        except:
            pass
        try:
            if x <= assignment_date:
                self.add_error("x",
                    forms.ValidationError(_("The due date cannot be %(on_or_before)s the assignment date"),code='invalid',params={
                        'on_or_before': "on" if x == assignment_date else "before",
                    })
                )
        except:
            pass
        return cleaned_data

class SettingsForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        fields = "__all__"
        widgets = {
            "user": forms.HiddenInput(),
            'def_min_work_time': forms.NumberInput(attrs={"min":"0"}),
            'warning_acceptance': forms.NumberInput(attrs={"min":"1","max":"100"}),
            'date_now': forms.HiddenInput(),
            'oauth_token': forms.HiddenInput(),
            'highest_priority_color': ColorWidget,
            'lowest_priority_color': ColorWidget,
            'def_skew_ratio': forms.NumberInput(attrs={"step":"0.1"}),
            'added_gc_assignment_ids': forms.HiddenInput(),
        }
        error_messages = {
            'def_min_work_time': {
                'max_digits': _("This field can only have %(n)d digits before and %(n2)d digits after its decimal point") % {"n": SettingsModel.def_min_work_time.field.max_digits - SettingsModel.def_min_work_time.field.decimal_places, "n2": SettingsModel.def_min_work_time.field.decimal_places},
                'max_decimal_places': _("The default minimum work time has too many decimal places (>%(n)d decimal places)") % {"n": SettingsModel.def_min_work_time.field.decimal_places},
                'max_whole_digits': _("The default minimum work time has too many digits before its decimal point (>%(n)d digits)") % {"n": SettingsModel.def_min_work_time.field.max_digits - SettingsModel.def_min_work_time.field.decimal_places},
                'invalid': _("The default minimum work time is invalid"),
            },
            'def_skew_ratio': {
                'max_digits': _("The default skew ratio can only have %(n)d digits before and %(n2)d digits after its decimal point") % {"n": SettingsModel.def_skew_ratio.field.max_digits - SettingsModel.def_skew_ratio.field.decimal_places, "n2": SettingsModel.def_skew_ratio.field.decimal_places},
                'max_decimal_places': _("The default skew ratio has too many decimal places (>%(n)d decimal places)") % {"n": SettingsModel.def_skew_ratio.field.decimal_places},
                'max_whole_digits': _("The default skew ratio has too many digits before its decimal point (>%(n)d digits)") % {"n": SettingsModel.def_skew_ratio.field.max_digits - SettingsModel.def_skew_ratio.field.decimal_places},
                'invalid': _("The default skew ratio is invalid"),
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""