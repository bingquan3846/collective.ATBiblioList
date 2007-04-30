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

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

try:
    from Products.LinguaPlone.public import DisplayList, registerType
    from Products.LinguaPlone.public import BaseSchema, Schema
    from Products.LinguaPlone.public import BaseContent
    from Products.LinguaPlone.public import ReferenceField, ReferenceWidget
    from Products.LinguaPlone.public import StringField, SelectionWidget
    from Products.LinguaPlone.public import BooleanField, BooleanWidget
    from Products.LinguaPlone.public import TextField, RichWidget, TextAreaWidget
    from Products.LinguaPlone.Widget import TypesWidget
    from Products.LinguaPlone.Registry import registerWidget, registerPropertyType 
except:
    from Products.Archetypes.public import DisplayList, registerType
    from Products.Archetypes.public import BaseSchema, Schema
    from Products.Archetypes.public import BaseContent
    from Products.Archetypes.public import ReferenceField, ReferenceWidget
    from Products.Archetypes.public import StringField, SelectionWidget
    from Products.Archetypes.public import BooleanField, BooleanWidget
    from Products.Archetypes.public import TextField, RichWidget, TextAreaWidget
    from Products.Archetypes.Widget import TypesWidget
    from Products.Archetypes.Registry import registerWidget, registerPropertyType 

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# possible types of bibliographic references from module 'CMFBibliographyAT'
from Products.CMFBibliographyAT.config import REFERENCE_TYPES as search_types, \
     FOLDER_TYPES as BIB_FOLDER_TYPES, \
     ADD_CONTENT_PERMISSION

from Products.ATBiblioList.config import LISTING_VALUES, \
     REFERENCE_ALLOWED_TYPES, ATBIBLIST_BIBFOLDER_REF

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

relatedItemsField = ReferenceField('relatedItems',
        relationship = 'relatesTo',
        multiValued = True,
        isMetadata = True,
        languageIndependent = False,
        index = 'KeywordIndex',
        write_permission = permissions.ModifyPortalContent,
        widget = ReferenceBrowserWidget(
                        allow_search = True,
                        allow_browse = True,
                        show_indexes = False,
                        force_close_on_insert = False,
                        label = "Related Item(s)",
                        label_msgid = "label_related_items",
                        description = "Reference other items on your site here.",
                        description_msgid = "help_related_items",
                        i18n_domain = "plone",
                        visible = {'edit' : 'visible', 'view' : 'invisible' },
        ),
)

#NewSchema = Schema(tuple([ field.copy() for field in BaseSchema.fields() if field.getName() != 'description' ]))
NewSchema = BaseSchema.copy()
NewSchema['title'].widget.size = 60

NewSchema['description'].schemata = 'default'
NewSchema.moveField('description', after='title')

schema = NewSchema + Schema((
    TextField('biblioListHeader',
                searchable = True,
                required=0,
                default_content_type='text/html',
                default_output_type='text/x-html-captioned',
                allowable_content_types=('text/html',),
                widget=RichWidget(
                        label='Bibliography List Header',
                        label_msgid='label_bibliolist_header',
                        description='',
                        description_msgid='"help_bibliolist_header',
                        i18n_domain = 'atbibliolist',
                        rows=8,
                ),
    ),
    ReferenceField('references_list',
                   multiValued=1,
                   relationship='lists reference',
                   allowed_types=REFERENCE_ALLOWED_TYPES,
                   languageIndependent = True,
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
                languageIndependent = True,
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
                languageIndependent = True,
                widget=SelectionWidget(label="Bibliographical Style",
                              label_msgid="label_bibliolist_presentation",
                              description_msgid="help_bibliolist_presentation",
                              description="Bibliographical Style used for display.",
                              i18n_domain="plone",
                              format="select",
                              visible={'edit':'visible','view':'invisible'},),
                ),

    BooleanField('linkToOriginalRef',
                 languageIndependent = True,
                 widget=BooleanWidget(label="Link to Original Reference",
                              label_msgid="label_bibliolist_linkToOriginalRef",
                              description_msgid="help_bibliolist_linkToOriginalRef",
                              description="Should the bibliographical reference title be a link to the original bibliographical reference?",
                              i18n_domain="plone",
                              visible={'edit':'visible','view':'invisible'},),
                 ),
    BooleanField('linkToOriginalRefOnlyIfOwner',
                default = False,
                languageIndependent = True,
                widget=BooleanWidget(label="Only Show Link to Original Reference if Owner",
                              label_msgid="label_bibliolist_linktooriginalrefonlyifowner",
                              description_msgid="help_bibliolist_linktooriginalrefonlyifowner",
                              description="If linking to original references is enabled, this switch will narrow the number of linked references down to those items the authenticated user is owner of.",
                              i18n_domain="atbibliotopic",
                              visible={'edit':'visible','view':'invisible'},
                ),
    ),          
    ReferenceField('associatedBibFolder',
                multiValued=0,
                relationship=ATBIBLIST_BIBFOLDER_REF,
                allowed_types=BIB_FOLDER_TYPES,
                languageIndependent = True,
                widget=ReferenceWidget(label="Associated ",
                      label_msgid="label_associated_bibfolder",
                      description_msgid="help_associated_bibfolder",
                      description="Associates a specific BibliographyFolder with this list for the purpose of uploads only.",
                      i18n_domain="plone",
                ),
    ),            
    TextField('biblioListFooter',
                searchable = True,
                required=0,
                default_content_type='text/html',
                default_output_type='text/x-html-captioned',
                allowable_content_types=('text/html',),
                widget=RichWidget(
                        label='Bibliography List Footer',
                        label_msgid='label_bibliolist_footer',
                        description='',
                        description_msgid='"help_bibliolist_footer',
                        i18n_domain = 'atbibliolist',
                        rows=8,
                ),
    ),
    relatedItemsField,
    ))


