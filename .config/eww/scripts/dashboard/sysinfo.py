#!/usr/bin/env python3
import json
import glob
import psutil


def get_sys_info():
    cpu_percent = int(psutil.cpu_percent(interval=0.5))

    mem = psutil.virtual_memory()
    ram_total = int(mem.total / (1024 * 1024))
    ram_used = int((mem.total - mem.available) / (1024 * 1024))
    ram_percent = int(mem.percent)

    disk = psutil.disk_usage("/")

    def to_readable(bytes_value):
        for unit in ["B", "K", "M", "G", "T"]:
            if bytes_value < 1024:
                return f"{bytes_value:.1f}{unit}".replace(".0", "")
            bytes_value /= 1024
        return f"{bytes_value:.1f}T"

    disk_total = to_readable(disk.total)
    disk_used = to_readable(disk.used)
    disk_percent = int(disk.percent)

    temp = 0
    temps = psutil.sensors_temperatures()
    for chip in ["coretemp", "k10temp", "tctl", "acpitz", "zenpower", "amdgpu"]:
        if chip in temps and temps[chip]:
            temp = int(temps[chip][0].current)
            break

    if temp == 0:
        try:
            priority = ["x86_pkg_temp", "tcpu", "cpu", "soc", "pkg"]
            found = {}
            for zone in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
                zone_type = zone.replace("temp", "type")
                try:
                    with open(zone_type) as f:
                        ztype = f.read().strip().lower()
                    with open(zone) as f:
                        t = int(f.read().strip()) / 1000
                    if 0 < t < 120:
                        found[ztype] = int(t)
                except Exception:
                    continue
            for key in priority:
                for ztype, t in found.items():
                    if key in ztype:
                        temp = t
                        break
                if temp > 0:
                    break
        except Exception:
            temp = 0

    data = {
        "cpu": cpu_percent,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "ram_percent": ram_percent,
        "disk_used": disk_used,
        "disk_total": disk_total,
        "disk_percent": disk_percent,
        "temp": temp,
    }
    return json.dumps(data)


if __name__ == "__main__":
    print(get_sys_info())
