import time
import os
import sys
import datetime

ROOT = ""
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

    for line in cache.splitlines():
        key, value = line.split("=", 1)
        if key == "LAST_UPDATE":
            last_update = value

    last_update = datetime.datetime.strptime(last_update, "%m-%d-%Y")
    last_update = last_update.strftime("%m-%d-%Y")

    Now = datetime.datetime.now()

    minimum_date_for_update = datetime.datetime.strptime(last_update, "%m-%d-%Y")
    minimum_date_for_update = minimum_date_for_update + datetime.timedelta(
        days=update_elapse
    )
    minimum_date_for_update = minimum_date_for_update.strftime("%m-%d-%Y")

    days_until_update = (
        datetime.datetime.strptime(minimum_date_for_update, "%m-%d-%Y") - Now
    )
    days_until_update = days_until_update.days + 1

    print(
        f"next update will be on {minimum_date_for_update} (in {days_until_update} days)"
    )

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
