#!/usr/bin/env python3
"""Offline F3[t] module diagnostics and exact-source closure; no service calls.

Polynomial coefficients are compared, never only the three F3 group values.
Torus characters and dimensions remain integers. Written proof is decisive.
"""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
COUNTS={}
ONE={0:1}


def require(x,label):
    if not x:raise RuntimeError(label)


def count(label):COUNTS[label]=COUNTS.get(label,0)+1


def readj(name):return json.loads((BASE/name).read_text())


def sha(b):return hashlib.sha256(b).hexdigest()


def pa(*xs):
    out={}
    for x in xs:
        for d,c in x.items():out[d]=(out.get(d,0)+c)%3
    return {d:c for d,c in out.items() if c}


def ps(x,c):return {d:(a*c)%3 for d,a in x.items() if (a*c)%3}


def pm(x,y):
    out={}
    for d,a in x.items():
        for e,b in y.items():out[d+e]=(out.get(d+e,0)+a*b)%3
    return {d:c for d,c in out.items() if c}


def spmul(f,g):
    out={}
    for e,p in f.items():
        for d,q in g.items():
            key=tuple(a+b for a,b in zip(e,d));out[key]=pa(out.get(key,{}),pm(p,q))
    return {e:p for e,p in out.items() if p}


def action(images,basis):
    dim=len(images);columns=[]
    for exps in basis:
        f={(0,)*dim:ONE}
        for image,power in zip(images,exps):
            for _ in range(power):f=spmul(f,image)
        require(all(e in basis for e in f),'homogeneous action basis')
        columns.append([f.get(e,{}) for e in basis])
    return [[columns[j][i] for j in range(len(basis))] for i in range(len(basis))]


def linear_images(a):
    n=len(a);out=[]
    for j in range(n):
        out.append({tuple(int(i==k) for k in range(n)):a[i][j] for i in range(n) if a[i][j]})
    return out


def transpose(a):return [list(x) for x in zip(*a)]


def pmatmul(a,b):
    return [[pa(*(pm(a[i][k],b[k][j]) for k in range(len(b)))) for j in range(len(b[0]))] for i in range(len(a))]


def const(a):return [[{0:x%3} if x%3 else {} for x in row] for row in a]


def rank(a,n=None):
    if n is None:n=len(a[0]) if a else 0
    a=[[x%3 for x in row] for row in a];pivot=0
    for col in range(n):
        r=next((i for i in range(pivot,len(a)) if a[i][col]),None)
        if r is None:continue
        a[pivot],a[r]=a[r],a[pivot];inv=1 if a[pivot][col]==1 else 2
        a[pivot]=[(x*inv)%3 for x in a[pivot]]
        for i in range(len(a)):
            if i!=pivot and a[i][col]:
                c=a[i][col];a[i]=[(x-c*y)%3 for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==len(a):break
    return pivot


def coefficient_matrices(a):
    degree=max((d for row in a for p in row for d in p),default=0)
    return [[[p.get(d,0) for p in row] for row in a] for d in range(degree+1)]


def wrong(call,label):
    try:call()
    except RuntimeError:count('rejected_wrong_science')
    else:raise RuntimeError('wrong control escaped '+label)


def anchors():
    binding=readj('INPUT_BINDING.json')
    require(binding['head']=='d31d3b3cda1b56d9e85e3d5e07847355d1a6814f' and len(binding['files'])==8,'eight immutable files')
    for e in binding['files']:
        b=(BASE/e['local']).read_bytes()
        require(len(b)==e['bytes'] and sha(b)==e['sha256'],'PR bytes')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1'],'Git blob')
        count('authenticated_PR_blobs')
    for e in readj('AUTHENTICATED_INPUTS.json')['files']:
        b=(BASE/e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'local input '+e['path']);count('authenticated_local_inputs')
    for e in readj('ROOT_ANCHORS.json')['files']:
        b=(ROOT/e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'root anchor '+e['path']);count('authenticated_root_anchors')
    for e in readj('private/pr_source/MANIFEST.json')['files']:
        b=(BASE/'private/pr_source'/e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'submitted manifest')
    pins=readj('private/pr_source/SOURCE_PINS.json')['sources']
    names=['original.pdf','achar_sobaje.pdf','doty_henke.pdf','martin.pdf']
    for e,name in zip(pins,names):
        b=(BASE/'private/primary'/name).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'fresh primary '+name);count('exact_primary_matches')


