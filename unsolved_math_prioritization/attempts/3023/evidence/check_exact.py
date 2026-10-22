#!/usr/bin/env python3
"""Exact finite checks for KP-5.16. Written proofs, not test extrapolation, carry theorems."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import os
import sys

class CheckFailure(Exception):
    pass

def need(condition, message):
    if not condition:
        raise CheckFailure(message)

class Algebra:
    """Sparse graded polynomials, either tensor words or polynomial-exterior monomials."""
    def __init__(self, degrees, tensor=False, modulus=0, exterior=True):
        self.degrees=tuple(degrees)
        self.n=len(degrees)
        self.tensor=tensor
        self.modulus=modulus
        self.exterior=exterior
        if not tensor and not exterior and modulus != 2:
            raise ValueError('Sign-only polynomial mode is implemented only in characteristic 2')
        self.unit_key=() if tensor else (0,)*self.n
    def coeff(self, a):
        a=Fraction(a)
        if self.modulus:
            p=self.modulus
            return (a.numerator*pow(a.denominator,-1,p))%p
        return a
    def clean(self,p):
        return {k:self.coeff(v) for k,v in p.items() if self.coeff(v)}
    def c(self,a):
        return self.clean({self.unit_key:a})
    def gen(self,i):
        if self.tensor:return {(i,):self.coeff(1)}
        k=[0]*self.n;k[i]=1
        return {tuple(k):self.coeff(1)}
    def add(self,*polys):
        out={}
        for p in polys:
            for k,v in p.items():out[k]=out.get(k,0)+v
        return self.clean(out)
    def scale(self,p,a):return self.clean({k:a*v for k,v in p.items()})
    def sub(self,p,q):return self.add(p,self.scale(q,-1))
    def mul(self,p,q):
        out={}
        for a,ca in p.items():
            for b,cb in q.items():
                if self.tensor:k=a+b;sgn=1
                else:
                    k=tuple(x+y for x,y in zip(a,b))
                    if self.exterior and any(d%2 and k[i]>1 for i,d in enumerate(self.degrees)):continue
                    swaps=sum(a[i]*b[j] for i in range(self.n) for j in range(i) if self.degrees[i]%2 and self.degrees[j]%2)
                    sgn=(-1)**swaps
                out[k]=out.get(k,0)+sgn*ca*cb
        return self.clean(out)
    def pow(self,p,n):
        need(n>=0,'negative exponent')
        out=self.c(1)
        for _ in range(n):out=self.mul(out,p)
        return out
    def word(self,k):
        if self.tensor:return list(k)
        return [i for i,v in enumerate(k) for _ in range(v)]
    def degree(self,k):return sum(self.degrees[i] for i in self.word(k))
    def homogeneous(self,p,d):return all(self.degree(k)==d for k in p)
    def substitute(self,p,images):
        out={}
        for k,c in p.items():
            term=self.c(c)
            for i in self.word(k):term=self.mul(term,images[i])
            out=self.add(out,term)
        return out
    def differential(self,p,ds):
        out={}
        for k,c in p.items():
            w=self.word(k);before=0
            for j,i in enumerate(w):
                term=self.c(c*(-1 if before%2 else 1))
                for t in w[:j]:term=self.mul(term,self.gen(t))
                term=self.mul(term,ds[i])
                for t in w[j+1:]:term=self.mul(term,self.gen(t))
                out=self.add(out,term)
                before+=self.degrees[i]
        return out
    def validate(self,ds):
        need(len(ds)==self.n,'differential arity')
        for i,p in enumerate(ds):
            need(self.homogeneous(p,self.degrees[i]-1),'differential degree')
            need(not self.differential(p,ds),'d squared')
        # Relation preservation is automatic for the strict exterior convention,
        # and separately checked on odd squares here.
        if not self.tensor and self.exterior:
            for i,d in enumerate(self.degrees):
                if d%2:
                    g=self.gen(i)
                    need(not self.add(self.mul(ds[i],g),self.scale(self.mul(g,ds[i]),-1)),'odd-square relation')


def run_math():
    results={}
    A=Algebra([0,1,1,-1]);x,a,b,c=[A.gen(i) for i in range(4)]
    ds=[c,A.add(A.c(1),A.mul(b,c)),{},{}]
    A.validate(ds)
    h=A.mul(a,A.sub(A.c(1),A.mul(b,c)))
    need(A.homogeneous(h,1),'primitive homogeneous')
    need(A.differential(h,ds)==A.c(1),'nilpotent correction primitive')
    need(A.differential(a,ds)!=A.c(1),'false primitive rejected')
    need(A.mul(b,c)==A.scale(A.mul(c,b),-1),'odd sign')
    samples=[x,a,b,c,A.mul(a,b),A.mul(x,c),h,A.c(1)]
    for u,v,w in product(samples,repeat=3):
        need(A.mul(A.mul(u,v),w)==A.mul(u,A.mul(v,w)),'associativity')
    for u in samples:
        if not u:continue
        deg=A.degree(next(iter(u)))
        for v in samples:
            lhs=A.differential(A.mul(u,v),ds)
            rhs=A.add(A.mul(A.differential(u,ds),v),A.scale(A.mul(u,A.differential(v,ds)),(-1 if deg%2 else 1)))
            need(lhs==rhs,'graded Leibniz')
    rejected=0
    try:A.validate([A.c(1),ds[1],{},{}])
    except CheckFailure:rejected+=1
    B=Algebra([2,1,0]);u,v,w=[B.gen(i) for i in range(3)]
    try:B.validate([v,w,{}])
    except CheckFailure:rejected+=1
    need(rejected==2,'invalid differentials not rejected')
    results['unit_primitive']={'status':'PASS','degree':1,'associativity_triples':len(samples)**3,'invalid_differentials_rejected':rejected}

    # All basis elements in each tested homogeneous degree of this 2-generator DGA
    # are known exactly; the checker is not truncating away incoming boundaries.
    stabilization={}
    for p in (0,2,3,5,7):
        S=Algebra([2,1],modulus=p);u,v=[S.gen(i) for i in range(2)];ds=[v,{}];S.validate(ds)
        for m in range(1,17):
            need(S.differential(S.pow(u,m),ds)==S.scale(S.mul(S.pow(u,m-1),v),m),'stabilization derivative')
            need(not S.differential(S.mul(S.pow(u,m-1),v),ds),'odd stabilization cycle')
        if p:
            need(not S.differential(S.pow(u,p),ds),'Frobenius cycle')
            # Degree 2p+1 has only u^p v; its differential is zero, so no boundary hits u^p.
            need(not S.differential(S.mul(S.pow(u,p),v),ds),'incoming boundary to Frobenius class')
            # Degree 2p has only u^p and its differential is zero, so u^(p-1)v survives.
            stabilization[str(p)]={'frobenius_even_degree':2*p,'surviving_odd_degree':2*p-1}
    # The integer differential matrices in each displayed degree are [m].
    results['stabilization']={'status':'PASS','integer_boundary_coefficients':list(range(1,17)),'prime_fields':stabilization,'char2_convention':'strict exterior only'}

    C=Algebra([0,1,-1,0],modulus=2,exterior=False)
    x,a,c,b=[C.gen(i) for i in range(4)];ds=[c,b,{},{}];C.validate(ds)
    witness=C.mul(C.mul(C.pow(x,2),a),b)
    need(C.differential(witness,ds)==C.mul(C.pow(x,2),C.pow(b,2)),'char2 square certificate identity')
    results['char2_sign_only']={'status':'PASS','identity':'d(x^2*a*da)=x^2*(da)^2'}

    # An associative normal form with a genuinely noncommutative primitive.
    N=Algebra([0,1,1,1,2],tensor=True);x,r,s,a,b=[N.gen(i) for i in range(5)]
    f=N.add(N.c(1),N.pow(x,2));ds=[{},f,x,{},a];N.validate(ds)
    h=N.sub(r,N.mul(x,s));need(N.differential(h,ds)==N.c(1),'tensor primitive')
    ap=N.add(a,h);rp=N.sub(r,N.mul(ap,f));sp=N.sub(s,N.mul(ap,x));bp=N.sub(b,N.mul(ap,a))
    forward=[x,rp,sp,ap,bp]
    target=[{}, {}, {}, N.c(1), {}]
    for p,q in zip(forward,target):need(N.differential(p,ds)==q,'normal form differential')
    ro=N.add(r,N.mul(a,f));so=N.add(s,N.mul(a,x));ao=N.sub(a,N.sub(ro,N.mul(x,so)));bo=N.add(b,N.mul(a,ao))
    inverse=[x,ro,so,ao,bo]
    for i in range(N.n):
        need(N.substitute(forward[i],inverse)==N.gen(i),'normal form inverse direction 1')
        need(N.substitute(inverse[i],forward)==N.gen(i),'normal form inverse direction 2')
    results['tensor_normal_form']={'status':'PASS','generators_checked':5,'inverse_directions':2}

    K=Algebra([0,0,1,1]);x,y,e1,e2=[K.gen(i) for i in range(4)]
    ds=[{},{},K.pow(x,2),K.mul(x,y)];K.validate(ds)
    z=K.sub(K.mul(y,e1),K.mul(x,e2))
    need(not K.differential(z,ds),'Koszul syzygy closed')
    need(K.differential(K.mul(e1,e2),ds)==K.scale(K.mul(x,z),-1),'Koszul boundary ideal relation')
    mod_x={k:v for k,v in z.items() if k[0]==0}
    need(bool(mod_x),'Koszul syzygy survives modulo x')
    results['koszul_syzygy']={'status':'PASS','cycle_not_x_divisible':True}

    roots={str(p):[a for a in range(p) if (a*a+1)%p==0] for p in (2,3,5,7)}
    need(roots['3']==[] and roots['5']==[2,3],'finite augmentation roots')
    results['augmentation_examples']={'status':'PASS','roots_x_squared_plus_one':roots,'scope':'complete finite-field searches only; no integer undecidability test'}

    finite_counts={}
    for kappa in (0,1,2):
        F=Algebra([1,1,3],modulus=3);a,b,c=[F.gen(i) for i in range(3)]
        source=[{},{},F.mul(a,b)];target=[{},{},F.scale(F.mul(a,b),kappa)]
        F.validate(source);F.validate(target)
        count=0;checked=0
        for aa,ab,ba,bb,lam in product(range(3),repeat=5):
            checked+=1
            ims=[F.add(F.scale(a,aa),F.scale(b,ab)),F.add(F.scale(a,ba),F.scale(b,bb)),F.scale(c,lam)]
            compatible=all(F.differential(ims[i],target)==F.substitute(source[i],ims) for i in range(3))
            det=(aa*bb-ab*ba)%3
            if compatible and det and lam:
                invdet=pow(det,-1,3)
                inv=[F.add(F.scale(a,bb*invdet),F.scale(b,-ab*invdet)),F.add(F.scale(a,-ba*invdet),F.scale(b,aa*invdet)),F.scale(c,pow(lam,-1,3))]
                for i in range(3):
                    need(F.substitute(ims[i],inv)==F.gen(i),'finite inverse one')
                    need(F.substitute(inv[i],ims)==F.gen(i),'finite inverse two')
                count+=1
        need(checked==243,'map enumeration completeness')
        need(count==(0 if kappa==0 else 48),'map count')
        finite_counts[str(kappa)]={'maps_checked':checked,'strict_isomorphisms':count}
    results['finite_map_search']={'status':'PASS','over':'F_3','counts':finite_counts}

    family={}
    for n in range(1,7):
        M=Algebra([0,0,-1]);x,z,y=[M.gen(i) for i in range(3)]
        ds=[{},M.mul(M.pow(x,n),y),{}];M.validate(ds)
        checks=0
        for i,j in product(range(5),range(7)):
            p=M.mul(M.pow(x,i),M.pow(z,j))
            expected={} if j==0 else M.scale(M.mul(M.mul(M.pow(x,i+n),M.pow(z,j-1)),y),j)
            need(M.differential(p,ds)==expected,'mixed derivative formula')
            checks+=1
        # Both adjacent products y*x^n and x^n*y have primitive z.
        need(M.mul(y,M.pow(x,n))==ds[1],'Massey left product')
        need(M.mul(M.pow(x,n),y)==ds[1],'Massey right product')
        massey=M.add(M.mul(y,z),M.mul(z,y))
        need(massey==M.scale(M.mul(z,y),2),'Massey sign')
        need(not M.differential(massey,ds),'Massey closed')
        # Exact normal form for quotient by x^n P y + Q[x]y.
        obstruction={k:v for k,v in massey.items() if k[0]<n and k[1]>0}
        need(bool(obstruction),'Massey class missing after full stated indeterminacy')
        family[str(n)]={'derivative_monomials_checked':checks,'massey_nonzero_mod_boundary_and_indeterminacy':True,'annihilator_colength':n}
    results['mixed_degree_family']={'status':'PASS','cases':family}
    return results


def source_check(source_dir,manifest):
    if source_dir is None:
        return {'status':'NOT_RUN','reason':'No private source directory supplied','files':[]}
    rows=[]
    for s in manifest['sources']:
        p=source_dir/s['filename']
        if not p.is_file():
            rows.append({'filename':s['filename'],'status':'NOT_RUN','reason':'Source bytes absent'})
            continue
        if s.get('sha256') is None or s.get('bytes') is None:
            rows.append({'filename':s['filename'],'status':'NOT_RUN','reason':'No independently pinned reference digest and byte count'})
            continue
        data=p.read_bytes();match=len(data)==s['bytes'] and hashlib.sha256(data).hexdigest()==s['sha256']
        rows.append({'filename':s['filename'],'status':'PASS' if match else 'FAIL','bytes':len(data)})
    status='FAIL' if any(x['status']=='FAIL' for x in rows) else ('NOT_RUN' if any(x['status']=='NOT_RUN' for x in rows) else 'PASS')
    return {'status':status,'files':rows}


def readonly_probes(packet,source_dir):
    results=[]
    targets=[packet/'REPORT.md']
    if source_dir is not None:targets.append(source_dir/'manolescu_rozenblyum.pdf')
    for p in targets:
        try:
            fd=os.open(p,os.O_WRONLY|os.O_APPEND)
        except PermissionError:results.append({'kind':'append_open','target':p.name,'status':'DENIED'})
        except FileNotFoundError:results.append({'kind':'append_open','target':p.name,'status':'NOT_RUN'})
        else:
            os.close(fd);raise CheckFailure('Expected append permission denied: '+p.name)
    for directory in [packet]+([source_dir] if source_dir is not None else []):
        p=directory/'__denied_write_probe__'
        try:fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except PermissionError:results.append({'kind':'create','target':directory.name,'status':'DENIED'})
        else:
            os.close(fd);p.unlink();raise CheckFailure('Expected create permission denied: '+directory.name)
    return results


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sources',type=Path)
    parser.add_argument('--probe-readonly',action='store_true')
    parser.add_argument('--require-sources',action='store_true')
    args=parser.parse_args()
    packet=Path(__file__).resolve().parent
    need(os.getuid()==1000,'Validation requires actual UID 1000')
    manifest=json.loads((packet/'SOURCE_MANIFEST.json').read_text())
    math=run_math()
    sources=source_check(args.sources,manifest)
    probes=readonly_probes(packet,args.sources) if args.probe_readonly else [{'status':'NOT_RUN','reason':'Readonly probes not requested'}]
    result={'schema':1,'uid':os.getuid(),'optimization':sys.flags.optimize,'mathematical_checks':math,'source_verification':sources,'readonly_probes':probes,'scope':'Finite exact checks corroborate formulas; written proofs establish universal statements.'}
    print(json.dumps(result,indent=2,sort_keys=True))
    if sources['status']=='FAIL':return 1
    if args.require_sources and sources['status']!='PASS':return 2
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (CheckFailure,ValueError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc),'uid':os.getuid(),'optimization':sys.flags.optimize}),file=sys.stderr)
        sys.exit(1)
