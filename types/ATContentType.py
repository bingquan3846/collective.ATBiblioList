#  ATContentTypes http://sf.net/projects/collective/
#  Archetypes reimplementation of the CMF core types
#  Copyright (c) 2003-2004 AT Content Types development team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""

$Id: ATContentType.py,v 1.43 2004/10/08 16:23:16 tiran Exp $
"""
__author__  = ''
__docformat__ = 'restructuredtext'

from Products.ATContentTypes.config import *
from Products.ATContentTypes.ConstrainTypesMixin import ConstrainTypesMixin

from copy import copy

if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import BaseContent
    from Products.LinguaPlone.public import BaseFolder
    from Products.LinguaPlone.public import OrderedBaseFolder
    from Products.LinguaPlone.public import BaseBTreeFolder
else:
    from Products.Archetypes.public import BaseContent
    from Products.Archetypes.public import BaseFolder
    from Products.Archetypes.public import OrderedBaseFolder
    from Products.Archetypes.public import BaseBTreeFolder

from Products.Archetypes.TemplateMixin import TemplateMixin
from Products.Archetypes.debug import _default_logger
from Products.Archetypes.debug import _zlogger

from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

if HAS_PLONE2:
    from Products.CMFPlone.PloneFolder import ReplaceableWrapper

from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute
from Globals import InitializeClass
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from ExtensionClass import Base

from Products.ATContentTypes.interfaces.IATContentType import IATContentType
from Products.ATContentTypes.types.schemata import ATContentTypeSchema

DEBUG = 1

def updateActions(klass, actions):
    """Merge the actions from a class with a list of actions
    """
    kactions = copy(klass.actions)
    aids  = [action.get('id') for action in actions ]
    actions = list(actions)

    for kaction in kactions:
        kaid = kaction.get('id')
        if kaid not in aids:
            actions.append(kaction)

    return tuple(actions)

def cleanupFilename(filename):
    """Removes bad chars from file names to make them a good id
    """
    result = ''
    for s in str(filename):
        s = CHAR_MAPPING.get(s, s)
        if s in GOOD_CHARS:
            result+=s
    return result

def translateMimetypeAlias(alias):
    """Maps old CMF content types to real mime types
    """
    if alias.find('/') != -1:
        mime = alias
    else:
        mime = MIME_ALIAS.get(alias, None)
    assert(mime) # shouldn't be empty
    return mime


class ATCTMixin(TemplateMixin):
    """Mixin class for AT Content Types"""
    schema         =  ATContentTypeSchema

    #content_icon   = 'document_icon.gif'
    meta_type      = 'ATContentType'
    archetype_name = 'AT Content Type'
    immediate_view = 'base_view'
    suppl_views    = ()
    newTypeFor     = ()
    typeDescription= ''
    typeDescMsgId  = ''
    assocMimetypes = ()
    assocFileExt   = ()
    cmf_edit_kws   = ()

    __implements__ = IATContentType

    security       = ClassSecurityInfo()

    actions = ({
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${object_url}/view',
        'permissions' : (CMFCorePermissions.View,)
         },
        {
        'id'          : 'edit',
        'name'        : 'Edit',
        'action'      : 'string:${object_url}/atct_edit',
        'permissions' : (CMFCorePermissions.ModifyPortalContent,),
         },
        )

    security.declareProtected(CMFCorePermissions.ModifyPortalContent,
                              'initializeArchetype')
    def initializeArchetype(self, **kwargs):
        """called by the generated addXXX factory in types tool

        Overwritten to call edit() instead of update() to have the cmf
        compatibility method.
        """
        try:
            self.initializeLayers()
            self.setDefaults()
            if kwargs:
                self.edit(**kwargs)
            self._signature = self.Schema().signature()
        except Exception, msg:
            _zlogger.log_exc()
            if DEBUG and str(msg) not in ('SESSION',):
                # XXX debug code
                raise
                #_default_logger.log_exc()

    def _getPortalTypeName(self):
        """
        """
        ptTool = getToolByName(self, 'portal_types', None)

        portal_type = self.portal_type
        if callable(portal_type):
                portal_type = portal_type()

        if ptTool is None:
            # this may when we don't have an acquisition context
            return portal_type

        # make it easy to derive from atct:
        if hasattr(self,'newTypeFor') and self.newTypeFor:
            correct_pt = self.newTypeFor[0]
        else:
            correct_pt = portal_type

        fti = ptTool.getTypeInfo(correct_pt)
        if fti is None:
            # FTI is None which may happen in ATCT2CMF switching
            # script in this case the self.portal_type aka
            # self.__class__.__name__ is right but test to be sure
            assert(portal_type, self.__class__.__name__)
            return portal_type
        if fti.Metatype() == self.meta_type:
            return correct_pt
        else:
            return portal_type

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'edit')
    def edit(self, *args, **kwargs):
        """Reimplementing edit() to have a compatibility method for the old
        cmf edit() method
        """
        if len(args) != 0:
            # use cmf edit method
            return self.cmf_edit(*args, **kwargs)
        
        # if kwargs is containing a key that is also in the list of cmf edit
        # keywords then we have to use the cmf_edit comp. method
        cmf_edit_kws = getattr(aq_inner(self).aq_explicit, 'cmf_edit_kws', ())
        for kwname in kwargs.keys():
            if kwname in cmf_edit_kws:
                return self.cmf_edit(**kwargs)
        # standard AT edit - redirect to update()
        return self.update(**kwargs)

    security.declarePrivate('cmf_edit')
    def cmf_edit(self, *args, **kwargs):
        """Overwrite this method to make AT compatible with the crappy CMF edit()
        """
        raise NotImplementedError("cmf_edit method isn't implemented")

InitializeClass(ATCTMixin)

class ATCTContent(ATCTMixin, BaseContent):
    """Base class for non folderish AT Content Types"""

    __implements__ = (BaseContent.__implements__,
                      IATContentType)

    security       = ClassSecurityInfo()
    actions = updateActions(ATCTMixin,
        ({
          'id'          : 'external_edit',
          'name'        : 'External Edit',
          'action'      : 'string:${object_url}/external_edit',
          'permissions' : (CMFCorePermissions.ModifyPortalContent,),
          'visible'     : 0,
         },
        {
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        )
    )

InitializeClass(ATCTContent)

class ATCTFileContent(ATCTContent):
    """Base class for content types containing a file like ATFile or ATImage

    The file field *must* be the exclusive primary field
    """

    security       = ClassSecurityInfo()
    actions = updateActions(ATCTContent,
        ({
        'id'          : 'download',
        'name'        : 'Download',
        'action'      : 'string:${object_url}/download',
        'permissions' : (CMFCorePermissions.View,),
        'condition'   : 'member', # don't show border for anon user
         },
        )
    )

    security.declareProtected(CMFCorePermissions.View, 'download')
    def download(self, REQUEST=None, RESPONSE=None):
        """Download the file (use default index_html)
        """
        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE
        field = self.getPrimaryField()
        return field.download(self, REQUEST, RESPONSE)

    security.declareProtected(CMFCorePermissions.View, 'index_html')
    def index_html(self, REQUEST=None, RESPONSE=None):
        """Make it directly viewable when entering the objects URL
        """
        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE
        field = self.getPrimaryField()
        data  = field.getAccessor(self)(REQUEST=REQUEST, RESPONSE=RESPONSE)
        if data:
            return data.index_html(REQUEST, RESPONSE)
        # XXX would should be returned if no data is present?

    security.declareProtected(CMFCorePermissions.View, 'get_data')
    def get_data(self):
        """CMF compatibility method
        """
        data = aq_base(self.getPrimaryField().getAccessor(self)())
        return str(getattr(data, 'data', data))

    data = ComputedAttribute(get_data, 1)

    security.declareProtected(CMFCorePermissions.View, 'get_size')
    def get_size(self):
        """CMF compatibility method
        """
        f = self.getPrimaryField().getAccessor(self)()
        return f and f.get_size() or 0

    security.declareProtected(CMFCorePermissions.View, 'size')
    def size(self):
        """Get size (image_view.pt)
        """
        return self.get_size()

    security.declareProtected(CMFCorePermissions.View, 'get_content_type')
    def get_content_type(self):
        """CMF compatibility method
        """
        f = self.getPrimaryField().getAccessor(self)()
        return f and f.getContentType() or 'text/plain' #'application/octet-stream'

    content_type = ComputedAttribute(get_content_type, 1)

    def _setATCTFileContent(self, value, **kwargs):
        """Set id to uploaded id
        """
        field = self.getPrimaryField()
        # set first then get the filename
        field.set(self, value, **kwargs) # set is ok
        if self._isIDAutoGenerated(self.getId()):
            filename = field.getFilename(self)
            clean_filename = cleanupFilename(filename)
            if self.REQUEST.form.get('id'):
                # request contains an id - don't rename the obj
                # according to it's file name
                return
            elif clean_filename == self.getId():
                # destination id and old id are equal
                return
            elif clean_filename:
                # got a clean file name - rename it
                aq_parent(self).manage_renameObject(self.getId(), clean_filename)

    def _isIDAutoGenerated(self, id):
        """Avoid busting setDefaults if we don't have a proper acquisition context
        """
        skinstool = getToolByName(self, 'portal_skins')
        script = getattr(skinstool.aq_explicit, 'isIDAutoGenerated', None)
        if script:
            return script(id)
        else:
            return False

    security.declareProtected(CMFCorePermissions.View, 'post_validate')
    def post_validate(self, REQUEST=None, errors=None):
        """Validates upload file and id
        """
        id     = REQUEST.form.get('id')
        parent = aq_parent(self)
        parent_ids = parent.objectIds()
        field  = self.getPrimaryField()
        f_name = field.getName()
        upload = REQUEST.form.get('%s_file' % f_name, None)
        filename = getattr(upload, 'filename', None)
        clean_filename = cleanupFilename(filename)

        if upload:
            # the file may have already been read by a
            # former method
            upload.seek(0)

        if not id and clean_filename == self.getId():
            # already renamed - ok
            return
        elif id == self.getId():
            # id available and already renamed
            return
        elif id and id not in parent_ids:
            # id available and id not used
            return
        elif clean_filename in parent_ids or id in parent_ids:
            # failure
            used_id = id and id or clean_filename
            errors[f_name] = 'You have to upload the file again'
            errors['id'] = 'Id %s is already in use' % used_id
            REQUEST.form['id'] = used_id
        else:
            # everything ok
            pass

InitializeClass(ATCTFileContent)


class ATCTFolder(ATCTMixin, BaseFolder):
    """Base class for folderish AT Content Types (but not for folders)
    
    DO NOT USE this base class for folders but only for folderish objects like
    AT Topic. It doesn't support constrain types!
    """

    __implements__ = (ATCTMixin.__implements__,
                      BaseFolder.__implements__)

    security       = ClassSecurityInfo()

    actions = updateActions(ATCTMixin,
        ({
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        {
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${folder_url}/',
        'permissions' : (CMFCorePermissions.View,),
         },
        )
    )

InitializeClass(ATCTFolder)


class ATCTConstrainedFolderMixin(ConstrainTypesMixin, ATCTMixin):
    """ Constrained folderish type """

    __implements__ = (ATCTMixin.__implements__,
                      ConstrainTypesMixin.__implements__)

    security       = ClassSecurityInfo()

if ENABLE_CONSTRAIN_TYPES_MIXIN:
    ATCTFolderMixin = ATCTConstrainedFolderMixin
else:
    ATCTFolderMixin = ATCTMixin

InitializeClass(ATCTFolderMixin)


class ATCTOrderedFolder(ATCTFolderMixin, OrderedBaseFolder):
    """Base class for orderable folderish AT Content Types"""

    __implements__ = (ATCTFolderMixin.__implements__,
                      OrderedBaseFolder.__implements__)

    security       = ClassSecurityInfo()

    actions = updateActions(ATCTMixin,
        ({
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        {
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${folder_url}/',
        'permissions' : (CMFCorePermissions.View,),
         },
        )
    )

    security.declareProtected(CMFCorePermissions.View, 'index_html')
    def index_html(self):
        """ Acquire if not present. """
        if HAS_PLONE2:
            _target = aq_parent(aq_inner(self)).aq_acquire('index_html')
            return ReplaceableWrapper(aq_base(_target).__of__(self))
        else:
            OrderedBaseFolder.index_html(self)

    index_html = ComputedAttribute(index_html, 1)

    def __browser_default__(self, request):
        """ Set default so we can return whatever we want instead
        of index_html """
        if HAS_PLONE2:
            return getToolByName(self, 'plone_utils').browserDefault(self)
        else:
            return OrderedBaseFolder.__browser_default__(self, request)

InitializeClass(ATCTOrderedFolder)


class ATCTBTreeFolder(ATCTFolderMixin, BaseBTreeFolder):
    """Base class for folderish AT Content Types using a BTree"""

    __implements__ = ATCTFolderMixin.__implements__, \
                     BaseBTreeFolder.__implements__

    security       = ClassSecurityInfo()

    actions = updateActions(ATCTMixin,
        ({
        'id'          : 'local_roles',
        'name'        : 'Sharing',
        'action'      : 'string:${object_url}/folder_localrole_form',
        'permissions' : (CMFCorePermissions.ManageProperties,),
         },
        {
        'id'          : 'view',
        'name'        : 'View',
        'action'      : 'string:${folder_url}/',
        'permissions' : (CMFCorePermissions.View,),
         },
        )
    )

    security.declareProtected(CMFCorePermissions.View, 'index_html')
    def index_html(self):
        """
        BTree folders don't store objects as attributes, the
        implementation of index_html method in PloneFolder assumes
        this and by virtue of being invoked looked in the parent
        container. We override here to check the BTree data structs,
        and then perform the same lookup as BasePloneFolder if we
        don't find it.
        """
        _target = self.get('index_html')
        if _target is not None:
            return _target
        _target = aq_parent(aq_inner(self)).aq_acquire('index_html')
        if HAS_PLONE2:
            return ReplaceableWrapper(aq_base(_target).__of__(self))
        else:
            return aq_base(_target).__of__(self)

    index_html = ComputedAttribute(index_html, 1)

InitializeClass(ATCTBTreeFolder)


__all__ = ('ATCTContent', 'ATCTFolder', 'ATCTOrderedFolder',
           'ATCTBTreeFolder', 'updateActions' )
