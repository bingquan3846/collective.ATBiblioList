##########################################################################
#                                                                        #
#              copyright (c) 2004 Belgian Science Policy                 #
#                                 and contributors                       #
#                                                                        #
#     maintainers: David Convent, david.convent@naturalsciences.be       #
#                  Louis Wannijn, louis.wannijn@naturalsciences.be       #
#                                                                        #
##########################################################################

"""BiblioListTool class"""

# Zope stuff
from Globals import InitializeClass 
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder

# CMF stuff
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject

from Products.ATContentTypes.tool.topic import ATTopicsTool

# ATBiblioList stuff
from Products.ATBiblioList.interface import IBibrefStyle
from Products.ATBiblioList.styles.minimal import MinimalBibrefStyle
from Products.ATBiblioList.styles.chicago import ChicagoBibrefStyle
from Products.ATBiblioList.styles.harvard import HarvardBibrefStyle
from Products.ATBiblioList.styles.mla import MLABibrefStyle
from Products.ATBiblioList.styles.apa import APABibrefStyle

import Products

class BiblioListTool(UniqueObject, Folder, ATTopicsTool):
    """ Tool for managing format rendering for references 
        contained in the biblio list.
    """

    id = 'portal_bibliolist'
    meta_type = 'BiblioList Tool'

    security = ClassSecurityInfo()

    manage_options = (
        (Folder.manage_options[0],)
        + Folder.manage_options[2:]
        )

    index_html = None

    def __init__(self):
        self._setObject('Minimal', MinimalBibrefStyle('Minimal', ''))
        self._setObject('Chicago', ChicagoBibrefStyle('Chicago', ''))
        self._setObject('Harvard', HarvardBibrefStyle('Harvard', ''))
        self._setObject('MLA', MLABibrefStyle('MLA', ''))
        self._setObject('APA', APABibrefStyle('APA', ''))

    def all_meta_types(self):
        product_infos = Products.meta_types
        possibles = []
        for p in product_infos:
            try:
                if IBibrefStyle in p.get('interfaces', []):
                    possibles.append(p)
            except TypeError:
                pass
        definites = map(lambda x: x.meta_type, self.objectValues())
        return filter(lambda x,y=definites: x['name'] not in y, possibles)

    security.declarePrivate('getBibrefStyleNames')
    def getBibrefStyleNames(self):
        """ returns a list with the names of the available bibref styles
        """
        return [bibrefStyle.getFormatName()
                for bibrefStyle in self.objectValues()]

    security.declareProtected(CMFCorePermissions.View, 'formatList')
    def formatList(self, refs, style, title_link=None):
        """ renders BibliographyList referenced objects in the specified style
        """
#        at_tool = getToolByName(self, 'archetype_tool')
        objs = [ref.getTargetObject() for ref in refs];
        uflist = [self.getEntryDict(obj, title_link) for obj in objs]
        formatted_list = [self.formatDicoRef(obj, style)
                          for obj in self.sortBibrefDictList(uflist)]
        return tuple(formatted_list)

    security.declarePrivate('formatDicoRef')
    def formatDicoRef(self, refValues, style):
        """ returns a Bibliography Reference
            rendered in the specified style
            refValues must be a python dictionnary
        """
        bibrefStyle = self.getBibrefStyle(style)
        if bibrefStyle:
            return bibrefStyle.formatDictionnary(refValues)
        return 'The Selected Bibref Style could not be found.'

    security.declarePrivate('getBibrefStyle')
    def getBibrefStyle(self, style):
        """ returns the formatter for the specified style
        """
        if style[:4] == 'stl_':
            for bibrefStyle in self.objectValues():
                if style[4:].lower() == bibrefStyle.getId().lower():
                    return bibrefStyle
        else:
            at_tool = getToolByName(self, 'archetype_tool')
            try:
                bibrefStyle = at_tool.lookupObject(style)
                return bibrefStyle
            except: return None

    security.declarePrivate('findBibrefStyles')
    def findBibrefStyles(self):
        """ Builds style selection vocabulary
        """
        styles = []
        # portal_bibliolist styles
        for style in self.objectValues():
            styles.append(('stl_'+style.getId().lower(),style.getId()))
        # custom styles and sets
        catalog = getToolByName(self, 'portal_catalog')
        cstyles = catalog(portal_type=('BibrefCustomStyle','BibrefCustomStyleSet'))
        for cstyle in cstyles:
            obj = cstyle.getObject()
            if cstyle.meta_type == 'BibrefCustomStyle':
                styles.append((obj.UID(),obj.title_or_id()+' (Custom Style)'))
            if cstyle.meta_type == 'BibrefCustomStyleSet':
                styles.append((obj.UID(),obj.title_or_id()+' (Custom Style Set)'))
        return tuple(styles)

    security.declarePrivate('getEntryDict')
    def getEntryDict(self, entry, title_link):
        """ transform a BiblioRef Object into python dictionnary
        """
        ref_attributes = ('publication_year',
                          'publication_month',
                          'publication_url',
                          'abstract',
                          'note',
                          'publisher',
                          'editor',
                          'organization', 
                          'institution',
                          'school',
                          'address',
                          'booktitle',
                          'chapter',
                          'journal',
                          'volume',
                          'edition',
                          'number',
                          'pages',
                          'series',
                          'type',
                          'howpublished',
                          'preprint_server',
                          'pmid',
                          'isbn',)

        values = {}
        tmp_title = unicode(entry.Title(),'utf-8')
        if tmp_title[-1] == '.': tmp_title = tmp_title[:-1]
        values['title'] = tmp_title
        uniauthors=[]
        for author in entry.getAuthorList():
            uniauthor={}
            for field in author.keys():
                uniauthor[field] = unicode(author.get(field),'utf-8')
            uniauthors.append(uniauthor)
        values['authors'] = uniauthors
        uniauthors=[]
        uniauthor={}
        for attr in ref_attributes:
            field = entry.getField(attr)
            if field:
                value = getattr(entry, field.accessor)()
                if not value:
                    value = field.getDefault(entry)
                try:
                    for x in range(value.len()):
                        value[x] = unicode(value[x],'utf-8')
                    values[attr] = value
                except:
                    values[attr] = unicode(value,'utf-8')
        values['source'] = unicode(entry.Source(),'utf-8')
        values['meta_type'] = entry.meta_type
        if title_link:
            values['title_link'] = entry.absolute_url()
        return values

InitializeClass(BiblioListTool)
