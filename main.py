import argparse
import serial
import serial.tools.list_ports
import requests
import re
import os
import signal

import esptool


TARGET_DIR = os.path.dirname(__file__) + "/firmwares"
read_file_one = os.path.dirname(__file__) + "/data/boot_app0.bin"
read_file_two = os.path.dirname(__file__) + "/data/bootloader_qio_80m.bin"
commands = [
    "--chip",
    "esp32",
    "--port",
    "port...",
    "--baud",
    "921600",
    "--before",
    "default_reset",
    "--after",
    "hard_reset",
    "write_flash",
    "-z",
    "--flash_mode",
    "dio",
    "--flash_freq",
    "80m",
    "--flash_size",
    "detect",
    "0xe000",
    read_file_one,
    "0x1000",
    read_file_two,
    "0x10000",
    "file_1...",
    "0x8000",
    "file_2...",
]
port = 3
baud = 5
file_one = -3
file_two = -1

remote_url = "https://www.elephantrobotics.com/software/mystudio/apps-2.0/myCobot/"
item_re = re.compile(r"alt=\"\[DIR\]\"><\/td><td><a href=\"(.*?)\/\">")


def get_port():
    print("====================================================================")
    plist = list(serial.tools.list_ports.comports())
    max_ = len(plist)
    idx = 1
    for port in plist:
        print("{} : {}".format(idx, port))
        idx += 1

    _in = input("\nPlease input 1 - {} to choice(default {}):".format(idx - 1, max_))
    try:
        _in = int(_in)
        _in = max_ if _in > max_ else _in
    except Exception:
        _in = max_
    print('choice: {}'.format(_in))

    port = str(plist[(_in) - 1]).split(" - ")[0].strip()
    print(port)
    return port


# ====================================================================
# remote option functions
# ====================================================================
def get_remote_firmwares():
    try:
        resp = requests.get(remote_url)
    except Exception:
        print("Please check your network!!!")
        raise SystemExit(0)
    content = resp.content.decode()
    items = item_re.findall(content, re.S)
    return items


def get_remote_versions(name: str):
    resp = requests.get(remote_url + name)
    content = resp.content.decode()
    versions = item_re.findall(content, re.S)
    return versions


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def wether_exist(paths):
    return os.path.exists(paths[0])


def download_firmware(name, version):
    url = remote_url + f"{name}/{version}/"
    resp = requests.get(url)
    content = resp.content.decode()
    firmware_re = re.compile(r"alt=\"\[\s+\]\"><\/td><td><a href=\"(.*?)\">")
    firmwares = firmware_re.findall(content, re.S)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept-Encoding": "identity",
    }
    # print(firmwares)

    download_path = "/".join([TARGET_DIR, name, version])
    ensure_path(download_path)

    download_urls = [url + firmware for firmware in firmwares]
    pathes = [download_path + "/" + firmware for firmware in firmwares]
    has_downloaded = wether_exist(pathes)
    if has_downloaded:
        re_download = input("Do you want to download it again?[Y/n] (default: no):")
        if re_download in ["n", "no", "N", "NO", ""]:
            print("Flash from localtion.")
            return pathes

    print(f"Download path: {download_path}")
    for name, download_url, path in zip(firmwares, download_urls, pathes):
        resp_stream = requests.get(download_url, headers=headers, stream=True)
        total_size = int(resp_stream.headers["content-length"])
        sum = 0
        with open(path, "wb") as f:
            for chunk in resp_stream.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    sum += len(chunk)
                    print(
                        "\r  {} downloaded: [{}{}] {}".format(
                            name,
                            int(sum / total_size * 100) * "#",
                            int((1 - sum / total_size) * 100) * "*",
                            sum,
                        ),
                        end="",
                    )
        print("")
    return pathes


def remote_option():
    global commands

    print("====================================================================")
    remote_items = get_remote_firmwares()
    for idx, item_name in enumerate(remote_items):
        print(f"{idx}: {item_name}")
    item_idx = input("Please choice one firmware, input id(default: 0):")
    try:
        item_idx = int(item_idx)
    except Exception:
        item_idx = 0
    choice_item = remote_items[item_idx]
    print(f"choice: {item_idx}")

    print("====================================================================")
    versions = get_remote_versions(choice_item)
    for idx, version in enumerate(versions):
        print(f"{idx}: {version}")
    version_idx = input("Please choice one version, input id(default: 0):")
    try:
        version_idx = int(version_idx)
    except Exception:
        version_idx = 0
    choice_version = versions[version_idx]
    print(f"choice: {version_idx}")

    pathes = download_firmware(choice_item, choice_version)
    commands[file_one] = pathes[0]
    commands[file_two] = pathes[1]


# ====================================================================
# local option functions
# ====================================================================
def get_local_items():
    return os.listdir(TARGET_DIR)


def get_local_versions(name):
    dir_ = TARGET_DIR + "/" + name
    return os.listdir(dir_)


def local_option():
    global commands

    print("====================================================================")
    try:
        local_items = get_local_items()
    except FileNotFoundError:
        print("No local firmware, try to download remotely!!!")
        raise SystemExit(0)
    # check if has local firmware.
    if not local_items:
        print("No local firmware, try to download remotely!!!")
        raise SystemExit(0)
    for idx, item in enumerate(local_items):
        print(f"{idx}: {item}")
    item_idx = input("Please choice one(default: 0):")
    try:
        item_idx = int(item_idx)
    except Exception:
        item_idx = 0
    choice_item = local_items[item_idx]
    print(f"choice: {item_idx}")

    print("====================================================================")
    versions = get_local_versions(choice_item)
    for idx, version in enumerate(versions):
        print(f"{idx}: {version}")
    version_idx = input("Please choice one(default: 0):")
    try:
        version_idx = int(version_idx)
    except Exception:
        version_idx = 0
    choice_version = versions[version_idx]
    print(f"choice: {version_idx}")

    dir_path = f"{TARGET_DIR}/{choice_item}/{choice_version}/"
    firewares = os.listdir(dir_path)
    print(firewares)

    commands[file_one] = dir_path + firewares[0]
    commands[file_two] = dir_path + firewares[1]


def exit_(*args):
    raise SystemExit(0)


# main
def main():
    try:
        signal.signal(signal.SIGINT, exit_)
    except Exception:
        pass
    args = argparse.ArgumentParser()
    args.add_argument("-b", "--baudrate", help="Port baudrate.")
    stdargs = args.parse_args()
    if stdargs.baudrate:
        commands[baud] = stdargs.baudrate
    else:
        print("====================================================================")
        print("0: basic")
        print("1: atom")
        board = input("Please choice board(default: 0):")
        try:
            board = int(board)
        except Exception:
            board = 0
        if board == 1:
            commands[baud] = "1500000"

    port_str = get_port()
    commands[port] = port_str

    print("====================================================================")
    print("0: choice from local.")
    print("1: choice from remote.")
    c = input("Please firmware localtion(default: 0):")
    try:
        c = int(c)
    except Exception:
        c = 0
    print(f"choice: {c}")
    if c == 0:
        local_option()
    elif c == 1:
        remote_option()

    try:
        esptool.main(commands)
    except OSError as e:
        print(f"Error encountered! {e}")
        print()
        if "Permission denied" in str(e):
            print("Please ensure you part of the `dialout` group. See README "
                  "for more details")
        else:
            print("Please do not disconnect from the device.")
    except esptool.FatalError as e:
        print(e)


if __name__ == "__main__":
    main()
