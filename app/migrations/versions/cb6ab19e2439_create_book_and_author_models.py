"""create book and author models.

Revision ID: cb6ab19e2439
Revises: ebd2a55e5a9c
Create Date: 2024-08-06 15:21:39.630683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb6ab19e2439'
down_revision: Union[str, None] = 'ebd2a55e5a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('birth_year', sa.Date(), nullable=False),
    sa.Column('death_year', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('publish_year', sa.Date(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_publish_year'), 'book', ['publish_year'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_publish_year'), table_name='book')
    op.drop_table('book')
    op.drop_table('author')
    # ### end Alembic commands ###
