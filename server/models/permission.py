import sqlalchemy as sa


metadata = sa.MetaData()

tb_permission = sa.Table(
    'tb_permission', metadata,
    sa.Column('permission_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False, unique=True))
