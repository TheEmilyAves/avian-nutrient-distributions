"""
Functions used to generate output files for the Avian Nutrient Distributions Project
"""

# import modules
import csv

def getCol(bird):
    col_birdid = []
    col_sex = []
    col_treatment = []
    col_tissuetype = []
    col_mt = []
    col_tip = []
    col_rp = []
    col_conc = []
    col_tc = []
    col_tbc = []
    for bird_id,bird_obj in bird.items():
        for tissue_type,tissue_obj in bird_obj.tissues.items():
            col_birdid.append(bird_id)
            col_sex.append(bird_obj.sex)
            col_treatment.append(bird_obj.treatment)
            col_tissuetype.append(tissue_type)
            col_mt.append(tissue_obj.mass_total)
            col_tip.append(bird_obj.tissue_p[tissue_type])
            col_rp.append(bird_obj.relative_p[tissue_type])
            col_conc.append(bird_obj.carot_conc[tissue_type])
            col_tc.append(tissue_obj.total_carot)
            col_tbc.append(bird_obj.totalbodycarot)
    return col_birdid, col_sex, col_treatment, col_tissuetype, col_mt, col_tip, col_rp, col_conc, col_tc, col_tbc


def colToRow(col0, col1, col2, col3, col4, col5, col6, col7, col8, col9):
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
        row.append(col6[c])
        row.append(col7[c])
        row.append(col8[c])
        row.append(col9[c])
        list_rows.append(row)
        c += 1
    return list_rows


def writeOutput(outfile_name, list_rows, headers):
    outfile = open(outfile_name, "w")    
    with outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        writer.writerows(list_rows)

