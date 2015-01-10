devinstall:
	python setup.py develop

publish:
	python setup.py sdist upload

test:
	python -m nose .

test-pypy:
	pypy -m nose .
