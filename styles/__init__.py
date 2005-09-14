##########################################################################
#                                                                        #
#    copyright (c) 2004 Royal Belgian Institute for Natural Sciences     #
#                       and contributors                                 #
##########################################################################

from minimal import MinimalBibrefStyle, manage_addMinimalBibrefStyle
from chicago import ChicagoBibrefStyle, manage_addChicagoBibrefStyle
from mla import MLABibrefStyle, manage_addMLABibrefStyle
from apa import APABibrefStyle, manage_addAPABibrefStyle
from harvard import HarvardBibrefStyle, manage_addHarvardBibrefStyle


def initialize(context):
    context.registerClass(MinimalBibrefStyle,
                          constructors = (manage_addMinimalBibrefStyle,),
                          ) 
    context.registerClass(ChicagoBibrefStyle,
                          constructors = (manage_addChicagoBibrefStyle,),
                          ) 
    context.registerClass(MLABibrefStyle,
                          constructors = (manage_addMLABibrefStyle,),
                          ) 
    context.registerClass(APABibrefStyle,
                          constructors = (manage_addAPABibrefStyle,),
                          ) 
    context.registerClass(HarvardBibrefStyle,
                          constructors = (manage_addHarvardBibrefStyle,),
                          ) 
