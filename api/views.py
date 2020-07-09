from datetime import datetime

from rest_framework import viewsets, views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import Observation
from api.serializers import ObservationSerializer
from api import constants
import csv
import io

from api.use_case import insert_observation_into_database


class ObservationsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer

    def list(self, request, *args, **kwargs):

        observations = self.queryset
        if request.query_params:
            init_date = datetime.strptime(request.query_params['init_date'], constants.FORMAT_DATE)
            end_date = datetime.strptime(request.query_params['end_date'], constants.FORMAT_DATE)
            observations = Observation.objects.filter(date_time__range=(init_date, end_date))
        serializer = ObservationSerializer(observations, many=True)
        return Response(serializer.data)


class UploadCsv(views.APIView):
    parser_classes = [MultiPartParser, ]

    def post(self, request):

        csv_file = request.data['file']
        file_data = csv_file.read().decode("utf-8")
        io_string = io.StringIO(file_data)
        next(io_string)

        for observation_from_csv in csv.reader(io_string, delimiter=',', quotechar='|'):
            try:
                inserted = insert_observation_into_database(observation_from_csv)
            except Exception as err:
                print(err)

        return Response(status=204)