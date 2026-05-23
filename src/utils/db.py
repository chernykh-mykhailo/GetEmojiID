import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "settings.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                show_bound_emoji INTEGER DEFAULT 1,
                show_emoji_text INTEGER DEFAULT 1
            )
        """)
        await db.commit()

async def get_user_settings(user_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT show_bound_emoji, show_emoji_text FROM user_settings WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "show_bound_emoji": bool(row[0]),
                    "show_emoji_text": bool(row[1])
                }
            else:
                # Default settings: both True by default
                return {
                    "show_bound_emoji": True,
                    "show_emoji_text": True
                }

async def update_user_settings(user_id: int, show_bound_emoji: bool, show_emoji_text: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_settings (user_id, show_bound_emoji, show_emoji_text)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                show_bound_emoji = excluded.show_bound_emoji,
                show_emoji_text = excluded.show_emoji_text
        """, (user_id, int(show_bound_emoji), int(show_emoji_text)))
        await db.commit()
