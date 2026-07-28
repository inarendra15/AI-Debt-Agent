# In-memory conversation storage

conversation_store = {}


def get_history(customer_id: int):
    return conversation_store.get(customer_id, [])


def add_message(customer_id: int, role: str, message: str):

    if customer_id not in conversation_store:
        conversation_store[customer_id] = []

    conversation_store[customer_id].append(
        {
            "role": role,
            "message": message
        }
    )


def clear_history(customer_id: int):
    conversation_store.pop(customer_id, None)