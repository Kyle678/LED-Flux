from backend.database.init_db import init_db
from backend.database.animation_manager import *
from backend.database.config_manager import *
from backend.database.relation_manager import *

import os

class DatabaseManager:
    def __init__(self, db_name="leds.db"):
        self.db_name = os.path.join("backend", "database", db_name)
        if not os.path.exists(self.db_name):
            init_db(self.db_name)

    # Config methods
    def create_config(self, name, description):
        return create_config(self.db_name, name, description)

    def get_config(self, cid):
        return get_config(self.db_name, cid)

    def get_all_configs(self):
        return get_all_configs(self.db_name)
    
    def update_config(self, cid, name=None, description=None):
        return update_config(self.db_name, cid, name, description)
    
    def delete_config(self, cid):
        return delete_config(self.db_name, cid)

    # Animation methods
    def create_animation(self, name, description, length, type):
        return create_animation(self.db_name, name, description, length, type)

    def get_animation(self, aid):
        return get_animation(self.db_name, aid)
    
    def update_animation(self, aid, name=None, description=None, length=None, type=None):
        return update_animation(self.db_name, aid, name, description, length, type)
    
    def delete_animation(self, aid):
        return delete_animation(self.db_name, aid)

    # Relation methods
    def create_relation(self, cid, aid, start):
        return create_relation(self.db_name, cid, aid, start)
    
    def get_relation(self, rid):
        return get_relation(self.db_name, rid)
    
    def update_relation(self, rid, cid=None, aid=None, start=None):
        return update_relation(self.db_name, rid, cid, aid, start)
    
    def delete_relation(self, rid):
        return delete_relation(self.db_name, rid)
    
