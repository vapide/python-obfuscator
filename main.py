import errno
import pathlib
import math
import os
import py_compile
import shutil
import random

UNICODEDICT=dict(zip([chr(i) for i in range(1114111)],["{0:#0{1}x}".format(i, 8) for i in range(1114111)],))

UNICODEDICTREV=dict((v, k) for k, v in UNICODEDICT.items())

def stringtounicode(string):
	unicodestring = '/'
	for character in string:
		unicodestring += UNICODEDICT[character] + '/'
	return unicodestring

def unicodetostring(unicodestr):
	newstring = ''
	unicodestr = unicodestr.split("/")
	unicodestr = " ".join(unicodestr).split()
	for character in unicodestr:
		newstring += UNICODEDICTREV[character]
	return newstring

def splitdict(dictionary):
    split = []
    for key in dictionary:
        split.append((key, dictionary[key]))
    split.sort(key=lambda x: x[1])
    split.reverse()
    return split

def frequencycount(string):
	return {i: string.count(i) for i in set(string)}

def hexlimit(frequencies):
	return math.ceil(math.log(len(frequencies), 16))

def encodelist(split, hexlim):
    newdict = {}
    for i in range(len(split)):
        newdict[split[i][0]] = "{0:#0{1}x}".format(i, hexlim + 2) + "/"
    return newdict

def strtr(string, replace):
    if replace and string:
        s, r = replace.popitem()
        return r.join(strtr(subs, dict(replace)) for subs in string.split(s))
    return string

def compress(string):
    return strtr(string, encodelist(splitdict(frequencycount(string)), hexlimit(frequencycount(string)))), encodelist(splitdict(frequencycount(string)), hexlimit(frequencycount(string)))

def decompress(string, keys=""):
    if isinstance(string, tuple):
        keys = string[1]
        string = string[0]
    replace = dict((v, k) for k, v in keys.items())
    return strtr(string, replace)

def encrypt(code):
    oldcode = code
    newcode = compress(stringtounicode(code))[0]
    key = compress(stringtounicode(code))[1]
    return oldcode, newcode, key

def decrypt(code, key):
    return unicodetostring(decompress(code, key))

def readfile(path):
	with open(path, 'r') as file:
		return file.read()

def variablescramble(varlength, varcount, varprefix = 'ghost'):
	letters = ['1','I','i','l']
	varnames = []
	templst = []
	tempstr = ''
	for i in range(varcount):
		[templst.append(letters[random.randint(0,len(letters)-1)]) for x in range(varlength)]
		tempstr = str(varprefix) + '_'
		for x in templst: tempstr+=x
		varnames.append(tempstr)
		tempstr = ''
		templst = []
		random.seed()
	return varnames

