
.PHONY : develop build clean clean_pyc tseries doc test

test:
	py.test --cov=topojson --cov-report term

clean:
	-python setup.py clean

clean_pyc:
	-find . -name '*.py[co]' -exec rm {} \;

build: clean_pyc
	python setup.py bdist_wheel --universal;

lint-diff:
	git diff master --name-only -- "*.py" | grep "topojson" | xargs flake8

develop: build
	-python setup.py develop

doc:
	-rm -rf doc/build doc/source/generated
	cd doc; \
	python make.py clean; \
	python make.py html