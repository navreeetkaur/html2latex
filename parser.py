import ply.lex as lex
import ply.yacc as yacc
from anytree import Node, RenderTree
from node import *
from lexer import *

def p_doc(p):
	'''
	doc : start doc
		| end doc
		| sentence doc
		| selfclose doc
		| doctype doc
		| comment doc
		| END
	'''
	# print(p[1])
	try:
		p[0] = Node(type='doc', children=[p[1], p[2]])
	except:
		p[0] = Node(type='docend')


def p_start(p):
	'''
	start : START
	'''
	# print(p[1])
	t,attr = get_attributes_start_end(p[1])
	# print(t, attr)
	p[0] = Node(type='start', value=t.upper(), attr=attr)

def p_end(p):
	'''
	end : END
	'''
	# print(p[1])
	t,attr = get_attributes_start_end(p[1])
	p[0] = Node(type='start', value=t.upper())

def p_sentence(p):
	'''
	sentence : TEXT
	'''
	# print(p[1])
	# t,attr = get_attributes_start_end(p[1])
	p[0] = Node(type='sentence', text=p[1])	

def p_selfclose(p):
	'''
	selfclose : NOCLOSE
	'''
	# print(p[1])
	t,attr = get_attributes_start_end(p[1])
	p[0] = Node(type='selfclose', value=t.upper(), attr=attr)	


def p_doctype(p):
	'''
	doctype : DOCTYPE
	'''
	# print(p[1])
	# t,attr = get_attributes(p[1])
	p[0] = Node(type='doctype', text=p[1])

def p_comment(p):
	'''
	comment : COMMENT
	'''
	# print(p[1])
	# t,attr = get_attributes(p[1])
	p[0] = Node(type='comment', text=p[1])


def p_error(p):
   print ("|||||| Syntax error at ", p.value)


