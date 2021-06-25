## Burning mycobot firmware in the Terminal.

This is a very small tool to help you burn **mycobot** Firmware, it's not as big as GUI.

- Support local firmware
- Support remote firmware,

### Prerequisites

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
