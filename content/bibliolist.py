##########################################################################
#                                                                        #
#              copyright (c) 2004 Belgian Science Policy                 #
#                                 and contributors                       #
#                                                                        #
#     maintainers: David Convent, david.convent@naturalsciences.be       #
#                  Louis Wannijn, louis.wannijn@naturalsciences.be       #
#                                                                        #
##########################################################################

""" BibliographyList: personal list of bibliographic references
"""
from AccessControl import ClassSecurityInfo

from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

from Products.Archetypes.public import DisplayList, registerType
from Products.Archetypes.public import BaseSchema, Schema
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import ReferenceField, ReferenceWidget
from Products.Archetypes.public import StringField, SelectionWidget
from Products.Archetypes.public import BooleanField, BooleanWidget
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget, registerPropertyType

# possible types of bibliographic references from module 'CMFBibliographyAT'
from Products.CMFBibliographyAT.config import REFERENCE_TYPES as search_types

from Products.ATBiblioList.config import LISTING_VALUES, REFERENCE_ALLOWED_TYPES

class BibrefListWidget(TypesWidget):
    """ custom widget for TTW references input handling """
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': "widget_bibreflist",
        })

registerWidget(BibrefListWidget)

class BibrefBrowserWidget(ReferenceWidget):
    """This Widget is based on D. Bloemendaal's ATReferenceBrowserWidget"""
    _properties = ReferenceWidget._properties.copy()
    _properties.update({
        'macro': "widget_bibrefbrowser",
        'helper_js': ('bibrefbrowser.js',),
        'helper_css': ('popupbrowser.css',),
        'root': '',
        'default_search_index': 'SearchableText',
        })

registerWidget(BibrefBrowserWidget,
               title='Bibliography Reference Browser',
               description=('Reference widget that allows to browse or search the portal for Bibliographycal References.'),
               used_for=('Products.Archetypes.Field.ReferenceField',)
               )

registerPropertyType('root', 'string', BibrefBrowserWidget)
registerPropertyType('default_search_index', 'string', BibrefBrowserWidget)

NewSchema = BaseSchema.copy()
NewSchema['title'].widget.size = 60

schema = NewSchema + Schema((
    ReferenceField('references_list',
                   multiValued=1,
                   relationship='lists reference',
                   allowed_types=REFERENCE_ALLOWED_TYPES,
                   widget=BibrefBrowserWidget(label="Bibliographical References",
                      label_msgid="label_references_list",
                      description_msgid="help_references_list",
                      description="Click the 'Browse...' button to search/select references and add them to the list. To remove references from the list, select them (use ctrl/click for multiple selection) and click the 'Remove selected items' button. Don't forget to save your changes.",
                      i18n_domain="plone",
                      ),
                   ),

    # old widget
    #ReferenceField('references_list',
    #               multiValued=1,
    #               relationship='lists reference',
    #               allowed_types=REFERENCE_ALLOWED_TYPES,
    #               widget=BibrefListWidget(label="References",
    #                  label_msgid="label_references_list",
    #                  description_msgid="help_references_list",
    #                  description="Search and select references to add to the list or organize/remove listed references.",
    #                  i18n_domain="plone",
    #                  ),
    #               ),

    StringField('ListingLayout',
                multiValued=0,
                default = "bulletted",
                vocabulary=LISTING_VALUES,
                enforce_vocabulary=1,
                widget=SelectionWidget(label="Listing Layout",
                              label_msgid="label_bibliolist_listing_layout",
                              description_msgid="help_bibliolist_listing_layout",
                              description="Listing Format.",           
                              i18n_domain="plone",
                              format="pulldown",
                              visible={'edit':'visible','view':'invisible'},),
                ),

    StringField('PresentationStyle',
                multiValued=0,
                default = 'stl_minimal',
                vocabulary="vocabCustomStyle",
                enforce_vocabulary=1,
                widget=SelectionWidget(label="Bibliographical Style",
                              label_msgid="label_bibliolist_presentation",
                              description_msgid="help_bibliolist_presentation",
                              description="Bibliographical Style used for display.",
                              i18n_domain="plone",
                              format="select",
                              visible={'edit':'visible','view':'invisible'},),
                ),

    BooleanField('linkToOriginalRef',
                 widget=BooleanWidget(label="Link to Original Reference",
                              label_msgid="label_bibliolist_linkToOriginalRef",
                              description_msgid="help_bibliolist_linkToOriginalRef",
                              description="Should the bibliographical reference title be a link to the original bibliographical reference?",
                              i18n_domain="plone",
                              visible={'edit':'visible','view':'invisible'},),
                 ),
    ))


class BibliographyList(BaseContent):
    """Bibliography list"""

    archetype_name = "Bibliography List"

    global_allow = 1
    content_icon = 'biblist_icon.gif'

    schema = schema

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}/bibliolist_view',
         'permissions' : (CMFCorePermissions.View,)
         },
        {'id'          : 'exportBib',
         'name'        : 'Export Bibliography',
         'action'      : 'string:${object_url}/listDownloadForm',
         'permissions' : (CMFCorePermissions.View, ),
         'category'    : 'document_actions',
         },
               )

    security = ClassSecurityInfo()

    security.declareProtected(CMFCorePermissions.View, 'searchMatchingReferences')
    def searchMatchingReferences(self, searchterm):
        """ list existing references but rejects those already referenced
        """
        catalog = getToolByName(self, 'portal_catalog')
        field = self.getField('references_list')
        value = getattr(self, field.edit_accessor)()
        refList = [r for r
                   in catalog(SearchableText=searchterm, portal_type=search_types)
                   if r.getObject().UID() not in value]
        return refList
    
    security.declareProtected(CMFCorePermissions.View, 'vocabCustomStyle')
    def vocabCustomStyle(self):
        """ build a DisplayList based on existing styles
        """
        bltool = getToolByName(self, 'portal_bibliolist')
        return DisplayList(bltool.findBibrefStyles())

registerType(BibliographyList)