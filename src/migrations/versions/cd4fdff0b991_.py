"""empty message

Revision ID: cd4fdff0b991
Revises: 
Create Date: 2025-01-25 11:51:07.094780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cd4fdff0b991'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Удаляем таблицы с использованием CASCADE для зависимости
    op.execute("DROP TABLE IF EXISTS delivery_logs CASCADE")
    op.execute("DROP TABLE IF EXISTS messages CASCADE")

    # Создаём таблицу notifications
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("recipient", sa.JSON, nullable=False),
        sa.Column("delay", sa.Integer, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True),
    )
    op.create_index('ix_notifications_id', 'notifications', ['id'], unique=False)

    op.create_table(
        'delivery_logs',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('notification_id', sa.INTEGER(), nullable=False),
        sa.Column('status', sa.VARCHAR(length=20), nullable=False),
        sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('error_message', sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'], name='delivery_logs_notification_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='delivery_logs_pkey')
    )
    op.create_index('ix_delivery_logs_id', 'delivery_logs', ['id'], unique=False)


def downgrade():
    # Удаление новых таблиц
    op.drop_table('delivery_logs')
    op.drop_table('notifications')

    # Создание старых таблиц (если нужно откатиться назад)
    op.create_table(
        'messages',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('subject', sa.VARCHAR(length=255), nullable=True),
        sa.Column('message', sa.TEXT(), nullable=False),
        sa.Column('recipient', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('delay', sa.INTEGER(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )
    op.create_index('ix_messages_id', 'messages', ['id'], unique=False)

    op.create_table(
        'delivery_logs',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('message_id', sa.INTEGER(), nullable=False),
        sa.Column('status', sa.VARCHAR(length=20), nullable=False),
        sa.Column('timestamp', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('error_message', sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], name='delivery_logs_message_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='delivery_logs_pkey')
    )
    op.create_index('ix_delivery_logs_id', 'delivery_logs', ['id'], unique=False)
    # ### end Alembic commands ###
