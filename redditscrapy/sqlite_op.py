#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import sqlite3
import pandas as pd

def db_create_posts():
    """
    create table POSTS
    :return: 0
    """
    conn = sqlite3.connect('../data/reddit_db/reddit.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE POSTS
                (SUBREDDIT TEXT, URL TEXT PRIMARY KEY, TITLE TEXT, DATETIME TEXT, 
                AUTHOR TEXT, NCOMMENTS INT, NSCORES INT, MOD INT)''')
    conn.commit()
    conn.close()
    return 0


def db_create_userposts():
    """
    create table USERPOSTS
    :return: 0
    """
    conn = sqlite3.connect('../data/reddit_db/reddit.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE USERPOSTS
                (AUTHOR TEXT, SUBREDDIT TEXT, URL TEXT PRIMARY KEY, TITLE TEXT,
                 DATETIME TEXT, NCOMMENTS INT, NSCORES INT)''')
    conn.commit()
    conn.close()
    return 0


def db_insert_post(dict_data):
    """
    Inserting data into database
    :param dict_data: data dict
    :return: 0
    """
    conn = sqlite3.connect('../data/reddit_db/reddit.sqlite3')
    c = conn.cursor()
    print('Opened database successfully. ')
    try:
        c.execute("insert into POSTS values (?, ?, ?, ?, ?, ?, ?, ?)",
                  (dict_data['subreddit'], dict_data['url'], dict_data['title'], dict_data['datetime'],
                   dict_data['author'], dict_data['ncomments'], dict_data['nscores'], dict_data['mod']))
    except sqlite3.Error as e:
        print('Error:', e.args[0])
    conn.commit()
    conn.close()
    return 0


def db_insert_userposts(dict_data):
    """
    Inserting data into database
    :param dict_data: data dict
    :return: 0
    """
    conn = sqlite3.connect('../data/reddit_db/reddit.sqlite3')
    c = conn.cursor()
    print('Opened database successfully. ')
    try:
        c.execute("insert into USERPOSTS values (?, ?, ?, ?, ?, ?, ?)",
                  (dict_data['author'], dict_data['subreddit'], dict_data['url'], dict_data['title'],
                   dict_data['datetime'], dict_data['ncomments'], dict_data['nscores']))
    except sqlite3.Error as e:
        print('Error:', e.args[0])
    conn.commit()
    conn.close()
    return 0


def db_load_posts():
    """
    SELECT * FROM POSTS
    :return: pandas DataFrame
    """
    conn = sqlite3.connect('../data/reddit_db/reddit.sqlite3')
    c = conn.cursor()
    print('Opened database successfully. ')
    dict_data = {'subreddit':[], 'url':[], 'title':[], 'datetime': [],
                 'author':[], 'ncomments':[], 'nscores':[], 'mod':[]}
    try:
        c.execute('SELECT * FROM POSTS')
        all_rows = c.fetchall()
        for row in all_rows:
            dict_data['subreddit'].append(row[0])
            dict_data['url'].append(row[1])
            dict_data['title'].append(row[2])
            dict_data['datetime'].append(row[3])
            dict_data['author'].append(row[4])
            dict_data['ncomments'].append(row[5])
            dict_data['nscores'].append(row[6])
            dict_data['mod'].append(row[7])
        print('Number of elements:', len(all_rows))
    except sqlite3.Error as e:
        print('Error', e.args[0])
    conn.close()
    return pd.DataFrame(dict_data, index=None,
                        columns=['subreddit', 'url', 'title', 'datetime', 'author', 'ncomments', 'nscores', 'mod'])


def db_load_userposts():
    """
    SELECT * FROM USERPOSTS
    :return: pandas DataFrame
    """
    conn = sqlite3.connect('../data/reddit_db/reddit.sqlite3')
    c = conn.cursor()
    print('Opened database successfully. ')
    dict_data = {'author':[], 'subreddit':[], 'url':[], 'title':[], 'datetime': [],
                 'ncomments':[], 'nscores':[]}
    try:
        c.execute('SELECT * FROM USERPOSTS')
        all_rows = c.fetchall()
        for row in all_rows:
            dict_data['author'].append(row[0])
            dict_data['subreddit'].append(row[1])
            dict_data['url'].append(row[2])
            dict_data['title'].append(row[3])
            dict_data['datetime'].append(row[4])
            dict_data['ncomments'].append(row[5])
            dict_data['nscores'].append(row[6])
        print('Number of elements:', len(all_rows))
    except sqlite3.Error as e:
        print('Error', e.args[0])
    conn.close()
    return pd.DataFrame(dict_data, index=None,
                        columns=['author', 'subreddit', 'url', 'title', 'datetime', 'ncomments', 'nscores'])


if __name__ == '__main__':
    df = db_load_posts()
