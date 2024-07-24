"""create post table

Revision ID: 46fd436332c8
Revises: 
Create Date: 2024-07-24 17:27:06.514242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46fd436332c8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))

def downgrade() -> None:
    op.drop_table('posts')
