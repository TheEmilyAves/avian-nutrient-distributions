"""
Functions used to simulate data for the Avian Nutrient Distributions Project

Assumptions:
    -body and tissue masses are randomly normally distributed using house 
    finch data from fall 2017
    -each type of carotenoid is normally distributed within each tissue type
    for a given mu and sigma 
    -all same sex (male)
    -mass sample and mass total are the same for all tissues
    -simplest carotenoid profile (lutein and zeaxanthin only) with differences
    only in total amount by tissue or proportion of lutein vs. zeaxanthin and 
    all tissues except tidiff are plasma-like (2/3 lutein, 1/3 zeaxanthin)


What is the best method for generating variation in carotenoid types?
I could use carotenoid concentrations from real data (mu and sigma) then get 
the amount by multiplying by randomly generated tissue masses.
I could randomize amount and tissue mass separately and calculate concentraion 
from that. 
How are these two methods different? What effect would using either have on the data?
That decision rests on whether I think carotenoid allocation is driven by amount 
independent of tissue mass or concentration (dependent on tissue mass).
I think carotenoid allocation is tissue mass dependent, so I'm going to go with that.
Is there a way of testing that? I think there is, and I think it would be true.
But I should test it anyway if I want this to be truly based on real data.

Check best practices for when to set random seed when simulating data.
        
"""

# imports
import numpy as np
import ANDclasses as c

# global variable for group letters
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

# global variable for possible nutrient types
possnutri = ["lutein", "zeaxanthin"]

# global variable for tissue mass mu, sigma
# based on fall 2017 male house finches
tissue_masses = {"brain" : (0.78,0.07), 
                 "heart" : (0.27,0.03), 
                 "kidney" : (0.13,0.02), 
                 "liver" : (0.45,0.1), 
                 "lung" : (0.24, 0.04), 
                 "muscle" : (3.01,0.4), 
                 "spleen" : (0.017,0.009)}

# global variable for total carot conc mu, sigma
# based on fall 2017 male house finches
total_carot_conc = {"brain" : (0.99, 0.44), 
                    "heart" : (27.13, 8.24),
                    "kidney" : (26.42, 3.05), 
                    "liver" : (57.06, 25.35), 
                    "lung" : (32.70, 6.30), 
                    "muscle" : (7.17, 1.68), 
                    "spleen" : (47.04, 8.40)}


def simBIRD(parainput):
    """ 
    Similar to invokeBIRD but with simulated data
    
    Makes dictionary with key=birdid and value=BIRD object
    """
    # this entire function needs to be tested
    totalbird = parainput["ngroup"] * parainput["nbird"]  
    # generate list of unique numbers for each birdid
    birdnumbers = []
    for n in range(totalbird):
        birdnumbers.append(str(n + 1))
    # generate list of group letters for each birdid
    birdletters = []
    for g in range(parainput["ngroup"]):
        for nb in range(parainput["nbird"]):
            birdletters.append(alphabet[g])
    # merge letters and numbers to form birdids!
    birdids = [i + j for i, j in zip(birdletters, birdnumbers)]
    # generate sex data for BIRD init
    sex = ["Male"] * totalbird
    # generate treatment group data for BIRD init (same as birdletters)
    treatment = birdletters
    # generate tissue dictionaries with keys corresponding to tissue names
    # based on parameter inputs and empty values to be filled in later
    bird_tissue_dicts = {} # fill with key = birdid, value = tissue dict
    # iterate through birdids and add same tissue dict to each one
    # tissue dict contains key = tissue names, value = empty 
    for b in birdids:
        key1 = b
        value1 = {} # empty tissues dict
        for t in parainput["whichti"]:
            key2 = t
            value1.setdefault(key2, [])
        bird_tissue_dicts[key1] = value1
    # generate body mass data for BIRD init
    # using average (18.5) and stdev (1.6) of fall 2017 house finches
    # can edit this later to be more flexible
    mu, sigma = 18.5, 1.6
    np.random.seed()
    bodymass = np.random.normal(mu, sigma, totalbird).round(2)
    i = 0
    bird = {}
    for b in birdids:
        bird[b] = c.BIRD(i = b, s = sex[i], tr = treatment[i], bm = bodymass[i], ti = bird_tissue_dicts[b])
        i += 1
    return bird
    # right now this dictinary of bird objects contain id, sex, treatment, bodymass, 
    # and dictionaries of tissue types with empty values


