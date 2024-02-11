"""
Tests for Persistence Layer Singletonness
"""

from kink import di

from project_dash.services import ServiceGameplay, ServiceRegister, ServiceHighScore, DashService
from project_dash.persistences import DashSqlDb

import os


di["db_init"] = "True"
di["db_filename"] = "test_singleton.db"
di[DashSqlDb].db_path = os.path.join(di["main_dir"], "tests", di["db_filename"])

# Setup mock database
di[DashSqlDb].setup_database()


def test_if_gameplay_service_accesses_the_correct_persistence_layer():
    database_id = id(di[DashSqlDb])
    database_id_according_to_gameplay_service = id(di[ServiceGameplay].dash_db)
    assert database_id == database_id_according_to_gameplay_service


def test_if_register_service_accesses_the_correct_persistence_layer():
    database_id = id(di[DashSqlDb])
    database_id_according_to_register_service = id(di[ServiceRegister].dash_db)
    assert database_id == database_id_according_to_register_service


def test_if_highscore_service_accesses_the_correct_persistence_layer():
    database_id = id(di[DashSqlDb])
    database_id_according_to_highscore_service = id(di[ServiceHighScore].dash_db)
    assert database_id == database_id_according_to_highscore_service


# Hapus mock database
di[DashSqlDb].delete_database()