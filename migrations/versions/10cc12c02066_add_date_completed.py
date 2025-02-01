"""Add date completed

Revision ID: 10cc12c02066
Revises: 911d958d8f48
Create Date: 2025-02-01 18:53:22.462917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10cc12c02066'
down_revision = '911d958d8f48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_completed', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chores', schema=None) as batch_op:
        batch_op.drop_column('date_completed')

    # ### end Alembic commands ###
