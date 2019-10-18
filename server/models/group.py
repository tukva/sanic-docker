import sqlalchemy as sa


metadata = sa.MetaData()

tb_group = sa.Table(
    'tb_group', metadata,
    sa.Column('group_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False, unique=True))
