from import_export import resources
from .models import DogmaEmployee

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = DogmaEmployee
