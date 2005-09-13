import sys, content, tool
sys.modules['Products.ATBiblioList.BibliographyList'] = content.bibliolist
sys.modules['Products.ATBiblioList.BibrefCustomStyle'] = content.customstyle
sys.modules['Products.ATBiblioList.BibrefCustomStyleFolder'] = content.customstylefolder
sys.modules['Products.ATBiblioList.BibrefCustomStyleSet'] = content.customstyleset
sys.modules['Products.ATBiblioList.BiblioListTool'] = tool.bibliolist
