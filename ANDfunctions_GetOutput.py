"""
Functions used to generate output files for the Avian Nutrient Distributions Project
"""

# import modules
import csv


def getOutput_rp(bird):
    col_birdid = []
    col_sex = []
    col_treatment = []
    col_tissuetype = []
    col_rp = []
    for bird_id,bird_obj in bird.items():
        for tissue_type,tissue_obj in bird_obj.tissues.items():
            col_birdid.append(bird_id)
            col_sex.append(bird_obj.sex)
            col_treatment.append(bird_obj.treatment)
            col_tissuetype.append(tissue_type)
            col_rp.append(bird_obj.relative_p[tissue_type])
    return col_birdid, col_sex, col_treatment, col_tissuetype, col_rp


def getOutput_p(bird):
    col_birdid = []
    col_sex = []
    col_treatment = []
    col_tissuetype = []
    col_tip = []
    col_mt = []
    for bird_id,bird_obj in bird.items():
        for tissue_type,tissue_obj in bird_obj.tissues.items():
            col_birdid.append(bird_id)
            col_sex.append(bird_obj.sex)
            col_treatment.append(bird_obj.treatment)
            col_tissuetype.append(tissue_type)
            col_tip.append(bird_obj.tissue_p[tissue_type])
            col_mt.append(tissue_obj.mass_total)
    return col_birdid, col_sex, col_treatment, col_tissuetype, col_tip, col_mt


def colToRow(col0, col1, col2, col3, col4, col5):
    list_rows = []
    c = 0
    for i in col0:
        row = []
        row.append(col0[c])
        row.append(col1[c])
        row.append(col2[c])
        row.append(col3[c])
        row.append(col4[c])
        row.append(col5[c])
        list_rows.append(row)
        c += 1
    return list_rows


def writeOutput(outfile_name, list_rows, headers):
    outfile = open(outfile_name, "w")    
    with outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        writer.writerows(list_rows)

