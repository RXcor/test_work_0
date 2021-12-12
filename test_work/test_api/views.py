from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q, F
from django.db.models import Sum

from .models import Record
from .serializers import RecordSerializer


class RecordViewSet(ViewSet):
    '''Представление для работы с форматированной строкой
     "a,b;a,b;a,b;a,b"
     где `a`,`b`- int not null, `a` не уникально, пара не уникальна,
    '''
    permission_classes = (AllowAny,)

    def create(self, request):
        queryset = Record.objects.all()
        list = request.data.split(';')
        list_pairs = [ _.split(',') for _ in list ]
        instances = [ RecordSerializer(
            data={"a": pair[0], "b": pair[1]}) for pair in list_pairs ]
        validation = [ instance.is_valid() for instance in instances]
        try:
            if False not in validation:
                objs = Record.objects.bulk_create(
                    [Record(a=pair[0], b=pair[1]) for pair in list_pairs])                
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, IndexError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        a = self.request.query_params.get('a', None)
        b = self.request.query_params.get('b', None)
        a_condition = Q(a__gte=a) if a is not None else Q()
        b_condition = Q(b_sum__gte=b) if b is not None else Q()       
        res = Record.objects.filter(a_condition).annotate(av=F('a')).\
            values('av').annotate(b_sum=Sum('b')).filter(b_condition).\
                order_by('av', 'b_sum').values_list('av', 'b_sum')
        list = [ f'{_[0]},{_[1]}' for _ in res ]
        result_string = ';'.join(list)
        
        return Response(result_string, status=status.HTTP_200_OK)
