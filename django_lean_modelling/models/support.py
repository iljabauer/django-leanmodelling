from django_lean_modelling import helper
from django_lean_modelling.model import Model, Property
from natspec_utils.decorators import TextSyntax


class ModelSupport:
    def __init__(self):
        self.models = []
        
    @TextSyntax("#1", types=["list<str>", "Property"])
    def comment_definition(self, comment_words, p):
        comment = " ".join(comment_words)
        p.comment = comment
    
    @TextSyntax("Every #1 has:", types=["list<str>", ], return_type="Model")
    def model_name_definition(self, model_name_words):
        #TODO: handle list of words for name in camelcase
        verbose_name = " ".join(model_name_words)
        model_name = "".join(model_name_words)
        model = Model(model_name, verbose_name)
        self.models.append(model)
        return model
    
    @TextSyntax("Every #1 (plural #2) has:", types=["list<str>", "list<str>"], return_type="Model")
    def model_name_with_plural_definition(self, model_name_words, plural_names_words):
        verbose_name = " ".join(model_name_words)
        verbose_name_plural = " ".join(plural_names_words)
        model_name = "".join(model_name_words)
        model = Model(model_name,verbose_name)
        model.verbose_name_plural = verbose_name_plural
        self.models.append(model)
        return model
        
    @TextSyntax(["- a #1.", "- a #1:"], types=["list<str>", "Model"], return_type="Property")
    def string_property_definition(self, propertie_name_words, model):
        propertie_name = "_".join(propertie_name_words)
        propertie_verbose_name = " ".join(propertie_name_words)
        definition = "models.CharField"
        p = Property(propertie_name, definition, verbose_name=propertie_verbose_name)
        p.kwargs.update({"max_length":128})
        model.properties.append(p)
        return p
    
    @TextSyntax(["- a #1 as decimal.", "- a #1 as decimal:"], types=["list<str>", "Model"], return_type="Property")
    def typed_decimal_property_definition(self, propertie_name_words, model):
        definition = "models.DecimalField"
        return self.typed_property_definition(propertie_name_words, definition, model)
    
    @TextSyntax("- an email.", types=["Model"], return_type="Property")
    def email_property_definition(self, model):
        definition = "models.EmailField"
        return self.typed_property_definition(["email"], definition, model)
    
    @TextSyntax("- an #1 as email.", types=["list<str>", "Model"], return_type="Property")
    def typed_email_property_definition(self,propertie_name_words, model):
        definition = "models.EmailField"
        return self.typed_property_definition(propertie_name_words, definition, model)
    
    @TextSyntax("- an #1 as date time.", types=["list<str>", "Model"], return_type="Property")
    def typed_date_time_property_definition(self,propertie_name_words, model):
        definition = "models.DateTimeField"
        return self.typed_property_definition(propertie_name_words, definition, model)
    
    @TextSyntax("- an #1 as text.", types=["list<str>", "Model"], return_type="Property")
    def typed_text_property_definition(self,propertie_name_words, model):
        definition = "models.TextField"
        return self.typed_property_definition(propertie_name_words, definition, model)
    
    def typed_property_definition(self, propertie_name_words, definition, model):
        propertie_name = "_".join(propertie_name_words)
        propertie_verbose_name = " ".join(propertie_name_words)
        p = Property(propertie_name, definition, verbose_name=propertie_verbose_name)
        model.properties.append(p)
        return p
    
    @TextSyntax("- one #1.", types=["str", "Model"], return_type="Property")
    def foreign_key_property_definition(self, full_class_name, model):
        class_name = full_class_name.split(".")[-1]
        property_name = helper.convert(class_name)
        return self.foreign_key_with_name_property_definition(full_class_name, [property_name, ], model)
    
    @TextSyntax("- one #1 called #2.", types=["str", "list<str>", "Model"], return_type="Property")
    def foreign_key_with_name_property_definition(self, class_name, propertie_name_words, model):
        propertie_name = "_".join(propertie_name_words)
        definition = "models.ForeignKey"
        p = Property(propertie_name, definition)
        p.args.append("'%s'"%class_name)
        p.kwargs.update({"related_name":"'%s'"%propertie_name})
        model.properties.append(p)
        return p
    
    @TextSyntax("- one exclusive #1 called #2.", types=["str", "list<str>", "Model"], return_type="Property")
    def one_to_one_with_name_property_definition(self, class_name, propertie_name_words, model):
        propertie_name = "_".join(propertie_name_words)
        definition = "models.OneToOneField"
        p = Property(propertie_name, definition)
        p.args.append("'%s'"%class_name)
        p.kwargs.update({"related_name":"'%s_of'"%propertie_name})
        model.properties.append(p)
        return p
    
    
    

    @TextSyntax("decimal places: #1", types=["int", "Property"])  #
    def property_decimal_places_definition(self, value, prop):
        self.property_kwargs_definition("decimal_places", value, prop)
        
    @TextSyntax("max digits: #1", types=["int", "Property"])  #
    def property_max_digits_definition(self, value, prop):
        self.property_kwargs_definition("max_digits", value, prop)
        
    @TextSyntax("max length: #1", types=["int", "Property"])  #
    def property_max_length_definition(self, value, prop):
        self.property_kwargs_definition("max_length", value, prop)
        
    @TextSyntax("unique", types=["Property"])  #
    def property_unique_definition(self, prop):
        self.property_kwargs_definition("unique", True, prop)
        
    @TextSyntax("optional", types=["Property"])  #
    def property_optional_definition(self, prop):
        self.property_kwargs_definition("null", True, prop)
        self.property_kwargs_definition("blank", True, prop)
        
    @TextSyntax("set date on creation", types=["Property"])  #
    def property_auto_now_add_definition(self, prop):
        self.property_kwargs_definition("auto_now_add", True, prop)
    
    def property_kwargs_definition(self, name, value, prop):
        prop.kwargs.update({name: value})
    
        
    
    
