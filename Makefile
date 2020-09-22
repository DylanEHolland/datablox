PYPATH="./";

all:
	@-echo Requires one of [tests|clean]

clean:
	rm -rfv datablox/*.pyc datablox/__pycache__;

prepare:
	if ! [ -d "env" ]; then python3 -m venv env && pip3 install -r requirements.txt; fi;

test:
	PYTHONPATH=$(PYPATH) python3 tests/test_block.py;
