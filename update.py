import time
import os
import sys
import datetime

ROOT = "./Spicetify/"
CONFIG_PATH = ROOT + "update.conf"
CACHE_PATH = ROOT + "update.cache"

def check_for_update():
    with open(CONFIG_PATH, "r") as config_file:
        config = config_file.read()

    with open(CACHE_PATH, "r") as cache_file:
        cache = cache_file.read()

    for line in config.splitlines():
        key, value = line.split("=", 1)
        if key == "UPDATE_ELAPSE":
            update_elapse = int(value)

    try:
        update_elapse

    except NameError:
        print(f"UPDATE_ELAPSE not found in {CONFIG_PATH}.")
        print("using default settings (once every two days)")
        update_elapse = 2

    for line in cache.splitlines():
        key, value = line.split("=", 1)
        if key == "LAST_UPDATE":
            last_update = value

    try:
        last_update

    except NameError:
        print(f"LAST_UPDATE not found in {CACHE_PATH}.")
        print("using default settings (never)")
        last_update = None

    if not last_update == None:
        last_update = datetime.datetime.strptime(last_update, "%m-%d-%Y")
        last_update = last_update.strftime("%m-%d-%Y")

    Now = datetime.datetime.now()

    minimum_date_for_update = datetime.datetime.strptime(last_update, "%m-%d-%Y")
    minimum_date_for_update = minimum_date_for_update + datetime.timedelta(days=update_elapse)
    minimum_date_for_update = minimum_date_for_update.strftime("%m-%d-%Y")

    days_until_update = datetime.datetime.strptime(minimum_date_for_update, "%m-%d-%Y") - Now
    days_until_update = days_until_update.days + 1

    print(f"next update will be on {minimum_date_for_update} (in {days_until_update} days)")

    if last_update == None or Now.strftime("%m-%d-%Y") >= minimum_date_for_update:
        update_cache("LAST_UPDATE", datetime.datetime.now().strftime("%m-%d-%Y"))
        sys.exit(0)

    sys.exit(1)


def update_cache(key, value):
    with open(CACHE_PATH, "r") as cache_file:
        cache = cache_file.read()

    for line in cache.splitlines():
        key_cache, value_cache = line.split("=", 1)
        if key_cache == key:
            cache = cache.replace(line, key_cache + "=" + value)

    with open(CACHE_PATH, "w") as cache_file:
        cache_file.write(cache)


if __name__ == "__main__":
    check_for_update()
