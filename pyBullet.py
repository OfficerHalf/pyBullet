#!/usr/bin/env python3
import requests
import json
import os.path as path
import argparse
import subprocess


class pyBullet:
    def __init__(self, api_key=None):
        if not api_key:
            self.header = {"Content-Type": "application/json"}
            self.url = "https://api.pushbullet.com/v2/pushes"
            config_path = path.join(path.dirname(path.abspath(__file__)), "api.pub")
            if not path.isfile(config_path):
                raise FileNotFoundError("No api key specified and api.pub not found.")
            with open(config_path, 'r') as fp:
                self.api_key = fp.read().strip()
        else:
            self.api_key = api_key

    def push(self, title, body):
        jsonized_data = json.dumps({"title": title, "body": body, "type": "note"})
        response = requests.post(self.url, headers=self.header, auth=(self.api_key, ""), data=jsonized_data)
        print(response)


def main():
    parser = argparse.ArgumentParser(description="Do something, then send a notification.")
    parser.add_argument('arguments', nargs='*', help="Things to do.")
    parser.add_argument('-m', '--message', dest='message', help="Message to send.", default=None)
    parser.add_argument('-t', '--title', dest='title', help="Title of the message.", default=None)
    args = parser.parse_args()
    cmd_args = " ".join(args.arguments)
    cmds = filter(bool, cmd_args.split(','))
    cmds = "&".join(cmds)
    out = subprocess.call(cmds, shell=True)
    pb = pyBullet()

    message = "pyBullet task complete."
    title = "pyBullet"
    if args.message:
        message = args.message
    if args.title:
        title = args.title
    response = pb.push(title, message)

if __name__ == "__main__":
    main()
