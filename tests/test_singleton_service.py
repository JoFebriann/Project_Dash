from kink import di


from project_dash.ui import DashUI
from project_dash.persistences import DashSqlDb
from project_dash.services import DashService

import os


di["db_init"] = "True"
di["db_filename"] = "test_singleton.db"
di[DashSqlDb].db_path = os.path.join(di["main_dir"], "tests", di["db_filename"])

# Setup mock database
di[DashSqlDb].setup_database()


def test_if_ui_accesses_the_correct_service_layer():
    service_id = id(di[DashService])
    service_id_according_to_service = id(di[DashUI].service)
    assert service_id == service_id_according_to_service


# Hapus mock database
di[DashSqlDb].delete_database()
