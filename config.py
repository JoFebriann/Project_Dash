from kink import di

import os


# OS file system
di["main_dir"] = os.path.split(os.path.abspath(__file__))[0]
di["assets_dir"] = os.path.join(di["main_dir"], "assets")

# Ukuran
di["width"] = 900
di["height"] = 500

# Warna (berupa tupel Red-Green-Blue)
di["clr_black"] = (0, 0, 0)
di["clr_blurple"] = (17, 38, 59)
di["clr_dark_blue"] = (43, 49, 141)
di["clr_light_grey"] = (21, 222, 236)
di["clr_white"] = (255, 255, 255)
di["clr_red"] = (232, 37, 37)
di["clr_yellow"] = (252, 175, 23)

# Background music
di["bgm"] = os.path.join(di["main_dir"], "assets", "snd_bgm.ogg")

# Email
di["sender"] = 'timothyrt01@gmail.com'
di["password"] = 'xvwd gkcz ibxv jler'