##########################################################################
#                                                                        #
#              copyright (c) 2004 Belgian Science Policy                 #
#                                 and contributors                       #
#                                                                        #
#     maintainers: David Convent, david.convent@naturalsciences.be       #
#                  Louis Wannijn, louis.wannijn@naturalsciences.be       #
#                                                                        #
##########################################################################

""" File containing the displaylists for the different string formats 
    (these lists are used in the selection boxes in formatting files)
"""
try:
   from Products.LinguaPlone.public import DisplayList
except:
   from Products.Archetypes.public import DisplayList

from Products.CMFBibliographyAT.config import REFERENCE_TYPES

ATBIBLIST_BIBFOLDER_REF = 'ATBiblioList_associated_bibfolder'

formcontroller_transitions = (
    {'object_id'    : 'base_edit',
     'status'       : 'success',
     'context_type' : '',
     'button'       : 'reference_search',
     'action_type'  : 'traverse_to',
     'action_arg'   : 'string:base_edit'},

    {'object_id'    : 'base_edit',
     'status'       : 'success',
     'context_type' : '',
     'button'       : 'reference_add',
     'action_type'  : 'traverse_to',
     'action_arg'   : 'string:bibliography_list_edit'},

    {'object_id'    : 'base_edit',
     'status'       : 'success',
     'context_type' : '',
     'button'       : 'reference_delete',
     'action_type'  : 'traverse_to',
     'action_arg'   : 'string:bibliography_list_edit'},

    {'object_id'    : 'base_edit',
     'status'       : 'success',
     'context_type' : '',
     'button'       : 'reference_up',
     'action_type'  : 'traverse_to',
     'action_arg'   : 'string:bibliography_list_edit'},

    {'object_id'    : 'base_edit',
     'status'       : 'success',
     'context_type' : '',
     'button'       : 'reference_down',
     'action_type'  : 'traverse_to',
     'action_arg'   : 'string:bibliography_list_edit'},
    )

REFERENCE_ALLOWED_TYPES = [tn.replace(' Reference', 'Reference') for tn in REFERENCE_TYPES]

LISTING_VALUES = DisplayList((
    ('bulleted', 'Bulleted list'),
    ('ordered', 'Ordered list'),
    ('lines', 'Simple lines list'),
    ('table', 'Table listing'),
))

