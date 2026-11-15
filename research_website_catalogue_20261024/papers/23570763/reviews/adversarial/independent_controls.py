#!/usr/bin/env python3
"""New bounded diagnostics: full monomial-space ranks, never native checker imports."""
import itertools,json,hashlib
from fractions import Fraction

def check(b,msg):
    if not b: raise RuntimeError(msg)

def mons(n): return list(itertools.combinations_with_replacement(range(2*n),2))
def rels(n):
    mm=mons(n); ix={m:i for i,m in enumerate(mm)}; rr=[]
    def vec(a,b,c=1):
        v=[0]*len(mm);v[ix[tuple(sorted((a,b)))]]=c;return v
    for i in range(n):
        for j in range(i+1,n): rr.append(vec(i,j))
    for i in range(n):
        for j in range(i,n):rr.append(vec(n+i,n+j))
    for i in range(n):rr.append(vec(i,n+i))
    for i in range(n):
        for j,k in itertools.combinations([s for s in range(n) if s!=i],2):
            v=vec(i,n+j); w=vec(i,n+k)
            rr.append([a-b for a,b in zip(v,w)])
    return mm,rr

def rr_mod(rows,p):
    a=[[x%p for x in r] for r in rows]; piv=[]; row=0
    if not a:return [],[]
    for col in range(len(a[0])):
        q=next((j for j in range(row,len(a)) if a[j][col]),None)
        if q is None:continue
        a[row],a[q]=a[q],a[row]; inv=pow(a[row][col],-1,p)
        a[row]=[x*inv%p for x in a[row]]
        for j in range(len(a)):
            if j!=row and a[j][col]:
                q=a[j][col]; a[j]=[(x-q*y)%p for x,y in zip(a[j],a[row])]
        piv.append(col);row+=1
        if row==len(a):break
    return a[:row],piv

def rr_Q(rows):
    a=[[Fraction(x) for x in r] for r in rows];piv=[];row=0
    for col in range(len(a[0])):
        q=next((j for j in range(row,len(a)) if a[j][col]),None)
        if q is None:continue
        a[row],a[q]=a[q],a[row];d=a[row][col];a[row]=[x/d for x in a[row]]
        for j in range(len(a)):
            if j!=row and a[j][col]:
                q=a[j][col]; a[j]=[x-q*y for x,y in zip(a[j],a[row])]
        piv.append(col);row+=1
        if row==len(a):break
    return a[:row],piv

def product(n,c):
    mm=mons(n);ix={m:i for i,m in enumerate(mm)};out=[]
    for j in range(2*n):
        v=[0]*len(mm)
        for i,ci in enumerate(c):v[ix[tuple(sorted((i,j)))]]+=ci
        out.append(v)
    return out

def detQ(a):
    a=[[Fraction(x) for x in row] for row in a];out=Fraction(1)
    for i in range(len(a)):
        q=next((j for j in range(i,len(a)) if a[j][i]),None)
        if q is None:return Fraction(0)
        if q!=i:a[i],a[q]=a[q],a[i];out=-out
        d=a[i][i];out*=d
        for j in range(i+1,len(a)):
            t=a[j][i]/d
            for k in range(i+1,len(a)):a[j][k]-=t*a[i][k]
    return out

def coeff_matrix_Q(n,c):
    mm,r=rels(n);red,piv=rr_Q(r);free=[i for i in range(len(mm)) if i not in piv]
    columns=[]
    for row in product(n,c):
        row=[Fraction(x) for x in row]
        for v,k in zip(red,piv):
            t=row[k];row=[a-t*b for a,b in zip(row,v)]
        columns.append([row[i] for i in free])
    return [[col[i] for col in columns] for i in range(len(free))],free

def run():
    out={'mechanism':'rank in full commutative quadratic monomial space modulo literal relation span; no native imports','universal_evidence':'INITIAL_RECONSTRUCTION.md abstract integral algebra proof, not inferred from bounded diagnostics','finite_fields':[],'integer_determinants':[],'mutations':[]}
    for n,p in [(1,2),(1,3),(2,2),(2,3),(3,2),(3,3),(4,2)]:
        mm,r=rels(n);base=len(rr_mod(r,p)[1]);dim=len(mm)-base;check(dim==(1 if n==1 else 2*n),'Hilbert')
        counts={}; good=[]
        for c in itertools.product(range(p),repeat=2*n):
            images=product(n,c);rank=len(rr_mod(r+images,p)[1])-base
            nonzero=any(c)
            # Square l*l is linear combination of independently built product columns.
            sq=[sum(c[j]*images[j][i] for j in range(2*n))%p for i in range(len(mm))]
            sqnz=len(rr_mod(r+[sq],p)[1])>base
            wlp=nonzero and rank==dim
            slp=wlp and sqnz
            check(not slp or wlp,'SLP implication')
            if n>=2:
                predicted=(n-1)%p!=0 and all(c[i] for i in range(n))
                check(wlp==predicted,'all-coefficients determinant classification')
                # Any successful form has a nonzero a_i square, hence SLP.
                check(slp==predicted,'full strong classification')
            counts[str(rank)]=counts.get(str(rank),0)+1
            if slp:good.append(c)
        check(bool(good)==(n==1 or (n-1)%p!=0),'existence theorem')
        witness=tuple([1]*n+[0]*n)
        check((witness in good)==(n==1 or (n-1)%p!=0),'prime-field witness')
        if n>=2 and (n-1)%p==0:
            # z has ones on all y coordinates; every variable product vanishes mod relations.
            z=[0]*n+[1]*n
            for im in product(n,z):check(len(rr_mod(r+[im],p)[1])==base,'common-kernel z')
        out['finite_fields'].append({'n':n,'p':p,'forms_exhausted':p**(2*n),'quadratic_dim':dim,'rank_histogram':counts,'SLP_forms':len(good)})
    # Full literal quotient, nonsymmetric integer coefficient tests; target order is
    # a separately selected free monomial basis, whose orientation is recorded.
    for n in range(2,9):
        mm,_=rels(n)
        for seed in range(3):
            c=[((i+2)*(seed+3)+i*i)%11-5 for i in range(2*n)]
            mat,free=coeff_matrix_Q(n,c);basis=[mm[i] for i in free]
            expected=[(i,i) for i in range(n)]+[(i,n+max(j for j in range(n) if j!=i)) for i in range(n)]
            check(set(basis)==set(expected),'free-monomial labels')
            mat=[mat[basis.index(m)] for m in expected] # Explicitly reorder target u-all then v-all.
            d=detQ(mat);want=Fraction((-1)**(n-1)*(n-1))
            for a in c[:n]:want*=a*a
            check(d==want,'integer nonsymmetric determinant')
            out['integer_determinants'].append({'n':n,'coefficients':c,'determinant':str(d),'expected':str(want)})
    # Characteristic-two naive cross-term reasoning is false: squares remain.
    n=2;p=2;mm,r=rels(n);base=len(rr_mod(r,p)[1]);imgs=product(n,[1,1,0,0]);sq=[(imgs[0][i]+imgs[1][i])%p for i in range(len(mm))]
    check(len(rr_mod(r+[sq],p)[1])==base+1,'char2-square')
    out['mutations'].append({'false_claim':'all squares vanish in characteristic two','rejected_by':'n=2,p=2,l=x1+x2,l^2=u1+u2 nonzero'})
    out['mutations'].append({'false_claim':'badness follows p divides n rather than n-1','rejected_by':'n=2,p=2 success; n=3,p=2 failure'})
    out['mutations'].append({'false_claim':'n=1 obeys bad-width formula','rejected_by':'n=1,p=2 and3 have strong forms'})
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
