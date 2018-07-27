"""
Functions necessary to read and store data for the Avian Nutrient Distributions Project
"""

import ANDclasses as c
import csv

def getInput():
    """
    Get input on file name from user with option to input names of files to be 
    used for making calculation exceptions
    
    :returns: tuple of three items. item 0 (infile_name) is a str of the the 
    main input file. the input file must include a .csv designation. item 1 
    (alt_calc) is a Boolean value that, if True, means that 
    ANDfunctions_ModifyData.py functions will use an alternative calculation. 
    if False, it means that ANDfunctions_ModifyData.py will use default 
    calculations. item 2 (list_except) is a list that contains user-entered 
    names of .txt files containing data that require alternative calculations. 
    if no exceptions are needed, then alt_calc will be False and list_except 
    will be given "None" as the contents.
    
    Note to self: include try-except loop for correct file types used (.csv)
    """
    infile_name = input("Enter name of input file: ")
    print()
    response1 = input("Do you have calculation exceptions? ")
    if response1.lower() == "no":
        alt_calc = False
        list_except = None
    else:
        alt_calc = True
        print()
        print("Enter names of exception .txt files (one per line).")
        print("When you\'re done, just press enter without typing anything.")
        still_entering = True
        list_except = list()
        while still_entering == True:
            response2 = input("Enter name of exception file: ")
            if response2 != "":
                list_except.append(response2)
            else:
                still_entering = False
    return infile_name, alt_calc, list_except


def readData(infile_name):
    """
    Get columns of data from infile (using infile_name)
    
    :parameter infile_name: name of .csv file containing columns of data
    :returns: tuple of two dictionries (columns, indexToName). columns dictionary
    has keys that are headings in the infile_name, and values are a list of all
    the entries in that column. indexToName dictionary maps column index to names
    that are used as keys in the columns dictionary. The names are the same as the
    headings used in the infile_name.
    """  
    with open(infile_name, "r") as csvfile:
        data = list(csv.reader(csvfile))
        columns = {}
        indexToName = {}
        for rownum, row in enumerate(data):
            if rownum == 0:
                i = 0
                for heading in row:
                    heading = heading.strip()
                    columns[heading] = []
                    indexToName[i] = heading
                    i += 1
            else:
                i = 0
                for cell in row:
                    cell = cell.strip()
                    columns[indexToName[i]].append(cell)
                    i += 1
        return columns, indexToName         


def readExceptions(list_except):
    """
    Reads exception files, if there are any
    
    :parameter list_except: a list that contains user-entered names of .txt 
    files containing data that require alternative calculations.
    :returns: a dictionary of dictionaries where the outer dictionary has 
    key = name of exception file and value = dictionary of contents. the inner 
    dictionary has key = bird id and value = all numbers after the bird id in 
    a row which can represent different things depending on the exception.
    
    Note to self: add in file path to input options
    """
    except_files = {}
    for file in list_except:
        except_file = {}
        infile = open(file, "r")
        for line in infile:
            line_split = line.rstrip("\n").split(",")
            value = []
            for i in line_split:
                if i == line_split[0]:
                    key = i
                else:
                    value.append(i)
            except_file[key] = value
        except_files[file] = except_file
    infile.close()
    return except_files


def invokeBIRD(columns, indexToName, ti_list):
    """
    Makes dictionary with key=bird_id and value=BIRD object
    """
    # makes dictionary of keyword=birdid and value=dictionary of tissues
    bird_tissue_dicts = {}
    i = 0
    # iterate through rows within the bird id column
    for b in columns[indexToName[0]]:
        # if bird id is already in the dictionary...
        if b in bird_tissue_dicts:
            # find and assign tissue type for that bird
            tissue_type = columns[indexToName[3]][i]
            # call appropriate tissue object from list of tissue objects
            tissue_obj = ti_list[i]
            # finds and assigns new tissue object to the appropriate bird id
            bird_tissue_dicts[b][tissue_type] = tissue_obj
            i += 1
        # if bird id is not in the dictionary yet...
        else:
            # make new tissues dictionary
            tissues = {}
            # find and assign tissue type for that bird
            tissue_type = columns[indexToName[3]][i]
            # call appropriate tissue object from list of tissue objects
            tissue_obj = ti_list[i]
            # adds key=tissue name and value=tissue object to tissues dictionary
            tissues[tissue_type] = tissue_obj
            # adds key=bird id and value=dictionary of tissue objects to bird_tissue_dicts dictionary
            bird_tissue_dicts[b] = tissues
            i += 1
    # makes bird dictionary
    bird = {}
    i = 0
    # iterate through rows within bird id column
    for b in columns[indexToName[0]]:
        # if bird id is already in the bird dictionary, don't do anything
        if b in bird:
            i += 1
        # if bird id isn't in the bird dictionary...
        else:
            # assign contents to BIRD class property names
            sex = columns[indexToName[2]][i] 
            treatment = columns[indexToName[1]][i]
            tissues = bird_tissue_dicts[b]
            # invoke BIRD class to make bird objects
            bird[b] = c.BIRD(i=b, s=sex, tr=treatment, ti=tissues)
            i += 1
    return bird


