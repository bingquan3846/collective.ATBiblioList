## Script (Python) "bibrefSelectionLabel"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=bibref=None
##title=
##
authors = bibref.Authors()
title = bibref.Title()
source = bibref.Source()
pubyear = bibref.getPublication_year()
label = '%s, %s (%s). %s' % (authors, title, pubyear, source)

return test(len(label)>153, label[:160] + '...', label)
