import os
import base64

class SessionStore:

    def __init__(self):
        self.mSessions = {}

    def getSessionData(self, session_id):
        #check dictionary for given session id
        #if found, return it.
        if session_id in self.mSessions:
            return self.mSessions[session_id]
        else:
            return None

    def createSession(self):
        new_session_id = self.generateSessionId()
        self.mSessions[new_session_id] = {}
        return new_session_id

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        while rstr in self.mSessions:
            rnum = os.urandom(32)
            rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr