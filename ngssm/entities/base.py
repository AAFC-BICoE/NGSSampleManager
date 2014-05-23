from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
	
def as_dict(self):
	return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def __iter__(self):
	values = vars(self)
	for attr in self.__mapper__.columns.keys():
	    if attr in values:
		yield attr, values[attr]
