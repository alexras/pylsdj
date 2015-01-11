devinstall:
	python setup.py develop

publish:
	python setup.py sdist upload

test:
	nosetests --with-coverage --cover-package=pylsdj .

test-pypy:
	pypy -m nose .
