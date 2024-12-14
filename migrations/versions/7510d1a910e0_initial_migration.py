"""initial migration

Revision ID: 7510d1a910e0
Revises: 
Create Date: 2024-11-22 20:48:53.591832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7510d1a910e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_ratings', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'chores', ['chore_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chore_ratings', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###