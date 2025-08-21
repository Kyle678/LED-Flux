# animation_manager.py
import sqlite3

# -----------------------
# ANIMATION CRUD
# -----------------------

# -----------------------
# CREATE
# -----------------------
def create_animation(db_name, name, description=None, length=None, type_=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Animation (name, description, length, type) VALUES (?, ?, ?, ?)",
        (name, description, length, type_)
    )
    conn.commit()
    aid = cursor.lastrowid
    conn.close()
    return aid

# -----------------------
# READ
# -----------------------
def get_animation(db_name, aid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT aid, name, description, length, type FROM Animation WHERE aid = ?", (aid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"aid": row[0], "name": row[1], "description": row[2], "length": row[3], "type": row[4]}
    return None

def get_all_animations(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT aid, name, description, length, type FROM Animation")
    rows = cursor.fetchall()
    conn.close()
    return [{"aid": r[0], "name": r[1], "description": r[2], "length": r[3], "type": r[4]} for r in rows]

# -----------------------
# UPDATE
# -----------------------
def update_animation(db_name, aid, name=None, description=None, length=None, type_=None):
    conn = sqlite3.connect(db_name)
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
    return get_animation(db_name, aid)

# -----------------------
# DELETE
# -----------------------
def delete_animation(db_name, aid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Animation WHERE aid = ?", (aid,))
    conn.commit()
    conn.close()
    return True
