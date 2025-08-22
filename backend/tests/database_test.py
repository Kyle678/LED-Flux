import pytest # pyright: ignore[reportMissingImports]
from backend.database.db_manager import DatabaseManager

# Test cases for DatabaseManager

@pytest.fixture
def db():
    # Use an in-memory database for isolation
    db = DatabaseManager("test.db")
    return db

# Config Tests
def test_create_config(db):
    # Test creating a new config
    cid = db.create_config("Test Config", "This is a test config")
    assert cid is not None

def test_get_config(db):
    # Test retrieving a config
    cid = db.create_config("Test Config", "This is a test config")
    config = db.get_config(cid)
    assert config['name'] == "Test Config"
    assert config['description'] == "This is a test config"

def test_update_config(db):
    # Test updating a config
    cid = db.create_config("Test Config", "This is a test config")
    updated_config = db.update_config(cid, name="Updated Config", description="Updated description")
    assert updated_config['name'] == "Updated Config"
    assert updated_config['description'] == "Updated description"

def test_delete_config(db):
    # Test deleting a config
    cid = db.create_config("Test Config", "This is a test config")
    db.delete_config(cid)
    config = db.get_config(cid)
    assert config is None  # Should return None after deletion

# Animation Tests
def test_create_animation(db):
    # Test creating a new animation
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    assert aid is not None

def test_get_animation(db):
    # Test retrieving an animation
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    animation = db.get_animation(aid)
    assert animation['name'] == "Test Animation"
    assert animation['description'] == "This is a test animation"
    assert animation['length'] == 10
    assert animation['type'] == "type1"

def test_update_animation(db):
    # Test updating an animation
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    updated_animation = db.update_animation(aid, name="Updated Animation", description="Updated description", length=20, type="type2")
    assert updated_animation['name'] == "Updated Animation"
    assert updated_animation['description'] == "Updated description"
    assert updated_animation['length'] == 20
    assert updated_animation['type'] == "type2"

def test_delete_animation(db):
    # Test deleting an animation
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    db.delete_animation(aid)
    animation = db.get_animation(aid)
    assert animation is None  # Should return None after deletion

# Relation Tests
def test_create_relation(db):
    # Test creating a new relation
    cid = db.create_config("Test Config", "This is a test config")
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    assert rid is not None

def test_get_relation(db):
    # Test retrieving a relation
    cid = db.create_config("Test Config", "This is a test config")
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    relation = db.get_relation(rid)
    assert relation['cid'] == cid
    assert relation['aid'] == aid
    assert relation['start'] == 0

def test_update_relation(db):
    # Test updating a relation
    cid = db.create_config("Test Config", "This is a test config")
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    updated_relation = db.update_relation(rid, start=5)
    assert updated_relation['start'] == 5

def test_delete_relation(db):
    # Test deleting a relation
    cid = db.create_config("Test Config", "This is a test config")
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    rid = db.create_relation(cid, aid, 0)
    db.delete_relation(rid)
    relation = db.get_relation(rid)
    assert relation is None  # Should return None after deletion

def test_create_parameter(db):
    # Test creating a new parameter
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    pid = db.create_parameter(aid, "test_key", "int", int_value=42)
    assert pid is not None

def test_get_parameters(db):
    # Test retrieving parameters for an animation
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    db.create_parameter(aid, "test_key1", "int", int_value=42)
    db.create_parameter(aid, "test_key2", "float", float_value=3.14)
    params = db.get_parameters(aid)
    assert params["test_key1"] == 42
    assert params["test_key2"] == 3.14

def test_update_parameter(db):
    # Test updating a parameter
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    db.create_parameter(aid, "test_key", "int", int_value=42)
    db.update_parameter(aid, "test_key", "int", 100)
    params = db.get_parameters(aid)
    assert params["test_key"] == 100

def test_delete_parameter(db):
    # Test deleting a parameter
    aid = db.create_animation("Test Animation", "This is a test animation", 10, "type1")
    pid = db.create_parameter(aid, "test_key", "int", int_value=42)
    db.delete_parameter(aid, "test_key")
    params = db.get_parameters(aid)
    assert "test_key" not in params  # Should not exist after deletion