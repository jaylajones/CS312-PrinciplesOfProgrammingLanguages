import re, sys, string

debug = True
dict = { }
tokens = [ ]
ParseSemicolon = ';'
ParseEqual = "="
ParseColon = ":"
ParseElse = "else"
ParseAnd = "and"
ParseOr = "or"
ParseIfVar = "if"
ParseWhileVar = "while"
ParseEOLIndent = "@"

## need classes for VarRef, String and maybe the parseable items that need to be returning Statements or Expressions



#================================================Objects==========================================================#

		#======================================Semantic Objects===============================================#


class ListforStatementQueue( object ):
	def __init__(self):
		self.List = []

	def addStatement(self, statement):
		self.List.append(statement)

	def __str__(self):
		printStr = ''
		for statement in self.List:
			printStr += str(statement)
		return printStr


# Statement class and subclasses
class Statement( object ):
	def __str__(self):
		return ""

class Assignment( Statement ):
	def __init__(self, id, expr):
		self.id = id
		self.expr = expr
		
	def __str__(self):
		return "= " + str(self.id) + " " + str(self.expr) + "\n"

class WhileStatement( Statement ):
	def __init__(self, expr, block):
		self.expr = expr
		self.block = block

	def __str__(self):
		return "while " + str(self.expr) + "\n" + str(self.block) + "endwhile\n"


class IfStatement( Statement ):
	def __init__(self, expr, ifParse, elseParse):
		self.expr = expr
		self.ifParse = ifParse
		self.elseParse = elseParse

	def __str__(self):
		## syntax of what the sample outputs looked like
		return "if " + str(self.expr) + "\n" + str(self.ifParse) + "else\n" + str(self.elseParse) + "endif\n"



# Expression class and subclasses
class Expression( object ):
	def __str__(self):
		return "" 
	
class BinaryExpr( Expression ):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right
		
	def __str__(self):
		return str(self.op) + " " + str(self.left) + " " + str(self.right)

class Number( Expression ):
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return str(self.value)

class VarRef( Expression ):

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)


class String( Expression ):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)


		#==================================Lexer Class===============================================#


# Lexer, a private class that represents lists of tokens from a Gee
# statement. This class provides the following to its clients:
#
#   o A constructor that takes a string representing a statement
#       as its only parameter, and that initializes a sequence with
#       the tokens from that string.
#
#   o peek, a parameterless message that returns the next token
#       from a token sequence. This returns the token as a string.
#       If there are no more tokens in the sequence, this message
#       returns None.
#
#   o removeToken, a parameterless message that removes the next
#       token from a token sequence.
#
#   o __str__, a parameterless message that returns a string representation
#       of a token sequence, so that token sequences can print nicely

class Lexer :
	
	
	# The constructor with some regular expressions that define Gee's lexical rules.
	# The constructor uses these expressions to split the input expression into
	# a list of substrings that match Gee tokens, and saves that list to be
	# doled out in response to future "peek" messages. The position in the
	# list at which to dole next is also saved for "nextToken" to use.
	
	special = r"\(|\)|\[|\]|,|:|;|@|~|;|\$"
	relational = "<=?|>=?|==?|!="
	arithmetic = "\+|\-|\*|/"
	#char = r"'."
	string = r"'[^']*'" + "|" + r'"[^"]*"'
	number = r"\-?\d+(?:\.\d+)?"
	literal = string + "|" + number
	#idStart = r"a-zA-Z"
	#idChar = idStart + r"0-9"
	#identifier = "[" + idStart + "][" + idChar + "]*"
	identifier = "[a-zA-Z]\w*"
	lexRules = literal + "|" + special + "|" + relational + "|" + arithmetic + "|" + identifier
	
	def __init__( self, text ) :
		self.tokens = re.findall( Lexer.lexRules, text )
		self.position = 0
		self.indent = [ 0 ]
	
	
	# The peek method. This just returns the token at the current position in the
	# list, or None if the current position is past the end of the list.
	
	def peek( self ) :
		if self.position < len(self.tokens) :
			return self.tokens[ self.position ]
		else :
			return None
	
	
	# The removeToken method. All this has to do is increment the token sequence's
	# position counter.
	
	def next( self ) :
		self.position = self.position + 1
		return self.peek( )
	
	
	# An "__str__" method, so that token sequences print in a useful form.
	
	def __str__( self ) :
		return "<Lexer at " + str(self.position) + " in " + str(self.tokens) + ">"



#========================================Stand Alone Functions=========================================================#



# The "parse" function. This builds a list of tokens from the input string,
# and then hands it to a recursive descent parser for the PAL grammar.
# This is where the work is started after the tokens are loaded in correctly.
def parse( text ) :
	global tokens
	tokens = Lexer( text )
	stmtlist = parseStmtList( )
	print (stmtlist)
	return




	#======================================Statement Parsing Functions=================================#



def parseStmtList(  ):
	""" gee = { Statement } """
	tok = tokens.peek( )
	statementList = ListforStatementQueue()

	while tok != None  and tok != "~": #both cases that account for end 

		statement = parseStatement()
		statementList.addStatement(statement)
		tok = tokens.peek()

	return statementList


def parseStatement():


	tok = tokens.peek()
	if debug==False: print ("Statement: ", tok)
    
	elif re.match(ParseIfVar,tok):
		return parseIf()

	if re.match(ParseWhileVar,tok):
		return parseWhile()


	elif re.match(Lexer.identifier, tok):
		return parseAssign()

	error("First statement token invalid; must be an 'if','while' or identifier")
	return


