print("\033[H\033[J", end="")

from contextlib import nullcontext
from datetime import datetime
import praw

import os
import sys
import instaloader

from os.path import join
from os import listdir, rmdir
from shutil import move

parent_dir = 'D:/Directories/Documents/'
temp_dir = parent_dir + 'temp/'

accounts = []
loader = nullcontext

files = []

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    print('Creating directory: {}'.format(directory))

    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Directory created\n')
    else:
        print('Directory already exists\n')

def read_in_accounts():
    print('Reading in account names\n')

    with open(os.path.join(sys.path[0], 'account_names.txt')) as f:
        for line in f: 
            accounts.append(line.strip())

def get_filenames():
    global files
    files = os.listdir(temp_dir)

def insta_auth():
    print('Logging into instagram\n')
    global loader
    loader = instaloader.Instaloader()
    #loader.login('###########', '###########')

def get_post(account_name):
    print("Getting new posts from instagram:")
    profile = instaloader.Profile.from_username(loader.context, account_name)

    if profile.is_private:
        print('%s is a private account\n' % (account_name))
    else:
        posts = profile.get_posts()

        for post in posts:
            if post.is_pinned:
                continue
            
            if not post.is_video:
                temp_file = '%s%s_%s' % (temp_dir, post.owner_username, post.mediaid)
                perm_file = '%s%s_%s.jpg' % (parent_dir, post.owner_username, post.mediaid)

                if os.path.isfile(perm_file):
                    print('%s is up-to-date' % (post.owner_username))
                else:
                    loader.download_pic(temp_file, post.url, datetime.now())
            else:
                print('%s first is video' % (post.owner_username))
            print('\n')
            break

def reddit_auth():
    reddit = praw.Reddit(
        client_id="###########",
        client_secret="###########",
        user_agent="script by u/###########",
        username="###########",
        password="###########",
    )
    
    submit(reddit)

def submit(reddit):
    get_filenames()

    subreddit = reddit.subreddit("#######")
    reddit.validate_on_submit = True
    
    for name in files:
        title = name
        image = temp_dir + name
        subreddit.submit_image(title, image)

def move_pics():
    for filename in listdir(join(parent_dir, 'temp')):
        move(join(parent_dir, 'temp', filename), join(parent_dir, filename))

ensure_dir(parent_dir)
ensure_dir(temp_dir)
read_in_accounts()

insta_auth()

for acc in accounts:
    get_post(acc)

if os.listdir(temp_dir):
    reddit_auth()
    move_pics()

rmdir(temp_dir)

print('Program Finished\n')
