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

$Id: config.py,v 1.2 2004/03/08 15:15:49 tiran Exp $
""" 
__author__  = ''
__docformat__ = 'restructuredtext'

from Permissions import ADD_CONTENT_PERMISSION, ADD_TOPIC_PERMISSION

PROJECTNAME = "ATContentTypes"
SKINS_DIR = 'skins'

GLOBALS = globals()

# Load the validation package from Products.validation (1) or from the
# python site-packages (0)
# Archetypes 1.2.x requires: 0
# Archetypes 1.3.x requires: 1 
VALIDATION_IN_PRODUCTS = 0

ICONMAP = {'application/pdf' : 'pdf_icon.gif',
           'image'           : 'image_icon.gif'}
