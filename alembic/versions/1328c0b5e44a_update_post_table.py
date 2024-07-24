"""update post table

Revision ID: 1328c0b5e44a
Revises: 46fd436332c8
Create Date: 2024-07-24 18:07:40.982575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1328c0b5e44a'
down_revision: Union[str, None] = '46fd436332c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
