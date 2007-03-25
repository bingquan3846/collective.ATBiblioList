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


Requirements

  * Plone 3.0+
  
  * CMFBibliographyAT (1.0 or svn/trunk)

  * ATBiblioStyles (1.0 or svn/trunk)


Installation

  - First, add the product to Zope:

    * extract the product from its archive and move it to the Products
      directory of your Zope Instance.

  - Then, install the product in Plone:

    * From the Plone interface, log in as manager and go to 'Site Setup' >
      'Add-on Products'.
      Check 'ATBiblioStyles' and click Install.


Upgrade

  - If you upgrade from earlier version, you may have to reinstall the product
    with the portal_quickinstaller.


Licence

  see LICENCE.txt


Contact

  David Convent - david.convent(at)naturalsciences(dot)be

  Mailing list for topics about CMFBibliographyAT, its add-on products and
  bibliography reference management with Plone in general:
  plone-biblio(at)zaubberer(dot)net.
  
  Mailing list registration at:
  https://zaubberer.net/mailman/listinfo/plone-biblio


To Do

  * Write more unit tests !!

  * Enhance UI with ATBiblioTopic features