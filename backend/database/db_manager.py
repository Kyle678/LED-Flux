from init_db import init_db
from animation_manager import *
from config_manager import *
from parameter_manager import *
from relation_manager import *

def initialize_database():
    init_db("leds.db")  # Initialize the database with the specified name

