"""empty message

Revision ID: 01aa19126ae4
Revises: fc63ad167f9e
Create Date: 2023-07-06 11:02:16.347142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01aa19126ae4'
down_revision = 'fc63ad167f9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Password', sa.String(length=20), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('Password')

    # ### end Alembic commands ###
