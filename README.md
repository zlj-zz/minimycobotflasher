## Burning mycobot firmware in the Terminal.

This is a very small tool to help you burn **mycobot** Firmware, it's not as big as GUI.

- Support local firmware
- Support remote firmware,

### Permissions

If you need to communicate with your device, please ensure that you have the
correct permissions. For example, on Ubuntu Linux, you must ensure that your
user is part of the `dialout` group. e.g.: <br/>
<https://askubuntu.com/a/133244/692420> <br/>
Note that it will be easiest to log out of your current session and log back in
(see [this post](https://superuser.com/questions/272061/reload-a-linux-users-group-assignments-without-logging-out)
for more information). You can the check that your current shell session has
your the correct permissions by checking for `dialout` in a command like this:
```sh
$ id
uid=1001(myuser) gid=1002(myuser) groups=1002(myuser),20(dialout),27(sudo)
```

### Install

Ensure you have Python 3 and a way to provision local virtual environments.

As an example for Ubuntu:

```bash
sudo apt install python3 python3-venv
```

Then clone the repository.

```bash
git clone https://github.com/zlj-zz/minimycobotflasher.git
```

### Setup Virtual Environment

```bash
cd minimycobotflasher
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -U pip
pip3 install -r ./requirements.txt
```

### Run with source code.

```bash
source ./venv/bin/activate
python3 main.py --help
```

### Install for Packaging

If you want to build manually, require Python3.6 or later.

```bash
cd minimycobotflasher
source ./venv/bin/activate
make install
which minimycobotflasher
```