def parseAssign():

	identifier = tokens.peek()
	if debug==False: print ("Assign statement: ")

	if re.match(ParseEqual,tokens.next()) == False:
		error("assignment missing '='")

	tokens.next()
	exp = expression()

	tok = tokens.peek()
	if re.match(ParseSemicolon,tok) == False:
		error("No EOL at end of assignment")

	tokens.next()

	return Assignment(identifier, exp)
	


def parseIf():

	tok = tokens.next()
	if debug== False: print ("If statement: ", tok)

	expr = expression()
	ifBlock = parseBlock()
	eb= ''

	if re.match(ParseElse,tokens.peek()):
		tok = tokens.next()
		if debug==False: print ("Else statement: ", tok)
		eb = parseBlock()

	return IfStatement(expr, ifBlock, eb)


def parseWhile():
	tok = tokens.next()
	if debug==False: print ("While statement: ", tok)

	expr = expression()
	block = parseBlock()

	return WhileStatement(expr, block)



def parseBlock():

	tok = tokens.peek()
	if debug==False: print ("Block: ", tok)
	
	# Check to make sure each of the appropriate terminal tokens exist and are in the right place
	if re.match(ParseColon,tok)== False:
		error("Block is missing ':' ")

	tok = tokens.next()

	if re.match(ParseSemicolon,tok)== False:
		error("Block is missing EOL.")

	tok = tokens.next()

	if re.match(ParseEOLIndent,tok) == False:
		error("Block is missing EOL indent.")

	tok = tokens.next()

	stmtList = parseStmtList()

	if tokens.peek() != "~":
		error("Block is not indented after statements.")

	tokens.next()

	return stmtList



def expression():
	tok = tokens.peek( )
	if debug == False: print ("expression: ", tok)
	left = andExpr( )
	tok = tokens.peek( )
	while re.match(ParseOr,tok):
		tokens.next()
		right = andExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def andExpr():
	tok = tokens.peek( )
	if debug == False: print ("andExpr: ", tok)
	left = relationalExpr( )
	tok = tokens.peek( )
	while re.match(ParseAnd,tok):
		tokens.next()
		right = relationalExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def relationalExpr():
	tok = tokens.peek( )
	if debug == False: print ("relationalExpr: ", tok)
	left = addExpr( )
	tok = tokens.peek( )
	while re.match(Lexer.relational, tok):
		tokens.next()
		right = addExpr( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def addExpr( ):


	tok = tokens.peek( )
	if debug == False: print ("addExpr: ", tok)
	left = term( )
	tok = tokens.peek( )
	while tok == "+" or tok == "-":
		tokens.next()
		right = term( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left



def term( ):
	""" term    = factor { ('*' | '/') factor } """

	tok = tokens.peek( )
	if debug == False: print ("Term: ", tok)
	left = factor( )
	tok = tokens.peek( )
	while tok == "*" or tok == "/":
		tokens.next()
		right = factor( )
		left = BinaryExpr(tok, left, right)
		tok = tokens.peek( )
	return left


def factor( ):
	"""factor  = number | string | ident |  "(" expression ")" """

	tok = tokens.peek( )

	if debug == False: print ("Factor: ", tok)

	if re.match(Lexer.number, tok):
		expr = Number(tok)
		tokens.next( )
		return expr

	elif re.match(Lexer.string, tok):
		expr = String(tok)
		tokens.next()
		return expr

	elif re.match(Lexer.identifier, tok):
		expr = VarRef(tok)
		tokens.next()
		return expr

	if tok == "(":
		tokens.next( )  # or match( tok )
		expr = expression( )
		tokens.peek( )
		tok = match(")")
		return expr

	error("Invalid operand")
	return




	#=======================================Suppor Methods========================================#


def match(matchtok):
	tok = tokens.peek( )
	if (tok != matchtok): error("Expecting "+ matchtok)
	tokens.next( )
	return tok

def error( msg ):
	#print msg
	sys.exit(msg)





#======================================Main Function and File IO========================================#


def main():
	"""main program for testing"""
	global debug
	ct = 0
	for opt in sys.argv[1:]:
		if opt[0] != "-": break
		ct = ct + 1
		if opt == "-d": debug = True
	if len(sys.argv) < 2+ct:
		print ("Usage:  %s filename" % sys.argv[0])
		return
	parse("".join(mklines(sys.argv[1+ct])))
	return


def mklines(filename):
	"""Helper funciton to read in lines of given file in appropriate format."""
	inn = open(filename, "r")
	lines = [ ]
	pos = [0]
	ct = 0
	for line in inn:
		ct += 1
		line = line.rstrip( )+";"
		line = delComment(line)
		if len(line) == 0 or line == ";": continue
		indent = chkIndent(line)
		line = line.lstrip( )
		if indent > pos[-1]:
			pos.append(indent)
			line = '@' + line
		elif indent < pos[-1]:
			while indent < pos[-1]:
				del(pos[-1])
				line = '~' + line
		print (ct, "\t", line)
		lines.append(line)
	# print len(pos)
	undent = ""
	for i in pos[1:]:
		undent += "~"
	lines.append(undent)
	# print undent
	return lines


def chkIndent(line):
	ct = 0
	for ch in line:
		if ch != " ": return ct
		ct += 1
	return ct
		

def delComment(line):
	pos = line.find("#")
	if pos > -1:
		line = line[0:pos]
		line = line.rstrip()
	return line


main()
