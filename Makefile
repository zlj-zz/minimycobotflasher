VENV ?= $(shell echo ${VIRTUAL_ENV})
PY ?= $(shell (python3 -c 'import sys; sys.exit(sys.version < "3.5")' && \
	      which python3) )
TARGET = "~/.local/opt/"

ifeq ($(VENV),)
$(error You should only use this within a virtual environment. See README)
endif
ifeq ($(PY),)
$(error No suitable python found(>=3.6).)
endif

lint:
	@if [ ! -f flake8 ]; then $(PY) -m pip install flake8; fi
	@flake8 -v --ignore=E501,E402,E203,E741 --show-source ./minimycobotflasher/main.py
	@echo

build:
	$(PY) -m pip install pyinstaller
	$(PY) -m pip install -r ./requirements.txt
	$(PY) -m PyInstaller --clean ./main.spec
	@chmod -R 766 dist/main/data

install: build
	@echo "installing ..."
	@mv dist/main ~/.local/opt/minimycobotflasher
	@mkdir ~/.local/bin
	@ln -fs ~/.local/opt/minimycobotflasher/main ~/.local/bin/minimycobotflasher

uninstall:
	@echo "uninstall ..."
	@rm -r ~/.local/opt/minimycobotflasher
	@rm ~./local/bin/minimycobotflasher

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

del: clean
	@echo $(PY)
	@rm -rf ./dist/
	@rm -rf ./build

pack:
	@mv ./dist/main ./dist/minimycobotflasher
	@tar -zcvf ./minimycobotflasher.tar.gz ./dist/minimycobotflasher

todo:
	@grep --color -Ion '\(TODO\|XXX\).*' -r .

.PHONY: lint clean del build install uninstall todo
