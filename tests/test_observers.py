from project_dash.dtos import UserDTO
from project_dash.tests.mocks import MockEmailSender
from project_dash.services import NotifyIfPassCertainLimit, NotifyIfDropFromLeaderboards, NotifyIfReachLeaderboards


class NotifyIfPassCertainLimitUnderTest(MockEmailSender, NotifyIfPassCertainLimit):
    pass


class NotifyIfDropFromLeaderboardsUnderTest(MockEmailSender, NotifyIfDropFromLeaderboards):
    pass


class NotifyIfReachLeaderboardsUnderTest(MockEmailSender, NotifyIfReachLeaderboards):
    pass


# Uji observer
## uji observer_1: jika skor current user > top user, maka kirim email ke current user.
def test_reach_leaderboard():
    current_user = UserDTO("Yozef", "yozeft@gmail.com", 3)
    top_user = UserDTO("Andrea", "and@gmail.com", 2)
    observer_under_test = NotifyIfReachLeaderboardsUnderTest()
    email_output = observer_under_test.notified(current_user, top_user)
    assert email_output == (True, "yozeft@gmail.com")
    

## uji observer_1: jika skor current user <= top user, maka jangan kirim email ke current user.
def test_not_reach_leaderboard():
    current_user = UserDTO("David", "davidt@gmail.com", 5)
    top_user = UserDTO("Agung", "agung@gmail.com", 5)
    observer_under_test = NotifyIfReachLeaderboardsUnderTest()
    email_output = observer_under_test.notified(current_user, top_user)
    assert email_output == (False, "")


## uji observer_2: jika skor top user < current user, maka kirim email ke top user.
def test_drop_from_leaderboard_observer():
    current_user = UserDTO("Gracia", "graciansamosir@gmail.com", 110)
    top_user = UserDTO("Sanga", "lawalata@gmail.com", 100)
    observer_under_test = NotifyIfDropFromLeaderboardsUnderTest()
    email_output = observer_under_test.notified(current_user, top_user)
    assert email_output == (True, "lawalata@gmail.com")


## uji observer_2: jika skor top user >= current user, maka jangan kirim email ke top user.
def test_not_drop_from_leaderboard_observer():
    current_user = UserDTO("Gracia", "graciansamosir@gmail.com", 110)
    top_user = UserDTO("Sanga", "lawalata@gmail.com", 160)
    observer_under_test = NotifyIfDropFromLeaderboardsUnderTest()
    email_output = observer_under_test.notified(current_user, top_user)
    assert email_output == (False, "")


## uji observer_3: jika skor current user >= 16, maka kirim email ke current user.
def test_pass_certain_limit_observer():
    current_user = UserDTO("Gracia", "graciansamosir@gmail.com", 30)  # 30 >= 6, maka email dikirim
    top_user = UserDTO("Sanga", "lawalata@gmail.com", 100)
    observer_under_test = NotifyIfPassCertainLimitUnderTest()  # Subscriber dengan mock email sender
    email_output = observer_under_test.notified(current_user, top_user)
    assert email_output == (True, "graciansamosir@gmail.com")


## uji observer_3: jika skor current user < 16, maka jangan kirim email ke current user.
def test_not_pass_certain_limit_observer():
    current_user = UserDTO("Gracia", "graciansamosir@gmail.com", 5)  # 30 < 6, maka email tak dikirim
    top_user = UserDTO("Sanga", "lawalata@gmail.com", 100)
    observer_under_test = NotifyIfPassCertainLimitUnderTest()  # Subscriber dengan mock email sender
    email_output = observer_under_test.notified(current_user, top_user)
    assert email_output == (False, "")