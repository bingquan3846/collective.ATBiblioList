## Script (Python) "sortBibrefDictList"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=dictlist=[]
##title=sortBibrefDictList
##

# sorts a list of bibref dictonnaries using two different methods
# 1st sorting key: first author's lastname
# 2nd sorting key: publication_year

# method 1: publication_year
tmplist = [(x['publication_year'],x) for x in dictlist]
tmplist.sort()
dictlist = [y for (x,y) in tmplist]

# method 2: authors[0]['lastname']
def cmpLName(dica, dicb):
    autha, authb = dica.get('authors'), dicb.get('authors')
    if autha and authb:
        return cmp(autha[0].get('lastname'), authb[0].get('lastname'))
    return -1
dictlist.sort(cmpLName)

return dictlist