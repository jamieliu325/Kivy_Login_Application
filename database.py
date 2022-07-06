import datetime

class DataBase:
    def __init__(self,filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    # open and read the file
    def load(self):
        try:
            self.file = open(self.filename,"r")
            self.users = {}
            # read lines in file
            for line in self.file:
                email, password, name, created = line.strip().split(";")
                self.users[email] = (password, name, created)
            self.file.close()
        # create file if there is no one
        except:
            self.file = open(self.filename, "w")

    # get user info related to email
    def get_user(self,email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    # add user info to users
    def add_user(self,email,password,name):
        if email.strip() not in self.users:
            self.users[email.strip()]=(password.strip(),name.strip(),DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    # to check if the login is validated
    def validate(self,email,password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    # save users info in file, format is email;password;name;create time
    def save(self):
        with open(self.filename,"w") as f:
            for user in self.users:
                f.write(user+";"+self.users[user][0]+";"+self.users[user][1]+";"+self.users[user][2]+"\n")

    # get date without using object
    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]