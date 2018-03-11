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

############################### CONST VARAIBLES ################################
symbols    = {":", "=", "<", ">", "{", "}", "[", "]", "(", ")", ";", "-", "+", \
"/", "*", "."}
types      = {"node", "int", "bool", "char", "byte"}
keywords   = {"for", "while", "in"}
states     = ["READING", "READ_KEYWORD", "READ_TYPE", "READ_WHITESPACE"]



############################## PRIVATE FUNCTIONS ###############################
def safe_split(stringLines):
        wordsByLine = []
        readingString = False
        readQuote = False
        readApost = False

        newWord = ""
        for line in stringLines:
                words = []
                for char in line:
                        if char == '"':
                                if readQuote and not readApost:
                                        readingString = False
                                else:
                                        readingString = True

                                readQuote = not readQuote

                        elif char == "'":
                                if readApost and not readQuote:
                                        readingString = False
                                else:
                                        readingString = True

                                readApost = not readApost

                        if not readingString and char.strip() == "":
                                if not newWord.strip() == "":
                                        words.append(newWord)
                                        newWord = ""
                        else:
                                newWord += char

                if not newWord.strip() == "":
                        words.append(newWord)
                        newWord = ""

                wordsByLine.append(words)

        return wordsByLine

def is_type(token):
        return token in types

def update_state(prevState, prevToken, char):

        return prevState, prevToken + char, None

############################### LEXER VARAIBLES ################################
parenStack = []
bracketStack = []
braceStack = []

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
        splitLines = fileText.split("\n") 
        splitWords = safe_split(splitLines) #removes whitespace, keeps in strings
        token = ""
        state = ""

        for lineIndex in range(len(splitWords)):
                line = splitWords[lineIndex]
                for word in line:
                        for char in word:
                                state, token, err = update_state(state, token, char)
                                if err is not None:
                                        print("ERROR")

                        lexed.append(token)
                        token = ""

        print(lexed)
        return lexed