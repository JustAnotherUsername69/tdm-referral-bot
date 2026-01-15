import psycopg2
from bot.config import DB_CONFIG

def get_conn():
    return psycopg2.connect(**DB_CONFIG)
