## Script (Python) "sortBibrefDictList"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=dictlist=()
##title=sortBibrefDictList
##

# sorts a list of bibref python dictonaries using two different methods
# 1st sorting key: first author's lastname
# 2nd sorting key: publication_year

# method 1: sort_key = publication_year
tmplist = [(x['publication_year'],x) for x in dictlist]
dictlist = [y for (x,y) in tmplist.sort()]

# method 2: sort_key = authors[0]['lastname']
def cmpLName(self, dicta, dictb):
    a, b = dicta.get('authors'), dictb.get('authors')
    if a and b:
        return cmp(a[0].get('lastname'), b[0].get('lastname'))
    return -1
dictlist.sort(self.cmpLName)

return dictlist