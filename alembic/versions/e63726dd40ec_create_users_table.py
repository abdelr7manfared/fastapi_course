"""create users table

Revision ID: e63726dd40ec
Revises: 1328c0b5e44a
Create Date: 2024-07-24 18:14:38.149924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e63726dd40ec'
down_revision: Union[str, None] = '1328c0b5e44a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                    sa.Column('Email',sa.String(),nullable=False,unique=True),
                    sa.Column('Password',sa.String(),nullable=False),
                    sa.Column('username',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    )



def downgrade() -> None:
    pass
