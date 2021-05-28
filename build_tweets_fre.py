
# read_history_tweets
# 1. read from files
# 2. get their tweet_time and count them
# 3. pre with a graph
# TODO: download random users tweets and count their tweets fre and compare
from os import walk
import matplotlib.pyplot as plt

random_history_tweets_path = "random_history_tweets/"
history_tweets_path = "history_tweets/"
anti_history_tweets_path = "anti_history_tweets/"

names = ["notionalists", "anti_notionalists"]
files = [history_tweets_path, anti_history_tweets_path]

def read_history_tweets(filepath):
    x,y = [],[]
    c = 0
    date_count = {}
    _,_,filenames = next(walk(filepath))
    for fn in filenames:
        if c > 640:
            break
        with open(filepath+fn, 'r', encoding="UTF-8") as file:
            lines = file.readlines()
            if len(lines) < 10:
                continue
            contains = False
            for line in lines:
                if "2020-11" in line:
                    contains = True
                    break
            if not contains:
                continue
            c += 1
            for line in lines:
                date = line[25:30]
                if date in date_count:
                    date_count[date] += 1
                else:
                    date_count[date] = 1
    print("len of date_count:")
    print(len(date_count))
    count = 0
    for key in sorted(date_count.keys()):
        y.append(date_count[key])
        x.append(key)
        count += date_count[key]
    return x,y 

for i in range(len(files)):
    x, y = read_history_tweets(files[i])
    plt.plot(x,y, label=names[i])
plt.title("Number of tweets per day")
plt.xlabel("Date")
plt.xticks(rotation=90)
plt.ylabel("Number of tweets")
plt.legend()
plt.tick_params(axis='x', labelsize=8)
ax = plt.gca()
for index, label in enumerate(ax.xaxis.get_ticklabels()):
    if index % 5 != 0:
        label.set_visible(False)
plt.savefig("history.png")