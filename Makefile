.PHONY: setup
setup:
	virtualenv ngssmenv
	ngssmenv/bin/pip install flask
	ngssmenv/bin/pip install flask-restful
	ngssmenv/bin/pip install flask-httpauth
	ngssmenv/bin/pip install sqlalchemy
	ngssmenv/bin/pip install xlrd
	ngssmenv/bin/pip install selenium
	ngssmenv/bin/pip install nose

.PHONY: db_clean
db_clean:
	rm -f ngssm.db

.PHONY: clean
clean: db_clean
	rm -rf ngssmenv
	find . -name "*.pyc" -delete

.PHONY: load
load:
	./ngssm/loader.py

.PHONY: run
run: setup
	./runserver.py

.PHONY: test
test:
	./ngssmenv/bin/nosetests
