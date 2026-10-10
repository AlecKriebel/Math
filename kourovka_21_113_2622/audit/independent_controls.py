#!/usr/bin/env python3
"""Independent audit controls. No imports from author checkers, no frozen writes."""
from itertools import product
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json, sympy as S

class FiniteGroup:
    def __init__(self, elements, operation, identity):
        self.elements=list(elements); self.n=len(self.elements)
        self.index={g:i for i,g in enumerate(self.elements)}
        self.identity=self.index[identity]
        self.table=[[self.index[operation(g,h)] for h in self.elements] for g in self.elements]
        e=self.identity
        self.inverse=[next(j for j in range(self.n) if self.table[i][j]==e and self.table[j][i]==e) for i in range(self.n)]
        self.powers=[]
        for i in range(self.n):
            row=[e]; j=i
            while j!=e:
                row.append(j); j=self.table[j][i]
            self.powers.append(row)
        self.orders=[len(row) for row in self.powers]
        self.centralizers=[{j for j in range(self.n) if self.table[i][j]==self.table[j][i]} for i in range(self.n)]
        unseen=set(range(self.n)); self.classes=[]
        while unseen:
            i=min(unseen)
            c={self.table[self.table[g][i]][self.inverse[g]] for g in range(self.n)}
            self.classes.append(c); unseen-=c
        self.reps=[min(c) for c in self.classes]
    def regular(self,i,p):
        n=self.orders[i]; pp=1
        while n%p==0:n//=p;pp*=p
        return next(self.powers[i][k] for k in range(self.orders[i]) if k%pp==0 and (k-1)%n==0)
    def p_elements(self,p):
        return {i for i,n in enumerate(self.orders) if all(q==p for q in S.factorint(n))}
    def psi(self,p,subset=None):
        H=set(range(self.n)) if subset is None else set(subset)
        pe=H & self.p_elements(p)
        return {x:0 if self.orders[x]%p==0 else len(self.centralizers[x]&pe) for x in H}
    def cyclic(self,i):return set(self.powers[i])
    def quotient(self,N):
        assert all(self.table[self.table[g][n]][self.inverse[g]] in N for g in range(self.n) for n in N)
        cosets=[];remaining=set(range(self.n))
        while remaining:
            a=min(remaining); c=frozenset(self.table[a][n] for n in N);cosets.append(c);remaining-=c
        lookup={g:c for c in cosets for g in c}
        Q=FiniteGroup(cosets,lambda c,d:lookup[self.table[min(c)][min(d)]],lookup[self.identity])
        return Q,[Q.index[lookup[g]] for g in range(self.n)]
    def induced(self,H,values):
        return [Fraction(sum(values[self.table[self.table[self.inverse[a]][x]][a]]
                            for a in range(self.n) if self.table[self.table[self.inverse[a]][x]][a] in H),len(H))
                for x in range(self.n)]

def field4mul(x,y):
    r=0
    while y:
        if y&1:r^=x
        y>>=1;x<<=1
        if x&4:x^=7
    return r

def matrix_group(q):
    add=(lambda x,y:x^y) if q==4 else (lambda x,y:(x+y)%q)
    mul=field4mul if q==4 else (lambda x,y:x*y%q)
    neg=(lambda x:x) if q==4 else (lambda x:-x%q)
    matrices=[(a,b,c,d) for a,b,c,d in product(range(q),repeat=4) if add(mul(a,d),neg(mul(b,c)))==1]
    def op(x,y):
        a,b,c,d=x;e,f,g,h=y
        return (add(mul(a,e),mul(b,g)),add(mul(a,f),mul(b,h)),add(mul(c,e),mul(d,g)),add(mul(c,f),mul(d,h)))
    return FiniteGroup(matrices,op,(1,0,0,1)),add,mul

def symmetric(n):
    # SymPy's independent permutation machinery, rather than the author's implementation.
    from sympy.combinatorics.named_groups import SymmetricGroup
    P=SymmetricGroup(n); els=list(P.generate_schreier_sims())
    return FiniteGroup(els,lambda x,y:x*y,P.identity)

