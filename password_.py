# fill the database credentials amd change the name of this file from password_.py to password.py
uri = 'postgres://{user}:{password}@PostGIS:5432/{database}'.format(
    user="cansat", password="mysecretpassword", database="cansat")
# https://stackoverflow.com/a/50971274/9517898
# user = os.environ['POSTGRES_USER'] TODO
# password = os.environ['POSTGRES_PASSWORD']
