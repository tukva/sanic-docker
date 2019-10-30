import sqlalchemy as sa


metadata = sa.MetaData()

tb_user = sa.Table(
    'tb_user', metadata,
    sa.Column('user_id', sa.Integer, primary_key=True),
    sa.Column('username', sa.String(40), nullable=False, unique=True),
    sa.Column('password', sa.String(255), nullable=False))

tb_user_group = sa.Table(
    'tb_user_group', metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('tb_user.user_id')),
    sa.Column('group_id', sa.Integer, sa.ForeignKey('tb_group.group_id')))

tb_group = sa.Table(
    'tb_group', metadata,
    sa.Column('group_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False, unique=True))

tb_group_permission = sa.Table(
    'tb_group_permission', metadata,
    sa.Column('group_id', sa.Integer, sa.ForeignKey('tb_group.group_id')),
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('tb_permission.permission_id')))

tb_permission = sa.Table(
    'tb_permission', metadata,
    sa.Column('permission_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False, unique=True))

tb_session = sa.Table(
    'tb_session', metadata,
    sa.Column('session_id', sa.String(64), nullable=False, unique=True),
    sa.Column('user_id', sa.Integer, nullable=False, unique=True))
