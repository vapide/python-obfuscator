import errno
import pathlib
import math
import os
import py_compile
import shutil
import random
import time
import base64

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

def xor(s, t):
    if isinstance(s, str):
        return "".join(chr(ord(a) ^ b) for a, b in zip(s, t)).encode('utf8')
    else:
        return bytes([a ^ b for a, b in zip(s, t)])
    
def obfuscatecode(code):
    oldcode = code
    t = base64.b64encode(bytes(time.ctime().encode('utf8')))
    random.seed(t)
    xorkey = random.randbytes(len(code))
    code = xor(code.encode('utf8'),xorkey) + '\\'.encode('utf8') + str(t).encode('utf8')
    print(code)
    print(xorkey)
    encryptedcode = encrypt(str(code))
    buffer = 'O=dict;r=zip;t=chr;T=\'raise\';U=\'Exception\';s=range;n=set;w=len;X=isinstance;n=eval;F=\'*args\';g=tuple;W=[\'0x000070\',\'0x000072\',\'0x000069\',\'0x00006e\',\'0x000074\'];import math,pathlib,os,random,ast,sys;H=math.log;u=math.ceil;P=ast.literal_eval;L=[None,False,__name__,exec,True,int(0),2,3,\'hi\',\'exec\',\'utf8\'];J=O(r([t(i)for i in s(1114111)],[\"{0:#0{1}x}\".format(i,8)for i in s(1114111)],));q=O((v,k)for k,v in J.items());z=[\'0x000065\',\'0x000078\',\'0x000065\',\'0x000063\'];V=T+q[\'0x000020\']+U;\nZ,C = lambda l,L: [l:=l+q[k] for k in n(L)], lambda f: \'/\'+[bc:=bc+J[F]+\'/\' for F in f]\n#l = lambda bc, f=\"\":  [f:=f+q[v] for v in (lambda oh: (\" \".join(oh.split(\'/\'))).split())(bc)], f\n#l = lambda bc,f=\'\': (lambda: f,[f:=f+q[v] for v in (lambda oh: (\" \".join(bc.split(\'/\')).split()))(bc)])\nOl = lambda bc: (bc.replace(\'\\\\\\\\\'+bc[(-(str(bc[::-1]).find(\'\\\\\\\\\'))+len(bc)):-1],\'\'),bc[(-(str(bc[::-1]).find(\'\\\\\\\\\'))+len(bc)):-1])\ndef l(bc,f=\'\'):\n    [f:=f+q[v] for v in (lambda oh: (\" \".join(bc.split(\'/\')).split()))(bc)]\n    return f\ndef N(dictionary):\n G=[]\n [G.append((U,dictionary[U])) for U in dictionary];G.sort(key=lambda x:x[1]);G.reverse();return G\ndef j(f):\n return{i:f.count(i)for i in n(f)}\ndef E(frequencies):\n return u(H(w(frequencies),16))\ndef B(G,hexlim):\n p={}\n for i in s(w(G)):p[G[i][0]]=\"{0:#0{1}x}\".format(i,hexlim+2)+\"/\";\n return p\ndef y(f,W):\n if W and f:s,r=W.popitem();return r.join(y(subs,O(W))for subs in f.split(s));\n return f\ndef D(f):\n return y(f,B(N(j(f)),E(j(f)))),B(N(j(f)),E(j(f)))\ndef c(f,keys=\"\"):\n if X(f,g):keys=f[1];f=f[0]\n W=O([(v,k)for k,v in keys.items()]);\n return y(f,W)\ndef T(code):\n I=code;A=D(C(code))[1];Y=D(C(code))[0];return I,A,Y\ndef M(code,A):\n return l(c(code,A))\ndef x(s,t):\n return ((lambda s,t: [\"\".join(t(ord(a)^b)for a,b in r(s,t)).encode(L[10])] if X(s,str)else bytes([a^b for a,b in r(s,t)]))(s,t))\ndef IO(k):\n    random.seed(n(k[1].encode(L[10])))\n    a = (random.randbytes(len(n(k[0]))))\n    return x(n(k[0]),a).decode(L[10])\n#n(Z(\'\',\'z\'))(Z(\'\',\'W\') + \'=\' + V)\n#n(Z(\'\',\'z\'))(\'def \'+Z(\'\',\'W\')+\'(\'+F+\'): \'+V+\'(\"\'+n(\'t(110)+t(111)+t(112)+t(101)+t(33)+t(34)+t(41)+t(59)\'))\n'
    newcode = buffer + "print(IO(Ol(M('" + encryptedcode[1] + "',P(l(\'" + stringtounicode(str(encryptedcode[2])) + '\'))))))'
    print(t)
    return newcode # n(Z('','z'))

def obfuscate(name, code, compile = False, clearvars = False, outputname = None):
    if outputname == None:
        outputname = name + '.py'
    #code = code.replace('print', 'sys.stdout.write')
    if clearvars == True:
        code += '\nsys.modules[__name__].__dict__.clear()' # removes the variables from locals() globals() and vars()
    code = obfuscatecode(code)
    print(code)
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
