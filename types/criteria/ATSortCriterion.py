##############################################################################
#
# ATContentTypes http://sf.net/projects/collective/
# Archetypes reimplementation of the CMF core types
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# Copyright (c) 2003-2004 AT Content Types development team
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
""" Topic: 

$Id: ATSortCriterion.py,v 1.6 2004/05/10 00:34:59 tiran Exp $
"""

__author__  = 'Christian Heimes'
__docformat__ = 'restructuredtext'

from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

from Products.ATContentTypes.config import *
from Products.ATContentTypes.types.criteria import registerCriterion, \
    ALL_INDICES, DATE_INDICES, STRING_INDICES, LIST_INDICES
from Products.ATContentTypes.Permissions import ChangeTopics
from Products.ATContentTypes.interfaces.IATTopic import IATTopicCriterion
from Products.ATContentTypes.types.criteria.ATBaseCriterion import ATBaseCriterion
from Products.ATContentTypes.types.criteria.schemata import ATSortCriterionSchema


class ATSortCriterion(ATBaseCriterion):
    """A simple string criterion"""

    security       = ClassSecurityInfo()
    schema         = ATSortCriterionSchema
    meta_type      = 'ATSortCriterion'
    archetype_name = 'AT Sort Criterion'
    typeDescription= ''
    typeDescMsgId  = ''

    def getCriteriaItems(self):
        result = [('sort_on', self.Field())]

        if self.getReversed():
            result.append(('sort_order', 'reverse'))

        return tuple(result)

registerCriterion(ATSortCriterion, ALL_INDICES)
