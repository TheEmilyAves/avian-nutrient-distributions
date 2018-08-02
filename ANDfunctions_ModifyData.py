"""
Functions used to manipulate data for the Avian Nutrient Distributions Project
"""

# global variable list of ketocarotenoids
ketocarotenoids = ["astaxanthin"]


def convertCarot(bird, alt_calc=False, list_except=None, except_files=None):
    """
    Converts areas (HPLC output) into total amount of carotenoids in tissues.
    
    Note to self: add an elif statement to the alt_calc if statement so that 
    eye exceptions can be run by themselves
    """
    # iterate through bird dictionary with key=bird_id,value=bird_obj
    for bird_id,bird_obj in bird.items():
        # iterate through tissues dictionary with key=tissue_type,value=tissue_obj
        for tissue_type,tissue_obj in bird_obj.tissues.items():
            nutrients_ug = {}
            # iterate through nutrients_area dictionary with key=nutrient_type,value=nutrient_area
            for nutrient_type,nutrient_area in tissue_obj.nutrients_area.items():
                key = nutrient_type
                # if nutrient was not detectable
                if nutrient_area == "nd": 
                    value = 0
                # if nutrient has a detectable area from HPLC
                else: 
                    nutrient_area = eval(nutrient_area)
                    # if alternative calculations are needed (i.e. exceptions)
                    if alt_calc==True: 
                        # exception for eye and liver
                        if "eyeCalcExceptions.txt" in list_except and "liverCalcExceptions.txt" in list_except:
                            # for eye samples...
                            if tissue_type == "eye".lower() or tissue_type == "eyes".lower():
                                if bird_id in except_files["eyeCalcExceptions.txt"]:
                                    keto_vol = float(except_files["eyeCalcExceptions.txt"][bird_id][0])
                                    xan_vol = float(except_files["eyeCalcExceptions.txt"][bird_id][1])
                                    total_vol = keto_vol + xan_vol
                                    mult_keto = 4 * (total_vol / keto_vol)
                                    mult_xan = 4 * (total_vol / xan_vol)
                                    if nutrient_type in ketocarotenoids:
                                        value = calcCarot(tissue_obj, nutrient_area, mult_keto)
                                    else:
                                        value = calcCarot(tissue_obj, nutrient_area, mult_xan)
                                else:
                                    value = calcCarot(tissue_obj, nutrient_area, mult=8)
                            # for liver samples...
                            elif tissue_type == "liver".lower():
                                if bird_id in except_files["liverCalcExceptions.txt"]:
                                    liver_volume = float(except_files["liverCalcExceptions.txt"][bird_id][0])
                                    mult_liver = 4 * (liver_volume / 0.5)
                                else:
                                    mult_liver = 4 * (0.6 / 0.5)
                                value = calcCarot(tissue_obj, nutrient_area, mult_liver)
                            # for all other tissue types...
                            else:
                                value = calcCarot(tissue_obj, nutrient_area)
                        # all other potential exceptions
                        else:
                            print("There is no exception written for tissues other than eye and liver.")
                            print("This program will continue to completion using default calculations.")
                            # for eye samples...
                            if tissue_type == "eye".lower() or tissue_type == "eyes".lower():
                                value = calcCarot(tissue_obj, nutrient_area, mult=8)
                            # for all other tissue types...
                            else:
                                value = calcCarot(tissue_obj, nutrient_area)
                    # if default calculations can be used
                    else:
                        # for eye samples...
                        if tissue_type == "eye".lower() or tissue_type == "eyes".lower():
                            value = calcCarot(tissue_obj, nutrient_area, mult=8)
                        # for all other tissue types...
                        else:
                            value = calcCarot(tissue_obj, nutrient_area)
                nutrients_ug[key] = value
            setattr(tissue_obj, "nutrients_ug", nutrients_ug)


def calcCarot(tissue_obj, area, mult=4):
    """
    Calculates the total amount of carotenoids in a tissue given the area and 
    the appropriate multiplier.
    """
    carot_ug_sample = (0.0005 * area + 0.1294) * mult
    carot_ug_total = carot_ug_sample * (eval(tissue_obj.mass_total) / eval(tissue_obj.mass_sample))
    return carot_ug_total


def calcTotalCarot(bird):
    """
    Calculates total carotenoids in each tissue and the total amount of 
    carotenoids in the whole bird, then adds as properties to the TISSUE and 
    BIRD classes, respectively.
    
    total_carot is a float number that represents the total amount (ug) 
    of carotenoids in a given tissue.
    
    totalbodycarot (tbc) is a floating point number that represents the total
    amount of carotenoids in all tissues analyzed in an individual bird in 
    micrograms. used to calculate proportion of carotenoids in a given tissue 
    relative to the whole individual.
    """
    for bird_id,bird_obj in bird.items():
        totalbodycarot = 0
        for tissue_type,tissue_obj in bird_obj.tissues.items():
            totaltissuecarot = 0
            for nutrient_type, nutrient_ug in tissue_obj.nutrients_ug.items():
                totaltissuecarot += nutrient_ug
            setattr(tissue_obj, "total_carot", totaltissuecarot)
            totalbodycarot += totaltissuecarot
        setattr(bird_obj, "totalbodycarot", totalbodycarot)


def calcProp(bird):
    """
    Calculates proportion of carotenoids in a tissue out of total body 
    carotenoids in a bird and adds to appropriate bird object.
    """
    for bird_id,bird_obj in bird.items():
        tissue_p = {}
        for tissue_type, tissue_obj in bird_obj.tissues.items():
            key = tissue_type
            value = tissue_obj.total_carot / bird_obj.totalbodycarot
            tissue_p[key] = value
        setattr(bird_obj, "tissue_p", tissue_p)


def calcTissueRatio(bird):
    """
    Calculates proportion of whole tissue mass out of total body mass.
    """
    for bird_id,bird_obj in bird.items():
        tissue_r = {}
        for tissue_type, tissue_obj in bird_obj.tissues.items():
            key = tissue_type
            value = tissue_obj.mass_total / bird_obj.bodymass
            tissue_r[key] = value
        setattr(bird_obj, "tissue_r", tissue_r)


def calcRProp(bird):
    """
    Calculates relative proportion of all carotenoids in each tissue.
    """
    for bird_id,bird_obj in bird.items():
        relative_p = {}
        for tissue_type, tissue_obj in bird_obj.tissues.items():
            key = tissue_type
            value = bird_obj.tissue_p[tissue_type] / bird_obj.tissue_r[tissue_type]
            relative_p[key] = value
        setattr(bird_obj, "relative_p", relative_p)


def calcCarotConc(bird):
    """
    Calcultes concentration of all carotenoids in each tissue.
    """
    for bird_id,bird_obj in bird.items():
        carot_conc = {}
        for tissue_type, tissue_obj in bird_obj.tissues.items():
            key = tissue_type
            value = tissue_obj.total_carot / tissue_obj.mass_total
            carot_conc[key] = value
        setattr(bird_obj, "carot_conc", carot_conc)





