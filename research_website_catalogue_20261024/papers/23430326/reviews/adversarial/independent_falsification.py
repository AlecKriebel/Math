"""Independent endpoint/matching and WD-nilpotent checks; no support imports."""
from itertools import combinations, product
from fractions import Fraction
import json, re, sympy as sp
from pathlib import Path
S={'A':(0,2),'B':(1,4),'C':(3,3),'D':(2,5),'T':(4,6)}
names=tuple(S)
def prec(x,y):
    a,b=S[x];c,d=S[y]
    return a<c<=b+1 and b<d
def shifted_prec(x,y):
    a,b=S[x];c,d=S[y]
    return a-1<c<=b and b-1<d
def graph(M,N):
    X=[(x,y) for x in M for y in N if prec(x,y)]
    Y=[(x,y) for x in M for y in N if shifted_prec(x,y)]
    E={x:[y for y in Y if (x[0]==y[0] and prec(y[1],x[1])) or (x[1]==y[1] and prec(x[0],y[0]))] for x in X}
    def dfs(k,used):
        return k==len(X) or any(dfs(k+1,used|{y}) for y in E[X[k]] if y not in used)
    return {'X':X,'Y':Y,'edges':[{'x':x,'neighbors':E[x]} for x in X], 'injection':dfs(0,set()), 'isolated':[x for x in X if not E[x]]}
def ladder(M):
    a=sorted((S[x] for x in M))
    return all(a[i][0]<a[i+1][0] and a[i][1]<a[i+1][1] for i in range(len(a)-1))
partitions=[]
for k in (1,2):
    for M in combinations(names,k):
        N=tuple(x for x in names if x not in M)
        partitions.append({'m':M,'n':N,'ladder_m':ladder(M),'ladder_n':ladder(N),'mn':graph(M,N),'nm':graph(N,M)})
# Nilpotent tensor grade ranks: determine L-exponents from actual kernels.
def l_exponents(x,y):
    a,b=S[x];c,d=S[y];m=b-a+1;n=d-c+1
    exps=[]
    for k in range(m+n-1):
        domain=[(i,j) for i in range(m) for j in range(n) if i+j==k]
        codomain=[(i,j) for i in range(m) for j in range(n) if i+j==k-1]
        mat=sp.zeros(len(codomain),len(domain))
        for col,(i,j) in enumerate(domain):
            for im in ((i-1,j),(i,j-1)):
                if im in codomain:mat[codomain.index(im),col]+=1
        nullity=len(domain)-mat.rank()
        exp=Fraction(a+b-c-d,2)+Fraction(m+n-2,2)-k
        exps.extend([int(exp)]*nullity)
    return exps
z=sp.symbols('z')
def germ(P,Q,q,sgn):
    f=sp.prod((1-sgn*sp.Rational(q)**(-h)/z)*(1-sgn*sp.Rational(q)**(-1-h)/z) for h in Q)/sp.prod((1-sgn*sp.Rational(q)**(-h)*z)*(1-sgn*sp.Rational(q)**(-1-h)*z) for h in P)
    num,den=sp.fraction(sp.cancel(f))
    def mult(poly):
        p=sp.Poly(poly,z);v=0
        while p.eval(1)==0:
            p=sp.div(p,sp.Poly(z-1,z))[0];v+=1
        return v
    v=mult(num)-mult(den)
    lead=sp.limit(f/(z-1)**v,z,1)
    return {'order':v,'leading':str(lead)}
pairs=[]
for x,y in combinations(('T','D','C','B','A'),2):
    P=l_exponents(x,y);Q=l_exponents(y,x)
    pairs.append({'pair':x+y,'P_WD_kernel':P,'Q_WD_kernel':Q,'germs':{str(q)+','+str(s):germ(P,Q,q,s) for q,s in product((3,9),(1,-1))}})
orders=[tuple('TDCBA'),tuple('TCDBA'),tuple('TDBCA')]
relations=[]
for O in orders:
    violations=[]
    for i in range(5):
        for j in range(i+1,5):
            a,b=S[O[i]];c,d=S[O[j]]
            if a<=c<=b<=d: violations.append((O[i],O[j]))
    relations.append({'order':''.join(O),'forbidden_FLO_relations':violations,'forbidden_LM_precedences':[(O[i],O[j]) for i in range(5) for j in range(i+1,5) if prec(O[i],O[j])]})
cycle=(('T','D'),('D','B'),('B','A'),('A','C'),('C','T'))
colors=[]
for bits in product((0,1),repeat=4):
    labels=dict(zip(('T','D','B','A','C'),(0,)+bits))
    if all(labels[x]!=labels[y] for x,y in cycle): colors.append(labels)
# Compare actual paper's displayed table to independently formed named graphs.
tex=(Path(__file__).resolve().parents[2]/'sources/support/paper.tex').read_text()
checked_table=[]
for line in tex.splitlines():
    if not re.match(r'^\$[ABCDT]+/[ABCDT]+\$ &',line):continue
    cells=line.split(' & ')
    M,N=re.findall(r'[ABCDT]+',cells[1])
    witness=tuple(re.findall(r'\(([ABCDT]),([ABCDT])\)',cells[2])[0])
    displayed_Y=[tuple(x) for x in re.findall(r'\(([ABCDT]),([ABCDT])\)',cells[3])]
    g=graph(M,N)
    checked_table.append({'partition':cells[0],'correct_entire_Y':sorted(displayed_Y)==sorted(g['Y']),'correct_isolated_witness':witness in g['isolated']})
# Central-character exponent and norm-one restriction.
central=sum(sum(range(a,b+1)) for a,b in S.values())
out={'actual_manuscript_table':checked_table,'partitions':partitions,'pairs':pairs,'FLO_orders':relations,'odd_cycle_survivors_with_T_zero':colors,'central_character_absdet_exponent':central,'verified_all_partitions_have_ladder_side':all(p['ladder_m'] or p['ladder_n'] for p in partitions),'verified_all_partitions_fail_some_LC':all(not p['mn']['injection'] or not p['nm']['injection'] for p in partitions),'verified_all_partitions_have_singleton_Hall_obstruction':all(p['mn']['isolated'] or p['nm']['isolated'] for p in partitions)}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('partitions','pairs')},indent=2))
print('All 10 pairs, 40 exact germs, and 30 directed graphs saved; these are finite checks, not a Hom-space computation.')
