#
# ATBiblioList tests
#

from Products.ATBiblioList.tests import BibliolistTestCase

import constants

class TestSetup(BibliolistTestCase.BibliolistTestCase):

    def testSkins(self):
        portal_skins = self.portal.portal_skins.objectIds()
        for skin in constants.FSDIRECTORYVIEWS:
            self.failUnless(skin in portal_skins)

    def testSkinLayers(self):
        skin_paths = self.portal.portal_skins.getSkinPaths()
        for layer in constants.FSDIRECTORYVIEWS:
            for skin_path in [s[1] for s in skin_paths]:
                self.failUnless(layer in skin_path)

    def testPortalTypes(self):
        portal_types = self.portal.portal_types.objectIds()
        for content_type in constants.CONTENTTYPES:
            self.failUnless(content_type in portal_types)

    def testPortalFactorySetup(self):
        factoryTypes = self.portal.portal_factory.getFactoryTypes().keys()
        for t in constants.CONTENTTYPES:
            self.failUnless(t in factoryTypes)

    def testFolderishTypes(self):
        site_properties = self.portal.portal_properties.site_properties
        for folderish_type in constants.FOLDERISHTYPES:
            self.failUnless(folderish_type in site_properties.use_folder_tabs)
            self.failUnless(folderish_type in site_properties.typesLinkToFolderContentsInFC)

    def testFormControllerTransitions(self):
        fct = self.portal.portal_form_controller
        for button in constants.FORMCONTROLLERBUTTONS:
            self.failUnless(len(fct.listFormActions(button=button))==1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
