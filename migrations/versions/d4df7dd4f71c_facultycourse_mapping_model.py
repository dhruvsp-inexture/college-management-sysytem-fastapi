"""FacultyCourse  Mapping Model

Revision ID: d4df7dd4f71c
Revises: 122f0a482fdd
Create Date: 2023-05-02 15:38:15.313289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4df7dd4f71c'
down_revision = '122f0a482fdd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faculty_course_mapping',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('faculty_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['faculty_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'faculty_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('faculty_course_mapping')
    # ### end Alembic commands ###