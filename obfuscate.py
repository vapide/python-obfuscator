import errno
import pathlib
import math
import os
import py_compile
import shutil

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

def obfuscatecode(code):
	oldcode = code
	encryptedcode = encrypt(code)
	buffer = 'O=dict;r=zip;t=chr;T=\'raise\';U=\'Exception\';s=range;n=set;w=len;X=isinstance;n=eval;F=\'*args\';g=tuple;W=[\'0x000070\',\'0x000072\',\'0x000069\',\'0x00006e\',\'0x000074\'];import math,pathlib,os,ast,sys;H=math.log;u=math.ceil;P=ast.literal_eval;L=[None,False,__name__,exec,True,int(0),2,3,\'hi\',\'exec\'];J=O(r([t(i)for i in s(1114111)],[\"{0:#0{1}x}\".format(i,8)for i in s(1114111)],));q=O((v,k)for k,v in J.items());z=[\'0x000065\',\'0x000078\',\'0x000065\',\'0x000063\'];V=T+q[\'0x000020\']+U;\ndef Z(l,L):\n for k in n(L):l+=q[k];\n return l\ndef C(f):\n bc=\"/\"\n for F in f:bc+=J[F]+\"/\";\n return bc\ndef l(bc):\n f=\"\";bc=bc.split(\"/\");bc=\" \".join(bc).split();\n for v in bc:f+=q[v];\n return f\ndef N(dictionary):\n G=[]\n for U in dictionary:G.append((U,dictionary[U]));\n G.sort(key=lambda x:x[1]);G.reverse();return G\ndef j(f):\n return{i:f.count(i)for i in n(f)}\ndef E(frequencies):\n return u(H(w(frequencies),16))\ndef B(G,hexlim):\n p={}\n for i in s(w(G)):p[G[i][0]]=\"{0:#0{1}x}\".format(i,hexlim+2)+\"/\";\n return p\ndef y(f,W):\n if W and f:s,r=W.popitem();return r.join(y(subs,O(W))for subs in f.split(s));\n return f\ndef D(f):\n return y(f,B(N(j(f)),E(j(f)))),B(N(j(f)),E(j(f)))\ndef c(f,keys=\"\"):\n if X(f,g):keys=f[1];f=f[0];\n W=O((v,k)for k,v in keys.items());return y(f,W)\ndef T(code):\n I=code;A=D(C(code))[1];Y=D(C(code))[0];return I,A,Y\ndef M(code,A):\n return l(c(code,A))\n#n(Z(\'\',\'z\'))(Z(\'\',\'W\') + \'=\' + V)\n#n(Z(\'\',\'z\'))(\'def \'+Z(\'\',\'W\')+\'(\'+F+\'): \'+V+\'(\"\'+n(\'t(110)+t(111)+t(112)+t(101)+t(33)+t(34)+t(41)+t(59)\'))\n'
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
		print(outputpath)
	else:
		if not os.path.exists(os.path.dirname(outputpath)):
			try:
				os.makedirs(os.path.dirname(outputpath))
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		with open(outputpath, "w") as f:
			f.write(code)
		print(outputpath)
	return outputpath

def obfuscatefile(path):
	obfuscate(os.path.basename(path), readfile(path), compile = True, clearvars = True, outputname = os.path.basename(path).replace('py', 'exe'))
