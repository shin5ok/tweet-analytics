from dateutil import parser

class My_Tweet:
    def __init__(self, t):
        self.t = t

    def _debug(self, message):
        if not __debug__:
            print("Debug:" + message)

    def grep_from(self):
        t = self.t
        n = {}
        try:
            n["created_date"] = parser.parse(t["created_at"]).strftime("%Y-%m-%dT%H:%M:%S+00:00")
            n["text"] = t["text"]
            n["id"] = t["id"]
            n["user_id"] = t["user"]["id"]
            n["user_name"] = t["user"]["name"]
            n["user_screen_name"] = t["user"]["screen_name"]
            n["retweet_count"] = t["retweet_count"]
            n["lang"] = t["lang"]
            n["time_zone"] = t["user"]["time_zone"]
            n["followers_count"] = t["user"]["followers_count"]
            n["favourites_count"] = t["user"]["favourites_count"]
            n["friends_count"] = t["user"]["friends_count"]
        except Exception as e:
            self._debug(str(e))
        return n

