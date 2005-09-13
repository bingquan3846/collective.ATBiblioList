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

from Products.CMFCore.CMFCorePermissions import AddPortalContent

from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

PROJECTNAME = 'ATBiblioList'
GLOBALS = globals()
skin_names = ('bibliography_list',)

ADD_CONTENT_PERMISSION = AddPortalContent

registerDirectory('skins', GLOBALS)

import content
from tool import bibliolist as tool

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

    tools = (tool.BiblioListTool,)

    utils.ToolInit(
        'BiblioList Tool', tools=tools,
        product_name='ATBiblioList', icon='bib_tool.gif',
        ).initialize(context)

    styles.initialize(context)

import modulealiases
