# animation_manager.py
import sqlite3

DB_NAME = "animations.db"

# -----------------------
# ANIMATION CRUD
# -----------------------
def create_animation(name, description=None, length=None, type_=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Animation (name, description, length, type) VALUES (?, ?, ?, ?)",
        (name, description, length, type_)
    )
    conn.commit()
    aid = cursor.lastrowid
    conn.close()
    return aid

def get_animation(aid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT aid, name, description, length, type FROM Animation WHERE aid = ?", (aid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"aid": row[0], "name": row[1], "description": row[2], "length": row[3], "type": row[4]}
    return None

def get_all_animations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT aid, name, description, length, type FROM Animation")
    rows = cursor.fetchall()
    conn.close()
    return [{"aid": r[0], "name": r[1], "description": r[2], "length": r[3], "type": r[4]} for r in rows]

def update_animation(aid, name=None, description=None, length=None, type_=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fields = []
    values = []
    if name:
        fields.append("name = ?")
        values.append(name)
    if description:
        fields.append("description = ?")
        values.append(description)
    if length is not None:
        fields.append("length = ?")
        values.append(length)
    if type_:
        fields.append("type = ?")
        values.append(type_)
    if not fields:
        conn.close()
        return False
    values.append(aid)
    sql = f"UPDATE Animation SET {', '.join(fields)} WHERE aid = ?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return True

def delete_animation(aid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Animation WHERE aid = ?", (aid,))
    conn.commit()
    conn.close()
    return True

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
