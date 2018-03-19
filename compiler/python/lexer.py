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
types      = {"node", "int", "bool", "char", "byte", "string"}
keywords   = {"for", "while", "in"}
states     = ["READING", "READ_KEYWORD", "READ_TYPE", "READ_WHITESPACE"]

################################# GLOBAL VARS ##################################
parenStack   = [] #for grammar check
bracketStack = [] #for grammar check
braceStack   = [] #for grammar check
variables    = set() #for grammar check
nodes        = set() #for grammar check
existingVar  = False #for grammar check
expectingEquals = False
expectingBrace = False
expectingType = False
expectingVar = False
expectingInt = False
expectingBracket = False
expectingComma = False
expectingIn = False
expectingIterable = False
numParens = 0

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

# Determines if new token represents a newly defined variable
# Params:
#       token - next token to be processed
#       state - current state up to next token
# 
# Returns: 
#       True if token is new variable
#       False otherwise
#
def is_new_variable(token, state):
        global parenStack, bracketStack, braceStack, variables, nodes

        if token not in variables.union(nodes).union(keywords).union(symbols).union(types):
                if state != "READING_LITERAL":
                        return True

        return False

# Determines if new token is part of rval for variable assignment
# Params:
#       token - next token to be processed
#       state - current state up to next token
# 
# Returns: 
#       True if token is part of valid rval
#       False otherwise
#
def is_rval(token, state):
        if state == "READING_LITERAL":
                return True

        try:
                intval = int(token)
        except: #not int literal
                return False

        return True

