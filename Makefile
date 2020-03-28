run:
	PYTHONPATH="$(PWD):$(PYTHONPATH)" ./bin/backlinker

test:
	pytest -v