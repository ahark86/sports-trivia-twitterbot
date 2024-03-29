import requests
import random
import os
from twython import Twython
import html

APIKEY = os.environ.get('APIKEY_TB')
APISECRETKEY = os.environ.get('APISECRETKEY_TB')
BEARERTOKEN = os.environ.get('BEARERTOKEN_TB')
ACCESSTOKEN = os.environ.get('ACCESSTOKEN_TB')
ACCESSTOKENSECRET = os.environ.get('ACCESSTOKENSECRET_TB')


def question_tweet(q, a1, a2, a3, a4):
    choices = random.sample([a1, a2, a3, a4], 4)
    return f'{q}\n\n' \
           f'A: {choices[0]}\n' \
           f'B: {choices[1]}\n' \
           f'C: {choices[2]}\n' \
           f'D: {choices[3]}'


def answer_tweet(q, a):
    return f'{q}\n\n' \
           f'Answer: {a}'


if os.path.exists('answer_file.txt'):
    # tweet answer from the file and then delete the file
    try:
        with open('answer_file.txt') as f:
            ans_tweet = f.readlines()
            status_update = f'{ans_tweet[0].strip()}\n\n' \
                            f'{ans_tweet[2].strip()}'

        twitter = Twython(APIKEY, APISECRETKEY, ACCESSTOKEN, ACCESSTOKENSECRET)
        twitter.update_status(status=status_update)
        os.remove('answer_file.txt')
    except:
        os.remove('answer_file.txt')
else:
    # pull question/answers, generate question and answer tweet, tweet question, create file to hold answer
    URL = "https://opentdb.com/api.php?amount=1&category=21&type=multiple"
    try:
        r = requests.get(URL).json()
        question = html.unescape(r["results"][0]["question"])
        cor_answer = html.unescape(r["results"][0]["correct_answer"])
        inc_answer_1 = html.unescape(r["results"][0]["incorrect_answers"][0])
        inc_answer_2 = html.unescape(r["results"][0]["incorrect_answers"][1])
        inc_answer_3 = html.unescape(r["results"][0]["incorrect_answers"][2])

        status_update = question_tweet(question, cor_answer, inc_answer_1, inc_answer_2, inc_answer_3)

        twitter = Twython(APIKEY, APISECRETKEY, ACCESSTOKEN, ACCESSTOKENSECRET)
        twitter.update_status(status=status_update)

        with open('answer_file.txt', 'w') as f:
            f.write(answer_tweet(question, cor_answer))
    except:
        pass