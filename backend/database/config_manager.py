import sqlite3

# -----------------------
# CREATE
# -----------------------
def create_config(db_name, name, description=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Config (name, description) VALUES (?, ?)",
        (name, description)
    )
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid  # return the new config id

# -----------------------
# READ
# -----------------------
def get_config(db_name, cid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT cid, name, description FROM Config WHERE cid = ?", (cid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"cid": row[0], "name": row[1], "description": row[2]}
    return None

def get_all_configs(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT cid, name, description FROM Config")
    rows = cursor.fetchall()
    conn.close()
    return [{"cid": r[0], "name": r[1], "description": r[2]} for r in rows]

# -----------------------
# UPDATE
# -----------------------
def update_config(db_name, cid, name=None, description=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Only update provided fields
    if name and description:
        cursor.execute(
            "UPDATE Config SET name = ?, description = ? WHERE cid = ?",
            (name, description, cid)
        )
    elif name:
        cursor.execute("UPDATE Config SET name = ? WHERE cid = ?", (name, cid))
    elif description:
        cursor.execute("UPDATE Config SET description = ? WHERE cid = ?", (description, cid))
    else:
        conn.close()
        return False  # nothing to update
    conn.commit()
    conn.close()
    return get_config(db_name, cid)

# -----------------------
# DELETE
# -----------------------
def delete_config(db_name, cid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Config WHERE cid = ?", (cid,))
    conn.commit()
    conn.close()
    return True