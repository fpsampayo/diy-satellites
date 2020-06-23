from datetime import datetime

from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response

from api.models import Observation
from api.serializers import ObservationSerializer


class ObservationsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

    def list(self, request, *args, **kwargs):
        FORMAT_DATE = "%Y-%m-%dT%H:%M:%SZ"

        observations = self.queryset
        if request.query_params:
            init_date = datetime.strptime(request.query_params['init_date'], FORMAT_DATE)
            end_date = datetime.strptime(request.query_params['end_date'], FORMAT_DATE)
            observations = Observation.objects.filter(datetime__range=(init_date, end_date))
        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data)
