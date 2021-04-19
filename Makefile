PY ?= $(shell (python3 -c 'import sys; sys.exit(sys.version < "3.5")' && \
	      which python3) )

ifeq ($(PY),)
  $(error No suitable python found(>=3.6).)
endif

lint:
	@if [ ! -f flake8 ]; then $(PY) -m pip install flake8; fi
	@flake8 -v --ignore=E501,E402,E203,E741 --show-source ./minimycobotflasher/main.py
	@echo

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

del: clean
	@if [ -d ./dist ]; then rm -r ./dist/; fi
	@if [ -d ./build ]; then rm -r ./build; fi

todo:
	@grep --color -Ion '\(TODO\|XXX\).*' -r fungit

.PHONY: run lint clean del install release todo
