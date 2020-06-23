from rest_framework_gis.serializers import GeoFeatureModelSerializer

from api.models import Observation


class ObservationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Observation
        geo_field = "geom"
        fields = ('observationId', 'datetime', 'altGPS', 'temp', 'hum', 'altBar', 'pressure', 'NO2', 'CO',
                  'NH3', 'PM1_0', 'PM2_5', 'PM10_0')
