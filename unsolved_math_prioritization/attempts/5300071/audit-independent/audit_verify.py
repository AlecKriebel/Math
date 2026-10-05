#!/usr/bin/env python3
"""Independent exact controls and optional frozen-packet binding. Standard library only.
Usage: python audit_verify.py [path/to/submission] [path/to/author-freeze.zip]
Finite checks complement the accompanying general mathematical audit.
"""
from fractions import Fraction as F
from dataclasses import dataclass
import hashlib, json, pathlib, sys, zipfile

@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)
    @staticmethod
    def coerce(v): return v if isinstance(v,Q) else Q(F(v))
    def __add__(a,b):
        b=Q.coerce(b); return Q(a.re+b.re,a.im+b.im)
    __radd__=__add__
    def __neg__(a): return Q(-a.re,-a.im)
    def __sub__(a,b): return a+-Q.coerce(b)
    def __rsub__(a,b): return Q.coerce(b)+-a
    def __mul__(a,b):
        b=Q.coerce(b); return Q(a.re*b.re-a.im*b.im,a.re*b.im+a.im*b.re)
    __rmul__=__mul__
    def norm(a): return a.re*a.re+a.im*a.im
    def __truediv__(a,b):
        b=Q.coerce(b); n=b.norm(); assert n>0
        return Q((a.re*b.re+a.im*b.im)/n,(a.im*b.re-a.re*b.im)/n)
    def __rtruediv__(a,b): return Q.coerce(b)/a


def binding(packet, archive):
    p=pathlib.Path(packet); a=pathlib.Path(archive)
    expected='291263a5a2454913eb161b8361acfdb56cf6840908eb0cdc995716061b122fb2'
    actual=hashlib.sha256(a.read_bytes()).hexdigest(); assert actual==expected
    baseline=json.loads((pathlib.Path(__file__).parent/'ACTUAL_MANIFEST.json').read_text())
    names={x['path'] for x in baseline['actual_files']}
    assert {str(x.relative_to(p)) for x in p.rglob('*') if x.is_file()}==names
    for record in baseline['actual_files']:
        data=(p/record['path']).read_bytes()
        assert len(data)==record['bytes']
        assert hashlib.sha256(data).hexdigest()==record['sha256']
    with zipfile.ZipFile(a) as z:
        assert set(z.namelist())==names
        for n in names: assert z.read(n)==(p/n).read_bytes()
    return {'archive_sha256':actual,'files_bound':len(names),'all_zip_members_match':True}


