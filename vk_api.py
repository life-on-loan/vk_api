#!/usr/bin/env python3
import sys
import requests

request_pattern = "https://api.vk.com/method/{0}?{1}&access_token={2}&v=5.130"


def get_token():
    with open("token.txt", "r", encoding="utf-8") as file:
        return file.read()


def handle_response(user, vk_token):
    user_info = requests.get(request_pattern.format("users.get",
                                                    f"user_ids={user}&fields=city,bdate,counters",
                                                    vk_token)).json()['response'][0]
    res = "Information about user: \n"
    res += "*************************************************************************** \n"
    res += "User ID: " + str(user_info["id"]) + "\n"
    res += "First name: " + str(user_info["first_name"]) + "\n"
    res += "Last name: " + str(user_info["last_name"]) + "\n"
    res += "Birthday: " + user_info["bdate"] + "\n"
    res += "Сity: " + user_info["city"]["title"] + "\n" if user_info.get(
        "city") else "Сity: " + "the city is not specified" + "\n"
    res += "Number of videos: " + str(user_info["counters"]["videos"]) + "\n"
    res += "Number of audios: " + str(user_info["counters"]["audios"]) + "\n"
    res += "Number of gifts : " + str(user_info["counters"]["gifts"]) + "\n"
    res += "Number of photos : " + str(user_info["counters"]["photos"]) + "\n"
    res += "Number of followers : " + str(user_info["counters"]["followers"]) + "\n"
    res += "Number of friends : " + str(requests.get("https://api.vk.com/method/friends.get", {
        'user_id': args[1],
        'access_token': token,
        'v': '5.130'
    }).json()["response"]["count"]) + "\n"
    res += "*************************************************************************** \n"
    return res


def get_list_user_friends(user, vk_token):
    try:
        request = requests.get(request_pattern.format("friends.get",
                                                      f"user_id={user}&order=random",
                                                      vk_token))
        friend_request = requests.get(
            request_pattern.format("users.get",
                                   f"user_ids={(request.json()['response'])['items']}&fields=city",
                                   vk_token))
        count = 0
        list_friends = ""
        for friend_info in friend_request.json()['response']:
            count += 1
            first_name = friend_info['first_name']
            last_name = friend_info['last_name']
            city = friend_info.get("city")
            city = city.get("title") if city else "the city is not specified"
            list_friends += " - " + first_name + " " + last_name + " from " + city + "\n"
        return list_friends
    except KeyError:
        sys.exit("Error parameters.")
    except requests.exceptions.ConnectionError:
        sys.exit("Connection to Internet error.")


if __name__ == '__main__':
    args = sys.argv
    if args[1] == "-h" or args[1] == "-help":
        print("py vk_apy.py {user_id}")
    else:
        token = get_token()
        info = handle_response(args[1], token)
        friends = get_list_user_friends(args[1], token)
        print(info + "\n" + "List of friends:" + "\n" + friends)
