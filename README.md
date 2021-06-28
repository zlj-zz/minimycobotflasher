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

If you want to build manually, require Python3.6 or later.

```bash
cd minimycobotflasher
sudo make install
minimycobotflasher
```

### Run with source code.

Clone the repository.

```
git clone https://github.com/zlj-zz/minimycobotflasher.git <your path>
cd <your path>/minimycobotflasher
python3 main.py
```
