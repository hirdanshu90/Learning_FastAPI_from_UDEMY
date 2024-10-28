"""Create_phonenumber_for_user_column.py

Revision ID: fb05b5e17a21
Revises: 
Create Date: 2024-10-19 18:31:34.914218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb05b5e17a21'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# To add the phone number
def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

# To remove the phone_number
def downgrade() -> None:
    op.drop_column('users', 'phone_number')
