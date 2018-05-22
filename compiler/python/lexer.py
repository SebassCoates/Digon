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
opperands  = {"+", "-", "*", "/"}
types      = {"node", "int", "bool", "char", "byte", "string"}
keywords   = {"for", "while", "in"}
states     = ["READING", "READ_KEYWORD", "READ_TYPE", "READ_WHITESPACE"]

class LexerState:
        #Set to default state on creation
        def __init__(self):  
                self.reset()

        def reset(self):
                self.currentState = "NEUTRAL"
                self.parenStack   = [] #for grammar check
                self.bracketStack = [] #for grammar check
                self.braceStack   = [] #for grammar check
                self.variables    = set() #for grammar check
                self.nodes        = set() #for grammar check
                self.existingVar  = False #for grammar check
                self.expectingEquals = False
                self.expectingBrace = False
                self.expectingType = False
                self.expectingVar = False
                self.expectingInt = False
                self.expectingBracket = False
                self.expectingComma = False
                self.expectingIn = False
                self.expectingInt = False
                self.expectingIterable = False
                self.expectingLiteral = False
                self.expectingOperand = False
                self.expectingOpenBrace = False
                self.expectingString = False
                self.possiblyLinking = False
                self.expectingLessThan = False
                self.expectingGreaterThan = False
                self.expectingNode = False
                self.numParens = 0

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
# TODO : DON'T SPLIT BY PUNCTUATION IN STRINGS, DON'T SPLIT ON '.' IN DOUBLE 
#        LITERALS
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
        variables = state.variables
        nodes = state.nodes

        if token not in variables.union(nodes).union(keywords).union(symbols).union(types):
                if state.currentState != "READING_LITERAL":
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
        if state.currentState == "READING_LITERAL":
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
        variables = state.variables
        if token in variables: #TODO CHECK IF INT VARIABLE
                return True
        try:
                x = int(token)
        except:
                return False

        return True

# Updates state appropriately when in neutral state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_neutral(state, token, grammarError):
        if token == 'node':
                state.currentState = "NODE_DECLARED"
        elif is_int(token, state):  #TODO: Replace with is_literal
                state.currentState = "LINKING_NODE"
                state.expectingEquals = True
        elif is_new_variable(token, state):
                state.variables.add(token)
                state.currentState = "DEFINING_VAR"
        elif token in state.variables:
                state.currentState = "DEFINING_VAR"
                state.existingVar = True
        elif token == '}':
                if len(state.braceStack) > 0:
                        state.braceStack.pop()
                else:
                        grammarError = ('error', "Unbalanced brackets '" + token + "'")
                        state.currentState = "NEUTRAL"
        elif token == "{":
                state.braceStack.append(1)
        elif token == "for":
                state.currentState = "FOR_LOOP_DECLARED"
                state.expectingVar = True

        return grammarError

# Updates state appropriately when in node declared state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_node_declared(state, token, grammarError):
        if is_new_variable(token, state):
                state.nodes.add(token)
                state.currentState = "DEFINING_NODE"
        elif token in nodes:
                grammarError = ('error', "Redefinition of node '" + token + "'")
                state.currentState = "NEUTRAL"
        else:
                grammarError = ('error', "Expecting Node name, got '" + token + "'")
                state.currentState = "NEUTRAL"

        return grammarError

# Updates state appropriately when in defining node state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_defining_node(state, token, grammarError):
        if token == '{':
                state.braceStack.append(1)
                state.currentState = "NEUTRAL"
        elif token == '<':
                state.expectingEquals = True
        elif token == "=":
                if state.expectingEquals:
                        state.currentState = "READING_PARAMS"
                        state.numParens = len(state.parenStack)
                        state.expectingVar = True
                else:
                        grammarError = ('error', "Expecting '=', got '" + token + "'")

        return grammarError

