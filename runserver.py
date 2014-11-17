#! ngssmenv/bin/python

from ngssm import app, connect_db

connect_db()
if 'HOST' in app.config:
  HOST=app.config['HOST']
else:
  HOST='127.0.0.1'

app.run(debug=True, host=HOST)