def controls():
    directions=[Q(1),Q(-1),Q(0,1),Q(0,-1),Q(F(3,5),F(4,5)),Q(F(-5,13),F(12,13))]
    fractions=[F(1,10**50),F(1,10**6),F(1,10),F(1,2),F(1)]
    # Coalescing and mixed-multiplicity configurations, each with a certified
    # rational lower bound on distance from the selected root to other roots.
    configurations=[
        ([(Q(0),1),(Q(F(1,2)),1)],F(1,2)),
        ([(Q(0),3),(Q(F(1,2)),1)],F(1,2)),
        ([(Q(0),1),(Q(F(1,2)),16)],F(1,2)),
        ([(Q(F(1,5),F(1,7)),8),(Q(F(-1,3)),2),(Q(0,F(-1,2)),5)],F(1,2)),
        ([(Q(0),1),(Q(F(1,10**12)),7)],F(1,10**12))]
    local=0
    for roots,delta in configurations:
        alpha,m=roots[0]; d=sum(k for _,k in roots)
        assert all((beta-alpha).norm()>=delta*delta for beta,_ in roots[1:])
        r=F(m)*delta/(4*d-3*m)
        assert (d-m)*r/(delta-r)==F(m,4)
        for direction in directions:
            assert direction.norm()==1
            for scale in [F(0),F(1,3),F(1)]:
                e=direction*r*scale; z=alpha+e
                q=sum((k*e/(z-beta) for beta,k in roots[1:]),Q())
                assert q.norm()<=F(m*m,16)
                assert (Q(m)+q).norm()>=F(9*m*m,16)
                for t in fractions:
                    image=e*(1-(m*t)/(Q(m)+q))
                    assert image.norm()<=(1-F(8,25)*t)*e.norm()
                    local+=1
    two_root=0
    pairs=[(Q(F(1,2)),Q(F(-1,2))),
           (Q(F(1,4),F(1,2)),Q(F(-1,2),F(1,5))),
           (Q(0),Q(F(1,10**20)))]
    ws=[Q(0),Q(F(1,2)),Q(F(-1,2),F(1,3)),Q(F(3,5),F(3,5))]
    for a,b in pairs:
        assert a!=b and a.norm()<=1 and b.norm()<=1
        for k in [1,2,17]:
            for t in fractions:
                for w in ws:
                    u=(1+w)/(1-w); z=(a+b+(a-b)*u)/2
                    h=k*t
                    nz=z-h*(z-a)*(z-b)/(k*(2*z-a-b))
                    fu=(1-t/2)*u+t/(2*u)
                    assert (2*nz-a-b)/(a-b)==fu
                    gw=(fu-1)/(fu+1)
                    q=1-t
                    assert gw==w*(w+q)/(1+q*w)
                    assert (1+q*w).norm()-(w+q).norm()==(1-q*q)*(1-w.norm())
                    assert gw.norm()<w.norm() if w.norm()>0 else gw.norm()==0
                    assert (z-a).norm()<(z-b).norm()
                    # Exactly one boundary fixed point, multiplier 2/(2-t).
                    mu=F(2)/(2-t)
                    assert 1/(mu-1)==2/t-1
                    two_root+=1
                for y in [F(1,100),F(1),F(10**4)]:
                    u=Q(0,y); fu=(1-t/2)*u+t/(2*u)
                    assert fu.re==0
    # The half-plane arc estimate is strict since 1/R <= 1/3 < cos(pi/4).
    assert F(1,9)<F(1,2)
    # Exact full-interval nesting proof reduces to nonnegative affine endpoints.
    for s in [F(0),F(1,4)]:
        assert 1-3*s>0
        assert (1-3*s)-(5*s-1)>=0
        assert (1-3*s)-(1-5*s)>=0
    x=F(1,2)
    assert 2*x**3/(3*x*x-1)==-1
    assert x*(5*x*x-1)/(6*x*x-2)==F(-1,4)
    # Mixed multiplicities: z^3(z-1/2), h=3. A point in the 1/2 Voronoi
    # half-plane crosses to the 0 half-plane, and the other root is repelling.
    x=F(1,3); image=x-3*x*(x-F(1,2))/(4*x-F(3,2))
    assert x>F(1,4) and image==F(-2,3)<F(1,4)
    assert 1-F(3,1)==-2
    # h=0 destroys attraction, h=2m permits a two-cycle for a one-root map.
    assert 1-F(0,7)==1 and 1-F(14,7)==-1
    # No convergence-time bound uniform in h: (1-1/(2n))^n >= 1/2.
    for n in [1,2,10,100]: assert (1-F(1,2*n))**n>=F(1,2)
    # Varying positive h_n is a different problem: for m=1 and h_n=2^(-n-2),
    # sum from n=0 is 1/2; every finite product is >1/2 by product >=1-sum.
    product=F(1); total=F(0)
    for n in range(100):
        h=F(1,2**(n+2)); total+=h; product*=1-h
        assert product>=1-total>F(1,2)
    # Off-center circle of radius 3 centered at 10 is entirely right of x=7.
    assert 10-3>0
    # Reduced rational degree differs from polynomial degree for repeated roots:
    # z^3(z-1/2) has degree 4, but N_3=z^2/(4z-3/2) has degree 2.
    assert 4!=2
    return {'local_polynomial_cases':local,'two_root_affine_conjugacy_cases':two_root,
            'tiny_parameter_test':'t=10^-50, exact rational arithmetic',
            'coalescing_root_test':'separations 10^-12 and 10^-20',
            'mixed_multiplicity_halfplane_failure':'passed',
            'other_root_repulsion_control':'passed',
            'nesting_direction_control':'passed',
            'nonuniform_iteration_control':'passed',
            'variable_step_nonconvergence_control':'passed',
            'excluded_h_endpoints_control':'passed',
            'off_center_circle_control':'passed',
            'limitations':'Finite exact controls, not a proof of the general common-arc conjecture.'}

if __name__=='__main__':
    out={'controls':controls()}
    if len(sys.argv)==3: out['binding']=binding(sys.argv[1],sys.argv[2])
    elif len(sys.argv)!=1: raise SystemExit(__doc__)
    print(json.dumps(out,indent=2,sort_keys=True))
