################################################################################
#  Digon                                                                       #
#  A graph-based programming language for naturally concurrent and             #
#  well-structured code.                                                       #
#                                                                              #
#  Created by Sebastian Coates and John Tagliaferro at Tufts University.       #
#                                                                              #
#  node.py                                                                     #
#  Struct representation of a Node during compilation process.                 #
#  Contains name, parsed source code, list of neighbors, and color.            #
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

# Class to represent Node structure.
# Instance Variables:
#       name - name of node (unique identifier) 
#       sourceCode - lexed, parsed source code corresponding to node
#       neighbors - represents 'out-neighborhood' as list of names
#                   (list of nodes reachable from this node)
#       color - can't be same as any adjacent node
#               same-color nodes represent concurrent processes
#
class Node:
    def __init__(self, name, sourceCode, neighbors, color):
        self.name = name
        self.sourceCode = sourceCode
        self.neighbors = neighbors
        self.color = color

# Creates instance of node struct
# Params:
#       name - name of node (unique identifier) 
#       sourceCode - lexed, parsed source code of node
#       neighbors - represents 'out-neighborhood' as list of names
#                   (list of nodes reachable from this node)
#       color - can't be same any adjacent node 
#               same-color nodes represent concurrent processes
# 
# Returns: 
#       node initialized with parameter values
#
def create_node(name, sourceCode, neighbors, color="undefined"):
    return Node(name, sourceCode, neighbors, color)