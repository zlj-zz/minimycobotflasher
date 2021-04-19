PY ?= $(shell (python3 -c 'import sys; sys.exit(sys.version < "3.5")' && \
	      which python3) )

ifeq ($(PY),)
  $(error No suitable python found(>=3.6).)
endif

lint:
	@if [ ! -f flake8 ]; then $(PY) -m pip install flake8; fi
	@flake8 -v --ignore=E501,E402,E203,E741 --show-source ./minimycobotflasher/main.py
	@echo

build:
	$(PY) -m pip install pyinstaller
	$(PY) -m PyInstaller ./main.spec

install: build
	@echo "installing ..."
	@sudo cp -r dist/main /opt/minimycobotflasher
	@sudo ln -fs /opt/minimycobotflasher/main /usr/local/bin/minimycobotflasher
	@source ~/.zshrc

uninstall:
	@echo "uninstall ..."
	@sudo rm -r /opt/minimycobotflasher
	@sudo rm /usr/local/bin/minimycobotflasher

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

del: clean
	@echo $(PY)
	@if [ -d ./dist ]; then rm -r ./dist/; fi
	@if [ -d ./build ]; then rm -r ./build; fi

todo:
	@grep --color -Ion '\(TODO\|XXX\).*' -r fungit

.PHONY: lint clean del build install todo
