"""Change last run to date instead of datetime

Revision ID: 956a7c4d0d9f
Revises: c83368419b5a
Create Date: 2025-01-27 19:29:48.813049

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '956a7c4d0d9f'
down_revision = 'c83368419b5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chores', schema=None) as batch_op:
        batch_op.alter_column('last_scheduled',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=True)

    with op.batch_alter_table('households', schema=None) as batch_op:
        batch_op.alter_column('last_run_chore_allocation',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('households', schema=None) as batch_op:
        batch_op.alter_column('last_run_chore_allocation',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)

    with op.batch_alter_table('chores', schema=None) as batch_op:
        batch_op.alter_column('last_scheduled',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)

    # ### end Alembic commands ###
