"""image_uri

Revision ID: 3ec6531ebaf8
Revises: 76fc00120bf9
Create Date: 2023-04-28 19:31:12.327463

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ec6531ebaf8'
down_revision = '76fc00120bf9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('image_uri', sa.Text(), nullable=False, comment='Ссылка на доступ к фотографии.'))
    op.drop_column('photos', 'data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('data', postgresql.BYTEA(), autoincrement=False, nullable=False, comment='Байтовое представление фотографии'))
    op.drop_column('photos', 'image_uri')
    # ### end Alembic commands ###