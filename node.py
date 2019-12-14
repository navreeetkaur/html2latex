from anytree import Node, RenderTree
import html2latexmapping
import codecs

class Node:
    def __init__(self, type, value ,parent=None,children=[],attr=[],text=''):
        self.type = type
        self.children = children
        self.value = value
        self.text = text
        self.attr = attr
        self.parent = parent

    def print_children(self):
    	print("\nPrinting children of",self.value," : " )
    	for child in self.children:
    		print(child.value)

    def print_parent(self):
    	print("\nParent:", parent.value)

    # Mapping HTML AST to LaTeX ASt
    def map2latex(self):
    	if self.type=='start':
    		self.value = html2latexmapping.start_map[self.value]
    	elif self.type=='noclose':
    		self.value = html2latexmapping.noclose_map[self.value]

    	if self.children!=[]:
    		for i in range(len(self.children)):
    			self.children[i].map2latex()

    # write LaTeX AST to file
    def writelex(self, file):
    	if self.type=='start':
    		# HTML
    		if self.value=='\\documentclass':
    			file.write('\\documentclass{article}\n')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\n')
    		# HEAD
    		if self.value=='\\usepackage':
    			file.write('\\usepackage{times}\n\\usepackage{tabularx}\n\\usepackage{titlesec}\n\\setcounter{secnumdepth}{4}\n\\titleclass{\\subsubsubsection}{straight}[\\subsection]\n\\usepackage{url}\n\\usepackage{latexsym}\n\\usepackage{graphicx}\n\\usepackage{enumitem}\n\\usepackage{hyperref}\n')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\n')
    		# TITLE
    		if self.value=='\\title':
    			file.write('\\title{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# BODY
    		if self.value=='\\begin{document}':
    			file.write('\\begin{document}\n\\maketitle\n')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\\end{document}\n')
    		# H1
    		if self.value=='\\section':
    			file.write('\\section*{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# H2 or DIV
    		if self.value=='\\subsection':
    			file.write('\\subsection*{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# H3
    		if self.value=='\\subsubsection':
    			file.write('\\subsubsection*{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# H4
    		if self.value=='\\paragraph':
    			file.write('\\textbf{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# P
    		if self.value=='\\par':
    			file.write('\\par ')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\\\\\n')
    		# B or STRONG
    		if self.value=='\\textbf':
    			file.write('\\textbf{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# I
    		if self.value=='\\textit':
    			file.write('\\textit{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# U
    		if self.value=='\\underline':
    			file.write('\\underline{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# TT
    		if self.value=='\\texttt':
    			file.write('\\texttt{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# A
    		if self.value=='\\href':
    			for a in self.attr:
    				if a[0]=='href':
    					file.write('\\href{'+a[1][1:-1]+'}')
    			if self.children!=[]:
    				file.write('{')
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    				file.write('} ')


    		# OL
    		if self.value=='\\begin{enumerate}':
    			file.write('\\begin{enumerate}\n')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\n\\end{enumerate}\n')
    		# UL
    		if self.value=='\\begin{itemize}':
    			file.write('\\begin{itemize}\n')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\\end{itemize}\n')
    		# DL
    		if self.value=='\\begin{itemize}[label={}]':
    			file.write('\\begin{itemize}[label={}]\n')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\n\\end{itemize}\n')
    		# TABLE
    		if self.value=='\\begin{tabular}':
    			file.write('\\begin{tabular}')
    			border = False
    			for a in self.attr:
    				if a[0]=='border':
    					if int(a[1][1:-1])>0:
    						border=True
    						file.write('{|c|c|c|c|c|c|c|c|c|c|c|c|}\n')
    					else:
    						file.write('{cccccccccccc}\n')

    			if self.children!=[]:
    				for i in range(len(self.children)):
    					if border:
    						file.write('\\hline\n')
    					self.children[i].writelex(file)
    			if border:
    				file.write('\\hline\n')
    			file.write('\\end{tabular}\n')
    		# SUP
    		if self.value=='\\textsuperscript':
    			file.write('\\textsuperscript{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}')
    		# SUB
    		if self.value=='\\textsubscript':
    			file.write('\\textsubscript{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}')
    		# SMALL
    		if self.value=='\\tiny':
    			file.write('{\\tiny')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# CENTER
    		if self.value=='\\begin{center}':
    			file.write('\\begin{center}{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\\end{center}\n')
    		# EMPs
    		if self.value=='\\emph':
    			file.write('\\emph{')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')
    		# DT or LI 
    		if self.value=='\\item':
    			file.write('\\item ')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\n')
    		# DD
    		if self.value=='\\subitem':
    			file.write('\\subitem ')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\n')
    		# TD
    		if self.value=='&':
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write(' & ')
    		# TR
    		if self.value=='\\\\':
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('\\\\\n')
    		# FONT
    		if self.value=='\\fontsize':
    			for a in self.attr:
    				if a[0]=='size':
    					file.write('{\\fontsize{'+a[1][1:-1]+'mm}{'+a[1][1:-1]+'mm} \\selectfont ')
    			if self.children!=[]:
    				for i in range(len(self.children)):
    					self.children[i].writelex(file)
    			file.write('}\n')

    	elif self.type=='text':
    		# if '&alpha' in self.value:
    		# 	from IPython import embed; embed()
    		file.write(process_text_for_latex(self.value))

    	elif self.type=='noclose':
    		# BR
    		if self.value=='\\newline':
    			file.write('\n\\newline\n')
    		# IMG
    		if self.value=='\\figure':
    			file.write('\\begin{figure}[h]\n\\includegraphics[')
    			for a in self.attr:
    				if a[0]=='width':
    					width = a[1][1:-1]
    					file.write('width='+width+'cm')
    				if a[0]=='height':
    					height = int(a[1][1:-1])
    					file.write(', height='+height+'cm')
    				if a[0]=='src':
    					source = a[1]
    					file.write(']{'+source+'}\n')
    				if a[0]=='figcaption':
    					caption = a[1]
    					file.write('\\caption{'+caption+'}\n')
    			file.write('\\end{figure}')

# get attributes of tokens returned by lexer
def get_attributes(token):
    if token.type=='COMMENT':
        vals = token.value.replace('<!--', '').replace('-->', '')
    else:
        vals = token.value.replace('/>','').replace("</",'').replace(">",'').replace("<",'')
    tag = vals
    attrs = []
    if token.type=='START' or token.type=='NOCLOSE':
        vals = vals.split(" ")
        tag = vals[0]
        if len(vals)>1:
            vals = [v.replace(" ","").split("=") for v in vals]
            vals = [v for v in vals if len(v)>0 and v[0]!=''] 
            if len(vals)>1:
                attrs = vals[1:]
    return tag, attrs

# get attributes of start and end tags which are form of string
def get_attributes_start_end(text):
	vals = text.replace('/>','').replace("</",'').replace(">",'').replace("<",'')
	tag = vals
	attrs = []
	vals = vals.split(" ")
	tag = vals[0]
	if len(vals)>1:
	    vals = [v.replace(" ","").split("=") for v in vals]
	    vals = [v for v in vals if len(v)>0 and v[0]!=''] 
	    if len(vals)>1:
	        attrs = vals[1:]
	return tag, attrs

# convert text from html to latex format eg: &alpha -> \alpha, ^ -> \^{}
def process_text_for_latex(text):
	for key,value in html2latexmapping.text_map.items():
		text = text.replace(key,value)
	# codecs.decode(text, 'unicode_escape')
	text = bytes(text, 'utf-8').decode("unicode_escape")
	return text

