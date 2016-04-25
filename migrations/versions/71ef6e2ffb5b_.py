"""empty message

Revision ID: 71ef6e2ffb5b
Revises: None
Create Date: 2016-04-25 08:26:21.817035

"""

# revision identifiers, used by Alembic.
revision = '71ef6e2ffb5b'
down_revision = None

from alembic import op
import sqlalchemy as sa
import doorman.database


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filepath',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('target_paths', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category')
    )
    op.create_table('node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('node_key', sa.String(), nullable=False),
    sa.Column('enroll_secret', sa.String(), nullable=True),
    sa.Column('enrolled_on', sa.DateTime(), nullable=True),
    sa.Column('host_identifier', sa.String(), nullable=True),
    sa.Column('last_checkin', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('node_key')
    )
    op.create_table('pack',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('platform', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('shard', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('sql', sa.String(), nullable=False),
    sa.Column('interval', sa.Integer(), nullable=True),
    sa.Column('platform', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.create_table('nodetags',
    sa.Column('tag.id', sa.Integer(), nullable=True),
    sa.Column('node.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node.id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['tag.id'], ['tag.id'], )
    )
    op.create_table('packtags',
    sa.Column('tag.id', sa.Integer(), nullable=True),
    sa.Column('pack.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pack.id'], ['pack.id'], ),
    sa.ForeignKeyConstraint(['tag.id'], ['tag.id'], )
    )
    op.create_table('pathtags',
    sa.Column('tag.id', sa.Integer(), nullable=True),
    sa.Column('filepath.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['filepath.id'], ['filepath.id'], ),
    sa.ForeignKeyConstraint(['tag.id'], ['tag.id'], )
    )
    op.create_table('querypacks',
    sa.Column('pack.id', sa.Integer(), nullable=True),
    sa.Column('query.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pack.id'], ['pack.id'], ),
    sa.ForeignKeyConstraint(['query.id'], ['query.id'], )
    )
    op.create_table('querytags',
    sa.Column('tag.id', sa.Integer(), nullable=True),
    sa.Column('query.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['query.id'], ['query.id'], ),
    sa.ForeignKeyConstraint(['tag.id'], ['tag.id'], )
    )
    op.create_table('result_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('added', doorman.database.JSONBType(), nullable=True),
    sa.Column('removed', doorman.database.JSONBType(), nullable=True),
    sa.Column('node_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('severity', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('node_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status_log')
    op.drop_table('result_log')
    op.drop_table('querytags')
    op.drop_table('querypacks')
    op.drop_table('pathtags')
    op.drop_table('packtags')
    op.drop_table('nodetags')
    op.drop_table('tag')
    op.drop_table('query')
    op.drop_table('pack')
    op.drop_table('node')
    op.drop_table('filepath')
    ### end Alembic commands ###