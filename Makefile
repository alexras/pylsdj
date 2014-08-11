devinstall:
	python setup.py develop

test:
	pypy -m nose .
