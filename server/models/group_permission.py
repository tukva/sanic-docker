import sqlalchemy as sa


metadata = sa.MetaData()

tb_group_permission = sa.Table(
    'tb_group_permission', metadata,
    sa.Column('group_id', sa.Integer, sa.ForeignKey('tb_group.id')),
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('tb_permission.id')))
