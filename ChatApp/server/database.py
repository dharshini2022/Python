import sqlite3

connection = sqlite3.connect(".Message.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    user TEXT,
    room TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()


def save_message(user, room, message):
    cursor.execute(
        "INSERT INTO messages (user, room, message) VALUES (?, ?, ?)",
        (user, room, message)
    )
    connection.commit()

def get_last_messages(room, limit=50):
    cursor.execute(
        "SELECT user, message, timestamp FROM messages WHERE room = ? ORDER BY timestamp DESC LIMIT ?",
        (room, limit)
    )
    rows = cursor.fetchall()
    return [{"user": row[0], "message": row[1], "timestamp": row[2]} for row in reversed(rows)]