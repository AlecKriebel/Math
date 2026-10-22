#!/usr/bin/env python3
"""Independent exact audit controls. Standard library only; no imported author code."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]

def rank(rows):
    if not rows: return 0
    a = [list(map(Fraction, row)) for row in rows]
    pivot = 0
    for j in range(len(a[0])):
        k = next((i for i in range(pivot, len(a)) if a[i][j]), None)
        if k is None: continue
        a[pivot], a[k] = a[k], a[pivot]
        val = a[pivot][j]
        a[pivot] = [v/val for v in a[pivot]]
        for i in range(pivot+1, len(a)):
            val = a[i][j]
            a[i] = [v-val*w for v,w in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a): break
    return pivot

def det(rows):
    a = [list(map(Fraction, row)) for row in rows]
    n = len(a); ans = Fraction(1)
    for j in range(n):
        k = next((i for i in range(j,n) if a[i][j]), None)
        if k is None: return Fraction(0)
        if k != j: a[j],a[k]=a[k],a[j]; ans=-ans
        val=a[j][j]; ans*=val
        for i in range(j+1,n):
            scale=a[i][j]/val
            for c in range(j+1,n): a[i][c]-=scale*a[j][c]
    return ans

def exp(word,d):
    v=[0]*d
    for g in word: v[abs(g)-1] += 1 if g>0 else -1
    return v

def twisted_profile(d,rels):
    """Use the sign-isotypic chain complex, independently of the lifted 2-vertex one."""
    base=d-rank([exp(w,d) for w in rels]); out=[]
    for eps in product((0,1),repeat=d):
        if not any(eps): continue
        sig=[1-2*e for e in eps]
        if any(math.prod(sig[abs(g)-1] for g in w)!=1 for w in rels): continue
        rows=[]
        for w in rels:
            pref=1; row=[0]*d
            for g in w:
                j=abs(g)-1
                row[j] += pref if g>0 else -pref*sig[j]
                pref*=sig[j]
            assert pref==1
            assert sum(a*(s-1) for a,s in zip(row,sig))==0
            rows.append(row)
        anti=d-1-rank(rows)
        out.append({'epimorphism_to_C2':list(eps),'anti_invariant_b1':anti,'b1_cover':base+anti})
    return {'b1_base':base,'double_covers':out}

def trim(a,p):
    a=[x%p for x in a]
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def rem(a,b,p):
    a=trim(a,p); b=trim(b,p)
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b); c=a[-1]*pow(b[-1],-1,p)%p
        for i,v in enumerate(b): a[i+k]-=c*v
        a=trim(a,p)
    return a

def conv(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c

def resultant(a,b):
    # Coefficients supplied in descending degree order.
    m=len(a)-1; n=len(b)-1; rows=[]
    for i in range(n): rows.append([0]*i+a+[0]*(n-1-i))
    for i in range(m): rows.append([0]*i+b+[0]*(m-1-i))
    return det(rows)

def main():
    manifest=(ROOT/'public/SHA256SUMS').read_bytes()
    assert hashlib.sha256(manifest).hexdigest()=='697ef5b8667cba0b0bc6bc259fde7e6146275f693ce7d9125da00d720d572c64'
    checks={}
    for line in manifest.decode().splitlines():
        h,name=line.split(); got=hashlib.sha256((ROOT/'public'/name).read_bytes()).hexdigest()
        assert h==got; checks[name]=got
    assert (ROOT/'public/controls-output.json').read_bytes()==(ROOT/'audit/controls-replay.json').read_bytes()
    recorded=json.loads((ROOT/'audit/controls-replay.json').read_text())
    examples={'Z2':(2,[(1,2,-1,-2)]),'free_rank2':(2,[]),'Dinfty':(2,[(1,1),(2,2)]),'Klein_bottle':(2,[(1,2,-1,2)])}
    profiles={name:twisted_profile(*args) for name,args in examples.items()}
    for name,data in profiles.items():
        old=recorded['double_cover_profiles'][name]
        assert old['b1_base']==data['b1_base']
        assert [(r['epimorphism_to_C2'],r['b1_cover']) for r in old['double_covers']]==[(r['epimorphism_to_C2'],r['b1_cover']) for r in data['double_covers']]
    f=[8,-40,46,-17,2]
    factors=[]
    for degree in (1,2):
        for cs in product(range(7),repeat=degree):
            divisor=list(cs)+[1]
            if rem(f,divisor,7)==[0]: factors.append(divisor)
    assert not factors
    q=[1,0,-12,0,18,0,-10,0,2]
    deriv=[i*q[i] for i in range(1,len(q))]
    res=resultant(q[::-1],deriv[::-1]); disc=res/2
    assert disc==2**17*43**2
    fac=conv(conv(conv([2],[1,0,1]),[1,0,1]),conv([19,0,1],[17,0,1]))
    assert trim(fac,43)==trim(q,43)
    assert rem(q,[42,0,1],43)==[42]  # q(s)=-1 at s^2=1, no hidden denominator loss.
    presentation_matrix=[[6,2],[10,-5]]
    assert det(presentation_matrix)==-50
    assert math.gcd(*(x for row in presentation_matrix for x in row))==1
    trefoil_splice_matrix=[[2,-3,0,0],[0,0,2,-3],[1,-1,4,-6],[-4,6,-1,1]]
    assert det(trefoil_splice_matrix)==1
    finite=[]
    for p in (2,3,5):
        mats=[(a,b,c,d) for a,b,c,d in product(range(p),repeat=4) if (a*d-b*c)%p==1]
        invol=[m for m in mats if ((m[0]*m[0]+m[1]*m[2])%p,(m[0]*m[1]+m[1]*m[3])%p,(m[2]*m[0]+m[3]*m[2])%p,(m[2]*m[1]+m[3]*m[3])%p)==(1,0,0,1)]
        triples={( (a+d)%p,(e+h)%p,(a*e+b*g+c*f+d*h)%p ) for a,b,c,d in invol for e,f,g,h in invol}
        item={'p':p,'SL2_order':len(mats),'Hom_Dinfty_SL2_count':len(invol)**2,'distinct_generator_trace_triples':len(triples)}
        assert item==next(r for r in recorded['finite_matrix_controls'] if r['p']==p)
        finite.append(item)
    output={'all_checks_passed':True,'frozen_manifest_sha256':hashlib.sha256(manifest).hexdigest(),'frozen_files':checks,'author_replay_byte_identical':True,'independent_double_cover_method':'sign-isotypic Fox/cellular chain complex','independent_double_cover_profiles':profiles,'f_mod7_no_monic_factors_degrees_1_or_2':not factors,'q_discriminant':int(disc),'q_discriminant_factorization':{'2':17,'43':2},'q_mod43_factorization':'2*(s^2+1)^2*(s^2+19)*(s^2+17)','q_mod43_distinct_roots_over_algebraic_closure':6,'source_displayed_abelianization':'C50','trefoil_splice_abelianization_matrix':trefoil_splice_matrix,'trefoil_splice_determinant':1,'independent_finite_matrix_controls':finite,'scope':'Finite audits and consistency checks only. No general Haken/profinite resolution or census manifold certification.'}
    print(json.dumps(output,indent=2))
if __name__=='__main__': main()
