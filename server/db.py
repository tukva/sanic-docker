database_name = 'test'
database_host = 'database'
database_user = 'test'
database_password = 'test'

connection = 'postgres://{0}:{1}@{2}/{3}'.format(database_user,
                                                 database_password,
                                                 database_host,
                                                 database_name)
