import time
import psycopg2
from telegram import Bot
from bot.config import BOT_TOKEN, BROADCAST_LOG_CHANNEL, DB_CONFIG

bot = Bot(BOT_TOKEN)

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

while True:
    cur.execute("SELECT id, payload_type, payload_text, payload_file_id FROM broadcasts WHERE status='pending' LIMIT 1")
    row = cur.fetchone()

    if not row:
        time.sleep(5)
        continue

    bid, ptype, text, file_id = row
    cur.execute("UPDATE broadcasts SET status='running' WHERE id=%s", (bid,))
    conn.commit()

    cur.execute("INSERT INTO broadcast_recipients (broadcast_id, user_id) SELECT %s, user_id FROM users", (bid,))
    conn.commit()

    cur.execute("SELECT id, user_id FROM broadcast_recipients WHERE broadcast_id=%s", (bid,))
    for rid, uid in cur.fetchall():
        try:
            bot.send_message(uid, text)
            cur.execute("UPDATE broadcast_recipients SET status='sent' WHERE id=%s", (rid,))
        except Exception as e:
            cur.execute("UPDATE broadcast_recipients SET status='failed', error=%s WHERE id=%s", (str(e), rid))
        conn.commit()
        time.sleep(0.2)

    cur.execute("UPDATE broadcasts SET status='done' WHERE id=%s", (bid,))
    conn.commit()

    bot.send_message(BROADCAST_LOG_CHANNEL, f"Broadcast {bid} completed.")
