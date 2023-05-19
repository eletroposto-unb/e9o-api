"""create user table

Revision ID: 22484e0aa3da
Revises: 
Create Date: 2023-05-19 10:24:17.247252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22484e0aa3da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('firebase_uid', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('cpf', sa.String(length=100), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('telefone', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('cpf')
    )
    op.create_index(op.f('ix_users_cpf'), 'users', ['cpf'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_cpf'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
