from http.cookiejar import CookieJar


def get_cookies(cookiejar: CookieJar,
                fb_cookies=["datr", "sb", "c_user", "dpr", "spin", "xs", "fr"],
                domain=".facebook.com"):

    cookies = list(cookiejar)

    request_cookies = []

    for cookie in cookies:
        if cookie.name in fb_cookies and cookie.domain == domain:

            request_cookies.append(cookie.name + "=" + cookie.value)

    return "; ".join(request_cookies)
