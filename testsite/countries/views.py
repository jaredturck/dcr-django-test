from django.http import JsonResponse
from countries.models import Region
from django.db.models import Count, Sum, F

def stats(request):
    ''' Get a count of total population, and number of countries in each region '''
 
    qs = Region.objects.all().annotate(
        number_countries = Count(F('countries__name')),
        total_population = Sum(F('countries__population'))
    ).values('name', 'number_countries', 'total_population')

    return JsonResponse({"regions": list(qs)})
