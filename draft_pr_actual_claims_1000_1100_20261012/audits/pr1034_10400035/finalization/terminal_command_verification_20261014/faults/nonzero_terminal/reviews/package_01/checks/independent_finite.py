from collections import defaultdict
from fractions import Fraction
import json

def require(x):
    if not x: raise ValueError('independent finite check failed')

def product(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def unit(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def trace(a): return sum(row[i] for i,row in enumerate(a))
X=[[0,1,1,1],[1,0,0,0],[0,-1,0,0],[-1,-1,-1,1]]
Y=[[0,0,-1,1],[-1,-1,1,1],[-1,0,0,0],[0,0,-1,-1]]
M={'1':X,'2':Y}
def word(w,m=M):
    a=unit(len(next(iter(m.values()))))
    for c in w: a=product(a,m[c])
    return trace(a)

def ad(a):
    n=len(a);cols=[]
    for i in range(n):
        for j in range(n):
            e=[[int(r==i and s==j) for s in range(n)] for r in range(n)]
            ae=product(a,e);ea=product(e,a)
            cols.append([ae[r][s]-ea[r][s] for r in range(n) for s in range(n)])
    return [list(r) for r in zip(*cols)]
w='1121222';all_terms=0
for mask in range(128):
    left=''.join(c for i,c in enumerate(w) if not mask>>i&1)
    right=''.join(c for i,c in reversed(list(enumerate(w))) if mask>>i&1)
    all_terms+=(-1)**mask.bit_count()*word(left)*word(right)
A={c:ad(a) for c,a in M.items()}
require(all_terms==word(w,A)==6 and word(w[::-1],A)==-6)
vals={u:word(u) for u in ['2','1121222','1122212','112212','112122']}
require(vals=={'2':-2,'1121222':38,'1122212':20,'112212':-12,'112122':-23})

def determinant(a):
    a=[[Fraction(x) for x in row] for row in a];v=Fraction(1);n=len(a)
    for i in range(n):
        k=next((k for k in range(i,n) if a[k][i]),None)
        if k is None:return 0
        if k!=i:a[i],a[k]=a[k],a[i];v=-v
        x=a[i][i];v*=x
        for j in range(i,n):a[i][j]/=x
        for k in range(i+1,n):
            x=a[k][i]
            for j in range(i,n):a[k][j]-=x*a[i][j]
    return v
require(determinant([[2,0,0],[0,2,0],[2,2,-4]])==-16)
require(determinant([[1,5],[5,1]])==-24)
rows=[[1,0,0,0,0,0],[1,1,1,0,0,0],[1,-1,1,0,0,0],[1,Fraction(3,5),Fraction(9,25),0,0,1],[1,-2,4,1,5,93],[1,10,100,5,1,-29]]
require(determinant(rows)==-48)
# Independent degree-two series expansion of the three printed conjugators.
words=[[1,2,-1,3,1,-2,-1,-3],[-3,-1,3,1],[-3,-1,3,1,-2,-1,-3,1,3,1,2,-1]]
def magnus(w):
    p={():1}
    for a in w:
        terms={():1,(abs(a),):1 if a>0 else -1}
        if a<0:terms[(abs(a),abs(a))]=1
        q=defaultdict(int)
        for u,c in p.items():
            for v,d in terms.items():
                if len(u+v)<=2:q[u+v]+=c*d
        p={u:c for u,c in q.items() if c}
    return p
expected=[{():1,(2,3):1,(3,2):-1},{():1,(1,3):-1,(3,1):1},{():1,(1,2):1,(2,1):-1}]
require([magnus(w) for w in words]==expected)
print(json.dumps({'all_terms':128,'trace':all_terms,'reverse':word(w[::-1],A),'trace_values':vals,'determinants':[-16,-24,-48],'printed_magnus_terms_verified':True,'scope':'finite arithmetic; generator-level Artin derivation separately replayed from the new family checker','passed':True},indent=2))
