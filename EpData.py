import json
import os
import datetime
import pandas as pd
import numpy as np
import re
import nltk


class EpData(object):
    # def __init__(self):
    #     # self.path = source_path

    def json2excel(self, excel_path, json_path):
        files_list = os.listdir(json_path)
        # convert json file to csv
        for file_name in files_list:
            with open(json_path + file_name, 'r') as f:
                items = json.load(f)
            id, date, age, gender, likes, body = [], [], [], [], [], []
            for dic in items:
                if dic['id'] not in id:
                    id.append(dic['id'])
                    date.append(dic['date'])
                    age.append(dic['age'])
                    gender.append(dic['gender'])
                    likes.append(dic['likes'])
                    body.append(dic['body'])
            data = {'id': id,
                'date': date,
                'age': age,
                'gender': gender,
                'likes': likes,
                'body': body
            }
            reddit = pd.DataFrame(data, columns=['id', 'date', 'age', 'gender', 'likes', 'body'], index=None)
            reddit.to_excel(excel_path+'ep_{}.xlsx'.format(len(id)), sheet_name='default')


if __name__ == "__main__":
    ep = EpData()
    ep.json2excel('./data_ep/', './crawl_ep/')