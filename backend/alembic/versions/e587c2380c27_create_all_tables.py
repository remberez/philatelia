"""create all tables

Revision ID: e587c2380c27
Revises: 
Create Date: 2025-05-06 03:24:27.598484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e587c2380c27'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('groupname', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_groupname'), 'group', ['groupname'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('hashed_pass', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('collection',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_collection_name'), 'collection', ['name'], unique=False)
    op.create_index(op.f('ix_collection_owner_id'), 'collection', ['owner_id'], unique=False)
    op.create_table('meeting',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meeting_group_id'), 'meeting', ['group_id'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_group_id'), 'post', ['group_id'], unique=False)
    op.create_table('post_photo',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_photo_group_id'), 'post_photo', ['group_id'], unique=False)
    op.create_table('stamp',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('country', sa.BigInteger(), nullable=False),
    sa.Column('issue_year', sa.Date(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stamp_country'), 'stamp', ['country'], unique=False)
    op.create_index(op.f('ix_stamp_issue_year'), 'stamp', ['issue_year'], unique=False)
    op.create_index(op.f('ix_stamp_owner_id'), 'stamp', ['owner_id'], unique=False)
    op.create_table('user_group',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    op.create_index(op.f('ix_user_group_group_id'), 'user_group', ['group_id'], unique=False)
    op.create_index(op.f('ix_user_group_user_id'), 'user_group', ['user_id'], unique=False)
    op.create_table('meeting_user',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('meeting_id', sa.BigInteger(), nullable=False),
    sa.Column('is_visited', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['meeting_id'], ['meeting.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'meeting_id')
    )
    op.create_index(op.f('ix_meeting_user_meeting_id'), 'meeting_user', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_meeting_user_user_id'), 'meeting_user', ['user_id'], unique=False)
    op.create_table('stamp_collection',
    sa.Column('stamp_id', sa.BigInteger(), nullable=False),
    sa.Column('collection_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collection.id'], ),
    sa.ForeignKeyConstraint(['stamp_id'], ['stamp.id'], ),
    sa.PrimaryKeyConstraint('stamp_id', 'collection_id')
    )
    op.create_index(op.f('ix_stamp_collection_collection_id'), 'stamp_collection', ['collection_id'], unique=False)
    op.create_index(op.f('ix_stamp_collection_stamp_id'), 'stamp_collection', ['stamp_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stamp_collection_stamp_id'), table_name='stamp_collection')
    op.drop_index(op.f('ix_stamp_collection_collection_id'), table_name='stamp_collection')
    op.drop_table('stamp_collection')
    op.drop_index(op.f('ix_meeting_user_user_id'), table_name='meeting_user')
    op.drop_index(op.f('ix_meeting_user_meeting_id'), table_name='meeting_user')
    op.drop_table('meeting_user')
    op.drop_index(op.f('ix_user_group_user_id'), table_name='user_group')
    op.drop_index(op.f('ix_user_group_group_id'), table_name='user_group')
    op.drop_table('user_group')
    op.drop_index(op.f('ix_stamp_owner_id'), table_name='stamp')
    op.drop_index(op.f('ix_stamp_issue_year'), table_name='stamp')
    op.drop_index(op.f('ix_stamp_country'), table_name='stamp')
    op.drop_table('stamp')
    op.drop_index(op.f('ix_post_photo_group_id'), table_name='post_photo')
    op.drop_table('post_photo')
    op.drop_index(op.f('ix_post_group_id'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_meeting_group_id'), table_name='meeting')
    op.drop_table('meeting')
    op.drop_index(op.f('ix_collection_owner_id'), table_name='collection')
    op.drop_index(op.f('ix_collection_name'), table_name='collection')
    op.drop_table('collection')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_group_groupname'), table_name='group')
    op.drop_table('group')
    # ### end Alembic commands ###