class BibliographyList(BaseContent):
    """Bibliography list"""

    archetype_name = "Bibliography List"

    global_allow = 1
    content_icon = 'biblist_icon.gif'
    _at_rename_after_creation = True

    schema = schema

    actions = (
        {'id'          : 'view',
         'name'        : 'View',
         'action'      : 'string:${object_url}/bibliolist_view',
         'permissions' : (permissions.View,)
         },
        {'id'          : 'exportBib',
         'name'        : 'Export Bibliography',
         'action'      : 'string:${object_url}/bibliolist_exportForm',
         'permissions' : (permissions.View, ),
         'category'    : 'document_actions',
         },
        {
        'id'           : 'import',
        'name'         : 'Import',
        'action'       : 'string:${object_url}/bibliography_importForm',
        'permissions'  : (ADD_CONTENT_PERMISSION,),
        'condition'    : 'python:object.getAssociatedBibFolder() is not None',
         },
        {'id'          : 'local_roles',
         'name'        : 'Sharing',
         'action'      : 'string:${object_url}/folder_localrole_form',
         'permissions' : (permissions.ManageProperties,),
         'condition'   : 'python: object.portal_membership.checkPermission("ManageProperties", object)',
         },
        )

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'searchMatchingReferences')
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
    
    security.declareProtected(permissions.View, 'vocabCustomStyle')
    def vocabCustomStyle(self):
        """ build a DisplayList based on existing styles
        """
        bstool = getToolByName(self, 'portal_bibliostyles') or None
        return DisplayList(bstool.findBibrefStyles())    

    security.declareProtected(ADD_CONTENT_PERMISSION, 'processSingleImport')
    def processSingleImport(self, entry, infer_references=True, **kwargs):
        """
        """
        bf = self.getAssociatedBibFolder()
        # No need to put in a security check on the 'real' context (i.e. bf)
        # here because bf.processSingleImport(...) calls self.invokeFactory(...)
        # which has security built-in.

        result =  bf.processSingleImport(entry, infer_references=infer_references, **kwargs)
        if len(result) == 2:
            # skipped references only return report_line and import_status
            report_line, import_status = result
            out = (report_line, import_status, None )
        elif len(result) == 3:
            # successfully imported references additionally return an object
            report_line, import_status, ob = result
            out = (report_line, import_status, ob )
                                
        # This is just for clarity
        out = (report_line, import_status, ob )
        # XXX Ick, this should be something better than testing the value of a string.
        # BibliographyFolder.processSingleImport should probably be refactored to raise an exception.
        if import_status == 'ok':
            refs = self.getReferences_list()
            refs.append(ob)
            self.setReferences_list(refs)
        return out

    security.declareProtected(ADD_CONTENT_PERMISSION, 'logImportReport')
    def logImportReport(self, report, **kwargs):
        """Store the import report.
        """
        # Just pass off the import report to the place that actually did the importing.
        # XXX Should have a security check here though!
        self.getAssociatedBibFolder().logImportReport(report, **kwargs)

    security.declareProtected(ADD_CONTENT_PERMISSION, 'getEnableDuplicatesManager')
    def getEnableDuplicatesManager(self, **kwargs):
        """Check if the DuplicatesManager is enabled in the assoc. bibfolder
        """
        if self.getAssociatedBibFolder():
            return self.getAssociatedBibFolder().getEnableDuplicatesManager(**kwargs)
        else:
            return False

    security.declareProtected(ADD_CONTENT_PERMISSION, 'getDuplicatesMatchingPolicy')
    def getDuplicatesMatchingPolicy(self, **kwargs):
        """Retrieve the DuplicatesMatchingPolicy from the assoc. bibfolder
        """
        if self.getAssociatedBibFolder():
            return self.getAssociatedBibFolder().getDuplicatesMatchingPolicy(**kwargs)

registerType(BibliographyList)