"""drop name column in usercustomer table

Revision ID: 3dda1ab5fb15
Revises: 
Create Date: 2022-09-27 16:41:19.671751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dda1ab5fb15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('register')
    with op.batch_alter_table('user_customer', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), nullable=True))

    op.create_table('register',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('username', sa.VARCHAR(length=50), nullable=True),
    sa.Column('email', sa.VARCHAR(length=50), nullable=True),
    sa.Column('password', sa.VARCHAR(length=200), nullable=True),
    sa.Column('country', sa.VARCHAR(length=50), nullable=True),
    sa.Column('city', sa.VARCHAR(length=50), nullable=True),
    sa.Column('contact', sa.VARCHAR(length=50), nullable=True),
    sa.Column('address', sa.VARCHAR(length=50), nullable=True),
    sa.Column('zipcode', sa.VARCHAR(length=50), nullable=True),
    sa.Column('profile', sa.VARCHAR(length=200), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
