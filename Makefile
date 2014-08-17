devinstall:
	python setup.py develop

publish:
	python setup.py sdist upload

test:
	pypy -m nose .
