import twint
from datetime import datetime

def get_history_file_path(user,index):
    return "history_tweets/history_tweet_" + str(index) + "_" + user + ".txt"

def get_tweets(user,index):
    c = twint.Config()
    c.Username = user
    c.Since = "2020-09-01 00:00:00"
    c.Until = "2020-12-30 00:00:00"
    c.Output = get_history_file_path(user,index)
    twint.run.Search(c)   

def get_tweets_for_users(users):
    for user in users:
        get_tweets(user)

def ontime(user):
    before_election = []
    during_election = []
    after_election = []
    
    # election day is 11.03, we split time into 3 parts:
    be_s = datetime.strptime("2020-09-19 00:00:00", '%Y-%m-%d %H:%M:%S')
    be_e = datetime.strptime("2020-10-19 00:00:00", '%Y-%m-%d %H:%M:%S')
    de_s = datetime.strptime("2020-10-19 00:00:01", '%Y-%m-%d %H:%M:%S')
    de_e = datetime.strptime("2020-11-18 00:00:00", '%Y-%m-%d %H:%M:%S')
    ae_s = datetime.strptime("2020-11-18 00:00:01", '%Y-%m-%d %H:%M:%S')
    ae_e = datetime.strptime("2020-12-18 00:00:00", '%Y-%m-%d %H:%M:%S')

    with open(get_history_file_path(user), 'r') as file:
        lines = file.readlines()
        for line in lines:
            date_str = line[20:38]
            date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date_object > be_s and date_object < be_e:
                before_election.append(line)
            if date_object > de_s and date_object < de_e:
                during_election.append(line)
            if date_object > ae_s and date_object < ae_e:
                after_election.append(line)
    return before_election, during_election, after_election

# get all uses, read from directory /users
alluserList = []
with open("users/all_users.csv", "r") as usersfile:
# with open("users/users_IzzyFitton.csv", "r") as usersfile:
# with open("users/users_realSlaughtz.csv", "r") as usersfile:
# with open("users/users_RightStuff47.csv", "r") as usersfile:
# with open("users/users_AW_HateWatch.csv", "r") as usersfile:
# with open("users/users_ProWhiteDwight.csv", "r") as usersfile:
    alluser = {}
    lines = usersfile.readlines()
    for line in lines:
        user = line.split(',')[0]
        if user in alluser:
            print(user+" already exist")
        else:
            alluser[user] = 1
            alluserList.append(user)
print(len(alluserList))

# get all tweets and write to files
index = 0
for u in alluserList:
    get_tweets(u,index)
    index += 1
    # before, during, after = ontime(u)