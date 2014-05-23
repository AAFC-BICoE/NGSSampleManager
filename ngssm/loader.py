#! ngssmenv/bin/python

from entities.base import Base
from entities.sample import Sample
from entities.run import Run
from helpers.xlssample import summary_to_entity, entity_to_index
from helpers.orm import get_or_create

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import xlrd

workbook = xlrd.open_workbook('454_sample_summary.xls')
worksheet = workbook.sheet_by_name('Data')

engine = create_engine ('sqlite:///ngssm.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

num_cols = worksheet.ncols -1
print ("Columns: {} ").format(num_cols)
curr_col = -1
while curr_col < num_cols:
	curr_col += 1
	col = worksheet.col(curr_col)
	heading = worksheet.cell_value(0,curr_col)
	if heading in summary_to_entity:
		print ("Setting \"index\" to {} for {}").format(curr_col, heading)
		entity_to_index[summary_to_entity[heading]] = curr_col


session = Session()
num_rows = worksheet.nrows -1
print ("Rows: {} ").format(num_rows)
curr_row = 0 # skip the header row
while curr_row < num_rows:
	curr_row += 1

	run = get_or_create(session, Run, 
		type="454",
		mid_set=worksheet.cell_value(curr_row, entity_to_index['mid_set']),
		plate=worksheet.cell_value(curr_row, entity_to_index['plate']),
		sequencing_notes=worksheet.cell_value(curr_row, entity_to_index['sequencing_notes'])
	)

	sample = Sample(
		run=run,
		shipped=worksheet.cell_value(curr_row, entity_to_index['shipped']),
		received=worksheet.cell_value(curr_row, entity_to_index['received']),
		project=worksheet.cell_value(curr_row, entity_to_index['project']),
		sff=worksheet.cell_value(curr_row, entity_to_index['sff']),
		mid=worksheet.cell_value(curr_row, entity_to_index['mid']),
		sample=worksheet.cell_value(curr_row, entity_to_index['sample']),
		collector=worksheet.cell_value(curr_row, entity_to_index['collector']),
		year=worksheet.cell_value(curr_row, entity_to_index['year']),
		month=worksheet.cell_value(curr_row, entity_to_index['month']),
		day=worksheet.cell_value(curr_row, entity_to_index['day']),
		week=worksheet.cell_value(curr_row, entity_to_index['week']),
		year_week=worksheet.cell_value(curr_row, entity_to_index['year_week']),
		location=worksheet.cell_value(curr_row, entity_to_index['location']),
		city=worksheet.cell_value(curr_row, entity_to_index['city']),
		province=worksheet.cell_value(curr_row, entity_to_index['province']),
		crop=worksheet.cell_value(curr_row, entity_to_index['crop']),
		source=worksheet.cell_value(curr_row, entity_to_index['source']),
		treatment=worksheet.cell_value(curr_row, entity_to_index['treatment']),
		substrate=worksheet.cell_value(curr_row, entity_to_index['substrate']),
		target=worksheet.cell_value(curr_row, entity_to_index['target']),
		primer_forward=worksheet.cell_value(curr_row, entity_to_index['primer_forward']),
		primer_reverse=worksheet.cell_value(curr_row, entity_to_index['primer_reverse']),
		pcr_type=worksheet.cell_value(curr_row, entity_to_index['pcr_type']),
		taq=worksheet.cell_value(curr_row, entity_to_index['taq']),
		purification=worksheet.cell_value(curr_row, entity_to_index['purification']),
		rep_num=worksheet.cell_value(curr_row, entity_to_index['rep_num']),
		cycle_num=worksheet.cell_value(curr_row, entity_to_index['cycle_num']),
		dna_dil=worksheet.cell_value(curr_row, entity_to_index['dna_dil']),
		annealing=worksheet.cell_value(curr_row, entity_to_index['annealing']),
		dna_ug=worksheet.cell_value(curr_row, entity_to_index['dna_ug']),
		notes=worksheet.cell_value(curr_row, entity_to_index['notes']),
		tm_c_max=worksheet.cell_value(curr_row, entity_to_index['tm_c_max']),
		tm_c_min=worksheet.cell_value(curr_row, entity_to_index['tm_c_min']),
		tm_c_avg=worksheet.cell_value(curr_row, entity_to_index['tm_c_avg']),
	)
	session.add(sample)
session.commit()

