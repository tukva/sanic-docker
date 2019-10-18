import sqlalchemy as sa


metadata = sa.MetaData()

tb_session = sa.Table('tb_session', metadata,
                      sa.Column('session_id', sa.String(255)),
                      sa.Column('user_id', sa.Integer, nullable=False, unique=True))