import pytest # pyright: ignore[reportMissingImports]
from backend.database.db_manager import DatabaseManager

@pytest.fixture
def db():
    # Use an in-memory database for isolation
    db = DatabaseManager("test.db")
    return db

# -----------------------
# Config Tests
# -----------------------
def test_create_get_config(db):
    cid = db.create_config("Test Config", "This is a test config")
    cfg = db.get_config(cid)
    assert cfg["name"] == "Test Config"
    assert cfg["description"] == "This is a test config"

def test_update_config(db):
    cid = db.create_config("Old Config", "Old Desc")
    db.update_config(cid, name="New Config", description="New Desc")
    cfg = db.get_config(cid)
    assert cfg["name"] == "New Config"
    assert cfg["description"] == "New Desc"

def test_delete_config(db):
    cid = db.create_config("To Delete", "Delete me")
    db.delete_config(cid)
    assert db.get_config(cid) is None

# -----------------------
# Animation Tests
# -----------------------
def test_create_get_animation(db):
    aid = db.create_animation("Anim", "Desc", 10, "type1")
    anim = db.get_animation(aid)
    assert anim["name"] == "Anim"
    assert anim["length"] == 10
    assert anim["type"] == "type1"

def test_update_animation(db):
    aid = db.create_animation("Old", "Old Desc", 5, "type0")
    db.update_animation(aid, name="New", description="New Desc", length=20, type="type2")
    anim = db.get_animation(aid)
    assert anim["name"] == "New"
    assert anim["length"] == 20
    assert anim["type"] == "type2"

def test_delete_animation(db):
    aid = db.create_animation("To Delete", "Delete", 5, "typeX")
    db.delete_animation(aid)
    assert db.get_animation(aid) is None

# -----------------------
# Relation Tests
# -----------------------
def test_create_get_relation(db):
    cid = db.create_config("Cfg", "Desc")
    aid = db.create_animation("Anim", "Desc", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    rel = db.get_relation(rid)
    assert rel["cid"] == cid
    assert rel["aid"] == aid
    assert rel["start"] == 0

def test_update_relation(db):
    cid = db.create_config("Cfg", "Desc")
    aid = db.create_animation("Anim", "", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    db.update_relation(rid, start=5)
    rel = db.get_relation(rid)
    assert rel["start"] == 5

def test_delete_relation(db):
    cid = db.create_config("Cfg", "Desc")
    aid = db.create_animation("Anim", "", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    db.delete_relation(rid)
    assert db.get_relation(rid) is None

# -----------------------
# Parameter Tests
# -----------------------
def test_create_get_parameter(db):
    aid = db.create_animation("Anim", "Desc", 10, "type1")
    pid = db.create_parameter(aid, "key1", "int", int_value=42)
    params = db.get_parameters(aid)
    assert params["key1"] == 42

def test_update_parameter(db):
    aid = db.create_animation("Anim", "Desc", 10, "type1")
    db.create_parameter(aid, "key1", "int", int_value=42)
    db.update_parameter(aid, "key1", "int", 100)
    params = db.get_parameters(aid)
    assert params["key1"] == 100

def test_delete_parameter(db):
    aid = db.create_animation("Anim", "Desc", 10, "type1")
    db.create_parameter(aid, "key1", "int", int_value=42)
    db.delete_parameter(aid, "key1")
    params = db.get_parameters(aid)
    assert "key1" not in params
