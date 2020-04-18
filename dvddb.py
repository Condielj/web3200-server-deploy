import os
import psycopg2
import psycopg2.extras
import urllib.parse

class DVD_DB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        
        self.mConnection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.mCursor = self.mConnection.cursor()

    def __del__(self):
        self.mConnection.close()

    def createDVDTable(self):
        self.mCursor.execute("CREATE TABLE IF NOT EXISTS dvds (inv SERIAL PRIMARY KEY, title VARCHAR(255), rating VARCHAR(255), price VARCHAR(255), date VARCHAR(255), genre VARCHAR(255))")
        self.mConnection.commit()

    def insertOneDVD(self, title, rating, price, date, genre):
        data = [title, rating, price, date, genre]
        self.mCursor.execute("INSERT INTO dvds (title, rating, price, date, genre) VALUES (%s, %s, %s, %s, %s)", data)
        self.mConnection.commit()

    def retrieveAllDVDs(self):
        self.mCursor.execute("SELECT * FROM dvds")
        dvds = self.mCursor.fetchall()
        return dvds

    def retrieveOneDVD(self, inv):
        data = [inv]
        self.mCursor.execute("SELECT * FROM dvds WHERE inv = %s", data)
        dvd = self.mCursor.fetchone()
        return dvd

    def deleteOneDVD(self, inv):
        data = [inv]
        self.mCursor.execute("DELETE FROM dvds WHERE inv = %s", data)
        self.mConnection.commit()

    def editOneDVD(self, inv, title, rating, price, date, genre):
        data = [title, rating, price, date, genre, inv]
        self.mCursor.execute("UPDATE dvds SET title = %s, rating = %s, price = %s, date = %s, genre = %s WHERE inv = %s", data)
        self.mConnection.commit()

    def functionToGetRidOfAnnoyingWarning(self):
        #vscode kept bugging me about the unused instance of my databases in the server.run() function
        print("")


class uDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        
        self.mConnection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.mCursor = self.mConnection.cursor()

    def __del__(self):
        self.mConnection.close()

    def createUsersTable(self):
        self.mCursor.execute("CREATE TABLE IF NOT EXISTS users (uid SERIAL PRIMARY KEY, email VARCHAR(255), password VARCHAR(255), fname VARCHAR(255), lname VARCHAR(255))")
        self.mConnection.commit()

    def registerNewUser(self, email, password, fname, lname):
        data = [email, password, fname, lname]
        self.mCursor.execute("INSERT INTO users (email, password, fname, lname) VALUES (%s, %s, %s, %s)", data)
        self.mConnection.commit()
        #print("Done!")

    #def retrieveAllUsers(self):
    #    #testing purposes only
    #    self.mCursor.execute("SELECT * FROM users")
    #    users = self.mCursor.fetchall()
    #    return users

    def retrieveUser(self, uid):
        data = [uid]
        self.mCursor.execute("SELECT * FROM users WHERE uid = %s", data)
        user = self.mCursor.fetchone()
        return user

    def retrieveUserByEmail(self, email):
        data = [email]
        self.mCursor.execute("SELECT * FROM users WHERE email = %s", data)
        user = self.mCursor.fetchone()
        return user

    def functionToGetRidOfAnnoyingWarning(self):
        #vscode kept bugging me about the unused instance of my databases in the server.run() function
        print("")