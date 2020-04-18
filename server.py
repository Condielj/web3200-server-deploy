from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from dvddb import DVD_DB
from dvddb import uDB
import json
import sys
from passlib.hash import bcrypt
from http import cookies
from sessionstore import SessionStore

SESSIONSTORE = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):

    #end_headers override
    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        BaseHTTPRequestHandler.end_headers(self)



    def load_cookie(self):
        #read a header - capture cookie
        #OR create cookie if one doesnt exist
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        #write a header - send cookie data
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())


    
    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE, PUT')
        self.send_header("Access-Control-Allow_Headers", "Content-type")
        self.end_headers()

    def do_GET(self):
        self.load_session()
        print("GET Request recieved.  Retrieving... ")
        if self.path == "/dvds":
            self.retrieveAllDVDs()
        elif self.path.startswith("/dvds/"):
            self.retrieveSingleDVD()
        #elif self.path == "/users":
        #    self.retrieveAllUsers()
        #elif self.path.startswith("/users/"):
            #self.retrieveUser()
        else:
            self.handleNotFound()

    def do_POST(self):
        self.load_session()
        print("POST Request recieved.  Creating... ")
        if self.path == "/dvds":
            self.createDVD()
        elif self.path == "/users":
            self.registerUser()
        elif self.path == "/sessions":
            self.createSession()
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.load_session()
        print("PUT Request recieved.  Updating... ")
        if self.path.startswith("/dvds/"):
            self.editDVD()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.load_session()
        print("DELETE Request recieved.  Deleting... ")
        if self.path.startswith("/dvds/"):
            self.deleteDVD()
        else:
            self.handleNotFound()

    

    def retrieveAllDVDs(self):
        #ENFORCE AUTHORIZATION (user is logged in?)
        if "userId" not in self.sessionData:
            self.send_response(401) #not authorized
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content_type", "application/json")
        self.end_headers()
        db = DVD_DB()
        dvds = db.retrieveAllDVDs()
        self.wfile.write(bytes(json.dumps(dvds), "utf-8"))

    def retrieveSingleDVD(self):
        #ENFORCE AUTHORIZATION (user is logged in?)
        if "userId" not in self.sessionData:
            self.send_response(401) #not authorized
            self.end_headers()
            return
        db = DVD_DB()
        string_parts = self.path.split("/")
        inv = string_parts[2]
        dvd = db.retrieveOneDVD(inv)
        if dvd != None:
            self.send_response(200)
            self.send_header("Content_type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dvd), "utf-8"))
        else:
            self.handleNotFound()

    def createDVD(self):
        #ENFORCE AUTHORIZATION (user is logged in?)
        if "userId" not in self.sessionData:
            self.send_response(401) #not authorized
            self.end_headers()
            return
        length = self.headers["Content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        #print("Raw body", body)
        parsed_body = parse_qs(body)
        #print(parsed_body)
        title = parsed_body["title"][0]
        rating = parsed_body["rating"][0]
        price = parsed_body["price"][0]
        date = parsed_body["date"][0]
        genre = parsed_body["genre"][0]

        db = DVD_DB()
        db.insertOneDVD(title, rating, price, date, genre)
        self.send_response(201)
        self.end_headers()

    def deleteDVD(self):
        #ENFORCE AUTHORIZATION (user is logged in?)
        if "userId" not in self.sessionData:
            self.send_response(401) #not authorized
            self.end_headers()
            return
        db = DVD_DB()
        string_parts = self.path.split("/")
        inv = string_parts[2]
        dvd = db.retrieveOneDVD(inv)
        if dvd != None:
            self.send_response(200)
            self.send_header("Content_type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dvd), "utf-8"))
            db.deleteOneDVD(inv)
        else:
            self.handleNotFound()

    def editDVD(self):
        #ENFORCE AUTHORIZATION (user is logged in?)
        if "userId" not in self.sessionData:
            self.send_response(401) #not authorized
            self.end_headers()
            return
        db = DVD_DB()
        string_parts = self.path.split("/")
        inv = string_parts[2]
        dvd = db.retrieveOneDVD(inv)
        if dvd != None:
            self.send_response(200)
            self.send_header("Content_type", "application/json")
            self.end_headers()
            length = self.headers["Content-length"]
            body = self.rfile.read(int(length)).decode("utf-8")
            parsed_body = parse_qs(body)
            title = parsed_body["title"][0]
            rating = parsed_body["rating"][0]
            price = parsed_body["price"][0]
            date = parsed_body["date"][0]
            genre = parsed_body["genre"][0]
            db.editOneDVD(inv, title, rating, price, date, genre)
        else:
            self.handleNotFound()



    #def retrieveAllUsers(self):
    #    #testing purposes only
    #    self.send_response(200)
    #    self.send_header("Content_type", "application/json")
    #    self.end_headers()
    #    db = uDB()
    #    users = db.retrieveAllUsers()
    #    self.wfile.write(bytes(json.dumps(users), "utf-8"))

    #def retrieveUser(self):
    #    db = uDB()
    #    string_parts = self.path.split("/")
    #    uid = string_parts[2]
    #    user = db.retrieveUser(uid)
    #    if user != None:
    #        self.send_response(200)
    #        self.send_header("Content_type", "application/json")
    #        self.end_headers()
    #        self.wfile.write(bytes(json.dumps(user), "utf-8"))
    #    else:
    #        self.handleNotFound()

    def registerUser(self):
        length = self.headers["Content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        #print("Raw body", body)
        parsed_body = parse_qs(body)
        #print(parsed_body)
        fname = parsed_body["fname"][0]
        lname = parsed_body["lname"][0]
        email = parsed_body["email"][0]
        password = bcrypt.hash(parsed_body["password"][0])
        #print(password)
        db = uDB()
        existing_user = db.retrieveUserByEmail(email)
        #testing==
        #print(existing_user)
        #==testing
        if existing_user != None:
            print("Email already exists.")
            self.send_response(422)
            self.end_headers()
        else:
            #testing==
            #users = db.retrieveAllUsers()
            #print(users)
            #==testing
            db.registerNewUser(email, password, fname, lname)
            self.send_response(201)
            self.end_headers()



    def createSession(self):
        #pseudo code from class
        #inputs: email and password
        #1. check to see if user exists (by email)
        #   if user exists:
        #       verify encrypted given password == encrypted password in user db
        #       bcrypt.verify(given_pass, encrypted_old_pass) => True or False
        #       if passwords match:
        #           success (send good status code 201)
        #       else: (passwords dont match)
        #           failure (send status code 401 - unauthorized/not authenticated)
        #   else:
        #       failure (same error for purposes of vagueness 401)
        db = uDB()
        length = self.headers["Content-length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)
        email = parsed_body["email"][0]
        password = parsed_body["password"][0]
        existing_user = db.retrieveUserByEmail(email)
        if existing_user != None:
            if bcrypt.verify(password, existing_user['password']):
                #success
                self.send_response(201)
                self.end_headers()
                #SAVE USER ID INTO SESSION DATA
                self.sessionData["userId"] = existing_user["uid"]
            else:
                #failure
                self.send_response(401)
                self.end_headers()
        else:
            #failure
            self.send_response(401)
            self.end_headers()

    def load_session(self):
        #first, load the cookie data
        self.load_cookie()
        #if the sessionId is found in the cookie:
        if "sessionId" in self.cookie:
        #   load the session ID from the cookie
            sessionId = self.cookie["sessionId"].value
        #   use the session id to load the session data from the session store
            self.sessionData = SESSIONSTORE.getSessionData(sessionId)
        #   if the session data DOES NOT exist in the session store:
            if self.sessionData == None: #likely after server restart/data loss
        #       recreate the session and issue a new session id into a cookie
                sessionId = SESSIONSTORE.createSession()
                self.sessionData = SESSIONSTORE.getSessionData(sessionId)
                self.cookie["sessionId"] = sessionId
        #   else:
        #       ...
        #else (no session id in cookie):
        else:
        #   create a new session in the session store (createSession)
            sessionId = SESSIONSTORE.createSession()
            self.sessionData = SESSIONSTORE.getSessionData(sessionId)
        #   create a new cookie value with the new session ID
            self.cookie["sessionId"] = sessionId



    def handleNotFound(self):
        self.load_session()
        self.send_response(404)
        self.end_headers()




def run():
    dvddb = DVD_DB()
    dvddb.createDVDTable()
    dvddb = None
    udb = uDB()
    udb.createUsersTable()
    udb = None

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])


    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyRequestHandler)
    print("Listening on:", "{}:{}".format(*listen))
    server.serve_forever()

run()