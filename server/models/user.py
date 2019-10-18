import sqlalchemy as sa


metadata = sa.MetaData()

tb_user = sa.Table('tb_user', metadata,
                   sa.Column('user_id', sa.Integer, primary_key=True),
                   sa.Column('username', sa.String(255),
                             nullable=False, unique=True),
                   sa.Column('password', sa.String(255), nullable=False),
                   sa.Column("permission", sa.ARRAY(sa.String(50))))
