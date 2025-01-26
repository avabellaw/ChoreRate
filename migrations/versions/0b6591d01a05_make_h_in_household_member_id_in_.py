"""Make H in household_member_id in AllocatedChore lowercase

Revision ID: 0b6591d01a05
Revises: e1f64d35f71d
Create Date: 2025-01-26 14:17:27.508879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b6591d01a05'
down_revision = 'e1f64d35f71d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('allocated_chores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('household_member_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('allocated_chores_Household_member_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'household_members', ['household_member_id'], ['id'])
        batch_op.drop_column('Household_member_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('allocated_chores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Household_member_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('allocated_chores_Household_member_id_fkey', 'household_members', ['Household_member_id'], ['id'])
        batch_op.drop_column('household_member_id')

    # ### end Alembic commands ###
