################################################################################
#  Digon                                                                       #
#  A graph-based programming language for naturally concurrent and             #
#  well-structured code.                                                       #
#                                                                              #
#  Created by Sebastian Coates and John Tagliaferro at Tufts University.       #
#                                                                              #
#  digon.py                                                                    #
#  Compiles Digon source code to Go, runs Go compiler to generate executable.  #
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

from sys import argv #command line args
from os import remove as remove_file
from subprocess import Popen

from node import *   #node definition
import ccfg as CCFG #definition
from ccfg import Graph
from lexer import lex, types
from parser import parse
import errors as err
import transpiler as tr


# Processes file to be ready for compilation. Takes lexed, parsed, filetext and
# converts to CCFG representation.
# Params:
#       filename - path to .di source code file
# 
# Returns: 
#       Parsed file
#
def process_file(filename):
    try:
        filetext = open(filename, 'r').read()
    except:
        err.invalid_file(filename) #errors.py

    nodeList = parse(lex(filetext)) #lexer.py, parser.py
    
    return nodeList

# Writes go files corresponding to digon code to be compiled 
# Params:
#       ccfg - graph object for source code
# 
# Returns: 
#       List of go file names created
#
def generate_go(ccfg):
    builtinFunctions = ['length', 'println']

    file = open('gomain.go', 'w')
    gosource = 'package main\n\nimport "fmt"\n\n'
    #adjList, colors, nodes = ccfg

    for node in ccfg.nodes: #TODO: Replace with BFS?
        if node.name == "root": #Need a main function in Go!
            node.name = "main"

        gosource += "func " + node.name + "(" #Function headers
        assignments = []
        for i, param in enumerate(node.params):
            param = param.replace('float', 'float64')
            if len(node.ancestors) > 1:
                parts = param.split()
                assignments.append(parts[0])
                parts[0] = parts[0] + "chan"
                parts.insert(1, "chan")
                for part in parts:
                    gosource += part + " "
            else:
                gosource += param
            if i != len(node.params) - 1:
                gosource += ", " 

        if node.dest != '':
            gosource += ", channel chan " + node.destType

        gosource += ') {\n'

        for ass in assignments:
            gosource += ass + " := <- " + ass + "chan;\n"

        tr.transpile_to_go(node.sourceCode, node, ccfg.nodes) #modifies in place

        for i, token in enumerate(node.sourceCode): 
                gosource +=  token
                if ';' in token or token == '{' and node.sourceCode[i - 1] not in types:
                    gosource += '\n'
                if token == '}' and i < len(node.sourceCode) - 1 \
                                and node.sourceCode[i + 1] != 'else':
                    gosource += '\n'

        gosource += "}\n\n"
    
    #print(gosource) #debug
    file.write(gosource)
    return ['gomain.go']


################################### MAIN #######################################
parsedFiles = {}

for filename in argv[1:]:
    if filename[len(filename) - 3:] != '.di':
        err.invalid_file_extension(filename)

    parsedFiles[filename] = process_file(filename) 
#err.quit_if_error() #disable while lexer is incomplete/buggy to test compile

allNodes = []
for file in parsedFiles:
    allNodes += parsedFiles[file]

ccfg = Graph(allNodes)
ccfg.write_graph() #for debugging

filenames = generate_go(ccfg)
try:
    Popen(['go', 'fmt'])
    Popen(['go', 'build'])
except:
    print("Final compilation failed. Perhaps Go is not properly installed on your system.")

#for file in filenames: #clean up intermediary .go files
#    remove_file(file) #os.remove()