def cyclic(n):return FiniteGroup(range(n),lambda x,y:(x+y)%n,0)
def direct(G,H):
    return FiniteGroup(list(product(range(G.n),range(H.n))),
                       lambda a,b:(G.table[a[0]][b[0]],H.table[a[1]][b[1]]),(G.identity,H.identity))
def exact(x):return S.simplify(x)
def eq(a,b):return exact(a-b)==0

result={'group_checks':[], 'quotient_checks':[], 'induced_linear_checks':[], 'a5_matrix_checks':{}}
groups=[('S3',symmetric(3)),('S4',symmetric(4)),('S5',symmetric(5)),('SL2(3)',matrix_group(3)[0]),('SL2(4)',matrix_group(4)[0]),('C6',cyclic(6))]
for name,G in groups:
    for p in S.factorint(G.n):
        psi=G.psi(p);fibers=Counter(G.regular(i,p) for i in range(G.n))
        assert all(psi[x]==fibers[x] for x in range(G.n))
        rhs=[Fraction(0)]*G.n
        for y in G.reps:
            if G.orders[y]%p==0:continue
            H=G.centralizers[y]
            f=G.psi(p,H)
            z=G.induced(H,f)
            rhs=[a+b for a,b in zip(rhs,z)]
        assert all(rhs[x]==(len(G.centralizers[x]) if G.orders[x]%p else 0) for x in range(G.n))
        result['group_checks'].append({'group':name,'order':G.n,'prime':int(p),'degree':psi[G.identity],
                'primary_fibers':True,'full_centralizer_induction_identity':True,'classes':len(G.classes)})

# Every normal quotient in these groups: pointwise primary-part compatibility and
# all class-indicator averages, stronger than testing only a supplied character.
for name,G in groups:
    if name not in ['S3','S4','SL2(3)']:continue
    normals=[]
    if name=='S3':normals=[{i for i,o in enumerate(G.orders) if o in [1,3]}]
    if name=='S4':
        normals=[{i for i,g in enumerate(G.elements) if g.is_even},
                 {i for i,g in enumerate(G.elements) if i==G.identity or g.cycle_structure=={2:2}}]
    if name=='SL2(3)':normals=[{i for i,c in enumerate(G.centralizers) if len(c)==G.n},
                             {i for i,o in enumerate(G.orders) if o in [1,2,4]}]
    for N in normals:
        Q,pi=G.quotient(N)
        for p in S.factorint(G.n):
            assert all(pi[G.regular(x,p)]==Q.regular(pi[x],p) for x in range(G.n))
            for c in Q.classes:
                lhs=Fraction(sum(pi[G.regular(x,p)] in c for x in range(G.n)),G.n)
                rhs=Fraction(sum(Q.regular(x,p) in c for x in range(Q.n)),Q.n)
                assert lhs==rhs
            central=all(len(G.centralizers[z])==G.n for z in N)
            inflation=None
            if central and len(N)%p:
                inflation=all(G.psi(p)[x]==Q.psi(p)[pi[x]] for x in range(G.n));assert inflation
            result['quotient_checks'].append({'G':name,'kernel_order':len(N),'quotient_order':Q.n,'prime':int(p),
                    'primary_compatibility_and_class_indicator_averages':True,'central_pprime_inflation':inflation})

# Direct-product pointwise test, one p-factor and one p'-factor.
G=groups[0][1]
for k in [2,3]:
    H=cyclic(k);D=direct(G,H)
    assert all(D.psi(2)[i]==G.psi(2)[x]*H.psi(2)[y] for i,(x,y) in enumerate(D.elements))
result['direct_product_checks']=['S3 x C2 at p=2','S3 x C3 at p=2']

