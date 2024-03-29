"""empty message

Revision ID: 22c4bc806c8b
Revises: 871a07a7e83c
Create Date: 2019-12-20 12:28:59.538999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22c4bc806c8b'
down_revision = '871a07a7e83c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'seeking_description')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###
