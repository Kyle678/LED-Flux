import sqlite3

# -----------------------
# RELATION CRUD
# -----------------------

# -----------------------
# CREATE
# -----------------------
def create_relation(db_name, cid, aid, start=0):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Relation (cid, aid, start) VALUES (?, ?, ?)",
        (cid, aid, start)
    )
    conn.commit()
    rid = cursor.lastrowid
    conn.close()
    return rid

# -----------------------
# READ
# -----------------------
def get_relation(db_name, rid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT rid, cid, aid, start FROM Relation WHERE id = ?", (rid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"rid": row[0], "cid": row[1], "aid": row[2], "start": row[3]}
    return None

def get_all_relations(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT rid, cid, aid, start FROM Relation")
    rows = cursor.fetchall()
    conn.close()
    return [{"rid": r[0], "cid": r[1], "aid": r[2], "start": r[3]} for r in rows]

# -----------------------
# UPDATE
# -----------------------
def update_relation(db_name, rid, cid=None, aid=None, start=None):
    conn = sqlite3.connect(db_name)
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
    sql = f"UPDATE Relation SET {', '.join(fields)} WHERE rid = ?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return get_relation(db_name, rid)

# -----------------------
# DELETE
# -----------------------
def delete_relation(db_name, rid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Relation WHERE rid = ?", (rid,))
    conn.commit()
    conn.close()
    return True

# -----------------------
# GET RELATIONS BY CONFIG
# -----------------------
def get_relations_by_config(db_name, cid):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT rid, cid, aid, start FROM Relation WHERE cid = ?", (cid,))
    rows = cursor.fetchall()
    conn.close()
    return [{"rid": r[0], "cid": r[1], "aid": r[2], "start": r[3]} for r in rows]