def obfuscatecode(code):
	oldcode = code
	encryptedcode = encrypt(code)
	buffer = 'O=dict;r=zip;t=chr;T=\'raise\';U=\'Exception\';s=range;n=set;w=len;X=isinstance;n=eval;F=\'*args\';g=tuple;W=[\'0x000070\',\'0x000072\',\'0x000069\',\'0x00006e\',\'0x000074\'];import math,pathlib,os,ast,sys;H=math.log;u=math.ceil;P=ast.literal_eval;L=[None,False,__name__,exec,True,int(0),2,3,\'hi\',\'exec\'];J=O(r([t(i)for i in s(1114111)],[\"{0:#0{1}x}\".format(i,8)for i in s(1114111)],));q=O((v,k)for k,v in J.items());z=[\'0x000065\',\'0x000078\',\'0x000065\',\'0x000063\'];V=T+q[\'0x000020\']+U;\ndef Z(l,L):\n for k in n(L):l+=q[k];\n return l\ndef C(f):\n bc=\"/\"\n for F in f:bc+=J[F]+\"/\";\n return bc\ndef l(bc):\n f=\"\";bc=bc.split(\"/\");bc=\" \".join(bc).split();\n for v in bc:f+=q[v];\n return f\ndef N(dictionary):\n G=[]\n for U in dictionary:G.append((U,dictionary[U]));\n G.sort(key=lambda x:x[1]);G.reverse();return G\ndef j(f):\n return{i:f.count(i)for i in n(f)}\ndef E(frequencies):\n return u(H(w(frequencies),16))\ndef B(G,hexlim):\n p={}\n for i in s(w(G)):p[G[i][0]]=\"{0:#0{1}x}\".format(i,hexlim+2)+\"/\";\n return p\ndef y(f,W):\n if W and f:s,r=W.popitem();return r.join(y(subs,O(W))for subs in f.split(s));\n return f\ndef D(f):\n return y(f,B(N(j(f)),E(j(f)))),B(N(j(f)),E(j(f)))\ndef c(f,keys=\"\"):\n if X(f,g):keys=f[1];f=f[0];\n W=O((v,k)for k,v in keys.items());return y(f,W)\ndef T(code):\n I=code;A=D(C(code))[1];Y=D(C(code))[0];import random as e;letters=[\'1\', \'i\', \'I\', \'l\'];e.seed();gugu=[];fnr=\'\';length=9;[gugu.append(letters[e.randint(0,len(letters)-1)]) for xxz in range(length)];return I,A,Y\ndef M(code,A):\n return l(c(code,A))\n#n(Z(\'\',\'z\'))(Z(\'\',\'W\') + \'=\' + V)\n#n(Z(\'\',\'z\'))(\'def \'+Z(\'\',\'W\')+\'(\'+F+\'): \'+V+\'(\"\'+n(\'t(110)+t(111)+t(112)+t(101)+t(33)+t(34)+t(41)+t(59)\'))\n#for zzx in gugu: fnr+=zzx\n'
	newcode = buffer + "n(Z('','z'))(M('" + encryptedcode[1] + "',P(l(\'" + stringtounicode(str(encryptedcode[2])) + '\'))))'
	return newcode

def obfuscate(name, code, compile = False, clearvars = False, outputname = None):
	if outputname == None:
		outputname = name + '.py'
	#code = code.replace('print', 'sys.stdout.write')
	if clearvars == True:
		code += '\nsys.modules[__name__].__dict__.clear()' # removes the variables from locals() globals() and vars()
	code = obfuscatecode(code)
	filepath = str(pathlib.Path(str(pathlib.Path(__file__).parent)+'/temp/'+outputname)) # path to the obfuscated file (before compiling)
	outputpath = str(pathlib.Path(str(pathlib.Path(__file__).parent)+'/output/'+outputname)) # path to the final obfuscated file (after compiling)
	if compile == True:
		if not os.path.exists(os.path.dirname(filepath)):
			try:
				os.makedirs(os.path.dirname(filepath))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		with open(filepath,'w') as f:
			f.write(code)
		py_compile.compile(filepath, cfile = outputpath)
		shutil.rmtree(str(pathlib.Path(str(pathlib.Path(__file__).parent)+'/temp/')))
		print('Obfuscated file path: ' + outputpath)
	else:
		if not os.path.exists(os.path.dirname(outputpath)):
			try:
				os.makedirs(os.path.dirname(outputpath))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		with open(outputpath, "w") as f:
			f.write(code)
		print('Obfuscated file path: ' + outputpath)
	return outputpath

def obfuscatefile(path):
	obfuscate(os.path.basename(path), readfile(path), compile = True, clearvars = True, outputname = os.path.basename(path))

