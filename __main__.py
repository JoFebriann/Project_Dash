from argparse import ArgumentParser
from kink import di

from project_dash.ui import DashUI


if __name__ == "__main__":
    # Inisialisasikan objek ArgumentParser
    parser = ArgumentParser()
    
    # Simpan argument yang diberikan kepada parameter -db_init
    parser.add_argument("-db_init")
    di["db_init"]: str = parser.parse_args().db_init  # "True" or "False"
    di["db_filename"]: str = "dash.db"

    # Inisialisasikan objek DashUI
    dash_ui = di[DashUI]
    dash_ui.run()
