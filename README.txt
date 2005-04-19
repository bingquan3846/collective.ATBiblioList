Description

  This product is an add-on to Raphael Ritz's CMFBibliographyAT.
  It lets portal users organize existing bibliography references
  into lists.
  Bibliography lists can be displayed using one of the standard
  (file system based) bibliography styles shiped with the product,
  or using custom bibliography styles designed by protal users.

  It should not be too difficult for a python programmer to write its own
  file system based bibliography styles. If you do so, please share your
  interesting bibliography styles with the community.


What It Does

  * Installs the 'Bibliography List' content type.

  * Installs the 'Bibref Custom Style' content type.

  * Installs the 'Bibref Custom Style Set' content type.

  * Installs the 'Bibref Custom Style Folder' content type.

  * Installs the 'portal_bibliolist' tool.

  * Installs FS based Bibref Styles in the 'portal_bibliolist' tool:

    - Minimal: Default minimal bibliography style.

    - APA: American Psychological Association bibliography style.
    
    - MLA: Modern Language Association style.

    - Chicago and Harvard styles.


Requirements

  * Plone 2+ / Archetypes 1.2.5+
  
  * CMFBibliographyAT (svn.plone.org/svn/collective
    used to be cvs.sourceforge.net:/cvsroot/collective)

  * Epoz 0.8.x


Installation

  - First, add the product to Zope:

    * extract the product from its archive and move it to the Products directory of your Zope Instance.

  - Then, install the product in Plone:

    * Recommended (Plone way): use the 'QuickInstaller' Tool from the ZMI, or go to 'Plone Setup > Add/Remove Products' in the Plone User Interface. Check the corresponding checkbox and click the 'install' button.

    * Alternate (CMF Manual way): create an external method at the root of your cmf portal and run it by clicking its 'test' tab.

    External Method parameters:

    - Id: InstallATBiblioList

    - Title: Install ATBiblioList (optional)

    - Module Name: InstallATBiblioList.Install

    - Function Name: install

Upgrade

  - If you upgrade from version 0.2, you may have to reinstall the product with the portal_quickinstaller.


Documentation

  More documentation can be found in the 'doc' folder of this product.


Licence

  see LICENCE.txt


Contact

  David Convent - david.convent(at)naturalsciences(dot)be

  Louis Wannijn - louis.wannijn(at)naturalsciences(dot)be


Changes

  Version 0.3

  * Sort lists by 1st Author name and publication year.

  * Complete translation (i18n) support.

  * Added security declarations where needed.

  * Better Documentation.

  Version 0.4

  * Adapted ATReferenceBrowserWidget for choosing Biblio References to add to the list. References can now be found using an extended search form.

  * Adapted translation files (i18n) and the manual accordingly.

  * Moved the BiblioList sorting process (at display time) to the skins, so that it can be customized either on the File System or Through the web from the ZMI. see skins/bibliography_list/sortBibrefDictList.py .

To Do

  * Write unit tests !!

  * Export formatted lists in rtf.

  * More BibrefStyles to come: We'll have to write more specific styles in order to meet the needs of our scientific staff.


Very possible future:

  * As suggested by a few testers/users, a 'very nice to have' functionnality of a bibliolist is to let the list be dynamically updated, based on previous search criteria.
    I think the best way to implement such a functionnality would be to make the BiblioList behave like cmf topics do.

