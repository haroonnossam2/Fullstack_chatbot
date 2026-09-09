from sqlalchemy import text

from app.database.db import engine


def save_message(
    conversation_id: str,
    role: str,
    content: str,
    agent: str | None = None,
):
    query = text("""
        INSERT INTO conversation_messages
        (
            conversation_id,
            role,
            content,
            agent
        )
        VALUES
        (
            :conversation_id,
            :role,
            :content,
            :agent
        )
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "agent": agent,
            },
        )


def get_recent_messages(
    conversation_id: str,
    limit: int = 10,
):
    query = text("""
        SELECT
            role,
            content,
            agent,
            created_at
        FROM conversation_messages
        WHERE conversation_id = :conversation_id
        ORDER BY created_at DESC, id DESC
        LIMIT :limit
    """)

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            {
                "conversation_id": conversation_id,
                "limit": limit,
            },
        ).mappings().all()

    # We selected newest first.
    # Reverse so LangGraph receives
    # messages in conversation order.
    return list(reversed(rows))


def delete_old_messages(
    conversation_id: str,
    keep: int = 10,
):
    query = text("""
        DELETE FROM conversation_messages
        WHERE conversation_id = :conversation_id
        AND id NOT IN (
            SELECT id
            FROM conversation_messages
            WHERE conversation_id = :conversation_id
            ORDER BY created_at DESC, id DESC
            LIMIT :keep
        )
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "conversation_id": conversation_id,
                "keep": keep,
            },
        )