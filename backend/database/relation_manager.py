import sqlite3

DB_NAME = "leds.db"

# -----------------------
# RELATION CRUD
# -----------------------
def create_relation(cid, aid, start=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Relation (cid, aid, start) VALUES (?, ?, ?)",
        (cid, aid, start)
    )
    conn.commit()
    rid = cursor.lastrowid
    conn.close()
    return rid

def get_relation(rid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, cid, aid, start FROM Relation WHERE id = ?", (rid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "cid": row[1], "aid": row[2], "start": row[3]}
    return None

def get_all_relations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, cid, aid, start FROM Relation")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "cid": r[1], "aid": r[2], "start": r[3]} for r in rows]

def update_relation(rid, cid=None, aid=None, start=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fields = []
    values = []
    if cid is not None:
        fields.append("cid = ?")
        values.append(cid)
    if aid is not None:
        fields.append("aid = ?")
        values.append(aid)
    if start is not None:
        fields.append("start = ?")
        values.append(start)
    if not fields:
        conn.close()
        return False
    values.append(rid)
    sql = f"UPDATE Relation SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return True

def delete_relation(rid):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Relation WHERE id = ?", (rid,))
    conn.commit()
    conn.close()
    return True