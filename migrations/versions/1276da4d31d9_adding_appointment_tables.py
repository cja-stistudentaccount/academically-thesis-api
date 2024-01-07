"""adding appointment tables

Revision ID: 1276da4d31d9
Revises: c33dfc9704f2
Create Date: 2024-01-07 12:41:10.785329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1276da4d31d9'
down_revision = 'c33dfc9704f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointment',
    sa.Column('appointment_id', sa.String(), nullable=False),
    sa.Column('tutor_id', sa.String(), nullable=False),
    sa.Column('student_id', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['tutor_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('appointment_id'),
    sa.UniqueConstraint('appointment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment')
    # ### end Alembic commands ###
