"""Changed cart.product_id datatype

Revision ID: 39e272caeec6
Revises: e54e039df918
Create Date: 2022-05-05 14:44:10.277389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39e272caeec6'
down_revision = 'e54e039df918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('product_id', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'product_id')
    # ### end Alembic commands ###
