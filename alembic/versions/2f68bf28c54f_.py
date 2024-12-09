"""empty message

Revision ID: 2f68bf28c54f
Revises: 
Create Date: 2024-12-09 23:05:32.280633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f68bf28c54f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('ipn', sa.Integer(), nullable=True),
    sa.Column('full_name', sa.String(length=150), nullable=True),
    sa.Column('contacts', sa.String(length=150), nullable=True),
    sa.Column('photo', sa.String(length=150), nullable=True),
    sa.Column('passport', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ipn'),
    sa.UniqueConstraint('login')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('photo', sa.String(length=150), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('price_hour', sa.REAL(), nullable=True),
    sa.Column('price_day', sa.REAL(), nullable=True),
    sa.Column('price_week', sa.REAL(), nullable=True),
    sa.Column('price_month', sa.REAL(), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('available', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('search_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('search_text', sa.String(length=250), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contract',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(length=250), nullable=True),
    sa.Column('start_date', sa.String(length=20), nullable=True),
    sa.Column('end_date', sa.String(length=20), nullable=True),
    sa.Column('contract_num', sa.Integer(), nullable=True),
    sa.Column('leaser', sa.Integer(), nullable=True),
    sa.Column('taker', sa.Integer(), nullable=True),
    sa.Column('item', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.ForeignKeyConstraint(['leaser'], ['user.id'], ),
    sa.ForeignKeyConstraint(['taker'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favourites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('item', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=250), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('contract', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.ForeignKeyConstraint(['contract'], ['contract.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    op.drop_table('favourites')
    op.drop_table('contract')
    op.drop_table('search_history')
    op.drop_table('item')
    op.drop_table('user')
    # ### end Alembic commands ###
