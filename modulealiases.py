import sys, content, tool, styles
sys.modules['Products.ATBiblioList.BibliographyList'] = content.bibliolist
sys.modules['Products.ATBiblioList.BibrefCustomStyle'] = content.customstyle
sys.modules['Products.ATBiblioList.BibrefCustomStyleFolder'] = content.customstylefolder
sys.modules['Products.ATBiblioList.BibrefCustomStyleSet'] = content.customstyleset

sys.modules['Products.ATBiblioList.BiblioListTool'] = tool.bibliolist

sys.modules['Products.ATBiblioList.styles.Minimal'] = styles.minimal
sys.modules['Products.ATBiblioList.styles.APA'] = styles.apa
sys.modules['Products.ATBiblioList.styles.Chicago'] = styles.chicago
sys.modules['Products.ATBiblioList.styles.Harvard'] = styles.harvard
sys.modules['Products.ATBiblioList.styles.MLA'] = styles.mla

