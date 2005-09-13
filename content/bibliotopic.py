from Products.ATContentTypes.atct import ATTopic
from Products.Archetypes.atapi import registerType


class ATBiblioTopic(ATTopic):
    """A Smart Bibliography Folder"""
    meta_type = "BiblioTopic"
    portal_type = "ATBiblioTopic"
    archetype_name = "Smart Bibliography Folder"
    content_icon = 'biblist_icon.gif'

    allowed_content_types = ('BiblioTopic',)

registerType(ATBiblioTopic)