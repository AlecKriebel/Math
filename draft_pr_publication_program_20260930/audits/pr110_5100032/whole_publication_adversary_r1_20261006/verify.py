#!/usr/bin/env python3
"""Portable, explicit-guard R1 controls (standard library, Python 3.10+).

No arguments: independently reconstruct rational half-angle chords, test finite
odd/star orbits numerically, and authenticate adjacent review receipts/manifest.
--package DIR: additionally authenticate the frozen candidate and external seal.
--audit-root DIR --journal-final FILE: additionally authenticate every input pin.
Finite exact and floating controls supplement the report's all-real argument.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import sys
import zipfile

HERE = Path(__file__).resolve().parent
COUNT = 0

def require(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)

def pin(p):
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def norm2(p):
    return sum(x*x for x in p)

def det(p,q):
    return p[0]*q[1]-p[1]*q[0]

def sub(p,q):
    return p[0]-q[0],p[1]-q[1]

def solver(A,B,f):
    u,v = sub(A,f),sub(B,f)
    ru,rv = norm2(u),norm2(v)
    d = det(u,v)
    require(d != 0, 'independent antipedal lines')
    z = ((ru*v[1]-rv*u[1])/d,(u[0]*rv-v[0]*ru)/d)
    require(sum(z[i]*u[i] for i in (0,1)) == ru, 'first defining line')
    require(sum(z[i]*v[i] for i in (0,1)) == rv, 'second defining line')
    return z

def trig(p):
    return (1-p*p)/(1+p*p),2*p/(1+p*p)

def exact_controls():
    cases,horizontal = 0,0
    signs = {-1:0,0:0,1:0}
    # Construct endpoints from independently selected midpoint/half-angle trig
    # values, rather than using candidate chord-generation or support coordinates.
    for aa,bb,cc in [(5,3,4),(13,5,12),(13,12,5),(17,8,15)]:
        a,b,c = F(aa),F(bb),F(cc)
        for p,t in itertools.product([F(-4),F(-3),F(-2),F(-3,2),F(-1),F(-3,4),F(-1,2),F(-1,4),F(0),F(1,4),F(1,3),F(1,2),F(3,4),F(1),F(3,2),F(2),F(3),F(4)],
                                     [F(1,8),F(1,4),F(1,2),F(2,3),F(3,4),F(7,8)]):
            C,S = trig(p); U,V = trig(t)
            d2 = C*C/(a*a)+S*S/(b*b)
            lam = V*V/d2
            if not 0 < lam < b*b:
                continue
            A = (a*(C*U+S*V),b*(S*U-C*V))
            B = (a*(C*U-S*V),b*(S*U+C*V))
            require(det(A,B)>0, 'left orientation around inner origin')
            require(U*U == (a*a-lam)*C*C/(a*a)+(b*b-lam)*S*S/(b*b), 'confocal tangency')
            H = {s:U-s*c*C/a for s in (1,-1)}
            require(H[1]>0 and H[-1]>0, 'positive focal heights')
            require(H[1]*H[-1] == (b*b-lam)*d2, 'known focal height product')
            qscaled={}
            for sigma in (1,-1):
                f=(sigma*c,F(0));rA=a-sigma*c*A[0]/a;rB=a-sigma*c*B[0]/a
                require(rA>0 and rB>0,'ordinary positive endpoint roots')
                require(rA*rA==norm2(sub(A,f)) and rB*rB==norm2(sub(B,f)), 'focal distances')
                R=rA*rB
                require(R==a*a*H[sigma]*H[sigma]+b*b*V*V,'independent half-angle product')
                z=solver(A,B,f)
                require(z==solver(B,A,f),'unoriented intersection under reversal')
                qscaled[sigma]=R/H[sigma]
                require(qscaled[sigma]>0 and norm2(z)==d2*qscaled[sigma]**2,'ordinary norm squared with positive root')
                # Exact polarity order and inverse-edge metric distinction.
                u,v=sub(A,f),sub(B,f)
                invu=tuple(x/norm2(u) for x in u);invv=tuple(x/norm2(v) for x in v)
                require(sum(z[i]*invu[i] for i in (0,1))==1 and sum(z[i]*invv[i] for i in (0,1))==1,'antipedal original = polar inverse')
                require(norm2(sub(invu,invv))==norm2(sub(u,v))/(rA*rB)**2,'inverse-edge metric')
            bracket=-a*a+b*b*lam/(b*b-lam)
            difference=qscaled[1]-qscaled[-1]
            require(difference==c*bracket*(B[1]-A[1])/(a*b*V),'exact positive-norm coboundary')
            require(difference==-c*bracket*(A[1]-B[1])/(a*b*V),'reversed coefficient')
            signs[(bracket>0)-(bracket<0)]+=1
            horizontal+=B[1]==A[1]
            cases+=1
    require(cases>100 and horizontal>0 and signs[-1]>0 and signs[1]>0,'material exact coverage')
    # A zero-coefficient four-cycle independently solved at lambda=225/34.
    cycle=[(F(5),F(0)),(F(0),F(3)),(F(-5),F(0)),(F(0),F(-3))]
    lam=F(225,34)
    require(-F(25)+F(9)*lam/(F(9)-lam)==0,'zero coefficient in interior domain')
    for A,B in zip(cycle,cycle[1:]+cycle[:1]):
        require(norm2(solver(A,B,(F(4),F(0))))==norm2(solver(A,B,(F(-4),F(0)))),'zero Gamma ordinary norms')
    # Exact rational-rotation obstruction to generic averaging and symmetry.
    # The positive analytic functions 2 +/- cos(2 pi N x) have equal integrals
    # and half-turn interchange, but at x=0 on step 1/N all cosine values=1.
    for N in (3,5,7,9):
        require(3*N != N, 'equal means do not imply every odd finite sum')
        require(N%2==1,'half-turn exchanges the chosen cosine functions')
    return {'rational_half_angle_cases':cases,'horizontal_cases':horizontal,'coefficient_sign_cases':{str(k):v for k,v in signs.items()},'zero_Gamma_cycle_edges':4}

def advance(theta,lam,a=5.,b=4.):
    C,S=math.cos(theta),math.sin(theta)
    aa=1-lam*(S*S/(a*a)+C*C/(b*b))
    bb=-2*lam*C*S*(1/(b*b)-1/(a*a))
    cc=-lam*(C*C/(a*a)+S*S/(b*b))
    require(aa>0 and cc<0,'positive unique half-angle branch')
    z=(-bb+math.sqrt(bb*bb-4*aa*cc))/(2*aa)
    return theta+2*math.atan(z)

def numerical_orbits():
    # Exploratory floating falsification controls, not interval certificates.
    results=[]
    for N,winding in [(3,1),(5,1),(5,2),(7,2),(7,3)]:
        theta0=.137;low,high=1e-9,16*(1-1e-12)
        for _ in range(72):
            lam=(low+high)/2;theta=theta0
            for _ in range(N):theta=advance(theta,lam)
            if theta-theta0<2*math.pi*winding:low=lam
            else:high=lam
        lam=(low+high)/2;theta=theta0;points=[]
        for _ in range(N):
            points.append((5*math.cos(theta),4*math.sin(theta)))
            theta=advance(theta,lam)
        closure=abs(theta-theta0-2*math.pi*winding)
        require(closure<1e-9,'odd/star closure residual')
        gamma=3/(20*math.sqrt(lam))*(-25+16*lam/(16-lam))
        sums={1:0.,-1:0.};max_edge_error=0.;max_reflection_error=0.
        for i,A in enumerate(points):
            B=points[(i+1)%N];prev=points[(i-1)%N]
            require(det(A,B)>0,'same-side all odd/star chords')
            q={}
            for sigma in (1,-1):
                # Direct floating linear solution, independent of edge formula.
                f=(sigma*3.,0.);u,v=sub(A,f),sub(B,f);d=det(u,v)
                ru,rv=norm2(u),norm2(v)
                Z=((ru*v[1]-rv*u[1])/d,(u[0]*rv-v[0]*ru)/d)
                q[sigma]=math.sqrt(norm2(Z));sums[sigma]+=q[sigma]
            residual=abs(q[1]-q[-1]-gamma*(B[1]-A[1]))
            max_edge_error=max(max_edge_error,residual)
            incoming=sub(A,prev);outgoing=sub(B,A)
            incoming=tuple(x/math.sqrt(norm2(incoming)) for x in incoming)
            outgoing=tuple(x/math.sqrt(norm2(outgoing)) for x in outgoing)
            normal=(A[0]/25,A[1]/16)
            dot=sum(incoming[j]*normal[j] for j in (0,1))
            reflected=tuple(incoming[j]-2*dot*normal[j]/norm2(normal) for j in (0,1))
            err=math.sqrt(norm2(sub(reflected,outgoing)))
            max_reflection_error=max(max_reflection_error,err)
        require(max_reflection_error<1e-8 and max_edge_error<1e-7,'regular odd/star reflection and identity')
        require(abs(sums[1]-sums[-1])<1e-7,'odd/star ordinary sums')
        require(abs(gamma)>1e-5,'nontrivial Gamma odd/star cases')
        for repeat,reverse in [(1,False),(2,False),(3,True)]:
            vertices=points*repeat
            if reverse:vertices=list(reversed(vertices))
            fs={1:0.,-1:0.}
            for i,A in enumerate(vertices):
                B=vertices[(i+1)%len(vertices)]
                for sigma in (1,-1):
                    u,v=sub(A,(sigma*3.,0.)),sub(B,(sigma*3.,0.));d=det(u,v)
                    z=((norm2(u)*v[1]-norm2(v)*u[1])/d,(u[0]*norm2(v)-v[0]*norm2(u))/d)
                    fs[sigma]+=math.sqrt(norm2(z))
            require(abs(fs[1]-fs[-1])<1e-6,'repeated/reversed odd/star sums')
        results.append({'primitive_period':N,'winding':winding,'lambda':lam,'Gamma':gamma,'closure_angle_error':closure,'max_edge_identity_error':max_edge_error,'max_reflection_error':max_reflection_error,'focal_sum_difference':sums[1]-sums[-1]})
    return results

def authenticate_review():
    for name in ('PACKAGE_VERIFICATION_NORMAL.json','PACKAGE_VERIFICATION_OPTIMIZED.json'):
        x=json.loads((HERE/name).read_bytes())
        require(x['status']=='passed' and x['directed_chord_cases']==1456 and x['explicit_passing_guard_checks']==63346,'fresh package replay counts')
        require(len(x['mandatory_invalid_controls'])==4 and all(y['rejected'] for y in x['mandatory_invalid_controls']),'four internal controls')
    e=json.loads((HERE/'PACKAGE_EXECUTION_ENVELOPE.json').read_bytes())
    require(len(e['operations'])==10 and e['required_failed_subprocess_controls']==8,'eight subprocess controls')
    for op in e['operations']:
        require(op['child_PID']>0 and op['UTC_start']<=op['UTC_end'],'fresh PID and UTC')
        if op['invalid_control'] is None:
            name='PACKAGE_VERIFICATION_OPTIMIZED.json' if op['optimization'] else 'PACKAGE_VERIFICATION_NORMAL.json'
            x=json.loads((HERE/name).read_bytes());q=pin(HERE/name)
            require(op['child_PID']==x['actual_verifier_PID'] and all(q[k]==op['stdout'][k] for k in q),'fresh output PID and full buffer binding')
        else:
            r=op['verified_rejection']
            expected={'coefficient':'coboundary: correct fixed coefficient','height':'norm: independent solver and focal height','sign':'norm: positive ordinary root','proof-binding':'binding: manuscript SHA256'}[op['invalid_control']]
            require(op['exit_code']==2 and op['stdout']['bytes']==0 and r['actual_verifier_PID']==op['child_PID'],'actual faulty subprocess')
            require(r['status']=='rejected' and r['reason']==expected and r['optimization_level']==int(op['optimization']),'exact faulty rejection mechanism')
            body=(json.dumps({'status':r['status'],'reason':r['reason'],'actual_verifier_PID':r['actual_verifier_PID'],'optimization_level':r['optimization_level']})+'\n').encode()
            require(len(body)==op['stderr']['bytes'] and hashlib.sha256(body).hexdigest()==op['stderr']['sha256'],'faulty stderr complete binding')
    m=HERE/'OUTPUT_MANIFEST.json'
    if m.exists():
        for entry in json.loads(m.read_bytes())['files']:
            require(pin(HERE/entry['path'])=={k:entry[k] for k in ('bytes','sha256')},'review output hash '+entry['path'])
        receipt=HERE/'SEAL_RECEIPT.json'
        if receipt.exists():require(pin(m)==json.loads(receipt.read_bytes())['manifest_pin'],'review external seal')

def authenticate_package(p):
    seal=p.parent/(p.name+'_SEAL.json')
    require(pin(seal)=={'bytes':6538,'sha256':'691ae196a8a18472bac50df9202477fb1eb48428091b27258a371fecdfc946c7'},'fixed external candidate seal')
    entries=json.loads(seal.read_bytes())['files'];names={i['path'] for i in entries}
    require({x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file()}==names,'candidate exact file set')
    for entry in entries:
        require(not (p/entry['path']).is_symlink(),'no payload symlink')
        require(pin(p/entry['path'])=={k:entry[k] for k in ('bytes','sha256')},'candidate full byte pin '+entry['path'])
    with zipfile.ZipFile(p/'focal_antipedal_sum_support.zip') as z:
        require(set(z.namelist())==names-{'focal_antipedal_sum_support.zip'} and len(z.namelist())==33,'ZIP member set')
        for name in z.namelist():require(z.read(name)==(p/name).read_bytes(),'ZIP complete member bytes '+name)
    binding=json.loads((p/'proof_binding.json').read_bytes())
    require(binding['path']=='focal_antipedal_sum.tex' and pin(p/binding['path'])=={k:binding[k] for k in ('bytes','sha256')},'exact portable manuscript binding')
    for n in ('PACKAGE_MANIFEST.json','source_payload_manifest.json'):
        manifest=json.loads((p/n).read_bytes())
        if n=='PACKAGE_MANIFEST.json':require({i['path'] for i in manifest['files']}==names-set(manifest['excluded']),'package manifest exact coverage')
        for entry in manifest['files']:
            require(pin(p/entry['path'])=={k:entry[k] for k in ('bytes','sha256')},'candidate manifest '+entry['path'])
    for line in (p/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);require(pin(p/name)['sha256']==digest,'SHA256SUMS '+name)
    meta=json.loads((p/'intended_zenodo_metadata.json').read_bytes())['metadata']
    require(meta==json.loads((p/'zenodo-deposit.json').read_bytes())['metadata'],'metadata exact agreement')
    require(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'creator and ORCID')
    require(meta['license']=='cc-by-4.0' and meta['version']=='1.0' and meta['publication_date']=='2026-10-06','license/version/date')

    # Preserve historic process envelopes while rechecking their byte/PID links.
    for base,en,nn,on in [(p,'execution_envelope.json','verification_normal.json','verification_optimized.json'),(p/'root_reproduction','root_execution_envelope.json','root_verification_normal.json','root_verification_optimized.json')]:
        envelope=json.loads((base/en).read_bytes())
        require(len(envelope['operations'])==10 and envelope['positive_runs']==2 and envelope['required_failed_subprocess_controls']==8,'historic envelope counts')
        for op in envelope['operations']:
            require(op['child_PID']>0 and op['UTC_start']<=op['UTC_end'],'historic PID/UTC coherence')
            if op['invalid_control'] is None:
                f=base/(on if op['optimization'] else nn);x=json.loads(f.read_bytes())
                require(x['actual_verifier_PID']==op['child_PID'] and op['exit_code']==0,'historic process/result PID')
                require(all(pin(f)[k]==op['stdout'][k] for k in ('bytes','sha256')),'historic complete output buffer')
                require(x['proof_sha256']==binding['sha256'],'historic exact manuscript binding')
            else:
                r=op['verified_rejection']
                body=(json.dumps({'status':r['status'],'reason':r['reason'],'actual_verifier_PID':r['actual_verifier_PID'],'optimization_level':r['optimization_level']})+'\n').encode()
                require(op['exit_code']==2 and r['actual_verifier_PID']==op['child_PID'] and len(body)==op['stderr']['bytes'] and hashlib.sha256(body).hexdigest()==op['stderr']['sha256'],'historic fault output buffer/PID')
    source_receipt=json.loads((p/'source_seal_receipt.json').read_bytes())
    require(pin(p/'source_payload_manifest.json')=={k:source_receipt['source_manifest'][k] for k in ('bytes','sha256')},'historic source seal manifest binding')


def authenticate_inputs(a,j):
    x=json.loads((HERE/'INPUT_PINS.json').read_bytes())
    for entry in x['inputs']:
        if entry['root']=='audit':p=a/entry['path']
        elif entry['root']=='journal_final':p=j
        else:raise RuntimeError('unknown input root')
        require(pin(p)=={k:entry[k] for k in ('bytes','sha256')},'reviewed input '+entry['path'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',type=Path)
    parser.add_argument('--audit-root',type=Path)
    parser.add_argument('--journal-final',type=Path)
    args=parser.parse_args()
    exact=exact_controls();numerical=numerical_orbits();authenticate_review()
    if args.package:authenticate_package(args.package)
    if args.audit_root:
        require(args.journal_final is not None,'journal final explicit location required')
        authenticate_inputs(args.audit_root,args.journal_final)
    print(json.dumps({'status':'passed','actual_verifier_PID':os.getpid(),'UTC':datetime.now(timezone.utc).isoformat(),'optimization_level':sys.flags.optimize,'explicit_guard_calls':COUNT,'exact_controls':exact,'floating_falsification_controls':numerical,'floating_scope':'Ordinary double-precision falsification controls; not interval-certified evidence.','package_authentication_requested':args.package is not None,'all_input_authentication_requested':args.audit_root is not None},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
