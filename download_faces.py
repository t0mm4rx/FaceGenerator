import pyperclip
import requests
import os
import platform
import json
from progress.bar import Bar
import subprocess

if __name__ != '__main__':
    exit(0)

CODE_URL = "https://api.intra.42.fr/oauth/authorize?client_id=dded57253bdd723f2b41103a4c0e562117daff785fe27008cbebac4e4a502cec&redirect_uri=https%3A%2F%2Ftommarx.fr%2F&response_type=code"

MAX_REQUEST = 200

def get_bearer():
    if (not os.path.exists("./bearer.txt")):
        pyperclip.copy(CODE_URL)

        print("Paste copied URL in your browser if not opened, log in, and then paste code parameter here :")
        if (platform.system() == "Darwin"):
            os.system("open " + CODE_URL)
        else:
            os.system("xdg-open " + CODE_URL)
        code = input()

        api_call = requests.post('https://api.intra.42.fr/oauth/token', data={
            'grant_type': 'authorization_code',
            'client_id': 'dded57253bdd723f2b41103a4c0e562117daff785fe27008cbebac4e4a502cec',
            'client_secret': 'ca335789c4f3c82a9001f587928d07e86be14758f7642fdbc11902c8caffa82f',
            'redirect_uri': 'https://tommarx.fr/',
            'code': code
        })

        bearer = api_call.json()
        token = bearer['access_token']
        with open("bearer.txt", "w+") as file:
            file.write(token)
        return token
    else:
        return open("./bearer.txt", "r").read()


def get_users():
    if (not os.path.exists("./users.json")):
        bar = Bar('Fetching users', max=MAX_REQUEST + 400)
        result = []
        for i in range(200, MAX_REQUEST + 400):
            api_call = requests.get('https://api.intra.42.fr/v2/campus/1/users?page={}'.format(i), headers={'Authorization': 'Bearer {}'.format(get_bearer())})
            res = api_call.text
            print(res)
            try:
                res = json.loads(res)
            except ValueError as e:
                res = None
            bar.next()
            if (res != None):
                for obj in res:
                    if (not obj['login'] in result and not obj['login'][0] in "0123456789"):
                        result.append(obj['login'])
        bar.finish()
        with open("users.json", "w+") as file:
            file.write(json.dumps(result))
        print("Downloaded {} logins".format(len(result)))
        return result
    else:
        return list(set(json.loads(open("users.json").read())))

def download_images():
    users = get_users()
    bar = Bar('Downloading images', max=len(users))
    for user in users:
        if (not os.path.isfile('./images/{}.jpg'.format(user))):
            request = requests.get('https://cdn.intra.42.fr/users/small_{}.jpg'.format(user))
            with open('./images/{}.jpg'.format(user), "wb+") as file:
                file.write(request.content)
        bar.next()
    bar.finish()
    cleanup()

def cleanup():
    os.system("rm -if ./images/[0-9]*")
    deleted = 0
    for file in os.listdir("images/"):
        try:
            height = subprocess.check_output(["identify", "-format", "\"%h\"", "./images/{}".format(file)]).decode("utf-8")
            height = height.replace('"', '')
            height = int(height)
            if (int(height) != 175):
                deleted += 1
                os.system("rm -rf ./images/{}".format(file))
        except subprocess.CalledProcessError as e:
            deleted += 1
            os.system("rm -rf ./images/{}".format(file))
    print("{} files removed (piscine pictures and empty image)".format(deleted))

download_images()
