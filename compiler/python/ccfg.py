################################################################################
#  Digon                                                                       #
#  A graph-based programming language for naturally concurrent and             #
#  well-structured code.                                                       #
#                                                                              #
#  Created by Sebastian Coates and John Tagliaferro at Tufts University.       #
#                                                                              #
#  ccfg.py                                                                     #
#  Representation of a 'colored control flow graph', a high-level control flow #
#  graph where same-color nodes represent concurrent processes.                #
#                                                                              #
#  Copyright 2018 Sebastian Coates and John Tagliaferro.                       #
#                                                                              #
#  Digon is free software: you can redistribute it and/or modify               #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  Digon is distributed in the hope that it will be useful,                    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with Digon.  If not, see <http://www.gnu.org/licenses/>.              #
################################################################################

from node import *

# Builds colored control flow graph (CCFG)
# Params:
#       nodeList - list of node structs representing source code (see node.py) 
# 
# Returns: 
#       CCFG tuple representation (adjList, colors, nodeList)
#
#
def build_CCFG(nodeList):
        adjList = [set() for node in nodeList]
        nodeNames = set([node.name for node in nodeList])


        return ("hello", "world")