def diagnostic():
    data=readj('CONTROL_INPUTS.json');basis_v=[tuple(x) for x in data['basis_v']];basis_w=[tuple(x) for x in data['basis_w']];basis_e4=[tuple(x) for x in data['basis_e4']]
    natural=[
        [{(1,0):ONE,(0,1):{1:1}},{(0,1):ONE}],
        [{(1,0):ONE},{(0,1):ONE,(1,0):{1:1}}],
    ]
    vs=[action(x,basis_v) for x in natural];ws=[action(linear_images(x),basis_w) for x in vs];four=[action(x,basis_e4) for x in natural]
    bv=data['form_v'];require(rank(bv)==3,'V form nondegenerate')
    pairs=data['basis_w_pairs'];cw=[]
    for i,j in pairs:
        cw.append([(bv[i][k]*bv[j][l]+bv[i][l]*bv[j][k])%3 for k,l in pairs])
    require(cw==data['form_w'] and rank(cw)==6,'induced W form nondeggenerate')
    m=data['multiplication'];q=data['q'];ell=data['ell'];weights=data['weights_w']
    require(rank(m)==5 and all(sum(a*b for a,b in zip(row,q))%3==0 for row in m),'multiplication kernel q')
    require(sum(a*b for a,b in zip(q,ell))%3==0,'all invariant functionals kill q')
    constraints=[];dual=[];endomorphism=[]
    for v,w,a4 in zip(vs,ws,four):
        require(pmatmul(pmatmul(transpose(v),const(bv)),v)==const(bv),'V form polynomial invariance')
        require(pmatmul(pmatmul(transpose(w),const(cw)),w)==const(cw),'W form polynomial invariance')
        require(pmatmul(const(m),w)==pmatmul(a4,const(m)),'multiplication intertwines entire algebraic root subgroup')
        for i,row in enumerate(w):require(pa(*(ps(p,q[j]) for j,p in enumerate(row)))==({0:q[i]%3} if q[i]%3 else {}),'q invariant polynomial')
        for j in range(6):require(pa(*(ps(w[i][j],ell[i]) for i in range(6)))==({0:ell[j]%3} if ell[j]%3 else {}),'ell invariant polynomial')
        cms=coefficient_matrices(w)
        for d,a in enumerate(cms):
            minus=[[x-(int(i==j) if d==0 else 0) for j,x in enumerate(row)] for i,row in enumerate(a)]
            constraints.extend(minus);dual.extend(transpose(minus))
            # Linear equations for every matrix entry in X*A-A*X.
            for i in range(6):
                for j in range(6):
                    row=[0]*36
                    for k in range(6):row[i*6+k]+=a[k][j];row[k*6+j]-=a[i][k]
                    endomorphism.append(row)
        count('entire_polynomial_root_actions')
    for i,weight in enumerate(weights):
        if weight!=0:
            row=[int(j==i) for j in range(6)];constraints.append(row);dual.append(row)
        for j,other in enumerate(weights):
            if weight!=other:
                row=[int(k==i*6+j) for k in range(36)];endomorphism.append(row)
    require(6-rank(constraints)==1 and 6-rank(dual)==1,'invariant vector/functional dimensions')
    require(36-rank(endomorphism)==2,'algebraic G endomorphism algebra dimension')
    n=[[q[i]*ell[j]%3 for j in range(6)] for i in range(6)]
    require(any(any(row) for row in n) and pmatmul(const(n),const(n))==const([[0]*6 for _ in range(6)]),'nonzero square-zero endomorphism')
    for w in ws:require(pmatmul(const(n),w)==pmatmul(w,const(n)),'radical commutes with root actions')
    count('local_endomorphism_algebra_check')
    orbit=transpose([[p.get(d,0) for row in ws[0] for p in [row[0]]] for d in range(5)])
    require(rank(transpose(orbit))==5,'lower orbit of a2 coefficient rank')
    require([(2*row[2])%3 for row in orbit]==[x%3 for x in q],'orbit t2 coefficient equals -q')
    count('elementary_indecomposability_orbit_check')
    # Exact torus exponents, with INTEGER character multiplicities.
    st=Counter(data['weights_v']);quotient=Counter(data['hypothetical_weights']);product=Counter()
    for a,x in st.items():
        for b,y in quotient.items():product[a+b]+=x*y
    require(product==Counter(weights) and product[0]==2,'integer character division; zero-weight dimension2 retained')
    require(Counter(weights)==Counter(data['weyl4_weights'])+Counter([0]),'Doty-Henke character cross-check')
    for a in quotient:
        for shift in [2,-2]:require(a+shift not in quotient,'root differential target absent at exact torus weight');count('exact_weight_shift_exclusions')
    require(2%3!=0 and all((3*a)%3==0 for a in data['hypothetical_weights']),'nonzero weight2 differential vs Frobenius-twist weights')
    # Countercheck why evaluating only t in F3 is insufficient: t^3-t
    # vanishes at all three samples and is not the zero polynomial.
    polynomial={3:1,1:2};require(all(sum(c*(a**d) for d,c in polynomial.items())%3==0 for a in range(3)) and polynomial!={},'finite group values are insufficient')
    count('finite_field_sampling_countercheck')
    st_square=Counter()
    for a,x in st.items():
        for b,y in st.items():st_square[a+b]+=x*y
    require(st_square[0]==3,'integer zero-weight dimension in St tensor St')
    wrong(lambda:require(st_square[0]==st_square[0]%3,'must not reduce formal dimensions to characteristic'),'integer character mod-p corruption')
    wrong(lambda:require(all(a%3==0 for a in quotient),'proposed weights are not Frobenius-twisted'),'false Frobenius escape')
    wrong(lambda:require((-2)-2==2,'exact integer weights not residues'),'false modular weight identification')
    wrong(lambda:require(sum(a*b for a,b in zip(q,ell))%3!=0,'invariant line cannot split'),'false direct-sum retraction')
    wrong(lambda:require({3:1,1:2}=={},'nonzero polynomial despite all F3 values zero'),'finite field sampling-as-proof')


