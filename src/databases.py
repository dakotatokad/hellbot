import sqlite3
from warnings import deprecated

from . import classes

DEFAULT_DATABASE_PATH = "./data/hellbot.db"


def create_major_order_table(db_path: str = DEFAULT_DATABASE_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS major_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            briefing TEXT NOT NULL,
            reward_type_index INTEGER NOT NULL,
            reward_amount INTEGER NOT NULL,
            expiration TEXT NOT NULL,
            last_fetched TEXT NOT NULL,
            reward_type TEXT NOT NULL,
            ttl INTEGER NOT NULL,
            response_code INTEGER NOT NULL,
            active BOOLEAN NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@deprecated("Use insert_row instead.")
def add_major_order(order: classes.MajorOrder, db_path: str = DEFAULT_DATABASE_PATH):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO major_orders (
                order_id,
                briefing,
                reward_type_index, 
                reward_amount, 
                expiration, 
                last_fetched, 
                reward_type, 
                ttl, 
                response_code
                )
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                order.order_id, 
                order.briefing,
                order.reward_type_index, 
                order.reward_amount, 
                order.expiration, 
                order.last_fetched, 
                order.reward_type, 
                order.ttl, 
                order.response_code
                )
        )
        conn.commit()
        

def insert_row(table: str, db_path: str = DEFAULT_DATABASE_PATH, **kwargs):
    columns = ', '.join(kwargs.keys())
    placeholders = ', '.join(['?'] * len(kwargs))
    values = tuple(kwargs.values())
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values
        )
        conn.commit()
        

# TODO: Get all active orders

# TODO: Set expired orders to inactive


def get_active_orders(db_path: str = "./data/hellbot.db") -> list:
    with sqlite3.connect(db_path) as conn:     
        cursor = conn.cursor()
        cursor.execute("SELECT id, briefing, reward_amount, reward_type, expiration FROM major_orders WHERE active = 1")
        results = cursor.fetchall()
    
    return results
