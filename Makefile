PYPATH="./";

all:
	@-echo Requires one of [tests]

test:
	PYTHONPATH=$(PYPATH) python3 tests/test_block.py;

clean:
	rm -rfv datablox/*.pyc datablox/__pycache__;