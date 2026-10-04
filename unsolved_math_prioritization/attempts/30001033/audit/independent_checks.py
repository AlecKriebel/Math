#!/usr/bin/env python3
"""Independent audit: no import from, or writes to, the frozen package.
Uses dense coefficient matrices, Gaussian inversion, explicit span sets,
integer Heisenberg matrices, and finite dihedral permutations.
"""
import hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/'package'
WORDS=[ [('y',1),('x',1),('y',1),('x',1),('y',1),('x',1),('y',-3),('x',-3)],
[('y',1),('x',-1),('y',-1),('x',-3),('y',2),('x',-1),('y',1),('x',1),('y',1)],
[('y',3),('x',-1),('y',1),('x',1),('y',1),('x',2),('y',2),('x',1),('y',1),('x',1)] ]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zeros(n):return [[0]*n for _ in range(n)]
def mul(A,B,p=2):
 n=len(A);C=[[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
 return C if p is None else [[c%p for c in row] for row in C]
def madd(A,B):return [[a^b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def inv2(A):
 n=len(A);C=[a[:]+e for a,e in zip(A,eye(n))]
 for j in range(n):
  k=next(k for k in range(j,n) if C[k][j]);C[j],C[k]=C[k],C[j]
  for i in range(n):
   if i!=j and C[i][j]:C[i]=[x^y for x,y in zip(C[i],C[j])]
 assert [r[:n] for r in C]==eye(n)
 return [r[n:] for r in C]
def poly_mul(A,B):
 n=len(A[0]);C=[zeros(n) for _ in range(len(A)+len(B)-1)]
 for i,a in enumerate(A):
  for j,b in enumerate(B):C[i+j]=madd(C[i+j],mul(a,b))
 while len(C)>1 and C[-1]==zeros(n):C.pop()
 return C

def word(w,g,I,m):
 z=I
 for a,p in w:
  for _ in range(abs(p)):z=m(z,g[a if p>0 else a.upper()])
 return z
source_rows={
'A0':['100000000','010001010','001011001','000100000','000010001','000001011','000000100','000000010','000000001'],
'A1':['000000000','011001010','010011001','000000000','010011001','001010011','000000000','001010011','011001010'],
'B0':['100000000','010010111','001111011','000100011','000010100','000001000','000000100','000000010','000000001'],
'B1':['000000000','011010111','010111011','010111011','001101100','000000000','010111011','001101100','010111011']}
M=json.loads((P/'matrices.json').read_text())['matrices']
assert M=={name:[[int(x) for x in r] for r in rows] for name,rows in source_rows.items()}
gens={'x':[M['A0'],M['A1']],'y':[M['B0'],M['B1']]}
for name in ['x','y']:
 A,B=gens[name];C=inv2(A);gens[name.upper()]=[C,mul(mul(C,B),C)]
 assert poly_mul(gens[name],gens[name.upper()])==[eye(9)]
 assert poly_mul(gens[name.upper()],gens[name])==[eye(9)]
rels=[word(w,gens,[eye(9)],poly_mul)==[eye(9)] for w in WORDS]
assert all(rels)
assert word(WORDS[0]+[('x',1)],gens,[eye(9)],poly_mul)!=[eye(9)]

def ipow_upper(A,n):
 if n<0:
  a,b,c=A[0][1],A[1][2],A[0][2]
  A=[[1,-a,a*b-c],[0,1,-b],[0,0,1]];n=-n
 ans=eye(3)
 for _ in range(n):ans=mul(ans,A,None)
 return ans
hx=[[1,1,0],[0,1,0],[0,0,1]];hy=[[1,0,0],[0,1,1],[0,0,1]]
hg={'x':hx,'X':ipow_upper(hx,-1),'y':hy,'Y':ipow_upper(hy,-1)}
col=[]
for w in WORDS:
 A=word(w,hg,eye(3),lambda a,b:mul(a,b,None));a,b=A[0][1],A[1][2]
 col.append((a,b,a*b-A[0][2]))
assert col==[(0,0,6),(-4,4,0),(4,8,26)]
def compose(p,q):return tuple(p[q[i]] for i in range(4))
rx=tuple((-i)%4 for i in range(4));ry=tuple((1-i)%4 for i in range(4))
dg={'x':rx,'X':rx,'y':ry,'Y':ry};identity=tuple(range(4))
assert all(word(w,dg,identity,compose)==identity for w in WORDS)
comm=word([('y',-1),('x',-1),('y',1),('x',1)],dg,identity,compose)
assert comm!=identity and compose(comm,comm)==identity

def diagonal(poly,d):
 ans=[]
 for r in range(3):
  q,c=divmod(r+d,3);A=poly[q] if q<len(poly) else zeros(9)
  ans.append(tuple(A[3*r+i][3*c+j] for i in range(3) for j in range(3)))
 return tuple(ans)
def triple_encode(T):return tuple(sum(z<<i for i,z in enumerate(t)) for t in T)
def uncode(t):return tuple(tuple((v>>i)&1 for i in range(9)) for v in t)
def addtr(A,B):return tuple(tuple(a^b for a,b in zip(ar,br)) for ar,br in zip(A,B))
def mm3(a,b):return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3))%2 for i in range(3) for j in range(3))
def action(u,v,d):
 return tuple(tuple(a^b for a,b in zip(mm3(u[r],v[(r+d)%3]),mm3(v[r],u[(r+1)%3]))) for r in range(3))
zero=((0,)*9,)*3
def span(vectors):
 S={zero}
 for v in vectors:S|={addtr(a,v) for a in S}
 return S
a,b=diagonal(gens['x'],1),diagonal(gens['y'],1)
assert triple_encode(a)==(416,416,416) and triple_encode(b)==(464,14,162)
V={zero,action(b,a,1)}
assert triple_encode(action(b,a,1))==(224,402,76)
spaces={};ranks=[]
for i in range(1,6):
 spaces[i]=V;ranks.append(len(V).bit_length()-1)
 V=span(action(v,g,i+1) for v in V for g in [a,b])
assert ranks==[1,2,3,3,2] and spaces[2]==spaces[5]
bases={1:[(224,402,76)],2:[(0,478,370),(0,370,172)],3:[(112,430,258),(328,484,150),(152,490,52)],4:[(176,176,176),(408,308,70),(376,166,10)]}
assert all(span(uncode(v) for v in vs)==spaces[i] for i,vs in bases.items())
transitions=[]
for i in [2,3,4]:
 for j,v in enumerate(bases[i],1):
  transitions.append([i,j,triple_encode(action(uncode(v),a,i+1)),triple_encode(action(uncode(v),b,i+1))])
# Independent degree-four Magnus coefficients, integer counts reduced mod two.
def series_mul(A,B):
 C={}
 for a,x in A.items():
  for b,y in B.items():
   if len(a+b)<=4:C[a+b]=(C.get(a+b,0)+x*y)%2
 return {a:x for a,x in C.items() if x}
mag=[]
for w in WORDS:
 C={'':1}
 for g,n in w:
  factor={'':1,g:1} if n>0 else {g*k:1 for k in range(5)}
  for _ in range(abs(n)):C=series_mul(C,factor)
 del C[''];d=min(map(len,C));assert d==4
 mag.append(sorted(C))
recorded=json.loads((P/'controls-output.json').read_text())
assert mag==[x['initial_terms'] for x in recorded['magnus']]
manifest=json.loads((P/'MANIFEST.json').read_text())
for f in manifest['files']:
 data=(P/f['path']).read_bytes()
 assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
result={'package_manifest_sha256':hashlib.sha256((P/'MANIFEST.json').read_bytes()).hexdigest(),'manifest_entries_verified':len(manifest['files']),'source_matrix_transcription_match':True,'exact_dense_polynomial_relators':rels,'both_sided_polynomial_inverses':True,'integer_heisenberg_collection':col,'dihedral_order_eight_witness':True,'leading_ranks_indices_1_through_5':ranks,'full_span_phase_cycle':[2,5,3],'table_transitions':transitions,'independent_magnus_initial_forms':mag,'target_complete':False,'new_proof_search':False}
print(json.dumps(result,indent=2))
