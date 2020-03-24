"""
Functions used to simulate data for the Avian Nutrient Distributions Project

To do:
    -write function(s) to construct bird obj with parameterized carotenoid types/amounts
        -inputs: number of groups, whether you want total carot and/or carot profile
        to be same/different between groups/tissues, whether you want differences between 
        tissue types, number of tissues (or list of which tissues?), number of individuals, 
        mean and variation for carotenoids in each tissue
        -these inputs should probably be a txt file rather than manual inputs
        with only one manual input (name of this txt file)
        -do I edit my original getInputs func or write new one? Prob edit
        -output: csv file with data that I can analyze in R
        -some of this involves editing of existing functions (e.g., getInput)
        -randomly generate data for nutrient dictionaries based on inputs
        -how to do this in python?
    -take bottom up approach to coding this
    -so far these are the assumptions:
        -body and tissue masses are randomly normally distributed using house 
        finch data from fall 2017
        -each type of carotenoid is normally distributed within each tissue type
        for a given mu and sigma (should explore the real data to confirm if this is
        true or not)
        -all same sex (male)
        -mass sample and mass total are the same for all tissues
        -simplest carotenoid profile (lutein and zeaxanthin only) with differences
        only in total amount by tissue or proportion of lutein vs. zeaxanthin and 
        all tissues except tidiff are plasma-like

Might have to take top down approach for this one...because we're starting with
individual level factors and generating nutrients based on that.

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


def simBIRD(parainput):
    """ 
    Similar to invokeBIRD but with simulated data
    
    Makes dictionary with key=birdid and value=BIRD object
    """
    # this entire function needs to be tested
    bird = {}
    totalbird = int(parainput["ngroup"])*int(parainput["nbird"])  
    # generate list of unique numbers for each birdid
    birdnumbers = []
    for n in range(totalbird):
        birdnumbers.append(n + 1)
    # generate list of group letters for each birdid
    for g in range(int(parainput["ngroup"])):
        birdletters = list(alphabet[g + 1]) * int(parainput["nbird"])
    # merge letters and numbers to form birdids!
    birdids = [i + j for i, j in zip(str(birdletters), str(birdnumbers))]
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

        # use this code later to make sure I'm able to add values to these dicts
            #a.setdefault(key, [])
            #a[key].append()
    
    # generate body mass data for BIRD init
    # using average (18.5) and stdev (1.6) of fall 2017 house finches
    # can edit this later to be more flexible
    mu, sigma = 18.5, 1.6
    np.random.seed()
    bodymass = np.random.normal(mu, sigma, totalbird)
    i = 0
    for b in birdids:
        bird[b] = c.BIRD(i = b, s = sex[i], tr = treatment[i], bm = bodymass[i], ti = bird_tissue_dicts[b])
        i += 1
    return bird
    # right now this dictinary of bird objects contain id, sex, treatment, bodymass, 
    # and dictionaries of tissue types with empty values


def simTISSUE(bird, parainput):
    """
    Similar to invokeTISSUE but with simulated data
    
    to invoke TISSUE, need id, tissue type, mass sample, mass total, and 
    nutrients dict (key = nutrient name, value = carotenoid concentration
    generated randomly based on given mu and sigma)
    
    put all of this except call simNutrients when getting to the part about 
    carotenoid concentration random generation, which will pass through a series 
    of if/else statements to determine what the mu/sigma are and which tissues 
    will vary between groups and in what ways
    
    need to incorporate randomly generating nutrient concentrations for each tissue
    and randomly generating tissue masses for each tissue
    and the boolean values for constanttc and constantcp as well as tidiff
    
    might be a simpler solution to have a dictionary of tuples (mu, sigma) for 
    each tissue type rather than a bunch of if/else statements (but this only 
    covers total carot for each tissue, what about carotenoid types?)
    
    maybe based on total concentration and proportion of each carotenoid type 
    is calculated based on response to constancp
    
    could use random choice function to select group that differs
    e.g. diff = rand.choice("A", "B")
    
    output of this function should be simulated version of carot_conc_ind, 
    which is a bird_obj dictionary with key = tissue_type and value = 
    dictionary with key = nutrient_type and value = carot conc
    
    I would also like to make tissue_obj and add these to bird_obj
    
    start coding as if both statements are true (no diff at all) then edit 
    later to incorporate other possibilities (one true, one false, both false)
    """
    carot_conc_ind = {}
    for bird_id, bird_obj in bird.items():
        for tissue_type in bird_obj.tissues.key():
            key1 = tissue_type
            value1 = {}
            # for each possible nutrient in these tissues
            for n in possnutri:
                # set key in value1 to nutrient type
                key2 = n
                value2 = simNutrients(n, tissue_type, parainput)
                value1[key2] = value2
            carot_conc_ind[key1] = value1
            mass_total = simMass(tissue_type)
            mass_sample = mass_total
            tissue_obj = c.TISSUE(n = tissue_type, ms = mass_sample, mt = mass_total, b = bird_id)
            bird_obj.tissues[tissue_type].append(tissue_obj)
        setattr(bird_obj, "carot_conc_ind", carot_conc_ind)
        
    
    
    
    for bird_id, bird_obj in bird.items():
        for tissue_type in bird_obj.tissues.keys():
            # plasma, gut, and feathers are excluded for now
            # I've got placeholder numbers in here for now until I can add in the right ones
            if tissue_type.lower() == "brain":
                mass_sample = 1
                mass_total = 1
                mu = 1
                sigma = 1
            if tissue_type.lower() == "eye":
                pass
            if tissue_type.lower() == "liver":
                pass
            if tissue_type.lower() == "spleen":
                pass
            if tissue_type.lower() == "lung":
                pass
            if tissue_type.lower() == "kidney":
                pass
            if tissue_type.lower() == "gonad":
                # make more if/else statements for female/male differentiation
                pass
            if tissue_type.lower() == "heart":
                pass
            if tissue_type.lower() == "muscle":
                pass
            if tissue_type.lower() == "fat":
                pass
            # This is mainly for debugging purposes
            else:
                print()
                print("There is at least one tissue that is not built into the code.")
                print("Or there is a problem with the tissue type data.")
            
            
            # I'm letting nutri_a be an empty dictionary since I'm not using areas
            tissue_obj = c.TISSUE(n = tissue_type, ms = mass_sample, mt = mass_total, b = bird_id)
            # all nutrients will be generated by simNutrients using mu and sigma set above
            carot_conc = simNutrients(mu, sigma)
            # add carot_conc to tissue objs
            setattr(tissue_obj, "carot_conc", carot_conc)


def simNutrients(nt, tt, parainput):
    """
    Similar to getNutrients but with simulated data
    :returns nutri_list: list of dictionaries with one for each tissue in each 
    individual (bird). each dictionary has a key corresponding to the nutrient 
    name (e.g. lutein) and a value corresponding to the area of that nutrient 
    from the raw data file (i.e. HPLC output).
    
    This requires that the list be in order of bird/tissue id so at this point
    the data already "know" what birds/tissues they belong to; need to already
    know bird and tissue id to generate nutri_list
    
    series of nested if/else statements with whether groups are different 
    or not in one way v. another. use number of groups and nbirds to generate 
    ids with letters (ABC) followed by numbers (123) so that it is treated as 
    str not int. use tidiff and whichti to get number of nutrient entries in 
    nutri_list and also which sets of nutrients to use "standard" mean and 
    variation vs modified mean and variation. do i actually need to generate 
    ids here or just use numbers to figure out nutri_list?
    
    parainput variables are all str right now; may have to add code to convert 
    to Bool vs. other types of info
    
    check first to what the distributions of real data are. then if normal, 
    use random.gauss(mu, sigma). this function only makes one value, so it 
    would have to be repeated as many times as there are nutrients/tissues/
    birds
    
    iterate through every tissue then maybe write a function that checks the 
    tissue and hardcode mean and variation for each of these tissues but 
    have it do different things to tissues that are supposed to be different 
    depending on if the difference is total amount, profile, or both.
    """
    # total number of birds; do I need to do minus 1 for zero?
    totalbird = int(parainput["ngroup"])*int(parainput["nbird"]) # not tested yet
    # for every bird...
    for b in totalbird:
        pass
    
    
    # if user wants to keep total carotenoids constant but have groups with
    # different carotenoid profiles (props of carotenoid types), then...
    if parainput["constanttc"] == True and parainput["constantcp"] == False:
        pass
    # if user wants to have groups with different levels of total carotenoids 
    # and different carotenoid profiles (props of carotenoid types), then...
    if parainput["constanttc"] == False and parainput["constantcp"] == False:
        pass
    # if user wants groups to have the same total carotenoids and carotenoid 
    # profiles between groups (e.g. if testing for false positives), then...
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
        















