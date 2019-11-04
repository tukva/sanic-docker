from os import getenv

POSTGRES_HOST = getenv("POSTGRES_HOST") or 'localhost'
POSTGRES_DB = getenv("POSTGRES_DB") or 'test'
POSTGRES_USER = getenv("POSTGRES_USER") or 'test'
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD") or 'test'

url = 'postgres://{0}:{1}@{2}/{3}'.format(POSTGRES_USER,
                                          POSTGRES_PASSWORD,
                                          POSTGRES_HOST,
                                          POSTGRES_DB)
