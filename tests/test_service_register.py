"""
Tests for ServiceRegister
"""

from kink import di

from project_dash.dtos import GameOverDTO, LoginDTO, RegisterDTO, SwitchSceneDTO  # , LoginDTO
from project_dash.persistences import DashSqlDb
from project_dash.services import ServiceRegister

import os
import pygame as pg


di["db_init"] = "True"
di["db_filename"] = "test_service_register.db"
di[DashSqlDb].db_path = os.path.join(di["main_dir"], "tests", di["db_filename"])


def test_register_successful():
    # Setup mock database
    di[DashSqlDb].setup_database()

    service_under_test = di[ServiceRegister]
    temp_username = 'Penguin'
    temp_email = 'pengu@gmail.com'
    registration_output = service_under_test.register_acc(RegisterDTO(temp_username, temp_email))
    db_result = di[DashSqlDb].get_exact_player(temp_username)
    username_from_db = db_result.name
    email_from_db = db_result.email
    score_from_db = db_result.score
    assert (type(registration_output), registration_output.scene_name, username_from_db, email_from_db, score_from_db) == (SwitchSceneDTO, "gameplay", temp_username, temp_email, 0)

    # Hapus mock database
    di[DashSqlDb].delete_database()


def test_login_successful():
    # Setup mock database
    di[DashSqlDb].setup_database()
    # Isi data sembarang untuk keperluan tes
    di[DashSqlDb].insert_acc("Penguin", "robinhood@yahoo.com", 12)

    service_under_test = di[ServiceRegister]
    temp_username = 'Penguin'
    login_output = service_under_test.login_acc(LoginDTO(temp_username))
    assert (type(login_output), login_output.scene_name) == (SwitchSceneDTO, "gameplay")

    # Hapus mock database
    di[DashSqlDb].delete_database()


def test_check_username_in_db():
    # Setup mock database
    di[DashSqlDb].setup_database()
    # Isi data sembarang untuk keperluan tes
    di[DashSqlDb].insert_acc("Kangaroo", "kanga@gmail.com", 12)
    
    service_under_test = di[ServiceRegister]
    
    assert service_under_test.check_username_in_db("Kangaroo") == True

    # Hapus mock database
    di[DashSqlDb].delete_database()

def test_check_username_not_in_db():
    # Setup mock database
    di[DashSqlDb].setup_database()
    # Isi data sembarang untuk keperluan tes
    di[DashSqlDb].insert_acc("Kangaroo", "kanga@gmail.com", 12)

    service_under_test = di[ServiceRegister]

    assert service_under_test.check_username_in_db("Squidward") == False

    # Hapus mock database
    di[DashSqlDb].delete_database()