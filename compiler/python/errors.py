################################################################################
#  Digon                                                                       #
#  A graph-based programming language for naturally concurrent and             #
#  well-structured code.                                                       #
#                                                                              #
#  Created by Sebastian Coates and John Tagliaferro at Tufts University.       #
#                                                                              #
#  errors.py                                                                   #
#  Contains all code for error reporting during compilation including compiler #
#  usage, compiler warnings, and compiler errors.                              #
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

warnCount  = 0 #track total number of warnings reported
errorCount = 0 #track total number of errors reported, used as flag

# Prints error message and exits for file argument of invalid type
# Params:
#       filepath - path to invalid file
# 
def invalid_file_extension(filepath):
    print("Supported file extensions: .di")
    print(filepath + " does not have a valid extension")
    quit()

# Prints error message and exits for invalid file argument.
# Params:
#       filepath - path to invalid file
# 
def invalid_file(filepath):
    print("Could not open '" + filepath + "'")
    print("Ensure '" + filepath + "' exists and is a valid .di file")
    quit()

# Prints warning message.
# Params:
#       lineNumber - line number of warning in source code
#       warnType - type of warning (determines which message to print)
# 
def compile_warning(lineNumber, warnType):
    global warnCount
    warnCount += 1

    print("Warning at line " + str(lineNumber) + ":\n\t" + warnType + "\n")

# Prints error message.
# Params:
#       lineNumber - line number of error in source code
#       errorType - type of error (determines which message to print)
# 
def compile_error(lineNumber, errorType):
    global errorCount
    errorCount += 1

    print("Error at line " + str(lineNumber) + ":\n\t" + errorType + "\n")

# Quits program if any errors occurred during compilation.
def quit_if_error():
    if errorCount != 0:
        quit()