# Determines if new token is int literal or int variable
# Params:
#       token - next token to be processed
#       state - current state up to next token
# 
# Returns: 
#       True if token is int
#       False otherwise
#
def is_int(token, state):
        global variables
        if token in variables: #TODO CHECK IF INT VARIABLE
                return True
        try:
                x = int(token)
        except:
                return False

        return True

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
        global parenStack, bracketStack, braceStack, variables, nodes
        global existingVar, expectingEquals, numParens, expectingBrace
        global expectingType, expectingVar, expectingInt, expectingBracket
        global expectingComma, expectingIn, expectingIterable
        grammarError = None

        if state == "NEUTRAL":
                if token == 'node':
                        state = "NODE_DECLARED"
                elif is_new_variable(token, state):
                        variables.add(token)
                        state = "DEFINING_VAR"
                elif token in variables:
                        state = "DEFINING_VAR"
                        existingVar = True
                elif token == '}':
                        if len(braceStack) > 0:
                                braceStack.pop()
                        else:
                                grammarError = ('error', "Unbalanced brackets '" + token + "'")
                                state = "NEUTRAL"
                elif token == "{":
                        braceStack.append(1)
                elif token == "for":
                        state = "FOR_LOOP_DECLARED"
                        expectingVar = True

        elif state == "NODE_DECLARED":
                if is_new_variable(token, state):
                        nodes.add(token)
                        state = "DEFINING_NODE"
                elif token in nodes:
                        grammarError = ('error', "Redefinition of node '" + token + "'")
                        state = "NEUTRAL"
                else:
                        grammarError = ('error', "Expecting Node name, got '" + token + "'")
                        state = "NEUTRAL"

        elif state == "DEFINING_NODE":
                if token == '{':
                        braceStack.append(1)
                        state = "NEUTRAL"
                elif token == '<':
                        expectingEquals = True
                elif token == "=":
                        if expectingEquals:
                                state = "READING_PARAMS"
                                numParens = len(parenStack)
                                expectingVar = True
                        else:
                                grammarError = ('error', "Expecting '=', got '" + token + "'")

        elif state == "READING_PARAMS":
                if token == "{":
                        if expectingBrace:
                                state = "NEUTRAL"
                                expectingBrace = False
                                braceStack.append(1)
                        else:
                                grammarError = ('error', "Expecting parameters but got '{'")
                elif token == "(":
                        parenStack.append(1)
                elif is_int(token, state):
                        if not expectingInt:
                                grammarError = ('error', "Expecting int but got '" + token + "'")
                        else:
                                expectingInt = False
                                expectingBracket = True
                elif token == ")":
                        if len(parenStack) == 0:
                                grammarError = ('error', "You have unbalanced parentheses (more open than closed)")
                                state = "NEUTRAL"
                        else:
                                parenStack.pop()
                        if len(parenStack) == numParens:
                                expectingBrace = True
                                numParens = 0
                elif is_new_variable(token, state):
                        if expectingVar:
                                variables.add(token)
                                expectingType = True
                                expectingVar = False
                        else:
                                grammarError = ('error', "Not expecting variable, but got'" + token + "'")
                elif token in types:
                        if expectingInt or expectingBracket:
                                grammarError = ('error', "Expecting integer or closing bracket but got '" + token + "'")
                        elif expectingType:
                                expectingType = False
                        else:
                                grammarError = ('error', "Not expecting type but got '" + token + "'")
                elif token == ",":
                        if expectingType:
                                grammarError = ('error', "Expecting type but got ','")
                        elif expectingVar:
                                grammarError = ('error', "Expecting var but got ','")
                        else:
                                expectingVar = True
                elif token == "[":
                        if not expectingType:
                                grammarError = ('error', "Expecting type but got '" + token + "'")
                        elif expectingInt:
                                grammarError = ('error', "Expecting integer literal or variable but got '" + token + "'")
                        elif expectingBracket: #closing bracket
                                grammarError = ('error', "Expecting ']' but got '" + token + "'")
                        else:
                                expectingInt = True
                                expectingBracket = True
                elif token == "]":
                        if not expectingType:
                                grammarError = ('error', "Expecting type but got '" + token + "'")
                        elif not expectingBracket:
                                grammarError = ('error', "Unexpected ']'")
                        else:
                                expectingInt = False
                                expectingBracket = False

        elif state == "DEFINING_VAR":
                if token == ",":
                        state = "DEFINING_TUPLE"
                elif token == ":":
                        if not existingVar:
                                state = "EXPECTING_="
                        else:
                                grammarError = ('error', "Redefinition of variable")
                                state = "NEUTRAL"
                elif token == "=":
                        if not existingVar:
                                grammarError = ('error', "Variable undeclared before assignment")
                        else:
                                state = "ASSINGING_TO_VAR"
                                existingVar = False
                else:
                        grammarError = ('error', "During variable declaration got '" + token + "'")
                        state = "NEUTRAL"

        elif state == "EXPECTING_=":
                if token != "=":
                        grammarError = ('error', "Expecting '=', got '" + token + "'")
                        state = "NEUTRAL"
                else:
                        state = "ASSINGING_TO_VAR"

        elif state == "ASSINGING_TO_VAR":
                if is_rval(token, state):
                        state = "RESOLVING_RVAL"
                else:
                        grammarError = ('error', "Expecting value, got '" + token + "'")
                        state = "NEUTRAL"

        elif state == "FOR_LOOP_DECLARED":
                if token == "(":
                        numParens = len(parenStack)
                        parenStack.append(1)
                elif token == ")":
                        if len(parenStack) > 0:
                                parenStack.pop()
                        else:
                                grammarError = ('error', "You have unbalanced parentheses (more open than closed)")
                                state = "NEUTRAL"
                elif token == "in":
                        if not expectingIn:
                                grammarError = ('error', "Unexpected 'in'")
                        else:
                                expectingIterable = True
                                expectingComma = False
                                expectingVar = False
                elif expectingIterable:
                        if token not in variables: #TODO: PROPER ITERABLE CHECK
                                grammarError = ('error', "Expecting iterable but got '" + token + "'")
                        else:
                                expectingBrace = True
                                expectingIterable = False
                elif token == "{":
                        if not expectingBrace:
                                grammarError = ('error', "Expecting for loop definition but got '{'")
                        state = "NEUTRAL"
                        braceStack.append(1)
                elif is_new_variable(token, state) or token in variables:
                        if expectingVar:
                                expectingVar = False
                                expectingComma = True
                                expectingIn = True
                                variables.add(token)
                        else:
                                grammarError = ('error', "Not expecting variable but got '" + token + "'")
                elif token == ',':
                        if expectingComma:
                                expectingVar = True
                                expectingComma = False
                        else:
                                grammarError = ('error', "Unexpected ,")

        elif token == ';' and state != "NEUTRAL" and state != "RESOLVING_RVAL":
                grammarError = ('error', "Got ';' before expected end of line")
                state = "NEUTRAL"
        
        else:
                state = "NEUTRAL"

        newState = state
        
        return newState, grammarError

# Checks grammar of lexed file, reports warnings and errors
# Params:
#       lexed - lexed plaintext as tokenized lines (list of string lists)
#
def check_grammar(lexed):
        global parenStack, bracketStack, braceStack, variables, nodes
        global existingVar
        token = ""
        state = "NEUTRAL"

        for lineIndex in range(len(lexed)):
                line = lexed[lineIndex]
                for token in line:
                        state, err = update_state(state, token, lexed)
                        if err is not None:
                                errType, message = err
                                if errType == "warning":
                                        compile_warning(lineIndex + 1, message)
                                else:
                                        compile_error(lineIndex + 1, message)
        if len(parenStack) > 0:
                compile_error(-1, "You have unbalanced parentheses (more open than closed)")
        if len(bracketStack) > 0:
                compile_error(-1, "You have unbalanced brackets (more open than closed)")
        if len(braceStack) > 0:
                compile_error(-1, "You have unbalanced braces (more open than closed)")


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