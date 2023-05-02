"""empty message

Revision ID: f20551a7a338
Revises: 09163d048cc9
Create Date: 2023-05-01 20:34:47.632267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f20551a7a338'
down_revision = '09163d048cc9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('photos_owner_id_key', 'photos', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('photos_owner_id_key', 'photos', ['owner_id'])
    # ### end Alembic commands ###