os.system('')
ghost = '\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m \x1b[0m\x1b[38;2;255;210;0m \x1b[0m\x1b[38;2;255;206;0m \x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m \x1b[0m\x1b[38;2;255;186;0m \x1b[0m\x1b[38;2;255;182;0m \x1b[0m\x1b[38;2;255;178;0m \x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m \x1b[0m\x1b[38;2;255;126;0m \x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m \x1b[0m\x1b[38;2;255;106;0m \x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m \x1b[0m\x1b[38;2;255;78;0m \x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m \x1b[0m\x1b[38;2;255;58;0m \x1b[0m\x1b[38;2;255;54;0m \x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m \x1b[0m\x1b[38;2;255;34;0m \x1b[0m\x1b[38;2;255;30;0m \x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m \x1b[0m\x1b[38;2;255;6;0m \x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m \x1b[0m\x1b[38;2;255;210;0m \x1b[0m\x1b[38;2;255;206;0m \x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m \x1b[0m\x1b[38;2;255;186;0m \x1b[0m\x1b[38;2;255;182;0m \x1b[0m\x1b[38;2;255;178;0m \x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m \x1b[0m\x1b[38;2;255;126;0m \x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m \x1b[0m\x1b[38;2;255;106;0m \x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m \x1b[0m\x1b[38;2;255;78;0m \x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m \x1b[0m\x1b[38;2;255;58;0m \x1b[0m\x1b[38;2;255;54;0m \x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m \x1b[0m\x1b[38;2;255;34;0m \x1b[0m\x1b[38;2;255;30;0m \x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m,\x1b[0m\x1b[38;2;255;6;0md\x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m \x1b[0m\x1b[38;2;255;210;0m \x1b[0m\x1b[38;2;255;206;0m \x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m \x1b[0m\x1b[38;2;255;186;0m \x1b[0m\x1b[38;2;255;182;0m \x1b[0m\x1b[38;2;255;178;0m \x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m \x1b[0m\x1b[38;2;255;126;0m \x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m \x1b[0m\x1b[38;2;255;106;0m \x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m \x1b[0m\x1b[38;2;255;78;0m \x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m \x1b[0m\x1b[38;2;255;58;0m \x1b[0m\x1b[38;2;255;54;0m \x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m \x1b[0m\x1b[38;2;255;34;0m \x1b[0m\x1b[38;2;255;30;0m \x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m8\x1b[0m\x1b[38;2;255;6;0m8\x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m,\x1b[0m\x1b[38;2;255;210;0ma\x1b[0m\x1b[38;2;255;206;0md\x1b[0m\x1b[38;2;255;202;0mP\x1b[0m\x1b[38;2;255;198;0mP\x1b[0m\x1b[38;2;255;194;0mY\x1b[0m\x1b[38;2;255;190;0mb\x1b[0m\x1b[38;2;255;186;0m,\x1b[0m\x1b[38;2;255;182;0md\x1b[0m\x1b[38;2;255;178;0m8\x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m,\x1b[0m\x1b[38;2;255;154;0md\x1b[0m\x1b[38;2;255;150;0mP\x1b[0m\x1b[38;2;255;146;0mP\x1b[0m\x1b[38;2;255;142;0mY\x1b[0m\x1b[38;2;255;138;0mb\x1b[0m\x1b[38;2;255;134;0ma\x1b[0m\x1b[38;2;255;130;0m,\x1b[0m\x1b[38;2;255;126;0m \x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m,\x1b[0m\x1b[38;2;255;106;0ma\x1b[0m\x1b[38;2;255;102;0md\x1b[0m\x1b[38;2;255;98;0mP\x1b[0m\x1b[38;2;255;94;0mP\x1b[0m\x1b[38;2;255;90;0mY\x1b[0m\x1b[38;2;255;86;0mb\x1b[0m\x1b[38;2;255;82;0ma\x1b[0m\x1b[38;2;255;78;0m,\x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m,\x1b[0m\x1b[38;2;255;58;0ma\x1b[0m\x1b[38;2;255;54;0md\x1b[0m\x1b[38;2;255;50;0mP\x1b[0m\x1b[38;2;255;46;0mP\x1b[0m\x1b[38;2;255;42;0mY\x1b[0m\x1b[38;2;255;38;0mb\x1b[0m\x1b[38;2;255;34;0ma\x1b[0m\x1b[38;2;255;30;0m,\x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0mM\x1b[0m\x1b[38;2;255;14;0mM\x1b[0m\x1b[38;2;255;10;0m8\x1b[0m\x1b[38;2;255;6;0m8\x1b[0m\x1b[38;2;255;2;0mM\x1b[0m\x1b[38;2;255;0;0mM\x1b[0m\x1b[38;2;255;0;0mM\x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0ma\x1b[0m\x1b[38;2;255;214;0m8\x1b[0m\x1b[38;2;255;210;0m"\x1b[0m\x1b[38;2;255;206;0m \x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m`\x1b[0m\x1b[38;2;255;186;0mY\x1b[0m\x1b[38;2;255;182;0m8\x1b[0m\x1b[38;2;255;178;0m8\x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0mP\x1b[0m\x1b[38;2;255;154;0m\'\x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m"\x1b[0m\x1b[38;2;255;130;0m8\x1b[0m\x1b[38;2;255;126;0ma\x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0ma\x1b[0m\x1b[38;2;255;110;0m8\x1b[0m\x1b[38;2;255;106;0m"\x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m"\x1b[0m\x1b[38;2;255;78;0m8\x1b[0m\x1b[38;2;255;74;0ma\x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0mI\x1b[0m\x1b[38;2;255;58;0m8\x1b[0m\x1b[38;2;255;54;0m[\x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m \x1b[0m\x1b[38;2;255;34;0m"\x1b[0m\x1b[38;2;255;30;0m"\x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m8\x1b[0m\x1b[38;2;255;6;0m8\x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m8\x1b[0m\x1b[38;2;255;214;0mb\x1b[0m\x1b[38;2;255;210;0m \x1b[0m\x1b[38;2;255;206;0m \x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m \x1b[0m\x1b[38;2;255;186;0m \x1b[0m\x1b[38;2;255;182;0m8\x1b[0m\x1b[38;2;255;178;0m8\x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m8\x1b[0m\x1b[38;2;255;126;0m8\x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m8\x1b[0m\x1b[38;2;255;110;0mb\x1b[0m\x1b[38;2;255;106;0m \x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m \x1b[0m\x1b[38;2;255;78;0md\x1b[0m\x1b[38;2;255;74;0m8\x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m \x1b[0m\x1b[38;2;255;58;0m`\x1b[0m\x1b[38;2;255;54;0m"\x1b[0m\x1b[38;2;255;50;0mY\x1b[0m\x1b[38;2;255;46;0m8\x1b[0m\x1b[38;2;255;42;0mb\x1b[0m\x1b[38;2;255;38;0ma\x1b[0m\x1b[38;2;255;34;0m,\x1b[0m\x1b[38;2;255;30;0m \x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m8\x1b[0m\x1b[38;2;255;6;0m8\x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m"\x1b[0m\x1b[38;2;255;214;0m8\x1b[0m\x1b[38;2;255;210;0ma\x1b[0m\x1b[38;2;255;206;0m,\x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m,\x1b[0m\x1b[38;2;255;186;0md\x1b[0m\x1b[38;2;255;182;0m8\x1b[0m\x1b[38;2;255;178;0m8\x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m8\x1b[0m\x1b[38;2;255;126;0m8\x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m"\x1b[0m\x1b[38;2;255;110;0m8\x1b[0m\x1b[38;2;255;106;0ma\x1b[0m\x1b[38;2;255;102;0m,\x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m,\x1b[0m\x1b[38;2;255;82;0ma\x1b[0m\x1b[38;2;255;78;0m8\x1b[0m\x1b[38;2;255;74;0m"\x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0ma\x1b[0m\x1b[38;2;255;58;0ma\x1b[0m\x1b[38;2;255;54;0m \x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m]\x1b[0m\x1b[38;2;255;34;0m8\x1b[0m\x1b[38;2;255;30;0mI\x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m8\x1b[0m\x1b[38;2;255;6;0m8\x1b[0m\x1b[38;2;255;2;0m,\x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m`\x1b[0m\x1b[38;2;255;210;0m"\x1b[0m\x1b[38;2;255;206;0mY\x1b[0m\x1b[38;2;255;202;0mb\x1b[0m\x1b[38;2;255;198;0mb\x1b[0m\x1b[38;2;255;194;0md\x1b[0m\x1b[38;2;255;190;0mP\x1b[0m\x1b[38;2;255;186;0m"\x1b[0m\x1b[38;2;255;182;0mY\x1b[0m\x1b[38;2;255;178;0m8\x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m8\x1b[0m\x1b[38;2;255;162;0m8\x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m8\x1b[0m\x1b[38;2;255;126;0m8\x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m`\x1b[0m\x1b[38;2;255;106;0m"\x1b[0m\x1b[38;2;255;102;0mY\x1b[0m\x1b[38;2;255;98;0mb\x1b[0m\x1b[38;2;255;94;0mb\x1b[0m\x1b[38;2;255;90;0md\x1b[0m\x1b[38;2;255;86;0mP\x1b[0m\x1b[38;2;255;82;0m"\x1b[0m\x1b[38;2;255;78;0m\'\x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m`\x1b[0m\x1b[38;2;255;58;0m"\x1b[0m\x1b[38;2;255;54;0mY\x1b[0m\x1b[38;2;255;50;0mb\x1b[0m\x1b[38;2;255;46;0mb\x1b[0m\x1b[38;2;255;42;0md\x1b[0m\x1b[38;2;255;38;0mP\x1b[0m\x1b[38;2;255;34;0m"\x1b[0m\x1b[38;2;255;30;0m\'\x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m"\x1b[0m\x1b[38;2;255;6;0mY\x1b[0m\x1b[38;2;255;2;0m8\x1b[0m\x1b[38;2;255;0;0m8\x1b[0m\x1b[38;2;255;0;0m8\x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0ma\x1b[0m\x1b[38;2;255;210;0ma\x1b[0m\x1b[38;2;255;206;0m,\x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0m \x1b[0m\x1b[38;2;255;194;0m \x1b[0m\x1b[38;2;255;190;0m \x1b[0m\x1b[38;2;255;186;0m,\x1b[0m\x1b[38;2;255;182;0m8\x1b[0m\x1b[38;2;255;178;0m8\x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m \x1b[0m\x1b[38;2;255;162;0m \x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m \x1b[0m\x1b[38;2;255;126;0m \x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m \x1b[0m\x1b[38;2;255;106;0m \x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m \x1b[0m\x1b[38;2;255;78;0m \x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m \x1b[0m\x1b[38;2;255;58;0m \x1b[0m\x1b[38;2;255;54;0m \x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m \x1b[0m\x1b[38;2;255;34;0m \x1b[0m\x1b[38;2;255;30;0m \x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m \x1b[0m\x1b[38;2;255;6;0m \x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m \x1b[0m\x1b[38;2;255;210;0m"\x1b[0m\x1b[38;2;255;206;0mY\x1b[0m\x1b[38;2;255;202;0m8\x1b[0m\x1b[38;2;255;198;0mb\x1b[0m\x1b[38;2;255;194;0mb\x1b[0m\x1b[38;2;255;190;0md\x1b[0m\x1b[38;2;255;186;0mP\x1b[0m\x1b[38;2;255;182;0m"\x1b[0m\x1b[38;2;255;178;0m \x1b[0m\x1b[38;2;255;174;0m \x1b[0m\x1b[38;2;255;170;0m \x1b[0m\x1b[38;2;255;166;0m \x1b[0m\x1b[38;2;255;162;0m \x1b[0m\x1b[38;2;255;158;0m \x1b[0m\x1b[38;2;255;154;0m \x1b[0m\x1b[38;2;255;150;0m \x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0m \x1b[0m\x1b[38;2;255;138;0m \x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0m \x1b[0m\x1b[38;2;255;126;0m \x1b[0m\x1b[38;2;255;122;0m \x1b[0m\x1b[38;2;255;118;0m \x1b[0m\x1b[38;2;255;114;0m \x1b[0m\x1b[38;2;255;110;0m \x1b[0m\x1b[38;2;255;106;0m \x1b[0m\x1b[38;2;255;102;0m \x1b[0m\x1b[38;2;255;98;0m \x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0m \x1b[0m\x1b[38;2;255;86;0m \x1b[0m\x1b[38;2;255;82;0m \x1b[0m\x1b[38;2;255;78;0m \x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0m \x1b[0m\x1b[38;2;255;66;0m \x1b[0m\x1b[38;2;255;62;0m \x1b[0m\x1b[38;2;255;58;0m \x1b[0m\x1b[38;2;255;54;0m \x1b[0m\x1b[38;2;255;50;0m \x1b[0m\x1b[38;2;255;46;0m \x1b[0m\x1b[38;2;255;42;0m \x1b[0m\x1b[38;2;255;38;0m \x1b[0m\x1b[38;2;255;34;0m \x1b[0m\x1b[38;2;255;30;0m \x1b[0m\x1b[38;2;255;26;0m \x1b[0m\x1b[38;2;255;22;0m \x1b[0m\x1b[38;2;255;18;0m \x1b[0m\x1b[38;2;255;14;0m \x1b[0m\x1b[38;2;255;10;0m \x1b[0m\x1b[38;2;255;6;0m \x1b[0m\x1b[38;2;255;2;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\x1b[38;2;255;0;0m \x1b[0m\n\n\x1b[38;2;255;218;0mD\x1b[0m\x1b[38;2;255;214;0mr\x1b[0m\x1b[38;2;255;210;0ma\x1b[0m\x1b[38;2;255;206;0mg\x1b[0m\x1b[38;2;255;202;0m \x1b[0m\x1b[38;2;255;198;0mf\x1b[0m\x1b[38;2;255;194;0mi\x1b[0m\x1b[38;2;255;190;0ml\x1b[0m\x1b[38;2;255;186;0me\x1b[0m\x1b[38;2;255;182;0m \x1b[0m\x1b[38;2;255;178;0my\x1b[0m\x1b[38;2;255;174;0mo\x1b[0m\x1b[38;2;255;170;0mu\x1b[0m\x1b[38;2;255;166;0m \x1b[0m\x1b[38;2;255;162;0mw\x1b[0m\x1b[38;2;255;158;0ma\x1b[0m\x1b[38;2;255;154;0mn\x1b[0m\x1b[38;2;255;150;0mt\x1b[0m\x1b[38;2;255;146;0m \x1b[0m\x1b[38;2;255;142;0mt\x1b[0m\x1b[38;2;255;138;0mo\x1b[0m\x1b[38;2;255;134;0m \x1b[0m\x1b[38;2;255;130;0mo\x1b[0m\x1b[38;2;255;126;0mb\x1b[0m\x1b[38;2;255;122;0mf\x1b[0m\x1b[38;2;255;118;0mu\x1b[0m\x1b[38;2;255;114;0ms\x1b[0m\x1b[38;2;255;110;0mc\x1b[0m\x1b[38;2;255;106;0ma\x1b[0m\x1b[38;2;255;102;0mt\x1b[0m\x1b[38;2;255;98;0me\x1b[0m\x1b[38;2;255;94;0m \x1b[0m\x1b[38;2;255;90;0mi\x1b[0m\x1b[38;2;255;86;0mn\x1b[0m\x1b[38;2;255;82;0mt\x1b[0m\x1b[38;2;255;78;0mo\x1b[0m\x1b[38;2;255;74;0m \x1b[0m\x1b[38;2;255;70;0mt\x1b[0m\x1b[38;2;255;66;0mh\x1b[0m\x1b[38;2;255;62;0me\x1b[0m\x1b[38;2;255;58;0m \x1b[0m\x1b[38;2;255;54;0mw\x1b[0m\x1b[38;2;255;50;0mi\x1b[0m\x1b[38;2;255;46;0mn\x1b[0m\x1b[38;2;255;42;0md\x1b[0m\x1b[38;2;255;38;0mo\x1b[0m\x1b[38;2;255;34;0mw\x1b[0m\x1b[38;2;255;30;0m.\x1b[0m\n\x1b[38;2;255;218;0m \x1b[0m\x1b[38;2;255;214;0m \x1b[0m\n'
obfuscatefile(input(ghost))
print([s for s in dir() if not '__' in s])
os.system('pause')