# Updates state appropriately when in defining reading params
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_reading_params(state, token, grammarError):
        if token == "{":
                if state.expectingBrace:
                        state.currentState = "NEUTRAL"
                        state.expectingBrace = False
                        state.braceStack.append(1)
                else:
                        grammarError = ('error', "Expecting parameters but got '{'")
        elif token == "(":
                state.parenStack.append(1)
        elif is_int(token, state):
                if not state.expectingInt:
                        grammarError = ('error', "Expecting int but got '" + token + "'")
                else:
                        state.expectingInt = False
                        state.expectingBracket = True
        elif token == ")":
                if len(state.parenStack) == 0:
                        grammarError = ('error', "You have unbalanced parentheses (more open than closed)")
                        state.currentState = "NEUTRAL"
                else:
                        state.parenStack.pop()
                if len(state.parenStack) == state.numParens:
                        state.expectingBrace = True
                        state.numParens = 0
        elif is_new_variable(token, state):
                if state.expectingVar:
                        state.variables.add(token)
                        state.expectingType = True
                        state.expectingVar = False
                else:
                        grammarError = ('error', "Not expecting variable, but got'" + token + "'")
        elif token in types:
                if state.expectingInt or state.expectingBracket:
                        grammarError = ('error', "Expecting integer or closing bracket but got '" + token + "'")
                elif state.expectingType:
                        state.expectingType = False
                else:
                        grammarError = ('error', "Not expecting type but got '" + token + "'")
        elif token == ",":
                if state.expectingType:
                        grammarError = ('error', "Expecting type but got ','")
                elif state.expectingVar:
                        grammarError = ('error', "Expecting var but got ','")
                else:
                        state.expectingVar = True
        elif token == "[":
                if not state.expectingType:
                        grammarError = ('error', "Expecting type but got '" + token + "'")
                elif state.expectingInt:
                        grammarError = ('error', "Expecting integer literal or variable but got '" + token + "'")
                elif state.expectingBracket: #closing bracket
                        grammarError = ('error', "Expecting ']' but got '" + token + "'")
                else:
                        state.expectingInt = True
                        state.expectingBracket = True
        elif token == "]":
                if not state.expectingType:
                        grammarError = ('error', "Expecting type but got '" + token + "'")
                elif not state.expectingBracket:
                        grammarError = ('error', "Unexpected ']'")
                else:
                        state.expectingInt = False
                        state.expectingBracket = False

        return grammarError

# Updates state appropriately when in defining var state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_defining_var(state, token, grammarError):
        if token == ",":
                state.currentState = "DEFINING_TUPLE" #TODO: Support Tuples
        elif token == ":":
                if not state.existingVar:
                        state.currentState = "EXPECTING_="
                else:
                        grammarError = ('error', "Redefinition of variable")
                        state.currentState = "NEUTRAL"
        elif token == "=":
                if not state.existingVar:
                        grammarError = ('error', "Variable undeclared before assignment")
                else:
                        state.currentState = "ASSINGING_TO_VAR"
                        state.expectingLiteral = True
                        state.existingVar = False
        else:
                grammarError = ('error', "During variable declaration got '" + token + "'")
                state.currentState = "NEUTRAL"

        return grammarError

# Updates state appropriately when in expecting equals state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_expecting_equals(state, token, grammarError):
        if token != "=":
                grammarError = ('error', "Expecting '=', got '" + token + "'")
                state.currentState = "NEUTRAL"
        else:
                state.currentState = "ASSINGING_TO_VAR"
                state.expectingLiteral = True
                state.possiblyLinking = True

        return grammarError

# Updates state appropriately when in assigning to var state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_assigning_to_var(state, token, grammarError):
        if state.possiblyLinking and token == ">":
                state.currentState = "LINKING_NODE"
                state.expectingLiteral = False
                state.possiblyLinking = False
        elif is_int(token, state) and state.expectingLiteral:
                state.expectingLiteral = False
                state.expectingOperand = True
        elif token in opperands:
                if not state.expectingOperand:
                        grammarError = ('error', "Unexpected " + token)
                state.expectingLiteral = True
                state.expectingOperand = False
        elif token == '"':
                pass #TODO: This
                #expectingString = True
        elif token == "'":
                pass #TODO: This
                #expectingString = True
        elif token == "[":
                state.expectingInt = True
                state.expectingBracket = True
                state.expectingLiteral = False
        elif token == "]":
                state.expectingInt = False
                state.expectingBracket = False
                state.expectingType = True
        elif is_int(token, state):
                if not state.expectingInt:
                        grammarError = ('error', "Unexpected '" + token + "'")
                else:
                        state.expectingComma = True
                        state.expectingBrace = False
                        state.expectingInt = False
                        state.expectingOperand = True
        elif token in types:
                if not state.expectingType:
                        grammarError = ('error', "Expecting type but got " + token + "'")
                else:
                        state.expectingOpenBrace = True
        elif token == "{":
                state.expectingOpenBrace = False
                state.expectingInt = True
                state.braceStack.append(1)
        elif token == "}":
                state.expectingComma = False
                state.expectingBrace = False
                if len(state.braceStack) > 0:
                        state.braceStack.pop(1)
                else:
                        pass
        elif token == ",":
                if not state.expectingComma:
                        grammarError = ('error', "Unexpected ','")
                else:
                        state.expectingInt = True
                        state.expectingComma = False
        elif token == ";":
                state.currentState = "NEUTRAL"
                state.expectingOpenBrace = False
        else:
                pass
                #grammarError = ('error', "While reading rval, got '" + token + "'")
                #state = "NEUTRAL"
        return grammarError

