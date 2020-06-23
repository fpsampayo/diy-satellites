from django.test import TestCase, Client


class TestApi(TestCase):

    fixtures = [
        './fixtures/observations.json'
    ]

    def test_get_observations(self):
        client = Client()
        url = '/api/v1/observations/'
        response = client.get(url)

        observations = response.json()

        self.assertEqual(observations['features'][0]['properties']['altGPS'], 1.0)
        self.assertEqual(observations['features'][29]['properties']['pressure'], 12.0)
        self.assertEqual(len(observations['features']), 30)
        self.assertEqual(response.status_code, 200)

    def test_get_observations_filter_by_date(self):

        client = Client()

        init_date = "2020-06-16T00:00:00Z"
        end_date = "2020-06-16T00:00:10Z"
        url = '/api/v1/observations/?init_date={init_date}&end_date={end_date}'.format(init_date=init_date, end_date=end_date)

        response = client.get(url)
        observations = response.json()

        self.assertEqual(observations['features'][0]['properties']['altGPS'], 1.0)
        self.assertEqual(len(observations['features']), 11)
        self.assertEqual(response.status_code, 200)

        init_date = "2020-06-16T23:59:59Z"
        end_date = "2020-06-17T00:00:29Z"
        url = '/api/v1/observations/?init_date={init_date}&end_date={end_date}'.format(init_date=init_date,
                                                                                       end_date=end_date)
        response = client.get(url)
        observations = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(observations['features']), 2)

