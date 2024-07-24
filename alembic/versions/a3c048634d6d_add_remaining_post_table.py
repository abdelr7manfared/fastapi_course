"""add remaining post_table

Revision ID: a3c048634d6d
Revises: 496ed661fc61
Create Date: 2024-07-24 18:55:44.992689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c048634d6d'
down_revision: Union[str, None] = '496ed661fc61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('Publised',sa.Boolean,nullable=False,server_default='TRUE'))
    
    op.add_column('posts',sa.Column('created_at',sa.DateTime(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','Publised')
    op.drop_column('posts','created_at')
    
    pass
