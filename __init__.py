##########################################################################
#                                                                        #
#              copyright (c) 2004 Belgian Science Policy                 #
#                                 and contributors                       #
#                                                                        #
#     maintainers: David Convent, david.convent@naturalsciences.be       #
#                  Louis Wannijn, louis.wannijn@naturalsciences.be       #
#                                                                        #
##########################################################################

""" package installer for ATBiblioList """

from Products.CMFCore.permissions import AddPortalContent
try:
    from Products.LinguaPlone.public import process_types, listTypes
except:
	from Products.Archetypes.public import process_types, listTypes

from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

PROJECTNAME = 'ATBiblioList'
GLOBALS = globals()
#skin_names = ('bibliography_list',)

ADD_CONTENT_PERMISSION = AddPortalContent

registerDirectory('skins', GLOBALS)

import content

def initialize(context):

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

import modulealiases
