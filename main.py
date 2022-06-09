#! /usr/bin/env python3

import json, os, sys, base64
import click
from requests_oauthlib import OAuth1Session
import mytweet
import uuid
from flask import Flask, request
import urllib
from google.cloud import pubsub_v1
import myutils


e = os.environ
GOOGLE_CLOUD_PROJECT = e.get("GOOGLE_CLOUD_PROJECT")
BUCKET_NAME = e.get("BUCKET_NAME")
CK = e.get("TWITTER_API_KEY")
CS = e.get("TWITTER_API_SECRET_KEY")
AT = e.get("TWITTER_ACCESS_TOKEN")
ATS = e.get("TWITTER_ACCESS_TOKEN_SECRET")
COUNT = e.get("COUNT", 2)

WORD = e.get("WORD", "日本")
TOPIC = e.get("TOPIC")

URL = "https://api.twitter.com/1.1/search/tweets.json"

app = Flask(__name__)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, TOPIC)


@click.command()
@click.option("-w", "--word", required=True)
@click.option("-c", "--count", default=1)
def _cmd(word, count):
    print(word, count)
    _process(word, count)

@app.route("/tweet", methods=['POST'])
def main():
    word = ""
    try:
        word = request.form.get("word")
        print(word)
        if not word:
            word = WORD
    except:
        pass

    filename = _process(word, COUNT)
    return {"word":word, "filename":filename}


def _process(keyword, count):
    keyword = keyword + str(" -filter:retweets")

    twitter = OAuth1Session(CK, CS, AT, ATS)

    nl = myutils.GCP_NL()

    params = {"q": keyword, "count": int(count)}
    if not __debug__:
        print(params)
    res = twitter.get(URL, params=params)
    if not __debug__:
        print(res)

    results = []

    if res.status_code == 200:
        search_timeline = json.loads(res.text)
        for message in search_timeline["statuses"]:
            tweet = mytweet.My_Tweet(message).grep_from()
            print(tweet)

            nl_response = nl.sentiment(tweet["text"])
            print("NL Response:",nl_response)
            if nl_response:
                tweet["google"] = {}
                tweet["google"]["magnitude"] = nl_response.magnitude
                tweet["google"]["score"] = nl_response.score

            # results.append(json.dumps(tweet))
            _pub(json.dumps(tweet))

    else:
        print(f"ERROR: {res.status_code}")

    return ""

def _pub(data: str) -> None:
    try:
        send_data: bytes = data.encode("utf-8")
        print(send_data)
        future = publisher.publish(
            topic_path, send_data,
        )
        future.result()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    _cmd()
