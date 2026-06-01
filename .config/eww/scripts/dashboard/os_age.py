#!/usr/bin/env python3
import json
import subprocess


def get_os_age():
    try:
        cmd = "stat -c %W /"
        birth_timestamp = int(subprocess.check_output(cmd, shell=True).decode().strip())

        import time

        seconds_alive = time.time() - birth_timestamp
        days_alive = int(seconds_alive / 86400)

        if days_alive < 0:
            days_alive = 0

    except Exception:
        days_alive = 0

    return json.dumps({"days": days_alive})


if __name__ == "__main__":
    print(get_os_age())
