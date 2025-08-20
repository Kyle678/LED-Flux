import sqlite3

DB_NAME = "animations.db"

# -----------------------
# CREATE
# -----------------------
def create_config(name, description=None):
    conn = sqlite3.connect(DB_NAME)
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
def get_config(cid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT cid, name, description FROM Config WHERE cid = ?", (cid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"cid": row[0], "name": row[1], "description": row[2]}
    return None

def get_all_configs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT cid, name, description FROM Config")
    rows = cursor.fetchall()
    conn.close()
    return [{"cid": r[0], "name": r[1], "description": r[2]} for r in rows]

# -----------------------
# UPDATE
# -----------------------
def update_config(cid, name=None, description=None):
    conn = sqlite3.connect(DB_NAME)
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
    return True

# -----------------------
# DELETE
# -----------------------
def delete_config(cid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Config WHERE cid = ?", (cid,))
    conn.commit()
    conn.close()
    return True