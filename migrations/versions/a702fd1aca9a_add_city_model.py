"""Add city model

Revision ID: a702fd1aca9a
Revises: 91cc2d323bde
Create Date: 2025-05-06 15:10:56.907240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a702fd1aca9a'
down_revision = '91cc2d323bde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_name', sa.String(length=100), nullable=False),
    sa.Column('lat', sa.Float, nullable=False),
    sa.Column('lon', sa.Float, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('city_name')
    )

    with op.batch_alter_table('weather_data', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_weatherdata_city_cityname', 'city', ['city'], ['city_name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weather_data', schema=None) as batch_op:
        batch_op.drop_constraint('fk_weatherdata_city_cityname', type_='foreignkey')
    op.drop_table('city')
    # ### end Alembic commands ###
