import logging
import sqlite3
from datetime import UTC, datetime
from warnings import deprecated

from . import classes

logger = logging.getLogger(__name__)

DEFAULT_DATABASE_PATH = "./data/hellbot.db"

def create_database_tables(db_path: str = DEFAULT_DATABASE_PATH):
    create_major_order_table(db_path)


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
        

async def insert_row(table: str, db_path: str = DEFAULT_DATABASE_PATH, **kwargs):
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


async def get_active_orders(db_path: str = "./data/hellbot.db") -> list[tuple]:
    """
    Retrieve all active major orders from the database.

    Args:
        db_path (str, optional): The location of the database. Defaults to "./data/hellbot.db".

    Returns:
        list[tuple]: A list of tuples containing the active major orders ordered respectively:
            - Key
            - Order Briefing
            - Reward Amount
            - Reward Type
            - Expiration Date
    """
    with sqlite3.connect(db_path) as conn:     
        cursor = conn.cursor()
        cursor.execute("SELECT id, briefing, reward_amount, reward_type, expiration FROM major_orders WHERE active = 1")
        results = cursor.fetchall()
    
    return results


async def set_expired_orders_to_inactive(db_path: str = "./data/hellbot.db"):
    """
    Set all expired major orders to inactive in the database.

    Args:
        db_path (str, optional): The location of the database. Defaults to "./data/hellbot.db".
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, expiration FROM major_orders WHERE active = 1")
        orders = cursor.fetchall()

        for order_id, expiration in orders:
            if (datetime.now(UTC).fromisoformat(expiration[:26]).replace(tzinfo=UTC)) <= datetime.now(UTC):
                logger.debug("Setting order %d to inactive due to expiration.", order_id)
                cursor.execute(f"UPDATE major_orders SET active = 0 WHERE id = {order_id}")
                conn.commit()


async def last_fetched_a_day_ago(db_path: str = "./data/hellbot.db") -> bool:
    """
    Check if the last fetched time for any major order is more than a day ago.

    Args:
        db_path (str, optional): The location of the database. Defaults to "./data/hellbot.db".

    Returns:
        bool: True if any order was last fetched more than a day ago, False otherwise.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_fetched FROM major_orders WHERE active = 1")
        orders = cursor.fetchall()

        for last_fetched in orders:
            last_fetched_dt = datetime.fromisoformat(last_fetched[0][:26]).replace(tzinfo=UTC)
            if (datetime.now(UTC) - last_fetched_dt).days > 1:
                logger.debug("Order was last fetched more than a day ago, updating cache.")
                return True
            
    logger.debug("All orders were last fetched within the last day.")
    return False


async def get_major_order_ids(db_path: str = "./data/hellbot.db") -> list[int]:
    """
    Retrieve all active major order IDs from the database.

    Args:
        db_path (str, optional): The location of the database. Defaults to "./data/hellbot.db".

    Returns:
        list[int]: A list of active major order IDs.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT order_id FROM major_orders")
        results = cursor.fetchall()
        
    flattened_results = [row[0] for row in results]
    
    return flattened_results
