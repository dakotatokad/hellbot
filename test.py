from src import databases as db
from src import classes
from datetime import datetime, UTC

db_path = "./data/test_db.db"

db.create_major_order_table(db_path = db_path)

expires = "2025-05-30T14:28:16.3524321Z"
expires_dt = datetime.fromisoformat(expires[:26]).replace(tzinfo=UTC)

ex_class = classes.MajorOrder(
    1234,
    "Test Major Order",
    1,
    50,
    "2025-05-30T14:28:16.3524321Z",
    expires,
)

ex_class2 = classes.MajorOrder(
    567,
    "Test Major Order2",
    1,
    50,
    "2025-05-27T14:28:16.3524321Z",
    "2025-05-27T14:28:16.3524321Z",
)

db.insert_row("major_orders",
            db_path=db_path,
            order_id=ex_class.order_id,
            briefing=ex_class.briefing,
            reward_type_index=ex_class.reward_type_index,
            reward_amount=ex_class.reward_amount,
            expiration=ex_class.expiration,
            last_fetched=ex_class.last_fetched,
            reward_type=ex_class.reward_type,
            ttl=ex_class.ttl,
            response_code=ex_class.response_code,
            active=1,
            )

db.insert_row("major_orders",
            db_path=db_path,
            order_id=ex_class2.order_id,
            briefing=ex_class2.briefing,
            reward_type_index=ex_class2.reward_type_index,
            reward_amount=ex_class2.reward_amount,
            expiration=ex_class2.expiration,
            last_fetched=ex_class2.last_fetched,
            reward_type=ex_class2.reward_type,
            ttl=ex_class2.ttl,
            response_code=ex_class2.response_code,
            active=1,
            )

orders = db.get_active_orders(db_path=db_path)

print(orders)

db.set_expired_orders_to_inactive(db_path=db_path)

orders = db.get_active_orders(db_path=db_path)

print(orders)
