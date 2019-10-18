import sqlalchemy as sa


metadata = sa.MetaData()

tb_user_group = sa.Table(
    'tb_user_group', metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('tb_user.id')),
    sa.Column('group_id', sa.Integer, sa.ForeignKey('tb_group.id')))
