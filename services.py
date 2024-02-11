from abc import ABC, abstractmethod
from kink import inject, di
from random import randint

from project_dash.dtos import GameOverDTO, LoginDTO, RegisterDTO, SoundDTO, SwitchSceneDTO, UserDTO, WarningDTO
from project_dash.email_sender import EmailSender
from project_dash.persistences import DashSqlDb

import pygame as pg


@inject
class PlayerLogic:
    def __init__(self) -> None:
        self.rect = pg.rect.Rect(100, 60, 144, 142)
        self.y_velocity = 0
        self.is_jumping = True

    def reset(self) -> None:
        self.rect = pg.rect.Rect(100, 60, 144, 142)
        self.y_velocity = 0
        self.is_jumping = True


@inject
class TreeLogic:
    def __init__(self) -> None:
        self.rect = pg.rect.Rect(600, 222, 78, 170)
        self.x_velocity = 20

    def reset(self) -> None:
        self.rect = pg.rect.Rect(600, 222, 78, 170)


@inject
class ServiceGameplay:
    ground_level = 250

    def __init__(self, _dash_db: DashSqlDb, _player_logic: PlayerLogic, _tree_logic: TreeLogic) -> None:
        self.dash_db = _dash_db
        self.player_username = ""
        self.email = ""
        self.player_score = 0 # tempat hold score sampai restart ulang

        self.player_logic = _player_logic
        self.tree_logic = _tree_logic
        self.subj = di[LeaderboardsSubject]

    def reset(self, _username: str, _email: str):
        self.player_username = _username
        self.player_email = _email
        self.player_score = 0
        
        self.player_logic.reset()
        self.tree_logic.reset()

    def play_mouse_click(self):
        if not self.player_logic.is_jumping:
            self.player_logic.is_jumping = True
            self.player_logic.y_velocity = -55

    def update_gravity(self):
        self.player_logic.y_velocity += 5
        self.player_logic.rect.y += self.player_logic.y_velocity

    def update_player_ground_collision(self):
        if self.player_logic.rect.y > ServiceGameplay.ground_level:
        # if player is lower than ground
            # then set player on ground
            self.player_logic.rect.y = ServiceGameplay.ground_level
            self.player_logic.is_jumping = False

    def update_tree_movement(self):
        self.tree_logic.rect.x -= self.tree_logic.x_velocity
        if self.tree_logic.rect.x < -100: # true kalau hasil kurangnya < -100, kalau yes > -100
            self.update_point()
            self.tree_logic.rect.x = 1100
            return SoundDTO(self.player_score)
        
    def update_player_tree_collision(self):
        if self.player_logic.rect.colliderect(self.tree_logic.rect):
            self.subj.notify(UserDTO(self.player_username, self.player_email, self.player_score),
                             self.dash_db.get_top_player())
            self.dash_db.add_score(self.player_username, self.player_score)
            return GameOverDTO(self.player_score)

    def update(self):
        self.update_gravity()
        self.update_player_ground_collision()

        update_output = self.update_tree_movement()
        if update_output is not None:
            return update_output
        
        update_output = self.update_player_tree_collision()
        if update_output is not None:
            return update_output

        # # increase player score for debug purpose
        # if randint(0, 60) == 0:  # remove later
        #     self.player_score += 1

    def update_point(self):
        self.player_score += 1


