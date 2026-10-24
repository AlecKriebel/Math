#!/usr/bin/env python3
"""Independent dihedral obstruction audit; no author code is imported.

Determinants use subset dynamic programming rather than permutation expansion.
Exact roots use Q(zeta_3,zeta_5,zeta_7), not reduction modulo Phi_210.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
AUTHOR=ROOT/'nonabelian_holonomy'
PAIRS=((3,2),(20,14),(119,84))

def add(a,b):
    out=dict(a)
    for e,c in b.items():
        out[e]=out.get(e,0)+c
        if not out[e]: del out[e]
    return out

def scale(a,c): return {e:c*v for e,v in a.items() if c*v}

def mul(a,b):
    out={}
    for (i,j),c in a.items():
        for (k,l),d in b.items():
            e=(i+k,j+l)
            out[e]=out.get(e,0)+c*d
    return {e:c for e,c in out.items() if c}

ONE={(0,0):1}

def matrix(pattern):
    first=pattern.index(1)
    other=[i for i in range(3) if i!=first]
    phase=[None]*3
    phase[first]=(0,0)
    phase[other[0]]=(1,0)
    phase[other[1]]=(0,1)
    rows=[]
    for (p,q),is_ref,(i,j) in zip(PAIRS,pattern,phase):
        z={(i,j):1}; zi={(-i,-j):1}
        r=[{} for _ in range(6)]; s=[{} for _ in range(6)]
        if is_ref:
            r[1]=scale(z,p); r[2]=scale(ONE,-q)
            r[4]=scale(ONE,-1); r[5]=z
            s[0]=scale(zi,p); s[3]=scale(ONE,-q)
            s[4]=zi; s[5]=scale(ONE,-1)
        else:
            r[0]=scale(z,p); r[2]=scale(ONE,-q)
            r[4]=add(z,scale(ONE,-1))
            s[1]=scale(zi,p); s[3]=scale(ONE,-q)
            s[5]=add(zi,scale(ONE,-1))
        rows.extend([r,s])
    return rows

def determinant(m):
    # dp[S] is the determinant of the first |S| rows and columns S.
    dp={0:ONE}
    for n in range(1,len(m)+1):
        for cs in combinations(range(len(m)),n):
            mask=sum(1<<c for c in cs)
            v={}
            # Laplace expansion along the final row of this minor.
            for j,c in enumerate(cs):
                v=add(v,scale(mul(dp[mask^(1<<c)],m[n-1][c]),(-1)**(n-1+j)))
            dp[mask]=v
    return dp[(1<<len(m))-1]

def partitions(n):
    # Restricted-growth strings, one representative per set partition.
    def visit(s,m):
        if len(s)==n:
            yield tuple(tuple(i for i,v in enumerate(s) if v==j) for j in range(m+1))
            return
        for v in range(m+2): yield from visit(s+[v],max(m,v))
    yield from visit([0],0)

def necessary(coeffs):
    a=sorted(abs(c) for c in coeffs)
    if len(a)<2: return False
    if a[-1]>sum(a[:-1]): return False
    if len(a)==2: return a[0]==a[1]
    if len(a)==3: return a[0]==a[1]==a[2] or a[0]+a[1]==a[2]
    return True

def egcd(a,b):
    if not b: return a,1,0
    g,s,t=egcd(b,a%b)
    return g,t,s-(a//b)*t

def verify_unit_basis(vectors):
    # Construct, rather than just infer, each unit lattice vector.
    g=0; weights=[]
    for i,j in combinations(range(len(vectors)),2):
        a,b=vectors[i]; c,d=vectors[j]; det=a*d-b*c
        if not det: continue
        g,s,t=egcd(g,abs(det))
        weights=[(u,v,k*s) for u,v,k in weights]
        weights.append((i,j,t*(1 if det>0 else -1)))
        if g==1: break
    assert g==1
    coefs=[[0]*len(vectors),[0]*len(vectors)]
    for i,j,k in weights:
        a,b=vectors[i]; c,d=vectors[j]
        coefs[0][i]+=k*d; coefs[0][j]-=k*b
        coefs[1][i]-=k*c; coefs[1][j]+=k*a
    for cs,expected in zip(coefs,((1,0),(0,1))):
        assert tuple(sum(c*v[j] for c,v in zip(cs,vectors)) for j in range(2))==expected
    return max(sum(abs(c) for c in cs) for cs in coefs)

def bound_partitions(poly):
    terms=sorted(poly.items())
    count=0; kept=0; indices=Counter(); examples=[]; max_unit_l1=0
    for blocks in partitions(len(terms)):
        count+=1
        if not all(necessary([terms[i][1] for i in b]) for b in blocks): continue
        kept+=1
        vectors=[]
        for b in blocks:
            v=terms[b[0]][0]
            vectors.extend((terms[i][0][0]-v[0],terms[i][0][1]-v[1]) for i in b[1:])
        ix=reduce(gcd,(abs(a*d-b*c) for (a,b),(c,d) in combinations(vectors,2)),0)
        indices[ix]+=1
        if ix!=1: examples.append(blocks)
        else: max_unit_l1=max(max_unit_l1,verify_unit_basis(vectors))
    assert not examples, ('bad lattice index',examples)
    return {'all_set_partitions':count,'survivors':kept,'lattice_index_counts':dict(indices),
            'explicit_unit_basis_checks':kept,'max_unit_basis_coefficient_l1':max_unit_l1}

def local_power(p,e):
    r=e%p
    return [-1]*(p-1) if r==p-1 else [int(i==r) for i in range(p-1)]

def tensor_power(e):
    a,b,c=(local_power(p,e) for p in (3,5,7))
    # zeta = -zeta_3*zeta_5*zeta_7 is primitive of order 210.
    return [(-1)**e*a[i]*b[j]*c[k] for k in range(6) for j in range(4) for i in range(2)]

def torsion_zeros(poly):
    g=reduce(gcd,(abs(c) for c in poly.values()))
    terms=[(a,b,c//g) for (a,b),c in poly.items()]
    prime=211
    root=next(x for x in range(2,prime) if pow(x,210,prime)==1 and all(pow(x,210//p,prime)!=1 for p in (2,3,5,7)))
    fp=[pow(root,i,prime) for i in range(210)]
    field=[tensor_power(i) for i in range(210)]
    assert field[0]==field[210%210]
    zero=[]; modular=0; exact_nonzero=0
    for x,y in product(range(210),repeat=2):
        exps=[(a*x+b*y)%210 for a,b,c in terms]
        if sum(c*fp[e] for (_,_,c),e in zip(terms,exps))%prime: continue
        modular+=1
        vec=[0]*48
        for (_,_,c),e in zip(terms,exps):
            for j,u in enumerate(field[e]): vec[j]+=c*u
        if not any(vec): zero.append([x,y])
        else: exact_nonzero+=1
    assert zero==[[0,0]], zero
    return {'pairs_checked':210**2,'screen_prime':prime,'primitive_root':root,
            'modular_survivors':modular,'exact_nonzeros_after_screen':exact_nonzero,'exact_zeros':zero}

def rank(m):
    a=[list(map(Fraction,r)) for r in m]; out=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(out,len(a)) if a[i][c]),None)
        if pivot is None: continue
        a[pivot],a[out]=a[out],a[pivot]
        z=a[out][c]; a[out]=[x/z for x in a[out]]
        for i in range(len(a)):
            if i!=out:
                z=a[i][c]; a[i]=[x-z*y for x,y in zip(a[i],a[out])]
        out+=1
    return out

def sign_checks():
    out=[]
    for signs in product((-1,1),repeat=3):
        m=[[p*s,-q,s-1] for (p,q),s in zip(PAIRS,signs)]
        r=rank(m)
        assert r==3 or (signs==(1,1,1) and r==2)
        out.append({'signs':signs,'rank':r})
    return out

def rational_plane_checks():
    # Independent real-coordinate equations, including reflection phases
    # that are not themselves roots of unity before normalization.
    # The reflection coset is lambda0 * mu4, lambda0=(-7-24i)/25.
    # Products of reflections are fourth-root rotations, so this is D4.
    quarter=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)),
             (Fraction(-1),Fraction(0)),(Fraction(0),Fraction(-1)))
    lam=(Fraction(-7,25),Fraction(-24,25))
    matrices=[]
    for x,y in quarter: matrices.append([[x,-y],[y,x]])
    for x,y in quarter:
        a,b=lam[0]*x-lam[1]*y,lam[0]*y+lam[1]*x
        matrices.append([[a,b],[b,-a]])
    ranks=Counter()
    for choices in product(range(8),repeat=3):
        rows=[]
        for (p,q),k in zip(PAIRS,choices):
            s=matrices[k]
            for i in range(2):
                rows.append([p*s[i][j] for j in range(2)]
                            +[-q*int(i==j) for j in range(2)]
                            +[s[i][j]-int(i==j) for j in range(2)])
        r=rank(rows); rt=rank([v[4:] for v in rows])
        assert r-rt==4,(choices,r,rt)
        ranks[(r,rt)]+=1
    return {'finite_dihedral_D4_triples':8**3,
            'unnormalized_reflection_phase':['-7/25','-24/25'],
            'full_and_vertical_rank_counts':{str(k):v for k,v in ranks.items()}}

def abelian_dependency_check():
    # Independently repeat the exact finite end of the reviewed commuting lemma.
    coefs=(99,812,714,714,820,105)
    assert [(i,j) for i,j in combinations(range(6),2) if coefs[i]==coefs[j]]==[(2,3)]
    assert not any(necessary([coefs[i] for i in cs]) for cs in combinations(range(6),3))
    # Here zeta_60=zeta_4*zeta_3*zeta_5 is primitive.
    p4=((1,0),(0,1),(-1,0),(0,-1))
    field=[]
    for e in range(60):
        a=p4[e%4]; b=local_power(3,e); c=local_power(5,e)
        field.append([a[i]*b[j]*c[k] for k in range(4) for j in range(2) for i in range(2)])
    prime=241
    root=next(x for x in range(2,prime) if pow(x,60,prime)==1 and all(pow(x,60//p,prime)!=1 for p in (2,3,5)))
    fp=[pow(root,e,prime) for e in range(60)]
    cs=(-99,812,-714,-714,820,-105)
    zero=[]; survived=0
    for x,y,z in product(range(60),repeat=3):
        exps=(x,y,z,(x+y)%60,(x+z)%60,(y+z)%60)
        if sum(c*fp[e] for c,e in zip(cs,exps))%prime: continue
        survived+=1
        if not any(sum(c*field[e][j] for c,e in zip(cs,exps)) for j in range(16)):
            zero.append([x,y,z])
    assert zero==[[0,0,0]],zero
    return {'rational_coefficient_triples_checked':20,'pairs_checked':60**3,
            'screen_prime':prime,'primitive_root':root,'modular_survivors':survived,
            'exact_zeros':zero,'field':'Q(zeta4,zeta3,zeta5)'}

def main():
    manifest=json.loads((AUTHOR/'DIHEDRAL_MANIFEST.json').read_text())
    hashes={}
    for k,v in list(manifest['files'].items())+list(manifest['dependencies'].items()):
        path=AUTHOR/k
        actual=sha256(path.read_bytes()).hexdigest()
        assert actual==v,(str(path),actual,v)
        hashes[str(path.relative_to(ROOT))]=actual
    raw=json.loads((AUTHOR/'dihedral_determinants.json').read_text())
    stored={tuple(r['types']):{tuple(t['exponent']):t['coefficient'] for t in r['terms']} for r in raw}
    out=[]
    for pattern in product((0,1),repeat=3):
        if not any(pattern): continue
        poly=determinant(matrix(pattern))
        assert poly==stored[pattern],('determinant mismatch',pattern,poly,stored[pattern])
        row={'pattern':pattern,'terms':len(poly),'partition_check':bound_partitions(poly),'torsion_check':torsion_zeros(poly)}
        out.append(row)
        print(json.dumps(row),flush=True)
    result={'utc':datetime.now(timezone.utc).isoformat(),'verdict':'PASS',
            'scope':'Seven plane-action patterns, all-order torsion reduction, exact zeros, and commuting sign endpoints; not arbitrary finite holonomy or21.124.',
            'input_sha256':hashes,'patterns':out,'sign_endpoint_ranks':sign_checks(),
            'rational_real_coordinate_crosscheck':rational_plane_checks(),
            'commuting_dependency_reproduction':abelian_dependency_check(),
            'method':'Subset-DP determinants; exhaustive restricted-growth partitions; integral tensor field Q(zeta3,zeta5,zeta7); distinct prime211 screen.'}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',flush=True)

if __name__=='__main__': main()