def scope():
    d=readj('SCOPE_DISPOSITION.json')
    require(d['original_full_resolution_verified'] is False and d['module_obstruction_verified'] is True,'partial-original/full-obstruction distinction')
    require(d['geometric_full_essential_proof_reviewed'] is False,'do not promote statement match to proof audit')
    require(d['publication_ready'] is False and d['new_publication'] is False and d['root_adopted'] is False,'no readiness')
    require(not (BASE/'LITERAL_FOUR_CELL_PROPOSAL.json').exists(),'no full-solution accounting row')
    count('scope_no_overpromotion_guard')


def package():
    m=readj('MANIFEST.json');expected={e['path'] for e in m['files']};actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}-set(m['self_exclusions'])
    require(expected==actual,'closed package membership')
    for p in BASE.rglob('*'):require(not p.is_symlink(),'no package symlinks')
    for e in m['files']:
        b=(BASE/e['path']).read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'closed payload '+e['path'])
    require(sum(p.stat().st_blocks*512 for p in BASE.rglob('*') if p.is_file())<=25*1024**2,'25MiB cap')
    count('complete_closed_readback')


def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-package',action='store_true');p.add_argument('--deliberate-bad-guard',action='store_true');a=p.parse_args();anchors();diagnostic();scope()
    if a.deliberate_bad_guard:require(False,'deliberate optimization-safe failure')
    if a.verify_package:package()
    print(json.dumps({'status':'PASS','optimize':sys.flags.optimize,'checker_sha256':sha(Path(__file__).read_bytes()),'counts':COUNTS,'scope':'complete explicit module obstruction; partial original geometric question; no full-solution row','service_calls':0},sort_keys=True))


if __name__=='__main__':main()
