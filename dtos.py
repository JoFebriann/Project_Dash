class EmailDTO:
    def __init__(self, _email: str):
        self.email = _email


class GameOverDTO:
    def __init__(self, _final_score: int) -> None:
        self.final_score = _final_score


class LeaderboardDTO:
    def __init__(self, _username: str, _score: int) -> None:
        self.username = _username
        self.score = _score
    
    def __str__(self) -> str:
        return f"{self.username} | {self.score}"


class LoginDTO:
    def __init__(self, _username: str):
        self.username = _username


class RegisterDTO:
    def __init__(self, _username: str, _email: str):
        self.username = _username
        self.email = _email


class SelectDTO:
    def __init__(self, _selected_name: str) -> None:
        self.selected_name = _selected_name


class SoundDTO:
    def __init__(self, _sound_name: str) -> None:
        self.score = _sound_name


class SwitchSceneDTO:
    def __init__(self, _scene_name: str):
        self.scene_name = _scene_name

    def __repr__(self):
        return f"SwitchSceneDTO({self.scene_name})"


class UserDTO:
    def __init__(self, _name: str, _email: str, _score: int):
        self.name = _name
        self.email = _email
        self.score = _score


class WarningDTO:
    email_empty = "Please enter your email."
    email_invalid = "Please enter a valid email."
    username_empty = "Please enter your chosen username."
    username_already_registered = "Sorry, this username has already been picked!"
    username_not_registered = "Sorry, this username hasn't been registered."

    def __init__(self, _warning: str) -> None:
        self.warning = _warning