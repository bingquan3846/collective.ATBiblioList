## Script (Python) "addtoFavorites"
##title=Add item to favourites (Plone Version)
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=

#
# Copied from CMFPlone 2.x
#

homeFolder=context.portal_membership.getHomeFolder()
if not hasattr(homeFolder, 'Favorites'):
    homeFolder.invokeFactory('ATFolder', id='Favorites')

targetFolder = homeFolder.Favorites
new_id='fav_' + str(int( context.ZopeTime()))
myPath=context.portal_url.getRelativeUrl(context)
# remove '/' if myPath starts with a '/'
if myPath.startswith('/'):
    myPath=myPath[1:]
    
targetFolder.invokeFactory( 'ATFavorite', id=new_id, title=context.TitleOrId(), remoteUrl=myPath)

msg = 'portal_status_message=\''+context.title_or_id()+'\'+has+been+added+to+your+Favorites'
return context.REQUEST.RESPONSE.redirect('%s/%s?%s' % ( context.absolute_url()
                                                      , context.getTypeInfo().getActionById('view')
                                                      , msg ))
