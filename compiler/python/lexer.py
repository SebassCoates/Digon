################################################################################
#  Digon                                                                       #
#  A graph-based programming language for naturally concurrent and             #
#  well-structured code.                                                       #
#                                                                              #
#  Created by Sebastian Coates and John Tagliaferro at Tufts University.       #
#                                                                              #
#  lexer.py                                                                    #
#  Code for lexing Digon source files.                                         #
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

from errors import *

############################## PRIVATE FUNCTIONS ###############################


############################### LEXER VARAIBLES ################################
symbols   = {""}
types     = {"int", "bool", "char", "byte"}
keywords  = {}
states    = ["NEW_LINE", "READ_KEYWORD", "READ_TYPE"]
state     = 0

###Used During Lexing
variables = {}


################################## INTERFACE ###################################

# Lexes file, reports warnings and errors.
# Params:
#       fileText - plaintext of file as string
# 
# Returns: 
#       lexed - lexed plaintext as list of tokens (tokens are strings)
#
def lex(fileText):
    lexed = []
    currentToken = ""

    for char in fileText:
        #append to current token
        #check if state change
                #check if valid state change
                #handle state change or print warning/error
                #update lexed list with appropriate token


    return lexed