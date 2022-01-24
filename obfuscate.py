U='{0:#0{1}x}'
T=len
N=str
M=range
E='/'
D=dict
import errno,pathlib as F,math as A,os,py_compile,shutil
G=D(zip([chr(A)for A in M(1114111)],[U.format(A,8)for A in M(1114111)]))
O=D(((B,A)for(A,B)in G.items()))
def H(string): # string to bytecode
	A=E
	for B in string:A+=G[B]+E
	return A
def P(bc): # bytecode to string
	A=bc;B='';A=A.split(E);A=' '.join(A).split()
	for C in A:B+=O[C]
	return B
def I(dictionary):
	B=dictionary;A=[]
	for C in B:A.append((C,B[C]))
	A.sort(key=lambda x:x[1]);A.reverse();return A
def B(string):A=string;return{B:A.count(B)for B in set(A)}
def J(frequencies):return A.ceil(A.log(T(frequencies),16))
def K(split,hexlim):
	A=split;B={}
	for C in M(T(A)):B[A[C][0]]=U.format(C,hexlim+2)+E
	return B
def C(string,replace):
	B=replace;A=string
	if B and A:E,F=B.popitem();return F.join((C(F,D(B))for F in A.split(E)))
	return A
def L(string):A=string;return C(A,K(I(B(A)),J(B(A)))),K(I(B(A)),J(B(A)))
def Q(string,keys=''):
	A=string
	if isinstance(A,tuple):keys=A[1];A=A[0]
	B=D(((B,A)for(A,B)in keys.items()));return C(A,B)
def R(code):A=code;B=A;C=L(H(A))[1];D=L(H(A))[0];return B,C,D
def V(code,huffkey):return P(Q(code,huffkey))
def S(code):D=code;A=R(code);B='O=dict;r=zip;t=chr;s=range;n=set;w=len;X=isinstance;n=eval;g=tuple;import math,pathlib,os,ast,sys;H=math.log;u=math.ceil;P=ast.literal_eval;L=[None,False,__name__,exec,True,int(0),2,3,\'hi\',\'exec\'];J=O(r([t(i)for i in s(1114111)],[\"{0:#0{1}x}\".format(i,8)for i in s(1114111)],));q=O((v,k)for k,v in J.items());z=[\'0x000065\',\'0x000078\',\'0x000065\',\'0x000063\'];\ndef Z(l):\n    for k in z:l+=q[k];\n    return l\ndef C(f):\n bc=\"/\"\n for F in f:bc+=J[F]+\"/\";\n return bc\ndef l(bc):\n f=\"\";bc=bc.split(\"/\");bc=\" \".join(bc).split();\n for v in bc:f+=q[v];\n return f\ndef N(dictionary):\n G=[]\n for U in dictionary:G.append((U,dictionary[U]));\n G.sort(key=lambda x:x[1]);G.reverse();return G\ndef j(f):\n return{i:f.count(i)for i in n(f)}\ndef E(frequencies):\n return u(H(w(frequencies),16))\ndef B(G,hexlim):\n p={}\n for i in s(w(G)):p[G[i][0]]=\"{0:#0{1}x}\".format(i,hexlim+2)+\"/\";\n return p\ndef y(f,W):\n if W and f:s,r=W.popitem();return r.join(y(subs,O(W))for subs in f.split(s));\n return f\ndef D(f):\n return y(f,B(N(j(f)),E(j(f)))),B(N(j(f)),E(j(f)))\ndef c(f,keys=\"\"):\n if X(f,g):keys=f[1];f=f[0];\n W=O((v,k)for k,v in keys.items());return y(f,W)\ndef T(code):\n I=code;A=D(C(code))[1];Y=D(C(code))[0];return I,A,Y\ndef M(code,A):\n return l(c(code,A))\n';C=B+"n(Z(\'\'))(M('"+A[2]+"',P(l(\'"+H(N(A[1]))+'\'))))';return C
def obfuscate(name,code, clearvars = False):
	B=code;B=S(B);A=N(F.Path(N(F.Path(__file__).parent)+'/temp/'+name+'.py'));LOZER=N(F.Path(N(F.Path(__file__).parent)+'/output/'+name+'.py'))
	if not os.path.exists(os.path.dirname(A)):
		try:os.makedirs(os.path.dirname(A))
		except OSError as C:
			if C.errno!=errno.EEXIST:raise
	with open(A,'w')as D:D.write(B)
	py_compile.compile(A, cfile = LOZER)
	shutil.rmtree(N(F.Path(N(F.Path(__file__).parent)+'/temp/')))
	print(LOZER)
	return A