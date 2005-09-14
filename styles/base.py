##########################################################################
#                                                                        #
#              copyright (c) 2004 Belgian Science Policy                 #
#                                 and contributors                       #
#                                                                        #
#     maintainers: David Convent, david.convent@naturalsciences.be       #
#                  Louis Wannijn, louis.wannijn@naturalsciences.be       #
#                                                                        #
##########################################################################

"""BibrefStyle main class"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem

from Products.ATBiblioList.interface import IBibrefStyle

class BibrefStyle(SimpleItem):
    """ Base class for the input formatter of the bibliolist tool.
    """
    __implements__ = (SimpleItem.__implements__,
                      IBibrefStyle,)

    meta_type = 'Bibref Style'
    
    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        """ minimal initialization
        """
        self.id = id
        self.title = title

    def formatDictionnary(self, refValues):
        """ renders a formatted bibliography reference based on dictionnary values
        """
        pass # needs to be overwritten by individual styles


# Class instanciation
InitializeClass(BibrefStyle)