@inject
class ServiceRegister:
    def __init__(self, _dash_db: DashSqlDb, _service_gameplay: ServiceGameplay):
        self.dash_db = _dash_db
        self.service_gameplay = _service_gameplay
        self.subj_register = di[RegisterSubject]
        self.subj_login = di[LoginSubject]

    # bagian user data
    def register_acc(self, _register_dto: RegisterDTO) -> (SwitchSceneDTO | WarningDTO):
        temp_username: str = _register_dto.username
        temp_email: str = _register_dto.email
        player_is_in_db: bool = self.check_username_in_db(temp_username)

        subject_output = self.subj_register.notify(temp_username, temp_email, player_is_in_db)
        if subject_output is not None:
            return subject_output
        
        self.dash_db.register_acc(_register_dto)
        self.service_gameplay.reset(temp_username, temp_email)
        return SwitchSceneDTO("gameplay")

        # # jika username/email tidak diisi
        # if len(temp_username) == 0:
        #     return WarningDTO(WarningDTO.username_empty)
            
        # if len(temp_email) == 0:
        #     return WarningDTO(WarningDTO.email_empty)

        # # jika email invalid
        # if temp_email[len(temp_email) - 10:len(temp_email)] != "@gmail.com":
        #     return WarningDTO(WarningDTO.email_invalid)

        # # jika username sudah ada di database
        # if self.check_username_in_db(temp_username) is True:
        #     return WarningDTO(WarningDTO.username_already_registered)

        # jika username tidak ada di database


    def login_acc(self, _login_dto: LoginDTO) -> (SwitchSceneDTO | WarningDTO):
        temp_username: str = _login_dto.username
        player_is_in_db: bool = self.check_username_in_db(temp_username)

        subject_output = self.subj_login.notify(temp_username, player_is_in_db)
        if subject_output is not None:
            return subject_output

        # # jika username tidak diisi
        # if len(temp_username) == 0:
        #     return WarningDTO(WarningDTO.username_empty)
        
        # # jika username tidak ada di database
        # return WarningDTO(WarningDTO.username_not_registered)

        # jika username sudah ada di database
        temp_email: str = self.dash_db.get_email(temp_username)
        self.service_gameplay.reset(temp_username, temp_email)
        return SwitchSceneDTO("gameplay")

    def check_username_in_db(self, _username: str):
        # jika username tidak ada di database
        if self.dash_db.search_player(_username) == []:
            return False

        # jika username sudah ada di database
        return True


@inject 
class ServiceHighScore:
    def __init__(self, _dash_db: DashSqlDb, _service_gameplay: ServiceGameplay):
        self.dash_db = _dash_db
        self.service_gameplay = _service_gameplay
    
    def get_leaderboards(self):
        return self.dash_db.get_leaderboards()


@inject
class DashService:
    def __init__(self, _service_register: ServiceRegister, _service_gameplay: ServiceGameplay, _service_highscore: ServiceHighScore):
        self.service_register = _service_register
        self.service_gameplay = _service_gameplay
        self.service_highscore = _service_highscore


# Leaderboards observer pattern
# -> Setiap observer berikut dinotifikasi ketika game over, lalu mengirimkan email bila kondisi tertentu terpenuhi
## Interface for register observer
class ILeaderboardsNotify(ABC):
    @abstractmethod
    def notified(self, _current_user_dto: UserDTO, _top_user_dto: UserDTO):
        pass
    
    
## Observer 1
@inject(alias=ILeaderboardsNotify)
class NotifyIfReachLeaderboards(ILeaderboardsNotify, EmailSender):
    def notified(self, _current_user_dto: UserDTO, _top_user_dto: UserDTO):
        subject = "Congratsss 🥳🥳🥳"
        body = "Congratulations you are the top player now!"
        if _top_user_dto.score < _current_user_dto.score:
            return True, self.send_email(_current_user_dto.email, subject, body)
        return False, ""


## Observer 2
@inject(alias=ILeaderboardsNotify)
class NotifyIfDropFromLeaderboards(ILeaderboardsNotify, EmailSender, DashSqlDb):
    def notified(self, _current_user_dto: UserDTO, _top_user_dto: UserDTO):
        subject = "Noooo 😭😭"
        body = "You're not the top player anymore!"
        if _top_user_dto.score < _current_user_dto.score:
            return True, self.send_email(_top_user_dto.email, subject, body)
        return False, ""


## Observer 3
@inject(alias=ILeaderboardsNotify)
class NotifyIfPassCertainLimit(ILeaderboardsNotify, EmailSender):
    def notified(self, _current_user_dto: UserDTO, _top_user_dto: UserDTO):
        subject = "Congratsss 🥳🥳🥳"
        body = "Congratulations, your score has reached 16. Here are your special rewards 🎁."
        if _current_user_dto.score >= 16:
            return True, self.send_email(_current_user_dto.email, subject, body)
        return False, ""


