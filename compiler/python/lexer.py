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
"/", "*", ".", ","}
types      = {"node", "int", "bool", "char", "byte"}
keywords   = {"for", "while", "in"}
states     = ["READING", "READ_KEYWORD", "READ_TYPE", "READ_WHITESPACE"]



############################## PRIVATE FUNCTIONS ###############################
# Splits lines of file into words but leaves whitespace in string literals
# Params:
#       stringLines - list of lines in file as strings
# 
# Returns: 
#       wordsByLine - plaintext lines split into words (list of string lists)
#
def split_whitespace(stringLines):
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

# Separates symbols from non-symbol tokens
# Params:
#       wordList - plaintext lines split into words (list of string lists)
# 
# Returns: 
#       tokenized - lexed plaintext as tokenized lines (list of string lists)
#
def tokenize_symbols(wordList):
        tokenized = [[] for line in wordList]

        for lineIndex in range(len(wordList)):
                line = wordList[lineIndex]
                for word in line:
                        start = 0
                        for charIndex in range(len(word)): 
                                char = word[charIndex]
                                if char in symbols:
                                        if charIndex > start:
                                                tokenized[lineIndex].append(word[start:charIndex])
                                        tokenized[lineIndex].append(word[charIndex:charIndex + 1])
                                        start = charIndex + 1

                        if start != len(word):
                                tokenized[lineIndex].append(word[start:])

        return tokenized

# Updates state according to next token, determins error if incorrect grammar
# Params:
#       state - current state up to next token
#       token - next token to be processed
#       lexed - lexed plaintext as tokenized lines (list of lists)
# 
# Returns: 
#       newState - updated state according to newly processed token
#       grammarError - tuple of error type (warning or error) and error message
#
def update_state(state, token, lexed):
        newState = state
        grammarError = None
        return newState, grammarError

# Checks grammar of lexed file, reports warnings and errors
# Params:
#       lexed - lexed plaintext as tokenized lines (list of string lists)
#
def check_grammar(lexed):
        pass
        token = ""
        state = ""
        parenStack = []
        bracketStack = []
        braceStack = []

        for lineIndex in range(len(lexed)):
                line = lexed[lineIndex]
                for token in line:
                        state, err = update_state(state, token, lexed)
                        if err is not None:
                                errType, message = err
                                if errType == "warning":
                                        compile_warning(lineIndex + 1, err)
                                else:
                                        compile_error(lineIndex + 1, err)


################################## INTERFACE ###################################
# Lexes file, reports warnings and errors.
# Params:
#       fileText - plaintext of file as string
# 
# Returns: 
#       lexed - lexed plaintext tokenized lines (list of lists)
#
def lex(fileText):
        splitLines = fileText.split("\n") 
        splitWords = split_whitespace(splitLines) #removes whitespace, keeps in strings
        
        lexed = tokenize_symbols(splitWords) 

        check_grammar(lexed)

        return lexed
