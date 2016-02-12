
import sys
import nltk
from nltk import word_tokenize
#TODO : if ';' - split in individual sentences

file_debug=open('debug_pos', 'w')
file_in=open('in.txt', 'r')
file_out=open('out.txt', 'w')

file_desambi_prep=open('desambi_prep.txt','r')
file_ambi_noun_verb=open('ambi_noun_verb.txt', 'r')#man, mans
file_ambi_noun_adj=open('ambi_noun_adj.txt', 'r')#orange

##################################disc->memory#############################################
dict_desambi={}
for line in file_desambi_prep:
	if line[0:1] != '*':
		pair=line.split(':')[0]
		value=line.split(':')[1].strip()
		(noun, preposition)=pair.split(',')
		dict_desambi[(noun,preposition)]=value
#print(dict_desambi)
#dict_desambi = {('bars', 'into'): '1', ('bar', 'at'): '2', ('bars', 'in'): '2', ('bar', 'into'): '1', ('bars', 'at'): '2', ('bar', 'in'): '2'}
	
list_ambi_noun_verb=[]
for line in file_ambi_noun_verb:
	list_ambi_noun_verb.append(line.strip())
	
list_ambi_noun_adj=[]
for line in file_ambi_noun_adj:
	list_ambi_noun_adj.append(line.strip())
##################################end of disc->memory#############################################
	
def isambi_lex(s):
	return (s in [first for (first,second)in dict_desambi.keys()])
	
def isambi_noun_verb(s):
	return (s in list_ambi_noun_verb)
	
def isambi_noun_adj(s):
	return (s in list_ambi_noun_adj)
	
def myisalpha(s):
	return s.isalpha() | s.replace('-','a').isalpha() #myisalpha('Ann-Marie')==True, 'Ann-Marie'.isalpha()==False

#tokens_in=''#global variable used to stock our sentence as a list of tokens
#ind_adj_dt_cc=[] #global variable for indexes of omitted adjectives etc; is used to restitute the omitted adj


###########################################FUNCTIONS####################################################

def simplification_pos(pos_pairs_punct):
	
	pos_pairs_punct_simplified=pos_pairs_punct
	for ind, (w,pos) in enumerate(pos_pairs_punct):
		if (pos=='NN') | (pos=='PRP') | (pos=='NNP') | (pos=='NNS'):
			pos_pairs_punct_simplified[ind]=(w,'NN')
		elif pos[0:2]=='VB':
			pos_pairs_punct_simplified[ind]=(w,'VB')
		elif pos=='PRP$':
			pos_pairs_punct_simplified[ind]=(w,'JJ')
	return pos_pairs_punct_simplified

def desambi_noun_adj(pos_pairs_punct_simplified):
	result=pos_pairs_punct_simplified
	
	def isprobably_false_noun(w,pos):
			return isambi_noun_adj(w) & (pos=='NN')
	
	
	pos_pairs_simplified=[p for p in pos_pairs_punct_simplified if myisalpha(p[0])]
	newpos=[pos for (w,pos) in pos_pairs_punct_simplified if myisalpha(w)]
	
	ind_in_punctuated={}#index of a WORD-pair from pos_pairs_simplified in pos_pairs_punct_simplified
	#for 'Boy, girl,man man boat.' ind_in_punctuated[0]=0,ind_in_punctuated[1]=2,ind_in_punctuated[2]=4,ind_in_punctuated[3]=5,ind_in_punctuated[4]=6
	
	indices_words=[]#values of the dictionary ind_in_punctuated; [0,2,4,5,6] in the previous example
		
	counter=0
	for i in range(len(pos_pairs_punct_simplified)):
		if myisalpha(pos_pairs_punct_simplified[i][0]):
			indices_words.append(i)
			ind_in_punctuated[counter]=i
			counter+=1
	
	for i in range(len(pos_pairs_simplified)):
		current_pos=pos_pairs_simplified[i][1]
		
		if i>0:
			previous_pos=pos_pairs_simplified[i-1][1]
			
		if i<len(pos_pairs_simplified)-1:
			next_pos=pos_pairs_simplified[i+1][1]
			
		if i<len(pos_pairs_simplified)-2:
			next_next_pos=pos_pairs_simplified[i+2][1]

		
		current_word=pos_pairs_simplified[i][0]
		
		if (isprobably_false_noun(current_word,current_pos)):
			if ((i<len(pos_pairs_simplified)-1) & ((next_pos=='NN')|(next_pos=='JJ'))|((i<len(pos_pairs_simplified)-2) & (next_pos=='CC') &  (next_next_pos=='JJ')) ) :
			#orange ball, big and orange ball
				newpos[i]='JJ'
			elif (i>0) & (i<len(pos_pairs_simplified)-1) & (previous_pos=='VB') & ((next_pos=='NN')|(next_pos=='JJ')):#knitted orange ball;the absence of article 
			#indicates that current is more probably an adjective than a noun
				newpos[i]='JJ'
	
	#at this moment result coinsides with pos_pairs_punct_simplified. We changed every pos in result by the corresponding pos of newpos
	#TODO : change only changed pos
	counter=0	
	for i in range(len(pos_pairs_punct_simplified)):
		if i in indices_words:
			
			result[i]=(pos_pairs_punct_simplified[ind_in_punctuated[counter]][0],newpos[counter])
			counter+=1
			
	global tokens_in #a global variable;is used to stock our sentence	as a list of tokens
	tokens_in=''
	global ind_adj_dt_cc   #a global variable for indices of omitted adjectives etc;is used to restitute the omitted adj
	ind_adj_dt_cc=[]		
	return result
	
