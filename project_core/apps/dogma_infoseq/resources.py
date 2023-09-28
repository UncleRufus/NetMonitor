from import_export import resources
from .models import InfoSeqUserCertficateModel

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = InfoSeqUserCertficateModel
