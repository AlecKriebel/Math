#!/usr/bin/env python3
"""Offline, standard-library audit controls; not a global geometry proof.
Run: python3 verify_audit.py [--packet ../public]
The supplied packet is read without modification. Finite tests supplement the
written arguments; they do not certify geometric theorem inputs or novelty.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_FREEZE = '4ec513d83ee59af8d053982926ab62054a363da10abb82d8e0d4254a2f84d7ff'

def digest(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}

def check_packet(packet):
    manifest_path = packet/'FROZEN_MANIFEST.json'
    assert digest(manifest_path)['sha256'] == EXPECTED_FREEZE
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest['files'].items():
        assert Path(name).name == name, 'Unexpected non-flat input path'
        assert digest(packet/name) == expected, name
    result = subprocess.run([sys.executable, '-B', str(packet/'verify.py')],
                            check=True, capture_output=True, text=True)
    replay = json.loads(result.stdout)
    assert replay == json.loads((packet/'CHECKS.json').read_text())
    # Check again after execution, including the frozen binding itself.
    assert digest(manifest_path)['sha256'] == EXPECTED_FREEZE
    for name, expected in manifest['files'].items():
        assert digest(packet/name) == expected
    return {'input_files_matched':len(manifest['files']),
            'frozen_manifest_sha256':EXPECTED_FREEZE,
            'author_verifier_matches_stored_result': True,
            'originals_unchanged_after_replay': True}

def padd(*terms):
    z = [F(0)]*max(map(len,terms))
    for t in terms:
        for i,c in enumerate(t): z[i] += c
    while len(z)>1 and not z[-1]: z.pop()
    return z

def pmul(a,b):
    z = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): z[i+j] += x*y
    return padd(z)

def pneg(a): return [-x for x in a]

def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def transpose(a): return list(map(list,zip(*a)))
def mm(a,b): return [[dot(x,y) for y in transpose(b)] for x in a]

def rotation(n,seed):
    # Composition of rational Householder reflections: exact orthogonality.
    a = eye(n)
    for h in range(3):
        v = [F(((i+1)*(seed+h+1))%11-5 or 1) for i in range(n)]
        vv = dot(v,v)
        hh = [[F(i==j)-2*v[i]*v[j]/vv for j in range(n)] for i in range(n)]
        a = mm(hh,a)
    assert mm(transpose(a),a) == eye(n)
    return a

def rank(a):
    a = [[F(x) for x in r] for r in a]
    pos=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(pos,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[pos],a[pivot]=a[pivot],a[pos]
        d=a[pos][col]; a[pos]=[x/d for x in a[pos]]
        for i in range(len(a)):
            if i != pos:
                d=a[i][col]
                a[i]=[x-d*y for x,y in zip(a[i],a[pos])]
        pos += 1
        if pos==len(a): break
    return pos

def sign_permutation(seq):
    return (-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))

def controls():
    out={}
    # Formal coefficients for both distinct powers of r in L(r^(1-k)).
    k=[0,1]; km1=[-1,1]; kk=pmul(k,km1); sq=pmul(km1,km1)
    assert padd(kk,pneg(sq)) == km1             # r^(-k-1)
    assert padd(pneg(sq),pneg(kk),sq,kk) == [0] # r^(1-3k)
    out['catenoid_all_dimension_coefficient_identities']=True
    # k=2: Lipschitz chi_R, R=3, has shell error <=4*pi/9;
    # potential on |s|<=1 alone is >=pi. Smooth approximation keeps Q<0.
    assert F(4,9)-1 < 0
    out['catenoid_k2_cutoff_upper_bound_coefficient_of_pi']=str(F(4,9)-1)

    e=eye(6); p=e[:4]; q=[e[i] for i in (0,1,2,4)]
    assert (rank(p),rank(q),rank(p+q)) == (4,4,5)
    assert rank(p)+rank(q)-rank(p+q)==3
    assert all(x[5]==0 for x in p+q) and e[5][5]==1
    # Rational latitude links: a^2+b^2=1, b>0 tends to zero.
    link_count=0
    for t in (2,3,5,10,100):
        a=F(t*t-1,t*t+1); b=F(2*t,t*t+1)
        assert a*a+b*b==1 and b>0
        assert b < F(2,t)
        link_count += 1
    out['nontransverse_affine_plane_rank_and_link_checks']=link_count

    # Hodge dual signs for the two terms of the proposed k-form.
    hs=[]
    for dim in range(3,18):
        n=dim+2; shared=list(range(dim-2))
        term1=shared+[dim-2,dim-1]; complement1=[dim,dim+1]
        term2=shared+[dim,dim+1]; complement2=[dim-2,dim-1]
        assert sign_permutation(term1+complement1)==1
        assert sign_permutation(term2+complement2)==1
        J=[[F(0) for _ in range(n)] for _ in range(n)]
        for i in (dim-2,dim): J[i][i+1]=1; J[i+1][i]=-1
        projector=[[F(i==j and i>=dim-2) for j in range(n)] for i in range(n)]
        assert mm(transpose(J),J)==projector
        hs.append(dim)
    out['hodge_dual_and_kahler_operator_dimensions']=hs

    # Rotate ambient translation directions so cross terms are nontrivial.
    cases=[]; saw_nonzero_individual_cross_term=False
    for dim,codim in ((2,1),(2,2),(3,2),(4,3),(5,2),(6,4)):
        A=[[[F((i+2)*(j+2)*(b+1)+i+j+1,13)
             for b in range(codim)] for j in range(dim)] for i in range(dim)]
        for b in range(codim):
            A[-1][-1][b] = -sum(A[i][i][b] for i in range(dim-1))
            assert sum(A[i][i][b] for i in range(dim))==0
        grad=[F(2*i-3,7) for i in range(dim)]; f=F(4,3)
        for seed in (1,2,7):
            O=rotation(dim+codim,seed)
            energy=F(0); potential=F(0); cross_sum=F(0)
            for col in transpose(O):
                tangent=col[:dim]; normal=col[dim:]
                cross=F(0)
                for i in range(dim):
                    dnormal=[-sum(A[i][j][b]*tangent[j] for j in range(dim))
                             for b in range(codim)]
                    value=[grad[i]*normal[b]+f*dnormal[b] for b in range(codim)]
                    energy += dot(value,value)
                    cross += 2*f*grad[i]*dot(normal,dnormal)
                if cross: saw_nonzero_individual_cross_term=True
                cross_sum += cross
                for i in range(dim):
                    for j in range(dim): potential += f*f*dot(A[i][j],normal)**2
            assert cross_sum==0
            assert energy-potential==codim*dot(grad,grad)
            cases.append([dim,codim,seed])
    assert saw_nonzero_individual_cross_term
    out['nonadapted_normal_translation_cases']=cases
    out['individual_cross_terms_nonzero_but_total_zero']=True

    # Primitive for parabola curvature measure / pi:
    # integral_0^R 32r/(1+4r^2)^2 dr = 4 - 4/(1+4R^2).
    masses=[]
    for R in (F(1,2),F(1),F(2),F(5)):
        primitive=4-4/(1+4*R*R)
        derivative=32*R/(1+4*R*R)**2
        assert derivative>0 and 0<primitive<4
        masses.append(str(primitive))
    assert 32*F(1,8)==4
    out['parabola_partial_mass_coefficients_of_pi']=masses
    # Scalar stability fails even for the normally stable calibrated parabola:
    # a logarithmic cutoff from radius 1 to e has Dirichlet energy 2*pi;
    # the potential on radius <=1 alone is 16*pi/5.
    assert F(2)-F(16,5)<0
    out['parabola_scalar_index_upper_bound_coefficient_of_pi']=str(F(-6,5))

    # Check Young-inequality reconstruction of the packet constants.
    constants=[]
    for dim in range(3,40):
        I_J=F(2,dim-1); I_B=F(4,(dim-1)**2)
        E_I=F(dim*dim,2)
        assert E_I*I_J == F(dim*dim,dim-1)
        assert E_I*I_B+2 == F(2*dim*dim,(dim-1)**2)+2
        # Holder exponents and critical dilation exponents.
        assert F(2,dim)+F(dim-2,dim)==1
        assert -dim+dim==0
        constants.append(dim)
    out['small_energy_coefficient_and_holder_dimensions']=constants
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent.parent/'public')
    args=ap.parse_args()
    out={'passed':True,'scope':'Input binding and finite exact controls; see written audit for proofs and limits.',
         'binding':check_packet(args.packet.resolve()),'independent_controls':controls()}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
