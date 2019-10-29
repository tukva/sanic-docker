from os import getenv

POSTGRES_HOST = getenv("POSTGRES_HOST")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")

url = 'postgres://{0}:{1}@{2}/{3}'.format(POSTGRES_USER,
                                          POSTGRES_PASSWORD,
                                          POSTGRES_HOST,
                                          POSTGRES_DB)
