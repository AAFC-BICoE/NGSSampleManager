#! ngssmenv/bin/python

from ngssm import app, connect_db
connect_db()
app.run(debug=True)
