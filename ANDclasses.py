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
    def __init__(self, i="", s="", tr="", ti={}, tbc="", bm="", tip={}, tir={}, rp={}):
        self.__idbird = i
        self.__sex = s
        self.__treatment = tr
        self.__tissues = ti
        self.__totalbodycarot = tbc
        self.__bodymass = bm
        self.__tissue_p = tip
        self.__tissue_r = tir
        self.__relative_p = rp
    

    @property
    def idbird(self):
        """
        idbird (i) is a string that represents the identification code
        (e.g. 41W) of an individul in the experiment
        """
        return self._idbird
    
    
    @idbird.setter
    def idbird(self, value):
        self.__idbird = value


    @property
    def sex(self):
        """
        sex (s) is a string that represents the biological sex of the individual
        """
        return self.__sex
    
    
    @sex.setter
    def sex(self, value):
        self.__sex = value

    
    @property
    def treatment(self):
        """
        treatment (tr) is a string that represents the experimental group that 
        the individual belonged to during the experiment
        """
        return self.__treatment
    
    
    @treatment.setter
    def treatment(self, value):
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
    def tissues(self, value):
        self.__tissues = value


    @property
    def totalbodycarot(self):
        """
        totalbodycarot (tbc) is a floating point number that represents the total
        amount of carotenoids in all tissues analyzed in an individual bird in 
        micrograms. used to calculate proportion of carotenoids in a given tissue 
        relative to the whole individual.
        """
        return self.__totalbodycarot
    
    
    @totalbodycarot.setter
    def totalbodycarot(self, value):
        self.__totalbodycarot = value
    

    @property
    def bodymass(self):
        """
        bodymass (bm) is a floating point number that represents the mass in 
        grams (g) of an individual bird. used to calculate relative proportions.
        """
        return self._bodymass
    
    
    @bodymass.setter
    def bodymass(self, value):
        self.__bodymass = value


    @property
    def tissue_p(self):
        """
        tissue_p (tip) is a dictionary 
        """
        return self.__tissue_p
    
    
    @tissue_p.setter
    def tissue_p(self, value):
        self.__tissue_p = value


    @property
    def tissue_r(self):
        """
        tissue_r (tir) is a dictionary
        """
        return self.__tissue_r
    
    
    @tissue_r.setter
    def tissue_r(self, value):
        self.__tissue_r = value


    @property
    def relative_p(self):
        """
        relative_p (rp) is a dictionary
        """
        return self.__relative_p
    
    
    @relative_p.setter
    def relative_p(self, value):
        self.__relative_p = value


    def __str__(self):
        """
        allows user to print the contents of a BIRD-generated object
        """
        return "Bird ID = {}, Sex = {}, Treatment = {}, Tissues = {}, Total Body Carotenoids = {}, Body Mass = {}, Tissue Proportions = {}, Tissue Ratios = {}, Relative Proportions = {}"\
                .format(self.__idbird, self.__sex, self.__treatment, self.__tissues, self.__totalbodycarot, self.__bodymass, self.__tissue_p, self.__tissue_r, self.__relative_p)



class TISSUE:
    """
    A class which represents a tissue (e.g. liver, spleen)
    
    This class will be used to create a dictionary of objects with properties
    associated with tissues (e.g. name/type, mass of the sample analyzed, total
    mass of the tissue, nutrients, and the bird the tissue came from)
    """
    def __init__(self, n="", ms=None, mt=None, nutri_a={}, nutri_ug={}, b=None, cc=None, tc=None):
        self.__name = n
        self.__mass_sample = ms
        self.__mass_total = mt
        self.__nutrients_area = nutri_a
        self.__nutrients_ug = nutri_ug
        self.__bird = b
        self.__carot_conc = cc
        self.__total_carot = tc


    @property
    def name(self):
        """
        name (n) is a string that represents the type of tissue (e.g. liver)
        """
        return self.__name
    
    
    @name.setter
    def name(self, value):
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
    def mass_sample(self, value):
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
    def mass_total(self, value):
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
    def nutrients_area(self, value):
        self.__nutrients_area = value


    @property
    def nutrients_ug(self):
        """
        nutrients_ug (nutri_ug) represents a dictionary of nutrients where the 
        keyword is the name of the nutrient type (e.g. lutein) and the value is 
        the amount of nutrient associated with that nutrient type in micrograms (ug).
        """
        return self.__nutrients_ug
    
    
    @nutrients_ug.setter
    def nutrients_ug(self, value):
        self.__nutrients_ug = value


    @property
    def bird(self):
        """
        bird (b) is a string that represents the bird id associated with the 
        tissue object. used to keep track of which tissue objects belong to 
        which individual birds.
        """
        return self.__bird
    
    
    @bird.setter
    def bird(self, value):
        self.__bird = value


    @property
    def carot_conc(self):
        """
        carot_conc (cc) is a float number that represents the total carotenoid 
        concentration (ug/g) in a given tissue.
        """
        return self.__carot_conc
    
    
    @carot_conc.setter
    def carot_conc(self, value):
        self.__carot_conc = value


    @property
    def total_carot(self):
        """
        total_carot (tc) is a float number that represents the total amount (ug) 
        of carotenoids in a given tissue.
        """
        return self.__total_carot
    
    
    @total_carot.setter
    def total_carot(self, value):
        self.__total_carot = value

    
    def __str__(self):
        return "Name = {}, Sample Mass = {}, Total Mass = {}, Bird = {}, Nutrients = {}"\
                .format(self.__name, self.__mass_sample, self.__mass_total, self.__bird, self.__nutrients)
                

