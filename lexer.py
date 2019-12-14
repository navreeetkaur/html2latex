import ply.lex as lex
import ply.yacc as yacc

# List of token names.
tokens = ['START','END','COMMENT', 'DOCTYPE', 'NOCLOSE', 'TEXT']

# Regular expression rules for simple tokens
t_START = r'<[^\/!][^<>!]*>'
# t_START = r'<[^<>!]*[^\/]>'
t_END = r'<\/[^!<>]+>'
t_COMMENT = r'<!--[^--]+-->'
t_DOCTYPE = r'<!DOCTYPE[^>]+>'
t_NOCLOSE =  r'<[^!\/][^<>]*\/>'
t_TEXT = r'[^\<\>\n\t]+'
t_ignore = ' '

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))