## Subject
@inject
class LeaderboardsSubject:
    def __init__(self, _observers: list[ILeaderboardsNotify]) -> None:
        self.observers = _observers

    def notify(self, _current_user_dto: UserDTO, _top_user_dto: UserDTO):
        for observer in self.observers:
            observer.notified(_current_user_dto, _top_user_dto)


# Register observer pattern
## Interface for register observer
class IRegisterNotify(ABC):
    @abstractmethod
    def notified(self, _username: str, _email: str, _player_is_in_db: bool) -> (WarningDTO | None):
        pass


## Observer 1
@inject(alias=IRegisterNotify)
class NotifyIfUsernameIsEmpty(IRegisterNotify):
    def notified(self, _username: str, _email: str, _player_is_in_db: bool) -> (WarningDTO | None):
        if len(_username) == 0:
            return WarningDTO(WarningDTO.username_empty)


## Observer 2
@inject(alias=IRegisterNotify)
class NotifyIfEmailIsEmpty(IRegisterNotify):
    def notified(self, _username: str, _email: str, _player_is_in_db: bool) -> (WarningDTO | None):
        if len(_email) == 0:
            return WarningDTO(WarningDTO.email_empty)


## Observer 3
@inject(alias=IRegisterNotify)
class NotifyIfEmailIsInvalid(IRegisterNotify):
    whitelist = ["gmail.com", "hotmail.com", "students.calvin.ac.id", "yahoo.com"]

    def notified(self, _username: str, _email: str, _player_is_in_db: bool) -> (WarningDTO | None):
        try:
            cleaned_email = _email.split("@")
            if cleaned_email[0] == "" or len(cleaned_email) != 2 or cleaned_email[1] not in NotifyIfEmailIsInvalid.whitelist:
                return WarningDTO(WarningDTO.email_invalid)
        except:
            return WarningDTO(WarningDTO.email_invalid)
        

## Observer 4
@inject(alias=IRegisterNotify)
class NotifyIfUsernameIsAlreadyInDatabase(IRegisterNotify):
    def notified(self, _username: str, _email: str, _player_is_in_db: bool) -> (WarningDTO | None):
        if _player_is_in_db:
            return WarningDTO(WarningDTO.username_already_registered)
        

## Subject
@inject
class RegisterSubject:
    def __init__(self, _observers: list[IRegisterNotify]) -> None:
        self.observers = _observers

    def notify(self, _username: str, _email: str, _player_is_in_db: bool) -> (WarningDTO | None):
        for observer in self.observers:
            observer_output = observer.notified(_username, _email, _player_is_in_db)
            if observer_output is not None:  # jika me-return WarningDTO
                return observer_output
        return None
           

## Login Observer Pattern
## Interface for login observer
class ILoginNotify(ABC):
    @abstractmethod
    def notified(self, _username: str, _player_is_in_db: bool) -> (WarningDTO | None):
        pass


## Observer 1
@inject(alias=ILoginNotify)
class NotifyIfNotInputUsername(ILoginNotify):
    def notified(self, _username: str, _player_is_in_db: bool) -> (WarningDTO | None):
        if len(_username) == 0:
            return WarningDTO(WarningDTO.username_empty)


## Observer 2
@inject(alias=ILoginNotify)
class NotifyIfUsernameNotRegistered(ILoginNotify):
    def notified(self, _username: str, _player_is_in_db: bool) -> (WarningDTO | None):
        if not _player_is_in_db:
            return WarningDTO(WarningDTO.username_not_registered)


## Subject
@inject
class LoginSubject:
    def __init__(self, _observers: list[ILoginNotify]) -> None:
        self.observers = _observers

    def notify(self, _username: str, _player_is_in_db: bool) -> (WarningDTO | None):
        for observer in self.observers:
            observer_output = observer.notified(_username, _player_is_in_db)
            if observer_output is not None:  # jika me-return WarningDTO 
                return observer_output 
        return None
    

   