#!/usr/bin/env python3
"""Bounded exact checks of DMK partial lemmas; no general PDE solver."""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def reject(function, fragment):
    try:
        function()
    except (RuntimeError, ValueError) as exc:
        require(fragment in str(exc), 'unexpected rejection: '+str(exc))
        return
    raise RuntimeError('negative control accepted')


def exact(value):
    require(type(value) in (int, F), 'exact rational required')
    value = F(value)
    require(abs(value.numerator) <= 10**12 and value.denominator <= 10**12, 'rational size guard')
    return value


def dissipation(m, v):
    m, v = exact(m), exact(v)
    require(m > 0, 'positive density required')
    require(v >= -m, 'velocity domain violation')
    return v*v/(2*m)+v*v*v/(6*m*m)


# Coefficients are in increasing powers, and all operations are exact.
def poly(coefficients):
    require(1 <= len(coefficients) <= 64, 'polynomial size guard')
    p = [F(x) for x in coefficients]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    return poly([(p[i] if i < len(p) else 0)+(q[i] if i < len(q) else 0) for i in range(max(len(p),len(q)))])


def scale(p, c):
    return poly([x*c for x in p])


def mul(p, q):
    out = [F(0)]*(len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return poly(out)


def derivative(p):
    return poly([i*p[i] for i in range(1,len(p))] or [0])


def primitive(p):
    return poly([0]+[x/F(i+1) for i,x in enumerate(p)])


def value(p, x):
    answer = F(0)
    for c in reversed(p):
        answer = answer*x+c
    return answer


def integrate(p, a, b):
    P = primitive(p)
    return value(P,b)-value(P,a)


def sign(x):
    return int(x > 0)-int(x < 0)


def energy_and_dissipation_checks():
    counts = 0
    for m in [F(1,7),F(1),F(3,2),F(13)]:
        for g in [F(0),F(1,10),F(1,2),F(1),F(3,2),F(5)]:
            v=m*(g-1); xi=(g*g-1)/2
            r=dissipation(m,v)
            require(v/m+v*v/(2*m*m)==xi, 'reaction inclusion algebra')
            require(r==m*(g-1)**2*(g+2)/6, 'primal dissipation formula')
            dual=xi*v-r
            require(dual==m*(g-1)**2*(2*g+1)/6, 'dual dissipation formula')
            require(r+dual==m*(g-1)**2*(g+1)/2, 'energy dissipation sum')
            require(r>=v*v/(3*m) and (m+v)/(m*m)>=0, 'dissipation convexity or coercivity')
            Sprime=v*(1-g*g)/2
            require(Sprime==-(r+dual), 'Lyapunov derivative identity')
            counts += 1
    entropy=0
    for m in [F(1,9),F(1),F(3),F(17,4)]:
        for rho in [F(0),F(1,3),F(1),F(5)]:
            g=rho/m; S=(m+rho*rho/m)/2; R=m*(g-1)**2/2
            Hprime=(1-rho/m)*(rho-m)
            require(Hprime==rho-S-R, 'scalar comparator entropy identity')
            require(S-rho==(m-rho)**2/(2*m)==R, 'fixed flux energy gap')
            require((m-rho)**2==2*m*(S-rho), 'mass discrepancy equality')
            for s in [-1,1]:
                current=s*rho/m; optimal=s if rho else 0
                rhs=m*(current-optimal)**2/2+m*(1-optimal*optimal)/2
                require(S-rho==rhs, 'weighted potential decomposition')
            entropy += 1
    reject(lambda:dissipation(0,0),'positive density')
    reject(lambda:dissipation(-1,0),'positive density')
    reject(lambda:dissipation(1,-2),'velocity domain')
    reject(lambda:dissipation(1.0,0),'exact rational')
    reject(lambda:dissipation(True,0),'exact rational')
    reject(lambda:dissipation(10**13,0),'rational size')
    reject(lambda:poly([0]*65),'polynomial size')
    return dict(dissipation_states=counts,scalar_entropy_states=entropy,negative_controls=7)


def fixed_flux_checks():
    count=0
    for initial in [F(1,7),F(1),F(5)]:
        for flux in [F(-4),F(-1,3),F(0),F(1,3),F(4)]:
            rho=abs(flux)
            for decay in [F(1),F(3,4),F(1,2),F(1,1024)]:
                m=decay*initial+(1-decay)*rho
                require(m>0 and m>=decay*initial, 'finite time positivity')
                mt=-decay*(initial-rho); grad=flux/m
                require(m*grad==flux and mt==m*(abs(grad)-1), 'fixed flux PDE algebra')
                require(m-rho==decay*(initial-rho), 'exponential density error')
                if decay<=F(1,2):
                    require(abs(grad)<=2, 'dominated convergence bound')
                count += 1
    radial=0
    for d in range(2,10):
        h=poly([1,0,-F(d+2,d)])
        Q=poly([0,-F(1,d),0,F(1,d)])
        weight=poly([0]*(d-1)+[1])
        require(derivative(mul(weight,Q))==scale(mul(weight,h),-1), 'radial divergence identity')
        require(integrate(mul(weight,h),F(0),F(1))==0, 'radial forcing mean')
        require(value(Q,F(0))==value(Q,F(1))==0, 'radial boundary flux')
        for j in range(17):
            x=F(j,16);q=value(Q,x)
            require(q<=0 and abs(q)<=x/F(d), 'radial flux bound')
            m0=1+x*x;r=F(1,4);m=r*m0+(1-r)*abs(q)
            require(abs(q)-m==m*(abs(q/m)-1), 'radial reaction identity')
        radial += 1
    return dict(fixed_flux_states=count,radial_dimensions_checked=radial)


def degenerate_construction_checks():
    zero=poly([0]);one=poly([1]);a=F(1,4);b=F(1,2);c=F(3,4)
    rho=mul(mul(poly([-a,1]),poly([b,-1])),mul(poly([-a,1]),poly([b,-1])))
    w=mul(mul(poly([-c,1]),poly([1,-1])),mul(poly([-c,1]),poly([1,-1])))
    forcing=scale(derivative(rho),-1);wp=derivative(w)
    require(value(rho,a)==value(rho,b)==value(derivative(rho),a)==value(derivative(rho),b)==0, 'density gluing')
    require(integrate(forcing,a,b)==0, 'compact forcing mean')
    require(value(w,c)==value(w,F(1))==value(wp,c)==value(wp,F(1))==0, 'potential gluing')
    h=[poly([0,4]),one,poly([3,-4]),zero]
    densities=[zero,rho,zero,zero];perturbations=[zero,zero,zero,wp]
    edges=[F(0),a,b,c,F(1)]
    previous=F(0);V=[]
    for i,H in enumerate(h):
        P=primitive(H);P=add(P,poly([previous-value(P,edges[i])]))
        require(value(P,edges[i])==previous,'base primitive gluing')
        previous=value(P,edges[i+1]);V.append(P)
        require(mul(densities[i],H)==densities[i], 'active-set unit gradient')
        require(mul(densities[i],perturbations[i])==zero, 'inactive perturbation flux')
        require(mul(H,perturbations[i])==zero, 'gradient supports separated')
    meanV=sum(integrate(V[i],edges[i],edges[i+1]) for i in range(4))
    meanW=integrate(w,c,F(1));squareW=integrate(mul(w,w),c,F(1))
    require(meanW>0 and squareW-meanW*meanW>0, 'mean-zero perturbation must be nonconstant')
    require(sum(integrate(add(V[i],poly([-meanV])),edges[i],edges[i+1]) for i in range(4))==0,'base mean normalization')
    require(integrate(w,c,F(1))-meanW==0,'perturbation mean normalization')
    count=0
    for i in range(4):
        for j in range(17):
            x=edges[i]+(edges[i+1]-edges[i])*F(j,16)
            m=value(densities[i],x);H=value(h[i],x);W=value(perturbations[i],x)
            require(m>=0 and 0<=H<=1 and abs(W)<=F(1,128),'construction bounds')
            for amplitude in [F(-1),F(-1,2),F(0),F(1,2),F(1)]:
                grad=H+amplitude*W
                require(abs(grad)<=1 and m*(abs(grad)-1)==0, 'degenerate stationary reaction')
                require(m*grad==m, 'degenerate exact flux')
                count += 1
    return dict(polynomial_piece_identities=12,rational_point_states=count,perturbation_mean=str(meanW),perturbation_mean_zero_L2_squared=str(squareW-meanW*meanW),strict_positivity_satisfied=False)


def mathematics():
    return dict(energy=energy_and_dissipation_checks(),fixed_flux=fixed_flux_checks(),degenerate=degenerate_construction_checks())


def integrity():
    pins=json.loads((BASE/'PAYLOAD_PINS.json').read_text())
    require(pins.get('schema')==1,'unknown pins schema')
    files=pins.get('files');require(isinstance(files,list) and files,'missing pins')
    require(len({x['path'] for x in files})==len(files),'duplicate pins')
    require({p.name for p in BASE.iterdir() if p.name!='PAYLOAD_PINS.json'}=={x['path'] for x in files},'payload file set changed')
    for x in files:
        p=BASE/x['path'];require(p.parent==BASE and p.is_file() and not p.is_symlink(),'invalid payload path')
        data=p.read_bytes();require(len(data)==x['bytes'],'pinned byte count mismatch: '+x['path'])
        require(hashlib.sha256(data).hexdigest()==x['sha256'],'pinned hash mismatch: '+x['path'])
    status=json.loads((BASE/'STATUS.json').read_text())
    require(status['problem_id']==30003937 and status['outcome']=='exhausted' and status['substantive_proof_search_approaches']==5,'status drift')
    require(status['full_target_resolved'] is False and status['complete_candidate'] is False and status['novelty_claim'] is False,'unsupported promotion')
    manifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['source_bodies_in_payload'] is False,'source bodies forbidden')
    require(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(Path(__file__).read_text()))),'assert nodes forbidden')
    return dict(pinned_files=len(files),all_hashes_matched=True,no_assert_nodes=True)


