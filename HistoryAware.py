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
"""History awareness

$Id: HistoryAware.py,v 1.4 2004/06/20 15:13:17 tiran Exp $
""" 
__author__  = 'Christian Heimes, Christian Theune'
__docformat__ = 'restructuredtext'

import difflib

from DateTime import DateTime
from OFS.History import historicalRevision
from DocumentTemplate.DT_Util import html_quote
from Acquisition import aq_parent
from Globals import InitializeClass

from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

from Products.ATContentTypes.config import *
from Products.ATContentTypes.interfaces.IHistoryAware import IHistoryAware

class HistoryAwareMixin:
    """History aware mixin class
    
    Shows a unified diff history of the content
    
    This mixin is using some low level functions of the ZODB to get the last
    transaction states (versions) of the current object. Older histories will
    disapear after packing the database so DO NOT rely on the history
    functionality. It's more a gimmick and nice helper to reviewers and site
    managers.
    """
    
    __implements__ = IHistoryAware

    security       = ClassSecurityInfo()

    actions = ({
        'id'          : 'history',
        'name'        : 'History',
        'action'      : 'string:${object_url}/atct_history',
        'permissions' : (HISTORY_VIEW_PERMISSION, )
         },
    )
    
    security.declarePrivate('getHistorySource')
    def getHistorySource(self):
        """get source for HistoryAwareMixin
        
        Must return a (raw) string
        """
        primary = self.getPrimaryField()
        if primary:
            return primary.getRaw(self)
        else:
            return ''

    security.declarePrivate('getHistories')
    def getHistories(self, max=10):
        """Get a list of historic revisions.
        
        Returns metadata as well    
        (object, time, transaction_note, user)
        """
    
        historyList = self._p_jar.db().history(self._p_oid, None, max)
    
        if not historyList:
            return ()
    
        # Build list of objects
        lst = []
        parent = aq_parent(self)
        for revision in historyList:
            serial = revision['serial']
            # get the revision object and wrap it in a context wrapper
            obj    = historicalRevision(self, serial)
            obj    = obj.__of__(parent)
            lst.append((obj,
                        DateTime(revision['time']),
                        revision['description'],
                        revision['user_name'],
                      ))

        return lst

    security.declareProtected(HISTORY_VIEW_PERMISSION, 'getDocumentComparisons')
    def getDocumentComparisons(self, max=10, filterComment=0):
        """Get history as unified diff
        """
        mTool = getToolByName(self, 'portal_membership')
        
        histories = self.getHistories()
        if max > len(histories):
            max = len(histories)

        lst = []

        for revisivon in range(1, max):
    
            oldObj, oldTime, oldDesc, oldUser = histories[revisivon]
            newObj, newTime, newDesc, newUser = histories[revisivon-1]

            oldText  = oldObj.getHistorySource().split("\n")
            newText  = newObj.getHistorySource().split("\n")
            # newUser is a string 'user' or 'folders to acl_users user'
            member   = mTool.getMemberById(newUser.split(' ')[-1])

            lines = [
                     html_quote(line)
                     for line in difflib.unified_diff(oldText, newText)
                    ][3:]

            description = newDesc            
            if filterComment:
                relativUrl = self.absolute_url(1)
                description = '<br />\n'.join(
                              [line
                               for line in description.split('\n')
                               if line.find(relativUrl) != -1]
                              )
            else:
                description.replace('\n', '<br />\n')
            
            if lines:
                lst.append({
                            'lines'       : lines,
                            'oldTime'     : oldTime,
                            'newTime'     : newTime,
                            'description' : description,
                            'user'        : newUser,
                            'member'      : member
                           })
        return lst

InitializeClass(HistoryAwareMixin)