def desambi_noun_transiverb(pos_pairs_punct_simplified): 
	result=pos_pairs_punct_simplified
	
	if len(pos_pairs_punct_simplified)>1:
		for i in range(1,len(pos_pairs_punct_simplified))[::-1]:#backwards, for the sake of "… man man boat"
			previous_pos=pos_pairs_punct_simplified[i-1][1]
			current_pos=pos_pairs_punct_simplified[i][1]
			
			if (isambi_noun_verb(pos_pairs_punct_simplified[i-1][0])) & (previous_pos=='NN' ) & ((current_pos=='NN') | (current_pos=='DT')) :
				if (i<=1) | ((i>1) & (pos_pairs_punct_simplified[i-2][1] != ',')):
					result[i-1]=(result[i-1][0],'VBZ')
	
	return result
	
def omit_adj_dt_cc(pos_pairs_simplified):
	simplified=pos_pairs_simplified
	result=[]
	for ind, (w,pos) in enumerate(pos_pairs_simplified):
		if (pos=='JJ')| (pos=='DT') | (pos=='CC') :
			ind_adj_dt_cc.append(ind)
		else:
			result.append((w,pos))
	return result
	

def treatment(sentence):

	def insert_in_first_empty(elt,l):
		for i in range(len(l)):
			if l[i]=='':
				l[i]=elt
				break
				
	
	###########################################FORETREATMENT####################################################	
				
	tokens=word_tokenize(sentence)
	
	file_debug.write(str(tokens))
	file_debug.write('\n')
			 
	long=nltk.pos_tag(tokens)
	long=simplification_pos(long)
	long=desambi_noun_adj(long)
	long=desambi_noun_transiverb(long)
	long=desambi_noun_adj(long)
	
	
	short=[]
	
	ind_adj_dt_cc=[]
	for ind, (w,pos) in enumerate(long):
		if (pos=='JJ')| (pos=='DT') | (pos=='CC') :
			ind_adj_dt_cc.append(ind)
		else:
			short.append((w,pos))
	
	###########################################TREATMENT####################################################
	result=['']*len(tokens)#list of empty strings
	
	
	grammar = """
	PP: { <IN> (<NN><,>)* <NN>} # PP=prepositional phrase
	"""
	parser=nltk.RegexpParser(grammar)
	tree=parser.parse(short)
		
	for st in tree.subtrees(filter=lambda x: x.label() == 'PP'):
		preposition=st[0][0]
		for i in range(1,len(st)):
			word=st[i][0]
			if isambi_lex(word):
				st[i]=(word+dict_desambi[word,preposition],'NN')#st[i][0]=word+dict_desambi[word,preposition] is impossible : tuple is not mutable
	
	tokens_short=[w for (w,pos) in tree.leaves()]
	
	#Restitution of articles, conjunctions, adjectives
	#print(ind_adj_dt_cc)
	for i in range(len(ind_adj_dt_cc)):
		result[ind_adj_dt_cc[i]]=tokens[ind_adj_dt_cc[i]]
	
	for i in range(len(tokens_short)):
		#print(result)
		insert_in_first_empty(tokens_short[i],result)
	
	return ' '.join(result)
	
for sentence in file_in:	
	file_out.write(treatment(sentence))
	file_out.write('\n')
	
sys.exit(0)
	
#print(traitement(pretraitement('Before you bite into a chocolate bar or take a sip of hot cocoa, consider, where did it come from?')))
