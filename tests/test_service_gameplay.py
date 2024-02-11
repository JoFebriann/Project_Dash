"""
Tests for ServiceGameplay
"""

from kink import di

from project_dash.dtos import GameOverDTO, RegisterDTO
from project_dash.persistences import DashSqlDb
from project_dash.services import ServiceGameplay

import os
import pygame as pg


di["db_init"] = "True"
di["db_filename"] = "test_service_gameplay.db"
di[DashSqlDb].db_path = os.path.join(di["main_dir"], "tests", di["db_filename"])


def test_should_reset_state():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_username = "Penguin"
    service_under_test.player_email = "pengu@gmail.com"
    service_under_test.score = 4
    service_under_test.reset("Kangaroo", "kanga@gmail.com")
    assert service_under_test.player_username, service_under_test.player_email == ('Kangaroo', 'kanga@gmail.com')


def test_play_mouse_click_when_penguin_is_not_jumping():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_logic.is_jumping = False
    service_under_test.player_logic.y_velocity = 100
    service_under_test.play_mouse_click()
    assert service_under_test.player_logic.is_jumping, service_under_test.player_logic.y_velocity == (True, 45)
    

def test_play_mouse_click_when_penguin_is_jumping():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_logic.is_jumping = True
    service_under_test.player_logic.y_velocity = 100
    service_under_test.play_mouse_click()
    assert service_under_test.player_logic.is_jumping, service_under_test.player_logic.y_velocity == (False, 100)
    
    
def test_update_gravity():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_logic.y_velocity = 20
    service_under_test.player_logic.rect.y = 25
    service_under_test.update_gravity()
    assert service_under_test.player_logic.y_velocity, service_under_test.player_logic.rect.y == (25, 50)


def test_update_player_ground_collision_where_player_above_ground():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_logic.rect.y = 30
    service_under_test.player_logic.is_jumping = True
    service_under_test.update_player_ground_collision()
    assert service_under_test.player_logic.rect.y, service_under_test.player_logic.is_jumping == (30, True)


def test_update_player_ground_collision_where_player_below_ground():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_logic.rect.y = 251
    service_under_test.player_logic.is_jumping = True
    service_under_test.update_player_ground_collision()
    assert service_under_test.player_logic.rect.y, service_under_test.player_logic.is_jumping == (250, False)


def test_update_tree_movement_if_not_out_of_screen():
    service_under_test = di[ServiceGameplay]
    service_under_test.tree_logic.rect.x = -90
    service_under_test.tree_logic.x_velocity = 5
    service_under_test.update_tree_movement()
    assert service_under_test.tree_logic.rect.x == -95


def test_update_tree_movement_if_out_of_screen():
    service_under_test = di[ServiceGameplay]
    service_under_test.tree_logic.rect.x = -120
    service_under_test.tree_logic.x_velocity = 5
    service_under_test.update_tree_movement()
    assert service_under_test.tree_logic.rect.x == 1100


def test_update_player_tree_when_collide():
    # Setup mock database
    di[DashSqlDb].setup_database()
    # Isi data sembarang untuk keperluan tes
    di[DashSqlDb].insert_acc("Robbie", "robinhood@yahoo.com", 12)
    di[DashSqlDb].insert_acc("Mech", "papiermecha@hotmail.com", 3)

    service_under_test = di[ServiceGameplay]
    service_under_test.player_username = "Mech"
    service_under_test.player_email = "papiermecha@hotmail.com"
    service_under_test.player_score = 15
    service_under_test.player_logic.rect = pg.rect.Rect(0, 0, 100, 100)
    service_under_test.tree_logic.rect = pg.rect.Rect(1, 1, 100, 100)
    update_output = service_under_test.update_player_tree_collision()
    assert update_output.final_score == 15

    di[DashSqlDb].delete_database()


def test_update_player_tree_when_not_collide():
    # Setup mock database
    di[DashSqlDb].setup_database()
    # Isi data sembarang untuk keperluan tes
    di[DashSqlDb].insert_acc("Robbie", "robinhood@yahoo.com", 12)
    di[DashSqlDb].insert_acc("Mech", "papiermecha@hotmail.com", 3)

    service_under_test = di[ServiceGameplay]
    service_under_test.player_username = "Mech"
    service_under_test.player_email = "papiermecha@hotmail.com"
    service_under_test.player_score = 15
    service_under_test.player_logic.rect = pg.rect.Rect(0, 0, 100, 100)
    service_under_test.tree_logic.rect = pg.rect.Rect(400, 400, 100, 100)
    update_output = service_under_test.update_player_tree_collision()
    assert update_output is None

    # Hapus mock database
    di[DashSqlDb].delete_database()


def test_update_point():
    service_under_test = di[ServiceGameplay]
    service_under_test.player_score = 4
    service_under_test.update_point()
    assert service_under_test.player_score == 5