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

def initialize(context):
    """ Import Types here to register them """
    import BibliographyList
    import PresentationFolder
    import ReferencePresentation
    import ReferencePresentationSet

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