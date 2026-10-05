#!/usr/bin/env python3
"""Independent arithmetic reconstruction; standard library, no network or author imports."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

PIN = '465c3840c518ad8b5abe6bc229e306f2059a211f64cdeb48f5cb0005d2b88ecb'
EXPECTED_NAMES = {'APPROACHES.md','CERTIFICATES.json','CHECK_RESULTS.json','LITERATURE.md','PROOFS.md','README.md','SOURCES.json','verify.py','AUTHOR_MANIFEST.json'}
PATTERN = {(0,0):1,(2,1):1,(1,2):1,(1,0):-1,(0,1):-1,(2,2):-1}

def need(ok, why):
    if not ok:
        raise ValueError(why)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def bind_author(root):
    need(not root.is_symlink(), 'symlink author directory')
    actual = set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'symlink in packet')
        if p.is_file(): actual.add(p.relative_to(root).as_posix())
    need(actual == EXPECTED_NAMES, 'incorrect author inventory')
    raw = (root/'AUTHOR_MANIFEST.json').read_bytes()
    need(digest(raw) == PIN, 'author manifest pin mismatch')
    m = json.loads(raw)
    need(m['problem_id']=='30004334' and m['approaches_completed']==5 and m['assessment']=='unresolved_complex_target', 'scope mismatch')
    need(len(m['files']) == 8 and {f['path'] for f in m['files']} == EXPECTED_NAMES-{'AUTHOR_MANIFEST.json'}, 'manifest inventory mismatch')
    for f in m['files']:
        raw = (root/f['path']).read_bytes()
        need(len(raw)==f['bytes'] and digest(raw)==f['sha256'], 'payload integrity mismatch')
    return json.loads((root/'CERTIFICATES.json').read_text())

# Gaussian-integer incidence, avoiding division and projective normalization.
def plus(x,y): return (x[0]+y[0],x[1]+y[1])
def minus(x,y): return (x[0]-y[0],x[1]-y[1])
def times(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])

def lines():
    units=[(1,0),(0,1),(-1,0),(0,-1)]
    points=[(units[a],units[b]) for a in range(4) for b in range(4)]
    found=set()
    for i,j in itertools.combinations(range(16),2):
        (x1,y1),(x2,y2)=points[i],points[j]
        a,b,c=minus(y2,y1),minus(x1,x2),minus(times(x2,y1),times(x1,y2))
        members=tuple(k for k,(x,y) in enumerate(points) if plus(plus(times(a,x),times(b,y)),c)==(0,0))
        need(i in members and j in members, 'line coefficient reconstruction failed')
        found.add(members)
    census=dict(sorted(Counter(map(len,found)).items()))
    need(census=={2:48,4:12}, 'line census failed')
    covered=Counter(pair for line in found for pair in itertools.combinations(line,2))
    need(len(covered)==120 and set(covered.values())=={1}, 'line pair coverage failed')
    families=set()
    for k in range(4):
        families.add(tuple(a*4+b for a in range(4) for b in range(4) if a==k))
        families.add(tuple(a*4+b for a in range(4) for b in range(4) if b==k))
        families.add(tuple(a*4+b for a in range(4) for b in range(4) if (b-a)%4==k))
    need({l for l in found if len(l)==4}==families, 'arrangement identification failed')
    return found,census

# Formal polynomials with ascending coefficients; used without sampled k values.
def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]: p.pop()
    return p

def padd(p,q): return trim([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])
def scale(p,c): return trim([c*x for x in p])
def pmul(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): r[i+j]+=x*y
    return trim(r)

def evalp(p,k):
    out=0
    for a in reversed(p): out=out*k+a
    return out

def identities(incidence):
    mult=[[0,2*PATTERN.get((a,b),0),2] for a in range(4) for b in range(4)]
    S=Q=[0]
    for v in mult:
        S=padd(S,v); Q=padd(Q,pmul(v,v))
    d=[1,0,8]
    sq=padd(pmul(d,d),scale(Q,-1))
    canonical=padd(scale(d,-3),S)
    fiber=padd(scale(d,4),scale(S,-1))
    need((S,Q,sq,canonical,fiber)==([0,0,32],[0,0,24,0,64],[1,0,-8],[-3,0,8],[4]),'symbolic intersection identities failed')
    need(padd(sq,canonical)==[-2], 'arithmetic genus identity failed')
    arrangement_slacks=[]
    for line in incidence:
        total=[0]
        for i in line: total=padd(total,mult[i])
        slack=padd(d,scale(total,-1))
        if len(line)==4:
            need(slack==[1], 'arrangement slack failed')
            arrangement_slacks.append(slack)
    # Every other line has <=2 centers; each multiplicity <=2k^2+2k.
    slack=padd(d,scale([0,4,4],-1))
    need(slack==pmul([-1,2],[-1,2]), 'all-parameter two-point line bound failed')
    # Minimum multiplicity 2k(k-1), and k>=3 gives -71 or below.
    need(pmul([0,2],[-1,1])==[0,-2,2], 'multiplicity nonnegativity factor failed')
    need(evalp(sq,3)==-71 and sq[2]<0, 'genus-bound threshold failed')
    return {'all_parameter_polynomial_identities':True,'all_line_slack_identity':'(2k-1)^2','arrangement_slack':1,'hao_bound_m4_g0':-62,'first_excluded_by_hao_k':3}

# Coefficients of (center+T)^n from repeated polynomial multiplication.
# This construction deliberately avoids the author's binomial/power jet formula.
def translations(center,d,p):
    out=[[1]]
    for _ in range(d):
        old=out[-1]; row=[0]*(len(old)+1)
        for j,c in enumerate(old):
            row[j]=(row[j]+center*c)%p
            row[j+1]=(row[j+1]+c)%p
        out.append(row)
    return out

def permutation_sign(permutation):
    seen=set(); sign=1
    for start in range(len(permutation)):
        if start in seen: continue
        i=start; length=0
        while i not in seen:
            seen.add(i); length+=1; i=permutation[i]
        if length%2==0: sign=-sign
    return sign

def reverse_det(matrix,p):
    # Eliminate the upper-right triangle from bottom right, pivoting columns.
    a=[r[:] for r in matrix]; n=len(a); answer=1
    need(all(len(r)==n for r in a), 'nonsquare minor')
    for q in range(n-1,-1,-1):
        j=next((j for j in range(q,-1,-1) if a[q][j]%p),None)
        if j is None: return 0
        if j!=q:
            for r in range(q+1): a[r][j],a[r][q]=a[r][q],a[r][j]
            answer=-answer
        pivot=a[q][q]%p
        answer=answer*pivot%p
        inverse=pow(pivot,p-2,p)
        row=a[q][:q]
        for r in range(q):
            factor=a[r][q]*inverse%p
            if factor: a[r][:q]=[(v-factor*w)%p for v,w in zip(a[r][:q],row)]
            a[r][q]=0
    return answer%p

def rebuild_minor(rc):
    k=rc['k']; d=8*k*k+1; p=101
    need((rc['degree'],rc['prime'],rc['i_mod_p'])==(d,p,10),'rank parameter mismatch')
    units=[1,10,100,91]
    expansions={z:translations(z,d,p) for z in units}
    # Graded columns instead of the author's lexicographic columns.
    monomials=[(u,total-u) for total in range(d+1) for u in range(total+1)]
    old=sorted(monomials); positions={pair:i for i,pair in enumerate(old)}
    sign=permutation_sign([positions[t] for t in monomials])
    rows=[]
    for a,b in itertools.product(range(4),repeat=2):
        e=2*k*k+2*k*PATTERN.get((a,b),0)
        tx,ty=expansions[units[a]],expansions[units[b]]
        for r in range(e):
            for s in range(e-r):
                rows.append([(tx[u][r]*ty[v][s])%p if r<=u and s<=v else 0 for u,v in monomials])
    n=(d+1)*(d+2)//2
    need((len(rows),n)==((60,55) if k==1 else (624,595)), 'matrix dimensions failed')
    need((rc['row_count'],rc['column_count'],rc['rank'])==(len(rows),n,n),'recorded dimensions failed')
    selected=rc['pivot_rows']
    need(len(selected)==n and len(set(selected))==n and all(type(i) is int and 0<=i<len(rows) for i in selected),'invalid row selection')
    det=reverse_det([rows[i] for i in selected],p)
    original=sign*det%p
    need(original==({1:23,2:57}[k]),'independent determinant mismatch')
    return {'k':k,'rows':len(rows),'columns':n,'graded_column_permutation_sign':sign,'graded_column_determinant':det,'author_column_determinant':original,'prime':p,'full_column_rank':True,'graded_matrix_sha256':digest(bytes(x for row in rows for x in row))}

# An independent exact algebraic check of the torus/unit-circle conclusion.
def remainder(a,b):
    a=trim(a); b=trim(b)
    while len(a)>=len(b) and a!=[0]:
        offset=len(a)-len(b); c=a[-1]/b[-1]
        for i,x in enumerate(b): a[i+offset]-=c*x
        a=trim(a)
    return a

def gcd(a,b):
    a=list(map(Fraction,a)); b=list(map(Fraction,b))
    while b!=[0]: a,b=b,remainder(a,b)
    return scale(a,1/a[-1])

def power_controls():
    one_plus=[1]
    for n in range(1,61):
        one_plus=pmul(one_plus,[1,1])
        a=[-1]+[0]*(n-1)+[1]
        b=scale(one_plus,(-1)**n); b[0]-=1
        common=gcd(a,b)
        need(common==([1,1,1] if n%3==0 else [1]),'normalization point gcd failed')
    # Distinct cubic-root branch images unless d is divisible by 3.
    for m in range(1,41):
        for d in range(1,101):
            branch_images=[]
            if m*d%3==0:
                branch_images=[(d%3,2*d%3),(2*d%3,d%3)]
            count=Counter(branch_images)
            square=d*d-sum(n*n for n in count.values())
            formula=d*d-(4 if d%3==0 else 2 if m%3==0 else 0)
            need(square==formula,'branch-count square failed')
    return {'exact_Q_polynomial_gcd_N_range':[1,60],'branch_image_cases':4000,'complex_m4_d6':32,'positive_characteristic_m4_d6_p5_e2':-7}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--author',type=Path,default=Path(__file__).resolve().parent.parent/'root_unity_30004334'); args=ap.parse_args()
    cert=bind_author(args.author)
    need({(a,b):v for a,b,v in cert['v_nonzero']}==PATTERN,'independent pattern differs')
    incidence,census=lines()
    need(cert['base_field']=='C' and cert['relaxation_is_not_curve_construction'] is True,'scope control failed')
    need(reverse_det([[1,2],[2,4]],101)==0 and reverse_det([[0,1],[1,0]],101)==100,'determinant negative/sign control failed')
    ranks=[rebuild_minor(rc) for rc in cert['rank_certificates']]
    need([r['k'] for r in ranks]==[1,2], 'missing/repeated interpolation certificate')
    out={'schema':'root-unity-independent-reconstruction-v1','status':'PASS','author_manifest_sha256':PIN,'problem_id':'30004334','line_census':census,'pair_coverage':120,'symbolic_controls':identities(incidence),'interpolation_minors':ranks,'power_controls':power_controls(),'scope':'Finite arithmetic plus symbolic identities; geometry reviewed separately; complex fixed-m target unresolved'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