def invokeTISSUE(columns, indexToName, nutri_list):
    """
    Make a list of TISSUE objects (ti_list) in row order (using columns, 
    indexToName, and nutri_list)
    
    :parameter columns: dictionary where the key is the heading title and the 
    value is a list of all the entries in that column
    :parameter indexToName: dictionary maps column index to names that are used 
    as keys in the columns dictionary. the names are the same as the headings 
    from infile_name.
    :parameter nutri_list: list of dictionaries with one for each tissue in each 
    individual (bird). each dictionary has a key corresponding to the nutrient 
    name (e.g. lutein) and a value corresponding to the area of that nutrient 
    from the raw data file (i.e. HPLC output).
    :returns ti_list: list of TISSUE objects in row order. each TISSUE object 
    contains the tissue type (name), mass (in grams) of the sample analyzed via 
    HPLC (mass_sample), total mass (in grams) of the tissue (mass_total), 
    dictionary with key=nutrient type (e.g. lutein) and value=area (i.e. HPLC 
    output) (nutrients), and id of the individual (bird).
    """
    # make list of tissue objects
    ti_list = []
    i = 0
    # iterate through rows in bird id column
    for b in columns[indexToName[0]]:
        # assign contents to TISSUE class property names
        bird_id = columns[indexToName[0]][i]
        tissue_type = columns[indexToName[3]][i]
        mass_sample = columns[indexToName[8]][i]
        mass_total = columns[indexToName[9]][i]
        nutri = nutri_list[i]
        # make tissue objects for each row in the bird id column
        tissue_obj = c.TISSUE(n=tissue_type, ms=mass_sample, mt=mass_total, b=bird_id, nutri=nutri)
        # add each tissue object to the list of tissue objects
        ti_list.append(tissue_obj)
        i += 1
    return ti_list
        

def getNutrients(columns, indexToName):
    """
    Make list of dictionaries (nutri_list) in row order (using columns and indexToName)
    
    :parameter columns: dictionary where the key is the heading title and the 
    value is a list of all the entries in that column
    :parameter indexToName: dictionary maps column index to names that are used 
    as keys in the columns dictionary. the names are the same as the headings 
    from infile_name.
    :returns nutri_list: list of dictionaries with one for each tissue in each 
    individual (bird). each dictionary has a key corresponding to the nutrient 
    name (e.g. lutein) and a value corresponding to the area of that nutrient 
    from the raw data file (i.e. HPLC output).
    
    Note to self: make for loop into while loop to generalize this part so it 
    doesn't have to have a fixed number of columns
    """
    # make new list of nutrient dictionaries 
    nutri_list = []
    i = 0
    # iterate through rows in bird id column
    for b in columns[indexToName[0]]:
        # make new dictionary of nutrients for each row in bird id column (each tissue for each bird)
        nutrients = {}
        # add all nutrient areas to the nutrients dictionary by name of nutrients
        nutrients[indexToName[4]] = columns[indexToName[4]][i]
        nutrients[indexToName[5]] = columns[indexToName[5]][i]
        nutrients[indexToName[6]] = columns[indexToName[6]][i]
        nutrients[indexToName[7]] = columns[indexToName[7]][i]
        # add dictionaries of nutrients (nutrient profiles in areas for each tissue in each bird) to list of nutrient dictionaries
        nutri_list.append(nutrients)
        i += 1
    return nutri_list


