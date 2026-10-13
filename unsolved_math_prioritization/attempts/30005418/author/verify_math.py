#!/usr/bin/env python3
"""Exact characteristic-zero controls for the scoped Kähler/Koszul research note.
Python standard library only. These are finite controls, not a universal proof.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr, product
from math import factorial
import hashlib, json, pathlib, sys
if not __debug__:
    raise SystemExit('Assertions must remain enabled; do not use python -O.')

def rank(rows):
    piv={}
    for row in rows:
        v={k:F(x) for k,x in (row.items() if isinstance(row,dict) else enumerate(row)) if x}
        while v:
            k=min(v)
            if k not in piv:
                a=v[k]; piv[k]={j:x/a for j,x in v.items()};break
            a=v[k]
            for j,x in piv[k].items():
                v[j]=v.get(j,F(0))-a*x
                if not v[j]:v.pop(j,None)
    return len(piv)

def rref(rows,n):
    a=[[F(x) for x in r] for r in rows];p=[];i=0
    for j in range(n):
        q=next((q for q in range(i,len(a)) if a[q][j]),None)
        if q is None:continue
        a[i],a[q]=a[q],a[i];z=a[i][j];a[i]=[x/z for x in a[i]]
        for k in range(len(a)):
            if k!=i and a[k][j]:
                z=a[k][j];a[k]=[x-z*y for x,y in zip(a[k],a[i])]
        p.append(j);i+=1
        if i==len(a):break
    return a[:i],p

def kernel(rows,n):
    a,p=rref(rows,n);free=[j for j in range(n) if j not in p];out=[]
    for j in free:
        v=[F(0)]*n;v[j]=1
        for row,k in zip(a,p):v[k]=-row[j]
        out.append(v)
    return out

def mm(a,b):
    return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]

def transpose(a):return list(map(list,zip(*a)))
def inertia(matrix):
    a=[[F(x) for x in row] for row in matrix];ans=[0,0,0]
    while a:
        n=len(a);p=next((i for i in range(n) if a[i][i]),None)
        if p is None:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n) if a[i][j]),None)
            if pair is None:ans[2]+=n;break
            i,j=pair
            # Replace basis vector e_i by e_i+e_j, by a congruence.
            a[i]=[x+y for x,y in zip(a[i],a[j])]
            for k in range(n):a[k][i]+=a[k][j]
            p=i
        a[0],a[p]=a[p],a[0]
        for row in a:row[0],row[p]=row[p],row[0]
        z=a[0][0];ans[0 if z>0 else 1]+=1
        a=[[a[i][j]-a[i][0]*a[0][j]/z for j in range(1,n)] for i in range(1,n)]
    return ans

def monomials(n,d):return list(cwr(range(n),d))
def macaulay_rows(relations,n,d):
    basis=monomials(n,d);ix={b:i for i,b in enumerate(basis)}
    for r in relations:
        for m in monomials(n,d-2):
            v={}
            for term,x in r.items():
                k=ix[tuple(sorted(term+m))];v[k]=v.get(k,0)+x
            yield v

def quotient_multiplication():
    # Published Roos/McCullough-Seceleanu base algebra, variables u,x,y,z.
    rel=[{(1,1):1,(2,3):1,(0,0):1},{(0,1):1},
         {(1,1):1,(1,2):1},{(1,3):1,(0,2):1},
         {(0,3):1,(0,0):1},{(2,2):1,(3,3):1}]
    mons=monomials(4,2);rows=[[r.get(m,0) for m in mons] for r in rel]
    a,p=rref(rows,len(mons));free=[j for j in range(len(mons)) if j not in p]
    assert len(p)==6 and len(free)==4
    mul={}
    for j,m in enumerate(mons):
        v=[F(int(i==j)) for i in range(len(mons))]
        for row,k in zip(a,p):
            z=v[k];v=[x-z*y for x,y in zip(v,row)]
        mul[m]=[v[k] for k in free]
    assert rank(macaulay_rows(rel,4,3))==20
    return rel,mul,[mons[k] for k in free]

def bar_basis(i,j):
    for ds in product((1,2),repeat=i):
        if sum(ds)==j:
            for ids in product(range(4),repeat=i):yield tuple(zip(ds,ids))

def bar_differential(i,j,mul):
    source=list(bar_basis(i,j));target=list(bar_basis(i-1,j));idx={b:k for k,b in enumerate(target)}
    columns=[]
    for b in source:
        v={}
        for k in range(i-1):
            if b[k][0]!=1 or b[k+1][0]!=1:continue
            for m,c in enumerate(mul[tuple(sorted((b[k][1],b[k+1][1]))) ]):
                if c:
                    row=idx[b[:k]+((2,m),)+b[k+2:]]
                    v[row]=v.get(row,0)+(-1)**k*c
        columns.append({k:x for k,x in v.items() if x})
    return source,target,columns

def idealization(mul):
    # A_1 = (R_1,R_2^*), A_2 = (R_2,R_1^*), A_3 = R_0^*.
    def mult11(i,j):
        if i<4 and j<4:return mul[tuple(sorted((i,j)))]+[F(0)]*4
        if i>=4 and j>=4:return [F(0)]*8
        if i>=4:i,j=j,i
        return [F(0)]*4+[mul[tuple(sorted((i,k)))][j-4] for k in range(4)]
    mons=monomials(8,2);cols=[mult11(*m) for m in mons]
    relations=kernel(transpose(cols),len(mons));assert len(relations)==28
    rel=[{m:x for m,x in zip(mons,row) if x} for row in relations]
    ranks={d:rank(macaulay_rows(rel,8,d)) for d in (2,3,4)}
    assert ranks=={2:28,3:119,4:330},ranks
    # A1*A2 perfect pairing: R1 with R1*, and R2* with R2.
    pairing=[[F(int((i<4 and j==i+4) or (i>=4 and j==i-4))) for j in range(8)] for i in range(8)]
    assert rank(pairing)==8
    # Search bounded binary R1 vectors only to provide an explicit HL control.
    found=None
    for a in product((0,1),repeat=4):
        T=[[sum(a[i]*mul[tuple(sorted((i,j)))][k] for i in range(4)) for j in range(4)] for k in range(4)]
        if rank(T)==4:
            # Pick b in R2* with b(a^2) != 0; this gives L^3 != 0.
            aa=[sum(a[i]*a[j]*mul[tuple(sorted((i,j)))][k] for i in range(4) for j in range(4)) for k in range(4)]
            b=next(k for k,x in enumerate(aa) if x)
            L=list(a)+[int(k==b) for k in range(4)]
            # Q_ij = degree(e_i*e_j*L) with degree(w)=1.
            Q=[[sum(mult11(i,j)[k]*L[k+4] for k in range(4))+sum(mult11(i,j)[k+4]*L[k] for k in range(4)) for j in range(8)] for i in range(8)]
            cube=sum(L[i]*Q[i][j]*L[j] for i in range(8) for j in range(8))
            assert rank(Q)==8 and cube!=0 and inertia(Q)==[4,4,0]
            found={'L':L,'cube':str(cube),'degree_one_inertia':inertia(Q)};break
    assert found is not None
    return {'hilbert':[1,8,8,1],'quadratic_macaulay_ranks':ranks,'square_zero_linear_subspace_dimension':4,'hard_lefschetz_control':found}

def polynomial_key(m):
    # Graded reverse lexicographic, variables ordered z_1,...,z_m,u,v,(t).
    return (sum(m),tuple(-x for x in reversed(m)))
def leading(f):return max(f,key=polynomial_key)
def shift_poly(f,m,c=F(1)):
    return {tuple(a+b for a,b in zip(k,m)):v*c for k,v in f.items() if v*c}
def plus(a,b,c=F(1)):
    out=a.copy()
    for m,x in b.items():
        out[m]=out.get(m,F(0))+c*x
        if not out[m]:del out[m]
    return out

def reduce_poly(f,G):
    f=f.copy();out={}
    while f:
        m=leading(f);a=f[m]
        for g in G:
            q=leading(g)
            if all(x>=y for x,y in zip(m,q)):
                f=plus(f,shift_poly(g,tuple(x-y for x,y in zip(m,q)),a/g[q]),F(-1));break
        else:out[m]=a;del f[m]
    return out

def positive_relations(n,tensor=False):
    nv=n+int(tensor);u=n-2;v=n-1
    def mon(i,j):return tuple(int(k==i)+int(k==j) for k in range(nv))
    G=[{mon(u,u):F(1)},{mon(v,v):F(1)}]
    for i in range(n-2):
        G.extend([{mon(u,i):F(1)},{mon(v,i):F(1)},{mon(i,i):F(1),mon(u,v):F(1)}])
        for j in range(i+1,n-2):G.append({mon(i,j):F(1)})
    if tensor:G.append({mon(n,n):F(1)})
    return G

def check_groebner(G):
    pairs=0
    for i,g in enumerate(G):
        for h in G[:i]:
            mg=leading(g);mh=leading(h);lc=tuple(max(x,y) for x,y in zip(mg,mh))
            sg=shift_poly(g,tuple(x-y for x,y in zip(lc,mg)),1/g[mg]);sh=shift_poly(h,tuple(x-y for x,y in zip(lc,mh)),1/h[mh])
            assert not reduce_poly(plus(sg,sh,-1),G)
            pairs+=1
    return pairs

def lorentz(n):
    B=[[F(0)]*n for _ in range(n)];B[0][1]=B[1][0]=1
    for i in range(2,n):B[i][i]=-1
    return B

def dot(a,B,b):return sum(a[i]*B[i][j]*b[j] for i in range(len(a)) for j in range(len(b)))
def tensor_form(B,a,s):
    n=len(a);Ba=[sum(B[i][j]*a[j] for j in range(n)) for i in range(n)]
    return [[s*B[i][j] for j in range(n)]+[Ba[i]] for i in range(n)]+[Ba+[F(0)]]
def primitive_inertia(Q,l):
    functional=[sum(l[i]*Q[i][j] for i in range(len(l))) for j in range(len(l))]
    K=kernel([functional],len(l));restricted=mm(mm(K,Q),transpose(K))
    return inertia([[-x for x in r] for r in restricted])

def positive_controls():
    out=[]
    for n in range(2,11):
        pairs=check_groebner(positive_relations(n))+check_groebner(positive_relations(n,True))
        B=lorentz(n);assert inertia(B)==[1,n-1,0]
        # Rational timelike points and mixed degree-one tests.
        cone=[]
        for k in range(1,5):
            a=[F(k+2),F(k+1)]+[F(1,k+2)]*(n-2);s=F(k,2)
            assert dot(a,B,a)>0;cone.append((a,s))
        mixed=0
        for a,s in cone:
            Q=tensor_form(B,a,s);assert inertia(Q)==[1,n,0]
            assert primitive_inertia(Q,a+[s])==[n,0,0]
            for b,t in cone:
                assert dot(b+[t],Q,b+[t])>0
                assert primitive_inertia(Q,b+[t])==[n,0,0];mixed+=1
        triple=0
        for (a,s),(b,t),(c,r) in product(cone,repeat=3):
            assert s*dot(b,B,c)+t*dot(a,B,c)+r*dot(a,B,b)>0;triple+=1
        out.append({'surface_embedding_dimension':n,'tensor_hilbert':[1,n+1,n+1,1], 'buchberger_pairs':pairs,'single_points':4,'mixed_HR_pairs':mixed,'mixed_degree_zero_triples':triple})
    return out

def fermat_control():
    # F=X^3-Y^3, normalized degree differential evaluation divided by 6.
    # A=R[x,y]/(xy,x^3+y^3), h=(1,2,2,1); quadratic ideal (xy) is insufficient.
    Q=[[F(2),0],[0,F(-1)]];l=[F(2),F(1)]
    assert dot(l,Q,l)==7 and inertia(Q)==[1,1,0]
    assert primitive_inertia(Q,l)==[1,0,0]
    # Poincare series reciprocity candidates, not a proof of Koszulness.
    return {'apolar_hilbert':[1,2,2,1],'L':[2,1],'cube':7,'primitive_Q1_inertia':[1,0,0],'quadratic':False,'reason':'The sole quadratic relation xy does not kill x^3+y^3.'}

def run():
    _,mul,free=quotient_multiplication()
    s3,t3,D3=bar_differential(3,4,mul);s4,t4,D4=bar_differential(4,4,mul)
    assert t4==s3
    for col in D4:
        v={}
        for k,x in col.items():
            for j,y in D3[k].items():v[j]=v.get(j,F(0))+x*y
        assert all(x==0 for x in v.values())
    r3,r4=rank(D3),rank(D4)
    rows3=[[c.get(i,0) for c in D3] for i in range(len(t3))]
    cycle_basis=kernel(rows3,len(s3))
    functionals=kernel([[c.get(i,0) for i in range(len(s3))] for c in D4],len(s3))
    selected=next((z,w,sum(x*y for x,y in zip(z,w))) for z in cycle_basis for w in functionals if sum(x*y for x,y in zip(z,w)))
    z,w,pairing=selected;w=[x/pairing for x in w]
    assert all(sum(x*y for x,y in zip(row,z))==0 for row in rows3)
    assert all(sum(w[i]*x for i,x in c.items())==0 for c in D4)
    assert sum(x*y for x,y in zip(z,w))==1
    names={1:['u','x','y','z'],2:['xy','xz','yz','zz']}
    def sparse_bar(v):
        return [{'word':[names[d][i] for d,i in s3[j]],'coefficient':str(x)} for j,x in enumerate(v) if x]
    witness={'cycle':sparse_bar(z),'separating_cocycle':sparse_bar(w),'pairing':'1'}
    assert (len(t3),len(s3),len(s4),r3,r4)==(16,192,256,16,175)
    assert len(s3)-r3-r4==1
    return {'claim_status':'general target unsolved; scoped controls only',
            'field':'Q, interpreted over R by exact scalar extension',
            'base_R':{'hilbert':[1,4,4],'degree_two_basis':[list(x) for x in free], 'bar_internal_degree':4,'bar_dimensions_C2_C3_C4':[16,192,256], 'bar_ranks_d3_d4':[r3,r4],'Tor_3_4':1,'d3_d4_zero':True,'explicit_nonzero_bar_class':witness},
            'idealization':idealization(mul),'positive_controls':positive_controls(),'nonquadratic_HR_control':fermat_control()}
if __name__=='__main__':
    result=run();data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)==3 and sys.argv[1]=='--output':pathlib.Path(sys.argv[2]).write_text(data)
    elif len(sys.argv)!=1:raise SystemExit('Usage: verify_math.py [--output FILE]')
    print(data,end='')
