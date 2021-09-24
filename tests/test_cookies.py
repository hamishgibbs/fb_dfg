import pytest
from fb_dfg import cookies


class MockCookie:

    def __init__(self, name, domain, value):
        self.name = name
        self.domain = domain
        self.value = value


@pytest.fixture()
def mock_cookiejar():

    cookies = ["datr", "sb", "c_user", "dpr", "spin", "xs", "fr"]

    cookie_jar = [MockCookie(x, ".facebook.com", x) for x in cookies]

    return cookie_jar


def test_get_cookies(mock_cookiejar):

    cookie_str = cookies.get_cookies(mock_cookiejar)

    exp = "datr=datr; sb=sb; c_user=c_user; dpr=dpr; spin=spin; xs=xs; fr=fr"

    assert cookie_str == exp
