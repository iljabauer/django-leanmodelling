from natspec_utils.decorators import TextSyntax
from django_lean_modelling.model import Wizard, Step, ModelForm, FormField



class WizardSupport(object):
    
    def __init__(self):
        self.wizard = None
    
    @TextSyntax("#1", types=["list<str>", "Property"])
    def comment_definition(self, comment_words, p):
        comment = " ".join(comment_words)
        p.comment = comment
    
    @TextSyntax("#1 wizard:", types=["list<str>"], return_type="Wizard")
    def create_wizard(self, title_words):
        name = "".join(title_words)
        wizard = Wizard(name)
        self.wizard = wizard
        return wizard
    
    @TextSyntax("Step #1:", types=["int", "Wizard"], return_type="Step")
    def step_definition(self, number, wizard):
        step = Step(number)
        wizard.steps.append(step)
        return step
    
    @TextSyntax("Form based on #1 model:", types=["list<str>", "Step"], return_type="ModelForm")
    def modelform_definition(self, model_name_words, step):
        name = "".join(model_name_words)
        model_form = ModelForm(name)
        step.form = model_form
        return model_form
    
    @TextSyntax("Form:", types=["Step"], return_type="ModelForm")
    def form_definition(self, step):
        model_form = ModelForm(None)
        step.form = model_form
        return model_form
    
    @TextSyntax("- #1.", types=["list<str>", "ModelForm"])
    def form_modelfield_definition(self, fields_words, model_form):
        name = " ".join(fields_words)
        splitted_fields = name.split("|")
        fields = []
        for field in splitted_fields:
            field = field.strip()
            field = field.replace(" ", "_")
            fields.append("'%s'" % field)
        model_form.fields.extend(fields)
        model_form.grouped_fields.append(fields)
    
    @TextSyntax(["- #1 (#2) - Choices are #3."], types=["list<str>", "list<str>", "list<str>", "ModelForm"])
    def form_field_choices_definition(self, fields_words, field_name_words, choices, model_form):
        field = self.form_field_definition(fields_words, field_name_words, "ChoiceField", model_form)
        real_choices = list([(c,c) for c in choices])
        field.kwargs.update({"choices":real_choices})
        
    @TextSyntax("- #1 (#2) - #3.", types=["list<str>", "list<str>", "str", "ModelForm"])
    def form_field_definition(self, fields_words, field_name_words, field_type, model_form):
        verbose_name = " ".join(fields_words)
        name = "_".join(field_name_words)
        if field_type == "Checkbox":
            field_type = "BooleanField"
        field = FormField(name, verbose_name, field_type)
        model_form.extra_fields.append(field)
        model_form.grouped_fields.append(["'%s'"%name])
        #return field
    
    @TextSyntax("Heading: #1", types=["list<str>", "ModelForm"])
    def heading_definition(self, fields_words, model_form):
        heading = " ".join(fields_words)
        model_form.heading = heading
    
    @TextSyntax("Condition: #1 from step #2 is #3", types=["list<str>", "int", "list<str>", "Step"])
    def condition_definitions(self, field_words, step_number, value, step):
        self.wizard.conditions = True
        name = "_".join(field_words)
        value = " ".join(value)
        step.condition.update({"step": "%s" % step_number, "name":"%s" % name, "value":value})
        
        
