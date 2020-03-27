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
    cols_carot = {}
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
        for tissue,nutrients in bird_obj.carot_conc_ind.items():
            for nutrient_type,carot_conc in nutrients.items():
                if nutrient_type in cols_carot:
                    cols_carot[nutrient_type].append(carot_conc)
                else:
                    value = []
                    value.append(carot_conc)
                    cols_carot[nutrient_type] = value
    return col_birdid, col_sex, col_treatment, col_tissuetype, col_mt, col_tip, col_rp, col_conc, col_tc, col_tbc, cols_carot


def getSimCol(bird):
    col_birdid = []
    col_sex = []
    col_treatment = []
    col_bodymass = []
    col_tissuetype = []
    col_mt = []
    cols_carot = {}
    for bird_id,bird_obj in bird.items():
        for tissue_type,tissue_obj in bird_obj.tissues.items():
            col_birdid.append(bird_id)
            col_sex.append(bird_obj.sex)
            col_treatment.append(bird_obj.treatment)
            col_bodymass.append(bird_obj.bodymass)
            col_tissuetype.append(tissue_type)
            col_mt.append(tissue_obj[0].mass_total)
        for tissue,nutrients in bird_obj.carot_conc_ind.items():
            for nutrient_type,carot_conc in nutrients.items():
                if nutrient_type in cols_carot:
                    cols_carot[nutrient_type].append(carot_conc)
                else:
                    value = []
                    value.append(carot_conc)
                    cols_carot[nutrient_type] = value
    return col_birdid, col_sex, col_treatment, col_bodymass, col_tissuetype, col_mt, cols_carot


# this function currently doesn't work, but I want to try and make it work 
# eventually - the point of it is to do what colToRow currently does but without 
# fixing the last column as cols_carot
def colToRow1(cols):
    list_rows = []
    for i in cols[0]:
        row = []
        for n,col in enumerate(cols):
            if isinstance(col, list):
                row.append(col[n])
            else:
                for nutrient_type,carot_conc in col.items():
                    row.append(carot_conc)
        list_rows.append(row)
    return list_rows


# allows n=10 (cols_carot) from getCol1 function to be "unpacked"
def colToRow(cols):
    list_rows = []
    for i,r in enumerate(cols[0]):
        row = []
        for n,col in enumerate(cols):
            if n == 6:
                for nutrient_type,carot_conc in col.items():
                    row.append(carot_conc[i])
            else:
                row.append(col[i])
        list_rows.append(row)
    return list_rows


def writeOutput(outfile_name, list_rows, headers):
    outfile = open(outfile_name, "w")    
    with outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)
        writer.writerows(list_rows)

