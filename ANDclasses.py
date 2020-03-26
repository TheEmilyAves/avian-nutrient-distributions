"""
Data Classes for the Avian Nutrient Distributions Project
"""


class BIRD:
    """
    A class which represents an individual subject (in this case birds)
    
    This class will be used to create a dictionary of objects with properties
    associated with individual birds in an experiment (e.g. id, sex, treatment,
    tissues, etc.).
    """
    def __init__(self, i="", s="", tr="", ti={}, bm=""):
        self.__idbird = i
        self.__sex = s
        self.__treatment = tr
        self.__tissues = ti
        self.__bodymass = bm

    
    @property
    def idbird(self):
        """
        idbird (i) is a string that represents the identification code
        (e.g. 41W) of an individul in the experiment
        """
        return self._idbird
    
    
    @idbird.setter
    def set_idbird(self, value):
        self.__idbird = value


    @property
    def sex(self):
        """
        sex (s) is a string that represents the biological sex of the individual
        """
        return self.__sex
    
    
    @sex.setter
    def set_sex(self, value):
        self.__sex = value

    
    @property
    def treatment(self):
        """
        treatment (tr) is a string that represents the experimental group that 
        the individual belonged to during the experiment
        """
        return self.__treatment
    
    
    @treatment.setter
    def set_treatment(self, value):
        self.__treatment = value
    
    
    @property
    def tissues(self):
        """
        tissues (ti) represents a dictionary of tissues where the keyword is
        the name of the tissue type (e.g. liver) and the value is an object
        created with class TISSUE
        """
        return self.__tissues
    
    
    @tissues.setter
    def set_tissues(self, value):
        self.__tissues = value
    

    @property
    def bodymass(self):
        """
        bodymass (bm) is a floating point number that represents the mass in 
        grams (g) of an individual bird. used to calculate relative proportions.
        """
        return self.__bodymass
    
    
    @bodymass.setter
    def set_bodymass(self, value):
        self.__bodymass = value


    def __str__(self):
        """
        allows user to print the contents of a BIRD-generated object
        """
        return "Bird ID = {}, Sex = {}, Treatment = {}, Tissues = {}, Body Mass = {}"\
                .format(self.__idbird, self.__sex, self.__treatment, self.__tissues, self.__bodymass)



class TISSUE:
    """
    A class which represents a tissue (e.g. liver, spleen)
    
    This class will be used to create a dictionary of objects with properties
    associated with tissues (e.g. name/type, mass of the sample analyzed, total
    mass of the tissue, nutrients, and the bird the tissue came from)
    """
    def __init__(self, n="", ms=None, mt=None, nutri_a={}, b=None):
        self.__name = n
        self.__mass_sample = ms
        self.__mass_total = mt
        self.__nutrients_area = nutri_a
        self.__bird = b


    @property
    def name(self):
        """
        name (n) is a string that represents the type of tissue (e.g. liver)
        """
        return self.__name
    
    
    @name.setter
    def set_name(self, value):
        self.__name = value


    @property
    def mass_sample(self):
        """
        mass_sample (ms) is a floating point number that represents the mass
        of the sample from which nutrients were extracted in grams. used to 
        determine the nutrient concentration in a given sample.
        """
        return self.__mass_sample
    
    
    @mass_sample.setter
    def set_mass_sample(self, value):
        self.__mass_sample = value


    @property
    def mass_total(self):
        """
        mass_total (mt) is a floating point number that represents the mass of 
        the tissue in grams which may or may not equal the mass_sample. used 
        to determine the total nutrient conent of a tissue within an individual.
        """
        return self.__mass_total
    
    
    @mass_total.setter
    def set_mass_total(self, value):
        self.__mass_total = value


    @property
    def nutrients_area(self):
        """
        nutrients_area (nutri_a) represents a dictionary of nutrients where the 
        keyword is the name of the nutrient type (e.g. lutein) and the value is 
        the area associated with that nutrient type.
        """
        return self.__nutrients_area
    
    
    @nutrients_area.setter
    def set_nutrients_area(self, value):
        self.__nutrients_area = value


    @property
    def bird(self):
        """
        bird (b) is a string that represents the bird id associated with the 
        tissue object. used to keep track of which tissue objects belong to 
        which individual birds.
        """
        return self.__bird
    
    
    @bird.setter
    def set_bird(self, value):
        self.__bird = value


    @property
    def carot_conc(self):
        """
        carot_conc (cc) is a float number that represents the total carotenoid 
        concentration (ug/g) in a given tissue.
        """
        return self.__carot_conc

    
    def __str__(self):
        return "Name = {}, Sample Mass = {}, Total Mass = {}, Bird = {}"\
                .format(self.__name, self.__mass_sample, self.__mass_total, self.__bird)
                
