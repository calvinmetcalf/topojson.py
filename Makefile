all:
	install

install:
	python setup.py install

test:
	python -m pytest --pyargs --doctest-modules topojson

test-coverage:
	python -m pytest --pyargs --doctest-modules --cov=topojson --cov-report term topojson

test-coverage-html:
	python -m pytest --pyargs --doctest-modules --cov=topojson --cov-report html topojson
