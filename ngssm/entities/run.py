from base import Base
from sqlalchemy import Column, Integer, String, Boolean

class Run(Base):
	__tablename__ = 'run'
	id = Column(Integer, primary_key=True)

	# sequencer type: e.g. 454, MiSeq, HiSeq
	type = Column(String)

	# collection of index tags used
	# TODO load midsets into DB?
	mid_set = Column(String)

	# Historically, we've referred to all our 454 sequencing as PlateX-Y, where:
	#    X is our sequencing plate (numbered from 1 as we've submitted plates)
	#    Y is the region on the 454 sequencing plate; a plate contains a minimum of 2 regions
	# TODO - needs to be more generic, perhaps "Run Alias"
	plate = Column(String)

	sequencing_notes = Column(String)
