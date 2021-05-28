import tweepy
import time
import csv
import os

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN_KEY = os.environ.get("ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# note: user may follow his/her followers
def get_followers(username):
    print(username)
    follwers = []
    try:
        follwers = api.followers(username)
    except tweepy.TweepError as e:
        follwers = []
        print(e)
    return follwers

def get_all_followers(user):
    with open("users_" + user +".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user, "origin"])
        all_followers = {
            user:1
        }
        # get all level-1 users
        users_level_1 = []
        followers = get_followers(user)
        count = 0
        print("followers for " + user)
        print(len(followers))
        for follower in followers:
            # get screen name
            screen_name = follower.screen_name
            if screen_name in all_followers: # we don't want uses duplicate
                continue
            # we don't want more than 100 child users
            if count > 100:
                break
            count+=1
            # add this follower
            users_level_1.append(screen_name)
            all_followers[screen_name] = 1
            
        # get all level-2 users
        print("users number in level 1")
        print(len(users_level_1))
        for user1 in users_level_1:
            writer.writerow([user1, 'level_1'])

        users_level_2 = []
        for username in users_level_1:
            followers = get_followers(username)
            count = 0
            for follower in followers:
                # get screen name
                screen_name = follower.screen_name
                if screen_name in all_followers: # we don't want uses duplicate
                    continue
                # we don't want more than child users
                if count > 100:
                    break
                count+=1
                # add this follower into all
                users_level_2.append(screen_name)
                all_followers[screen_name] = 1
            # Twitter api rate limit
            time.sleep(100)
        for user2 in users_level_2:
            writer.writerow([user2, 'level_2'])
    return users_level_1, users_level_2

# users = ["IzzyFitton","realSlaughtz","RightStuff47","AW_HateWatch","ProWhiteDwight"]
users = ["kk131066", "HANSEN_SOGROOVY", "DanegroQ", "outerspacemanII","AmericanFaye"]   
for user in users:
    users_level_1, users_level_2 = get_all_followers(user)
    print("done with download all users")