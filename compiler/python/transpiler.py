################################################################################
#  Digon                                                                       #
#  A graph-based programming language for naturally concurrent and             #
#  well-structured code.                                                       #
#                                                                              #
#  Created by Sebastian Coates and John Tagliaferro at Tufts University.       #
#                                                                              #
#  transpiler.py                                                               #
#  Transpiles Digon into equivalent Go.                                        #
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

# Changes Digon syntax to Go equivalent, or adds appropriate spacing
# Params:
#       sourcecode - Parsed Digon source code by line (list of string lists)
#
def change_syntax(sourcecode, node):
        #ensure appropriate whitespace, simple syntax changes
        explicitChildren = set([token for token in sourcecode if token in node.neighbors])

        for i, token in enumerate(sourcecode):
                if token == 'in':
                        sourcecode[i] = " := range "
                elif token == "println":
                        sourcecode[i] = "fmt.Println"
                elif token == 'if':
                        sourcecode[i] = 'if '
                elif token == 'for':
                        sourcecode[i] = 'for '
                elif token == 'float':
                        sourcecode[i] = 'float64'
                elif token == 'map' and sourcecode[i - 2] == ':': #map delcaration
                        sourcecode[i] = "make(map"
                        sourcecode[i + 1] = "["
                        sourcecode[i + 3] = ']'
                        sourcecode[i + 5] = ")"



# Changes Digon syntax to Go equivalent, or adds appropriate spacing
# Params:
#       sourcecode - Parsed Digon source code by line (list of string lists)
#
def transpile_function_calls(sourcecode, node):
        for i, token in enumerate(sourcecode):
                if token == '=' and sourcecode[i + 1] == ">":
                         #get lval
                        leftindex = i - 1 #index of lval
                        j = 1
                        param = "" 
                        while sourcecode[i - j] != ';' and sourcecode[i - j] != '}': #SEMICOLONS ARE NECESSARY (FOR NOW)
                                param = sourcecode[i - j] + param
                                sourcecode[i - j] = ""
                                j += 1
                        if sourcecode[i + 2] == 'dest':
                                sourcecode[i - 1] = "channel"
                                sourcecode[i] = '<'
                                sourcecode[i + 1] = '-'
                                sourcecode[i + 2] = param
                                sourcecode[i + 3] = "" #replace (
                                sourcecode[i + 4] = "" #replace )
                        else: 
                                sourcecode[i - 1] = sourcecode[i + 2] #function name
                                if sourcecode[i - 1] == "length":
                                        sourcecode[i - 1] = "len"
                                sourcecode[i] = '('
                                sourcecode[i + 1] = param
                                sourcecode[i + 2] = ')'
                                i += 3
                                while sourcecode[i] != ')':
                                        sourcecode[i] = ""
                                        i += 1
                                sourcecode[i] = ""
                                i += 1

                                if sourcecode[i] == '=':
                                        #check if assignment or pass on node
                                        if sourcecode[i + 3] != '(': #assignment
                                                sourcecode[leftindex] = sourcecode[i + 2] + " = " + sourcecode[leftindex]
                                                sourcecode[i] = ""
                                                sourcecode[i + 1] = ""
                                                sourcecode[i + 2] = ""
                                                i += 3
                                        else:
                                                while sourcecode[i] != ")":
                                                        sourcecode[i] = ""
                                                        i += 1
                                                sourcecode[i] = ""
                else:
                        pass
                       #print(token, end=" ")


################################## INTERFACE ###################################
# Transpiles Digon source to equivalent Go source
# Params:
#       sourcecode - Parsed Digon source code by line (list of string lists)
# 
# Returns: 
#       transpiled - Transpiled code in same form
#
def transpile_to_go(sourcecode, node):
        change_syntax(sourcecode, node)        
        transpile_function_calls(sourcecode, node)