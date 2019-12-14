from lexer import *
from parser import *
from utils import *
import sys
from anytree import Node, RenderTree
from node import Node

html_filename 	= sys.argv[1]
latex_filename 	= sys.argv[2]

# Building lexer
print("Doing Lexical Analysis. . .")
lex.lex()
with open(html_filename, 'r') as f:
    data = f.readlines()
    data = [d.lstrip().strip() for d in data]
    # print(data)
    data = ' '.join(data)
    lex.input(data)
data=lex
# Building Parser
print("Parsing. . .")
yacc.yacc()
root = parse(data)

print("Mapping HTML AST to LaTeX AST")
root.map2latex()
latex_file = open(latex_filename,'w')
root.writelex(latex_file)

# uncomment to print LaTeX AST
# for pre, fill, node in RenderTree(root):
#  	print(pre, node.value, node.attr, node.text)
