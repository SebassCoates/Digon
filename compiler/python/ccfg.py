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

from node import * #defines node 'struct'

############################## PRIVATE CONSTANTS ###############################
COLORS = set(open('colors.txt', 'r').read().split())

BUILT_IN_NODES = {'dest', 'length', 'println'} #TODO: replace with SPoT

#General graph class for storing graph coloring and more
class Graph:
        def __init__(self, nodes):
                self.adjList, self.colors, self.nodes = self.build_CCFG(nodes)

        ######################### INTERFACE FUNCTIONS ##########################
        # Writes graph data to Graph Viewer compatible files
        # Params:
        #       ccfg - CCFG tuple representation (adjList, colors, nodeList)
        # 
        # Writes Files:
        #       ccfg.txt - adjacency matrix data for ccfg
        #       ccfg_labels.txt - label names for ccfg
        #       ccfg_colors.txt - colors for ccfg       
        #
        def write_graph(self):
                graphfile = open('ccfg.txt', 'w')
                labelfile = open('ccfg_labels.txt', 'w')
                colorfile = open('ccfg_colors.txt', 'w')

                adjList  = self.adjList
                colors   = self.colors
                nodeList = self.nodes

                for i, node in enumerate(nodeList):
                        indexedLabels = [n.name for n in nodeList]
                        neighborIndices = [indexedLabels.index(n) for n in node.neighbors if n in adjList[i] and n in indexedLabels]

                        for j in range(len(adjList)):
                                if j in neighborIndices:
                                        graphfile.write('1 ')
                                elif node.dest != '' and j == indexedLabels.index(node.dest):
                                        graphfile.write('1 ')
                                else:
                                        graphfile.write('0 ')

                        graphfile.write("\n")
                        labelfile.write(node.name + "\n")

                for color in colors:
                        colorfile.write(color + "\n")

                graphfile.close()
                labelfile.close()
                colorfile.close()

        ########################## PRIVATE FUNCTIONS ###########################
        # Builds graph using list of nodes
        # Params:
        #       nodeList - list of node structs
        # 
        # Returns: 
        #       adjList - adjacency list for given graph
        #
        def build_graph(self, nodeList):
                adjList = [set() for node in nodeList]

                for i, node in enumerate(nodeList):
                        adjList[i] = set(node.neighbors)

                return adjList

        # Colors graph using super cool graph coloring algorithm
        # Params:
        #       adjList - adjacency list of graph (list of sets)
        # 
        # Returns: 
        #       colors - list of colors for graph
        #
        def color_graph(self, adjList, nodeList):
                nodes = [i for i in range(len(adjList))]
                visited = [False for node in nodes]
                colors = ['no_color' for i in range(len(nodes))] 
                indexedLabels = [node.name for node in nodeList]

                while len(nodes) > 0: 
                        root = nodes.pop(0)
                        nodeQ = [root]
                        visited[root] = True
                        colors[root] = 'Black'

                        while len(nodeQ) > 0:
                                node = nodeQ.pop(0)
                                COLORS.remove(colors[node])
                                newColor = COLORS.pop()
                                for child in adjList[node]:
                                        if child not in BUILT_IN_NODES:
                                                childIndex = indexedLabels.index(child)
                                                colors[childIndex] = newColor
                                                nodeQ.append(childIndex)
                                                visited[childIndex] = True
                                                if len(nodes) > 0:
                                                        nodes.remove(childIndex)
                                COLORS.add(colors[node])
                                COLORS.add(newColor)

                return colors

        # Builds colored control flow graph (CCFG)
        # Params:
        #       nodeList - list of node structs representing source code (see node.py) 
        # 
        # Returns: 
        #       CCFG tuple representation (adjList, colors, nodeList)
        #
        def build_CCFG(self, nodeList):
                nodeNames = set([node.name for node in nodeList])
                colors = []
                adjList = self.build_graph(nodeList)

                colors = self.color_graph(adjList, nodeList)

                return (adjList, colors, nodeList)