# Updates state appropriately when in for loop declared state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_for_loop_declared(state, token, grammarError):
        if token == "(":
                state.numParens = len(state.parenStack)
                state.parenStack.append(1)
        elif token == ")":
                if len(state.parenStack) > 0:
                        state.parenStack.pop()
                else:
                        grammarError = ('error', "You have unbalanced parentheses (more open than closed)")
                        state.currentState = "NEUTRAL"
        elif token == "in":
                if not state.expectingIn:
                        grammarError = ('error', "Unexpected 'in'")
                else:
                        state.expectingIterable = True
                        state.expectingComma = False
                        state.expectingVar = False
        elif state.expectingIterable:
                if token not in state.variables: #TODO: PROPER ITERABLE CHECK
                        grammarError = ('error', "Expecting iterable but got '" + token + "'")
                else:
                        state.expectingBrace = True
                        state.expectingIterable = False
        elif token == "{":
                if not state.expectingBrace:
                        grammarError = ('error', "Expecting for loop definition but got '{'")
                state.currentState = "NEUTRAL"
                state.braceStack.append(1)
        elif is_new_variable(token, state) or token in state.variables:
                if state.expectingVar:
                        state.expectingVar = False
                        state.expectingComma = True
                        state.expectingIn = True
                        state.variables.add(token)
                else:
                        grammarError = ('error', "Not expecting variable but got '" + token + "'")
        elif token == ',':
                if state.expectingComma:
                        state.expectingVar = True
                        state.expectingComma = False
                else:
                        grammarError = ('error', "Unexpected ,")

        return grammarError

# Updates state appropriately when in linking node state
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       grammarError - tuple of error type (warning or error) and error message
def process_linking_node(state, token, grammarError):
        if token == "=":
                if not state.expectingEquals:
                        grammarError = ('error', "Unexpected '='")
                else:
                        state.expectingGreaterThan = True
        elif token == ">":
                if not state.expectingGreaterThan:
                        grammarError = ('error', "Unexpected '>'")
                else:
                        state.expectingNode = True
                state.expectingEquals = False
                state.expectingGreaterThan = False
        elif token == "(":
                state.parenStack.append(1)
        elif token == ")":
                state.parenStack.pop()
                state.expectingEquals = True
        elif token == ";":
                state.currentState = "NEUTRAL"
                state.expectingEquals = False
                state.expectingNode = False
        else: #TODO: Check if valid node name and valid params instead of default acceptance
                pass #
                if state.expectingNode: 
                        pass

        return grammarError

# Updates state according to next token, determins error if incorrect grammar
# Params:
#       state - current state up to next token
#       token - next token to be processed
# 
# Returns: 
#       state - updated state according to newly processed token
#       grammarError - tuple of error type (warning or error) and error message
#
def update_state(state, token):
        grammarError = None

        if state.currentState == "NEUTRAL":
                return state, process_neutral(state, token, grammarError)
        elif state.currentState == "NODE_DECLARED":
                return state, process_node_declared(state, token, grammarError)
        elif state.currentState == "DEFINING_NODE":
                return state, process_defining_node(state, token, grammarError)
        elif state.currentState == "READING_PARAMS":
                return state, process_reading_params(state, token, grammarError)
        elif state.currentState == "DEFINING_VAR":
                return state, process_defining_var(state, token, grammarError)
        elif state.currentState == "EXPECTING_=":
                return state, process_expecting_equals(state, token, grammarError)
        elif state.currentState == "ASSINGING_TO_VAR":
                return state, process_assigning_to_var(state, token, grammarError)
        elif state.currentState == "FOR_LOOP_DECLARED":
                return state, process_for_loop_declared(state, token, grammarError)
        elif state.currentState == "LINKING_NODE":
                return state, process_linking_node(state, token, grammarError)
        elif token == ';' and state.currentState != "NEUTRAL":
                grammarError = ('error', "Got ';' before expected end of line")
                state.currentState = "NEUTRAL"
        else: #default case. when finished, should not trigger
                state.currentState = "NEUTRAL"
        
        return state, grammarError

# Checks grammar of lexed file, reports warnings and errors
# Params:
#       lexed - lexed plaintext as tokenized lines (list of string lists)
#
def check_grammar(lexed):
        global parenStack, bracketStack, braceStack, variables, nodes
        global existingVar
        token = ""
        state = LexerState()

        for lineIndex in range(len(lexed)):
                line = lexed[lineIndex]
                for token in line:
                        state, err = update_state(state, token)
                        if err is not None:
                                errType, message = err
                                if errType == "warning":
                                        compile_warning(lineIndex + 1, message)
                                else:
                                        compile_error(lineIndex + 1, message)
        if len(state.parenStack) > 0:
                compile_error(-1, "You have unbalanced parentheses (more open than closed)")
        if len(state.bracketStack) > 0:
                compile_error(-1, "You have unbalanced brackets (more open than closed)")
        if len(state.braceStack) > 0:
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
        splitWords = split_whitespace(splitLines) #removes whitespace (not in strings)
        
        lexed = tokenize_symbols(splitWords) 

        check_grammar(lexed) #Assure code is ready for parser, report errors

        return lexed