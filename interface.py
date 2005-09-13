from Interface import Interface

class IBibrefStyle(Interface):
    """ Interface for the format 
        renderers of the bibliolist tool.
    """
    def formatDictionnary(refValues):
        """ returns the rendered bib ref
            refValues must be a dictionnary holding all values
        """

