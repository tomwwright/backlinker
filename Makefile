run:
	PYTHONPATH="$(PWD):$(PYTHONPATH)" ./bin/backlinker

install:
	python setup.py install

test:
	pytest -vv
