.PHONY: setup
setup: ngssmenv

.PHONY: test
test: setup
	./ngssmenv/bin/nosetests

.PHONY: load
load: setup
	./ngssm/loader.py

.PHONY: run
run: setup
	./runserver.py

.PHONY: db_clean
db_clean:
	rm -f ngssm.db test.db

.PHONY: clean
clean: db_clean
	rm -rf ngssmenv
	find . -name "*.pyc" -delete

ngssmenv:
	virtualenv ngssmenv
	ngssmenv/bin/pip install flask==0.9
	ngssmenv/bin/pip install flask-restful
	ngssmenv/bin/pip install flask-login
	ngssmenv/bin/pip install flask-openid
	ngssmenv/bin/pip install flask-httpauth
	ngssmenv/bin/pip install flask-mail==0.7.6
	ngssmenv/bin/pip install sqlalchemy==0.7.9
	ngssmenv/bin/pip install flask-sqlalchemy==0.16
	ngssmenv/bin/pip install sqlalchemy-migrate==0.7.2
	ngssmenv/bin/pip install flask-whooshalchemy==0.55a
	ngssmenv/bin/pip install flask-wtf==0.8.4
	ngssmenv/bin/pip install pytz==2013b
	ngssmenv/bin/pip install flask-babel==0.8
	ngssmenv/bin/pip install flup
	ngssmenv/bin/pip install xlrd
	ngssmenv/bin/pip install selenium
	ngssmenv/bin/pip install nose