def simTISSUE(bird, parainput):
    """
    Similar to invokeTISSUE but with simulated data
    
    need to incorporate randomly generating nutrient concentrations for each tissue
    and the boolean values for constanttc and constantcp as well as tidiff
    
    maybe based on total concentration and proportion of each carotenoid type 
    is calculated based on response to constancp
    
    could use random choice function to select group that differs
    e.g. diff = rand.choice("A", "B")
    
    output of this function should be simulated version of carot_conc_ind, 
    which is a bird_obj dictionary with key = tissue_type and value = 
    dictionary with key = nutrient_type and value = carot conc
    
    start coding as if both statements are true (no diff at all) then edit 
    later to incorporate other possibilities (one true, one false, both false)
    """
    carot_conc_ind = {}
    for bird_id, bird_obj in bird.items():
        treatment = bird_obj.treatment
        for tissue_type in bird_obj.tissues.key():
            key1 = tissue_type
            value1 = {}
            # for each possible nutrient in these tissues
            for n in possnutri:
                # set key in value1 to nutrient type
                key2 = n
                value2 = simNutrients(n, tissue_type, treatment, parainput)
                value1[key2] = value2
            carot_conc_ind[key1] = value1
            mass_total = simMass(tissue_type)
            mass_sample = mass_total
            tissue_obj = c.TISSUE(n = tissue_type, ms = mass_sample, mt = mass_total, b = bird_id)
            bird_obj.tissues[tissue_type].append(tissue_obj)
        setattr(bird_obj, "carot_conc_ind", carot_conc_ind)


def simNutrients(nt, tt, tr, parainput):
    """
    Similar to getNutrients but with simulated data
    
    parainput variables are all str right now; may have to add code to convert 
    to Bool vs. other types of info
    
    check assumption that all nutrients within tissue types are normally distributed
    
    will need to generalize code later for more than two groups if needed
    """    
    # section 1 - assigning variables
    # mod_np = nutrient proportion modifier (e.g. 2/3 for lutein in group "A")
    # mod_ms = mu, sigma modifier (e.g. 1.5 for 50% increase in total carotenoids)
    
    # if the current tissue is different between groups AND 
    # this bird is not a control bird, then...
    if (tt in parainput["tidiff"]) and (tr != "A"):
        if parainput["constanttc"] == True:
            mod_ms = 1
            if parainput["constantcp"] == True:
                if nt == "lutein":
                    mod_np = 2/3
                elif nt == "zeaxanthin":
                    mod_np = 1/3
                else:
                    pass
            elif parainput["constantcp"] == False:
                if nt == "lutein":
                    mod_np = 1/3
                elif nt == "zeaxanthin":
                    mod_np = 2/3
                else:
                    pass
        elif parainput["constanttc"] == False:
            mod_ms = 1.5
            if parainput["constantcp"] == True:
                if nt == "lutein":
                    mod_np = 2/3
                elif nt == "zeaxanthin":
                    mod_np = 1/3
                else:
                    pass
            elif parainput["constantcp"] == False:
                if nt == "lutein":
                    mod_np = 1/3
                elif nt == "zeaxanthin":
                    mod_np = 2/3
                else:
                    pass     
        else:
                print("error")
    # otherwise (if tissue is not different or it is but this is a control bird)...
    else:
        mod_ms = 1
        if nt == "lutein":
            mod_np = 2/3
        elif nt == "zeaxanthin":
            mod_np = 1/3
        else:
            pass
    # section 2 - calculate carot_conc using variables
    for tissue_type, tissue_carot in total_carot_conc.items():
        if tt == tissue_type:
            mu, sigma = tissue_carot * mod_ms
            np.random.seed()
            carot_conc = np.random.normal(mu, sigma) * mod_np
            return carot_conc
        else:
            pass


def simMass(tt):
    """
    Simulates tissue masses 
    
    Currently based on house finch data from fall 2017
    """
    for tissue_type, tissue_mass in tissue_masses.items(): 
        # if the tissue type matches one of the tissues in the list...
        if tt == tissue_type:
            mu, sigma = tissue_mass
            np.random.seed()
            mass_total = np.random.normal(mu, sigma)
            return mass_total
        # do not do anything if there is a tissue that does not match
        else:
            pass
        

### test code zone ###

import ANDfunctions_StoreData as sd

my_file, outfile_name, alt_calc, list_except = sd.getInput()
parainput = sd.readSimInputs(my_file)
bird = simBIRD(parainput)














