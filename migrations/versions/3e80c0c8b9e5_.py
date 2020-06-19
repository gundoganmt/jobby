"""empty message

Revision ID: 3e80c0c8b9e5
Revises: 8b6ac5e77bed
Create Date: 2020-06-17 12:30:45.193069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e80c0c8b9e5'
down_revision = '8b6ac5e77bed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Offers', sa.Column('subject', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Offers', 'subject')
    # ### end Alembic commands ###
