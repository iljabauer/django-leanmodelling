from django_lean_modelling import helper
from django_lean_modelling.model import Model, Property, Admin
from natspec_utils.decorators import TextSyntax


class AdminSupport:
    def __init__(self):
        self.admins = []
        
    @TextSyntax(["Configure admin to:", "Configure standard admin."], types=["Model"], return_type="Admin")
    def configure_admin(self, model):
        admin = Admin(model)
        self.admins.append(admin)
        return admin
    


    def split_list(self, joined_parameters):
        joined_parameters = joined_parameters.split(",")
        params = []
        for param in joined_parameters:
            param = param.strip()
            param = param.replace(" ", "_")
            param = "'%s'" % param
            params.append(param)
        
        return params
    
    @TextSyntax("- display: #1.", types=["list<str>", "Admin"], return_type="Property")
    def display_definition(self, parameters, admin):
        property = self.create_property("list_display", parameters)
        admin.properties.append(property)
        return property

    @TextSyntax("- show filter for: #1.", types=["list<str>", "Admin"], return_type="Property")
    def filter_definition(self, parameters, admin):
        property = self.create_property("list_filter", parameters)
        admin.properties.append(property)
        return property
    
    @TextSyntax("- exclude: #1.", types=["list<str>", "Admin"], return_type="Property")
    def exlude_definition(self, parameters, admin):
        property = self.create_property("exclude", parameters)
        admin.properties.append(property)
        return property
    
    @TextSyntax("- fields: #1.", types=["list<str>", "Admin"], return_type="Property")
    def fields_definition(self, parameters, admin):
        property = self.create_property("fields", parameters)
        admin.properties.append(property)
        return property
        
    def create_property(self, name, parameters):
        joined_parameters = " ".join(parameters)
        params = self.split_list(joined_parameters)
        property = Property(name, "")
        property.args = params
        return property
        
        
        
        
        
