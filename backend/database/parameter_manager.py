import sqlite3

DB_NAME = "leds.db"

# -----------------------
# PARAMETERS CRUD
# -----------------------
def add_parameter(animation_id, key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    int_val = float_val = text_val = bool_val = None
    if isinstance(value, bool):
        bool_val = 1 if value else 0
    elif isinstance(value, int):
        int_val = value
    elif isinstance(value, float):
        float_val = value
    else:
        text_val = str(value)
    cursor.execute(
        "INSERT INTO Parameter (animation_id, key, int_value, float_value, text_value, bool_value) VALUES (?, ?, ?, ?, ?, ?)",
        (animation_id, key, int_val, float_val, text_val, bool_val)
    )
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return pid

def get_parameters(animation_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT key, int_value, float_value, text_value, bool_value FROM Parameter WHERE animation_id = ?",
        (animation_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    params = {}
    for key, int_val, float_val, text_val, bool_val in rows:
        if int_val is not None:
            params[key] = int_val
        elif float_val is not None:
            params[key] = float_val
        elif text_val is not None:
            params[key] = text_val
        elif bool_val is not None:
            params[key] = bool_val == 1
    return params

def update_parameter(animation_id, key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    int_val = float_val = text_val = bool_val = None
    if isinstance(value, bool):
        bool_val = 1 if value else 0
    elif isinstance(value, int):
        int_val = value
    elif isinstance(value, float):
        float_val = value
    else:
        text_val = str(value)
    cursor.execute("""
        UPDATE Parameter
        SET int_value = ?, float_value = ?, text_value = ?, bool_value = ?
        WHERE animation_id = ? AND key = ?
    """, (int_val, float_val, text_val, bool_val, animation_id, key))
    conn.commit()
    conn.close()
    return True

def delete_parameter(animation_id, key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Parameter WHERE animation_id = ? AND key = ?", (animation_id, key))
    conn.commit()
    conn.close()
    return True