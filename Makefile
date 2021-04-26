PY ?= $(shell (python3 -c 'import sys; sys.exit(sys.version < "3.5")' && \
	      which python3) )
TARGET = "~/.local/"

ifeq ($(PY),)
  $(error No suitable python found(>=3.6).)
endif

lint:
	@if [ ! -f flake8 ]; then $(PY) -m pip install flake8; fi
	@flake8 -v --ignore=E501,E402,E203,E741 --show-source ./minimycobotflasher/main.py
	@echo

build:
	$(PY) -m pip install pyinstaller
	$(PY) -m pip install -r ./requeirment.txt
	$(PY) -m PyInstaller --clean ./main.spec
	@sudo chmod -R 766 dist/main/data

install: build
	@echo "installing ..."
	@sudo mv dist/main ~/.local/minimycobotflasher
	@sudo ln -fs ~/.local/minimycobotflasher/main /usr/local/bin/minimycobotflasher
	@source ~/.zshrc

uninstall:
	@echo "uninstall ..."
	@sudo rm -r ~/.local/minimycobotflasher
	@sudo rm /usr/local/bin/minimycobotflasher

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

del: clean
	@echo $(PY)
	@if [ -d ./dist ]; then sudo rm -r ./dist/; fi
	@if [ -d ./build ]; then sudo rm -r ./build; fi

pack:
	@sudo mv ./dist/main ./dist/minimycobotflasher
	@sudo tar -zcvf ./minimycobotflasher.tar.gz ./dist/minimycobotflasher

todo:
	@grep --color -Ion '\(TODO\|XXX\).*' -r .

aa:
	@sudo source ~/.zshrc

.PHONY: lint clean del build install uninstall todo