# Reconstruct the two Fourier counts via independent quotient/coset labels, then
# evaluate the induced class function itself and average, using exact roots.
for name,G in groups:
    if name not in ['S4','S5']:continue
    if name=='S4':
        H={i for i,g in enumerate(G.elements) if g.is_even}
        V={i for i,g in enumerate(G.elements) if i==G.identity or g.cycle_structure=={2:2}}
        t=next(i for i in H if G.orders[i]==3)
        labels={G.table[G.powers[t][j]][v]:j for j in range(3) for v in V}
    else:
        t=next(i for i,g in enumerate(G.elements) if g.cycle_structure=={2:1,3:1})
        H=G.cyclic(t);labels={x:j%3 for j,x in enumerate(G.powers[t])}
    assert set(labels)==H
    assert all(labels[G.table[x][y]]==(labels[x]+labels[y])%3 for x in H for y in H)
    T=Counter(labels[G.regular(x,2)] for x in range(G.n) if G.regular(x,2) in H)
    # conjugate character roots have coordinates (1,0), (0,1), (-1,-1)
    roots=[(1,0),(0,1),(-1,-1)]
    av=[]
    for coordinate in [0,1]:
        induced=G.induced(H,{h:roots[labels[h]][coordinate] for h in H})
        av.append(sum(induced[G.regular(x,2)] for x in range(G.n))/G.n)
    assert av[1]==0 and av[0]==Fraction(T[0]-T[1],len(H))
    result['induced_linear_checks'].append({'G':name,'H_order':len(H),'T':[T[j] for j in range(3)],'direct_induction_average':str(av[0])})

# A5 entirely as determinant-one matrices over F4.
G,add,mul=matrix_group(4);assert G.n==60
vectors=[v for v in product(range(4),repeat=2) if v!=(0,0)]
lines=[];remaining=set(vectors)
while remaining:
    v=min(remaining);line=frozenset((mul(t,v[0]),mul(t,v[1])) for t in [1,2,3]);lines.append(line);remaining-=line
assert len(lines)==5
lookup={v:i for i,line in enumerate(lines) for v in line}
actions=[]
for a,b,c,d in G.elements:
    actions.append(tuple(lookup[(add(mul(a,x),mul(b,y)),add(mul(c,x),mul(d,y)))] for x,y in [min(l) for l in lines]))
assert len(set(actions))==60
chi4=[sum(i==j for i,j in enumerate(row))-1 for row in actions]
psi=G.psi(2);assert all(chi4[i]**2==psi[i] for i in range(G.n))
P={G.index[(1,b,0,1)] for b in range(4)}
orbits=[];unseen=set(range(5))
while unseen:
    x=min(unseen);orb={actions[g][x] for g in P};orbits.append(orb);unseen-=orb
assert sorted(map(len,orbits))==[1,4]
assert all(chi4[x]==(4 if x==G.identity else 0) for x in P)

# Matrix traces determine both natural 2-dimensional Brauer characters.
a=(S.sqrt(5)-1)/2;b=(-S.sqrt(5)-1)/2
phi={};phit={}
for i,(x,y,z,w) in enumerate(G.elements):
    if G.orders[i]%2==0:continue
    tr=add(x,w)
    phi[i]={0:2,1:-1,2:a,3:b}[tr]
    phit[i]={0:2,1:-1,2:b,3:a}[tr]
reg=list(phi);brauer=[{i:1 for i in reg},phi,phit,{i:chi4[i] for i in reg}]
# Natural module irreducibility via generators' unique invariant lines.
U=G.index[(1,1,0,1)];L=G.index[(1,0,1,1)]
assert len(set(i for i in range(5) if actions[U][i]==i))==1
assert len(set(i for i in range(5) if actions[L][i]==i))==1
assert not any(actions[U][i]==i and actions[L][i]==i for i in range(5))

# Derive ordinary characters from the exact A5 class algebra, rather than importing the table.
classid={g:i for i,c in enumerate(G.classes) for g in c}
sizes=[len(c) for c in G.classes]
matrices=[]
for ci in G.classes:
    columns=[]
    for cj in G.classes:
        counts=Counter(G.table[x][y] for x in ci for y in cj)
        assert all(len({counts[x] for x in c})==1 for c in G.classes)
        columns.append([counts[min(c)] for c in G.classes])
    matrices.append(S.Matrix(len(G.classes),len(G.classes),lambda i,j:columns[j][i]))
