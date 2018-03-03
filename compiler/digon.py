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
import errors as err #error reporting
from node import *   #node definition
from ccfg import *   #CCFG definition

# Lexes file, reports warnings and errors.
# Params:
#       fileText - plaintext of file as list of strings
# 
# Returns: 
#       lexed - lexed plaintext as list of tokens (tokens are strings)
#
def lex(fileText):
    lexed = fileText
    return lexed

# Parses file, reports warnings and errors.
# Params:
#       lexedFile - lexed plaintext of file as list of tokens 
# 
# Returns: 
#       parsed - lexed, parsed plaintext as dictionary {node ID --> node struct}
#
def parse(lexedFile):
    parsed = lexedFile
    return parsed

# Processes file to be ready for compilation. Takes lexed, parsed, filetext and
# converts to CCFG representation.
# Params:
#       filename - path to .di source code file
# 
# Returns: 
#       Parsed file in CCFG form
#
def process_file(filename):
    try:
        filetext = open(filename, 'r').read() 
    except:
        err.invalid_file(filename)

    processed = parse(lex(filetext))
    
    ccfg = processed
    return ccfg


################################### MAIN #######################################
parsedFiles = {}

for filename in argv[1:]:
    if '.di' not in filename:
        err.invalid_file_extension(filename)

    parsedFiles[filename] = process_file(filename) 

err.quit_if_error()
