## Script (Python) "listDownload"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=format='BibTex', output_encoding=None
##title=
##
request = container.REQUEST
RESPONSE =  request.RESPONSE

if not format: return None

RESPONSE.setHeader('Content-Type', 'application/octet-stream')
RESPONSE.setHeader('Content-Disposition',
                   'attachment; filename=%s' %\
                   context.getId() + '.' + format)

bibtool = context.portal_bibliography
output = ''
field = context.getField('references_list')

# in our case (ATBiblioList) the renderer can copy with a list of 
# bibliographical reference items. If it encounters a portal_type
# that is not a bibref item, it will ignore this.
# BUT: the first object we pass to the renderer will be used to
# generate a title, URL etc. That's why we pass the context (the bibliolist)
# object as first object to the renderer...
output += bibtool.render([context] + [ context.archetype_tool.lookupObject(uid=uid) for uid in getattr(context, field.edit_accessor)() ], format=format, output_encoding=output_encoding )

return output
    