M=sum(((j+1)**2*A for j,A in enumerate(matrices)),S.zeros(5))
ordinary=[]
for eigenvalue,multiplicity,vectors_ in M.eigenvects():
    assert multiplicity==1 and len(vectors_)==1
    v=vectors_[0];k=next(i for i,x in enumerate(v) if x!=0)
    omega=[exact((A*v)[k]/v[k]) for A in matrices]
    degree=exact(S.sqrt(S.Rational(G.n)/sum(omega[j]*S.conjugate(omega[j])/sizes[j] for j in range(5))))
    row=[exact(degree*omega[j]/sizes[j]) for j in range(5)]
    assert all(eq((A*v)[l],omega[j]*v[l]) for j,A in enumerate(matrices) for l in range(5))
    assert degree.is_integer and degree>0
    ordinary.append(row)
ordinary.sort(key=lambda row:(row[classid[G.identity]],str(row)))
assert [row[classid[G.identity]] for row in ordinary]==[1,3,3,4,5]
for i,row in enumerate(ordinary):
    for j,col in enumerate(ordinary):
        assert eq(sum(s*x*S.conjugate(y) for s,x,y in zip(sizes,row,col))/G.n,int(i==j))
psi_coeff=[exact(sum(psi[G.reps[j]]*S.conjugate(row[j])*sizes[j] for j in range(5))/G.n) for row in ordinary]
assert psi_coeff==[1]*5
pcoeff=[exact(sum(psi[i]*S.conjugate(row[i]) for i in reg)/G.n) for row in brauer]
assert pcoeff==[1,0,0,1]
alpha=[1+ordinary[1][classid[i]] for i in range(G.n)]
assert all(alpha[i]==0 for i in range(G.n) if G.orders[i]%2==0)
acoeff=[exact(sum(alpha[i]*S.conjugate(row[i]) for i in reg)/G.n) for row in brauer]
assert sorted(acoeff)==[-1,0,0,1]
# Exact PIMs from the inverse Brauer pairing linear system, to check cone membership.
B=S.Matrix([[row[i] for i in G.reps if i in reg] for row in brauer])
rs=[i for i in G.reps if i in reg];regsz=[len(G.classes[classid[i]]) for i in rs]
PIM=(B.conjugate()*S.diag(*[S.Rational(z,G.n) for z in regsz])).inv()
# columns of PIM are their values on p-regular classes.
assert all(eq(sum(PIM[j,k]*pcoeff[k] for k in range(4)),psi[rs[j]]) for j in range(4))
r=[exact(sum(S.conjugate(row[i]) for i in rs)) for row in brauer]
d=[exact(sum(sum(S.conjugate(row[x]) for x in G.centralizers[y])/len(G.centralizers[y]) for y in rs if y!=G.identity)) for row in brauer]
assert r==[4,0,0,3] and d==[3,0,0,2]
result['a5_matrix_checks']={'order':60,'class_sizes':sorted(sizes),'natural_degrees':[1,2,2,4],
 'ordinary_degrees_from_class_algebra':[1,3,3,4,5],'psi_ordinary_coefficients':list(map(str,psi_coeff)),
 'psi_projective_coefficients':list(map(str,pcoeff)),'alpha_projective_coefficients':list(map(str,acoeff)),
 'projective_cover_degrees':[str(PIM[rs.index(G.identity),k]) for k in range(4)],
 'sylow_orbits':sorted(map(len,orbits)),'augmentation_tensor_square_matches_psi':True,
 'Lambda_coefficients':list(map(str,r)),'proper_centralizer_coefficients':list(map(str,d))}
# C6 correction computed from roots in exact algebraic field.
G=cyclic(6);roots=[1,(1+S.sqrt(3)*S.I)/2,(-1+S.sqrt(3)*S.I)/2,-1,(-1-S.sqrt(3)*S.I)/2,(1-S.sqrt(3)*S.I)/2]
pure=[];mixed=[]
for i,n in enumerate(G.orders):
    if n%2:
        continue
    corr=exact(S.re(roots[G.regular(i,2)]-roots[i]))
    (pure if G.regular(i,2)==G.identity else mixed).append(corr)
assert pure==[2] and mixed==[-1,-1]
result['C6_signed_control']={'pure':list(map(str,pure)),'mixed':list(map(str,mixed))}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
