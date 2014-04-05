from base import Base
from sqlalchemy import Column, Integer, String, Boolean

class Sample(Base):
	__tablename__ = 'samples'
	id = Column(Integer, primary_key=True)
	shipped = Column(String)
	received = Column(String)
	project = Column(String)
	sff = Column(String)
	mid_set = Column(String)
	plate = Column(String)
	mid = Column(String)
	sample = Column(String)
	collector = Column(String)
	year = Column(String)
	month = Column(String)
	day = Column(String)
	week = Column(String)
	year_week = Column(String)
	location = Column(String)
	city = Column(String)
	province = Column(String)
	crop = Column(String)
	source = Column(String)
	treatment = Column(String)
	substrate = Column(String)
	target = Column(String)
	primer_forward = Column(String)
	primer_reverse = Column(String)
	pcr_type = Column(String)
	taq = Column(String)
	purification = Column(String)
	rep_num = Column(String)
	cycle_num = Column(String)
	dna_dil = Column(String)
	annealing = Column(String)
	dna_ug = Column(String)
	notes = Column(String)
	sequencing_notes = Column(String)
	tm_c_max = Column(String)
	tm_c_min = Column(String)
	tm_c_avg = Column(String)
	
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __iter__(self):
		values = vars(self)
		for attr in self.__mapper__.columns.keys():
		    if attr in values:
			yield attr, values[attr]

