"""
Tests for ServiceHighScore
"""

from kink import di

from project_dash.dtos import *
from project_dash.persistences import DashSqlDb
from project_dash.services import ServiceHighScore
from project_dash.dtos import LeaderboardDTO

import os
import pygame as pg


di["db_init"] = "True"
di["db_filename"] = "test_service_highscore.db"
di[DashSqlDb].db_path = os.path.join(di["main_dir"], "tests", di["db_filename"])


def test_should_get_leaderboards():
    # Setup mock database
    di[DashSqlDb].setup_database()
    
    # Isi data sembarang untuk keperluan tes
    di[DashSqlDb].insert_acc("Penguin", "pengu@gmail.com", 5)
    di[DashSqlDb].insert_acc("PenguinB", "pengub@gmail.com", 2)
    
    service_under_test = di[ServiceHighScore]

    lb = service_under_test.get_leaderboards()
    
    assert type(lb[0]) == LeaderboardDTO and type(lb[1]) == LeaderboardDTO and lb[0].username == "Penguin" and lb[0].score == 5 and lb[1].username == "PenguinB" and lb[1].score == 2

    # Hapus mock database
    di[DashSqlDb].delete_database()