def readonly_probes():
    require(os.geteuid()==1000,'read-only verification requires UID 1000')
    require(not os.access(BASE,os.W_OK),'packet directory is writable')
    p=BASE/('.write_probe_'+str(os.getpid()));require(not p.exists(),'write probe collision')
    try:
        fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except PermissionError:
        pass
    else:
        os.close(fd);p.unlink();raise RuntimeError('packet create unexpectedly succeeded')
    denied=0
    for p in BASE.iterdir():
        require(p.is_file() and not p.is_symlink(),'unexpected probe entry')
        require(not os.access(p,os.W_OK),'packet file is writable')
        try:
            fd=os.open(p,os.O_WRONLY)
        except PermissionError:
            denied+=1
        else:
            os.close(fd);raise RuntimeError('file write-open unexpectedly succeeded')
    return dict(directory_create_denied=True,existing_file_write_open_denials=denied,actual_write_probes=True)


def output_destination(value):
    p=Path(value).expanduser().resolve()
    require(p!=BASE and BASE not in p.parents,'output must be external to the packet')
    require(not p.exists(),'output already exists')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-readonly',action='store_true');parser.add_argument('--output')
    args=parser.parse_args();out=output_destination(args.output) if args.output else None
    ro=readonly_probes() if args.require_readonly else dict(actual_write_probes=False)
    result=dict(status='passed',uid=os.geteuid(),python_optimization=sys.flags.optimize,readonly_required=args.require_readonly,readonly=ro,checks=dict(integrity=integrity(),mathematics=mathematics()),limits='Bounded exact algebraic regression and integrity tests; not PDE existence, compactness, global convergence, or novelty certification.')
    data=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if out:
        with out.open('x') as f:
            f.write(data)
    else:
        sys.stdout.write(data)


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        sys.stderr.write(type(exc).__name__+': '+str(exc)+'\n');sys.exit(1)
