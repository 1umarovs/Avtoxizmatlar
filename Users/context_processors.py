from .models import ServiceType

def categories_processor(request):
    categories = ServiceType.objects.all()
    return {'categories': categories}
