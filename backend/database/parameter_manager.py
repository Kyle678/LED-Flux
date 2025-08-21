import sqlite3

# -----------------------
# PARAMETERS CRUD
# -----------------------

# -----------------------
# CREATE
# -----------------------
def create_parameter(db_name, aid, key, type, int_value=None, float_value=None, text_value=None, bool_value=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Parameter (animation_id, key, type, int_value, float_value, text_value, bool_value) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (aid, key, type, int_value, float_value, text_value, bool_value)
    )
    conn.commit()
    pid = cursor.lastrowid
    conn.close()
    return pid

# -----------------------
# READ
# -----------------------
def get_parameters(db_name, animation_id):
    conn = sqlite3.connect(db_name)
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

# -----------------------
# UPDATE
# -----------------------
def update_parameter(db_name, animation_id, key, type, value):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    int_val = float_val = text_val = bool_val = None
    if type == "bool":
        bool_val = 1 if value else 0
    elif type == "int":
        int_val = value
    elif type == "float":
        float_val = value
    else:
        text_val = str(value)
    cursor.execute("""
        UPDATE Parameter
        SET int_value = ?, float_value = ?, text_value = ?, bool_value = ?, type = ?
        WHERE animation_id = ? AND key = ?
    """, (int_val, float_val, text_val, bool_val, type, animation_id, key))
    conn.commit()
    conn.close()
    return 

# -----------------------
# DELETE
# -----------------------
def delete_parameter(db_name, animation_id, key):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Parameter WHERE animation_id = ? AND key = ?", (animation_id, key))
    conn.commit()
    conn.close()
    return True