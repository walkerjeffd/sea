"""empty message

Revision ID: 2b854e43388a
Revises: 1c69a06d235b
Create Date: 2014-05-21 09:07:47.202000

"""

# revision identifiers, used by Alembic.
revision = '2b854e43388a'
down_revision = '1c69a06d235b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('forecasts', sa.Column('latest', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('forecasts', 'latest')
    ### end Alembic commands ###
