"""Normalize distributed query architecture

Revision ID: 4f95ecd76bf8
Revises: 14c992522209
Create Date: 2016-05-16 23:52:00.328190

"""

# revision identifiers, used by Alembic.
revision = '4f95ecd76bf8'
down_revision = '14c992522209'

from alembic import op
from collections import namedtuple
import sqlalchemy as sa
import doorman.database
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    DistributedQueryTask = namedtuple('DistributedQueryTask', [
        'id', 'status', 'retrieved', 'guid', 'node_id'])

    distributed_query_task = op.create_table('distributed_query_task',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('guid', sa.String(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('distributed_query_id', sa.Integer(), nullable=False),
        sa.Column('node_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['distributed_query_id'], ['distributed_query.id'], ),
        sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('guid')
    )

    cursor = op.get_bind().execute("""
        SELECT id, status, retrieved, guid, node_id
        FROM distributed_query
        ORDER BY id;"""
    )
    results = map(DistributedQueryTask._make, cursor.fetchall())
    distributed_query_tasks = [dict(
        distributed_query_id=r.id,
        status=r.status,
        timestamp=r.retrieved,
        guid=r.guid,
        node_id=r.node_id) for r in results]

    op.bulk_insert(distributed_query_task, distributed_query_tasks)

    op.add_column(u'distributed_query', sa.Column('description', sa.String(), nullable=True))
    op.drop_constraint(u'distributed_query_guid_key', 'distributed_query', type_='unique')
    op.drop_constraint(u'distributed_query_node_id_fkey', 'distributed_query', type_='foreignkey')
    op.drop_column(u'distributed_query', 'status')
    op.drop_column(u'distributed_query', 'retrieved')
    op.drop_column(u'distributed_query', 'guid')
    op.drop_column(u'distributed_query', 'node_id')
    op.add_column(u'distributed_query_result', sa.Column('distributed_query_task_id', sa.Integer(), nullable=True))

    # distributed queries and tasks were the same before,
    # so their id's will remain the same as well.
    op.execute("""
        UPDATE distributed_query_result
        SET distributed_query_task_id = distributed_query_id;"""
    )

    op.alter_column(u'distributed_query_result', 'distributed_query_task_id', nullable=False)
    op.create_foreign_key(None, 'distributed_query_result', 'distributed_query_task', ['distributed_query_task_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    DistributedQuery = namedtuple('DistributedQuery', [
        'task_id', 'query_id',
        'guid', 'status', 'sql', 'timestamp', 'not_before',
        'retrieved', 'node_id'])

    cursor = op.get_bind().execute("""
        SELECT DISTINCT t.id AS task_id, q.id AS query_id,
            t.guid, t.status, q.sql, q.timestamp, q.not_before,
            t.timestamp AS retrieved, t.node_id
        FROM distributed_query q
        INNER JOIN distributed_query_task t
        ON q.id = t.distributed_query_id
        ORDER BY t.id;
    """)

    results = map(DistributedQuery._make, cursor.fetchall())

    op.drop_constraint(u'distributed_query_result_distributed_query_task_id_fkey', 'distributed_query_result', type_='foreignkey')
    op.drop_column(u'distributed_query_result', 'distributed_query_task_id')

    op.drop_constraint(u'distributed_query_task_distributed_query_id_fkey', 'distributed_query_task', type_='foreignkey')
    op.drop_table(u'distributed_query')

    distributed_query = op.create_table('distributed_query',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('guid', sa.String(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('sql', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('not_before', sa.DateTime(), nullable=True),
        sa.Column('retrieved', sa.DateTime(), nullable=True),
        sa.Column('node_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('guid')
    )

    distributed_queries = [dict(
        guid=r.guid,
        status=r.status,
        sql=r.sql,
        timestamp=r.timestamp,
        not_before=r.not_before,
        retrieved=r.retrieved,
        node_id=r.node_id) for r in results]

    op.bulk_insert(distributed_query, distributed_queries)
    op.drop_table('distributed_query_task')
    ### end Alembic commands ###