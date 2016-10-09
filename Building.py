
from enum import Enum

class SicherheitsCategory(Enum):
    K1 = 1
    K2 = 2
    K31 = 3
    K32 = 4
    K33 = 5
    K34 = 6
    K4 = 7

def strToSicherheitsCategory(string):
    if string == "K1 Keine":
        return SicherheitsCategory.K1
    elif string == "K2 BMA":
        return SicherheitsCategory.K2
    elif string == "K3.1 Staffel":
        return SicherheitsCategory.K31
    elif string == "K3.2 Gruppe":
        return SicherheitsCategory.K32
    elif string == "K3.3 2 Staffel":
        return SicherheitsCategory.K33
    elif string == "K3.4 3 Staffel":
        return SicherheitsCategory.K34
    elif string == "K4 Sprinkler":
        return SicherheitsCategory.K4
    raise ValueError 

class BaustoffCategory(Enum):
    F0A = 1
    F30A = 2
    F30AB = 3
    F30B = 4
    F60A = 5
    F60AB = 6
    F60B = 7
    F90A = 8
    F90AB = 9
    F90B = 10

def strToBaustoffCategory(string):
    if string == "F0-A":
        return BaustoffCategory.F0A
    elif string == "F30":
        return BaustoffCategory.F30A
    elif string == "F60-A":
        return BaustoffCategory.F60A
    elif string == "F90-A":
        return BaustoffCategory.F90A
    raise ValueError 


class Building(object):

    def __init__(self, squaremeters = None, sicherheits = None, height = None, subfloors = None, topfloors  = None, baustoff = None):
        self.squaremeters = squaremeters
        self.height       = height
        self.subfloors    = subfloors
        self.topfloors    = topfloors 
        self.sicherheits  = sicherheits
        self.baustoff     = baustoff 
        print(self.baustoff)

    def setSicherheitsFromString(self, sicherheitsStr):
        self.sicherheits = strToSicherheitsCategory(sicherheitsStr)
    def setBaustoffFromString(self, baustoffStr):
        self.baustoff = strToBaustoffCategory(baustoffStr)
        
