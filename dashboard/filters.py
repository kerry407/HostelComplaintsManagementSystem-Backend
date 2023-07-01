import django_filters
from .models import Complaint 

class ComplaintFilter(django_filters.FilterSet):
    '''Customize filter to allow any Caps'''
    student_first_name = django_filters.CharFilter(field_name="student__user__first_name", lookup_expr="icontains")
    student_last_name = django_filters.CharFilter(field_name="student__user__last_name", lookup_expr="icontains")
    filed_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Complaint 
        fields = ["student_first_name", "student_last_name", "filed_date", "is_resolved"]