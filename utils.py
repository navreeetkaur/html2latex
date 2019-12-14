import html2latexmapping
import codecs
from node import Node

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

# helper function for traversing the parsed AST
def parse(lex):
    for token in iter(lex.token, None):
        t = token.type
        v = token.value
        tag, attr = get_attributes_start_end(v)
        # print('--------------'+tag+'--------------')
        if t=='DOCTYPE' or t=='COMMENT':
            continue

        elif t=='START':
            # tag_stack.append(tag.upper())
            if tag=='html':
                root = Node(type='start', value=tag.upper(), attr=attr)
                # print('Adding HTMl root')
                # print("ROOT: ", root.value)
                curr_node = root
            else:
                new_node = Node(type='start', parent=curr_node, value=tag.upper(), attr=attr, children=[])
                curr_node.children.append(new_node)
                # print("START new_node: ", new_node.value, new_node.parent.value)
                # print("Making",new_node.value,"the child of",curr_node.value,"current node is new node")
                curr_node = new_node

            
        elif t=='NOCLOSE':
            new_node = Node(type='noclose', parent=curr_node, value=tag.upper(), attr=attr, children=[])
            curr_node.children.append(new_node)
            # print("Making",new_node.value,"the child of",curr_node.value,"Current node remains the same.")
            # print("NOCLOSE new_node: ", new_node.value, new_node.parent.value)

        elif t=='END':
            if tag!='html':
                curr_node = curr_node.parent
                # print("Current node is", curr_node.value, "which was the parent of previous current node")
                # print("END new_node: ", curr_node.value)

        elif t=='TEXT': 
            # curr_node.text = v
            new_node = Node(type='text', parent=curr_node, value=v, attr=[], children=[])
            curr_node.children.append(new_node)
            # print("attaching text to", curr_node.value)
            # print("TEXT: ", curr_node.value, curr_node.text, curr_node.parent.value)

    return root
