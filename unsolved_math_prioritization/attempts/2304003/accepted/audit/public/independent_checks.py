#!/usr/bin/env python3
"""Independent finite-identity and input-rejection checks; no analytic formalization."""
import copy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

ARCHIVE_SHA = '0e66432923a00ba78a2926096779430a0bbfb630edfcf299fcc20e77c6417989'
MANIFEST_SHA = '6ea1b356144ded0d39f7c7469f94ea7e8546de8e4bb440e36cce5e48d4661dd9'
BOOTSTRAP_SHA = 'caf367205cefac84461fbd5e270c3cad7548f4bb18bbb169857c42ca3f914196'
PINS_SHA = '4d164a991c90fa93d23a4349b6d90698ca29ff6ca0631d949fd546bdbb4d5781'
PUBLIC = {'README.md','REPORT.md','fixtures.json','provenance.json','sources.json','verify.py'}
EXTERNAL = {'AUDIT_INSTRUCTIONS.md','MANIFEST.json','PINS.json','TEST_RESULTS.json','bootstrap.py','test_harness.py'}

def require(ok, why):
    if not ok:
        raise RuntimeError(why)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def product(a,b):
    out = {}
    for i,x in a.items():
        for j,y in b.items():
            out[i+j] = out.get(i+j,0) + x*y
    return out

def cmul(x,y):
    return (x[0]*y[0]-3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])

def cadd(x,y):
    return (x[0]+y[0],x[1]+y[1])

def conjugate(x):
    return (x[0],-x[1])

def identities():
    energy = 0
    for n in range(2,129):
        for k in range(1,n):
            l = n-k
            require(k*k-n*k*(1-l) == k*l*(n-1), 'discriminant')
            require(k*(n-1)-l == n*(k-1), 'root at least one')
            energy += 1
    landau = 0
    c = [Q(1)]
    for j in range(1,97):
        c.append(c[-1]*Q(2*j-1,2*j))
    for r in range(97):
        square = product(dict(enumerate(c[:r+1])),dict(enumerate(c[:r+1])))
        require(all(square[j] == 1 for j in range(r+1)), 'Landau coefficient')
        landau += r+1
    fejer = {}
    multipliers = 0
    for s in range(97):
        raw = product({j:1 for j in range(s+1)}, {-j:1 for j in range(s+1)})
        for j in range(-s,s+1):
            require(Q(raw[j],s+1) == 1-Q(abs(j),s+1), 'Fejer multiplier')
            multipliers += 1
        p = {}
        for j in range(1,s+1,2):
            v = Q(s+1-j,j*(s+1))
            p[s-j] = -v
            p[s+j] = v
        lower = sum(Q(1,j) for j in range(1,s+1,2))-Q((s+1)//2,s+1)
        require(-sum(v for e,v in p.items() if e<s)==lower,'Fejer negative sum')
        require(len(p)==2*((s+1)//2),'Fejer terms')
        require(sum(p.values())==0,'Fejer value at one')
        fejer[s] = (p,lower)
    shifted = 0
    for d in range(2,131):
        for k in range(1,d):
            m = min(k,d-k)
            s = m-1
            p,b = fejer[s]
            shifted_p = {k-m+e:v for e,v in p.items()}
            require(all(0<=e<=d-2 for e in shifted_p),'shifted support range')
            require(-sum(v for e,v in shifted_p.items() if e<k)==b,'shifted cut')
            require(all((e<k)==(v<0) for e,v in shifted_p.items()),'cut selects negative block')
            shifted += 1
    for n in range(2,98,2):
        p,b = fejer[n-1]
        require(len(p)==n and sum(v<0 for v in p.values())==n//2,'exact even term count')
    numerator = {0:Q(2),1:Q(4),2:Q(-1)}
    norm = product(numerator,{-j:v for j,v in numerator.items()})
    require(norm=={0:Q(21),-1:Q(4),-2:Q(-2),1:Q(4),2:Q(-2)},'quadratic Laurent norm')
    slack = [Q(27)-norm[0]+2*norm[2],-2*norm[1],-4*norm[2]]
    require(slack == [2,-8,8],'quadratic square completion')
    omega = (Q(1,2),Q(1,2))
    u = (Q(1,2),Q(-1,6))
    require(cmul(omega,conjugate(omega))==(Q(1),Q(0)),'unit contact point')
    power = (Q(1),Q(0))
    p_at_contact = (Q(0),Q(0))
    for j,target in enumerate([1,1,0]):
        v = cmul(u,power)
        require(cadd(v,conjugate(v))==(Q(target),Q(0)),'dual coefficient')
        p_at_contact = cadd(p_at_contact,tuple(numerator[j]*x for x in power))
        power = cmul(power,omega)
    require(cmul(u,conjugate(u))==(Q(1,3),Q(0)),'dual mass')
    require(cmul(p_at_contact,conjugate(p_at_contact))==(Q(27),Q(0)),'norm contact')
    require(cmul(u,p_at_contact)==(Q(3),Q(0)),'dual alignment')
    require(Q((2+4)**2,27)==Q(4,3),'primal objective')
    r={0:1};s={0:1}
    rs_pairs=0
    for depth in range(10):
        n=2**depth
        rr=product(r,{-e:v for e,v in r.items()})
        ss=product(s,{-e:v for e,v in s.items()})
        require(all(rr.get(e,0)+ss.get(e,0)==(2*n if e==0 else 0) for e in set(rr)|set(ss)), 'complementary norm')
        require(len(r)==len(s)==n and all(v in [-1,1] for v in list(r.values())+list(s.values())), 'RS coefficients')
        require(sum(r.values())>=0 and sum(v==1 for v in r.values())>=Q(n,2),'positive subset')
        shifted_s={n+e:v for e,v in s.items()}
        r,s={**r,**shifted_s},{**r,**{e:-v for e,v in shifted_s.items()}}
        rs_pairs+=1
    require({e for e,v in r.items() if v>0} != set(range(sum(v>0 for v in r.values()))), 'RS positive set is scattered at final depth')
    return {'energy_cuts':energy,'landau_coefficients':landau,'fejer_multiplier_coefficients':multipliers,
            'fejer_polynomials_including_zero':len(fejer),'dense_shifted_cuts':shifted,
            'quadratic_primal_dual_certificates':1,'complementary_pairs':rs_pairs}

def rejection_tests(packet):
    fixture=(packet/'public'/'fixtures.json').read_bytes()
    original=json.loads(fixture)
    malformed=[]
    def add(label, path, value):
        obj=copy.deepcopy(original)
        dest=obj
        for key in path[:-1]:
            dest=dest[key]
        dest[path[-1]]=value
        malformed.append((label,json.dumps(obj,allow_nan=True).encode()))
    paths=[(k,) for k,v in original.items() if type(v) is int]
    paths += [('quadratic','normalization_squared'),('quadratic','cut')]
    paths += [('quadratic',key,j) for key in ['coefficients','slack_coefficients','objective_squared'] for j in range(len(original['quadratic'][key]))]
    for path in paths:
        name='.'.join(map(str,path))
        add('bool_'+name,path,True)
        add('float_'+name,path,1.0)
    for label,v in [('integer_overflow',10**100),('negative_overflow',-(10**100)),('null',None),('numeric_string','64'),('nan',float('nan')),('infinity',float('inf'))]:
        add(label,('energy_max_terms',),v)
    add('invalid_utf16_scalar',('status',),'\ud800')
    add('zero_denominator',('quadratic','objective_squared',1),0)
    add('negative_denominator',('quadratic','objective_squared',1),-3)
    add('noncanonical_rational',('quadratic','objective_squared'),[8,6])
    add('zero_claim',('quadratic','coefficients'),[0,0,0])
    add('false_objective',('quadratic','objective_squared'),[5,3])
    for field,lo,hi in [('energy_max_terms',2,100),('landau_max_index',1,100),('fejer_max_index',1,100),('rudin_shapiro_max_depth',1,12)]:
        add('below_min_'+field,(field,),lo-1)
        add('above_max_'+field,(field,),hi+1)
    token=b'"energy_max_terms": 64'
    for label,replacement in [('exponential_overflow',b'"energy_max_terms": 1e99999'),('oversized_decimal',b'"energy_max_terms": '+b'9'*5000),('nested_duplicate',b'"energy_max_terms": 64, "energy_max_terms": 64')]:
        require(token in fixture,'fixture token')
        malformed.append((label,fixture.replace(token,replacement)))
    malformed += [('truncated',fixture[:-2]),('trailing_document',fixture+b'{}'),('invalid_utf8',b'\xff'),('too_many_bytes',b' '*100001),('deep_nesting',b'['*10000+b'0'+b']'*10000)]
    modes=[]
    for mode in ['normal','O','OO']:
        flags=[] if mode=='normal' else ['-'+mode]
        cmd=[sys.executable,'-I','-B',*flags,str(packet/'public'/'verify.py'),'--stdin']
        results=[]
        for label,raw in malformed:
            r=subprocess.run(cmd,input=raw,capture_output=True,timeout=20)
            require(r.returncode!=0,'malformed accepted: '+label)
            structured=False
            try:
                structured=json.loads(r.stderr).get('ok') is False
            except (ValueError,AttributeError):
                pass
            require(not r.stdout,'failure produced success-like stdout: '+label)
            if label!='deep_nesting':
                require(structured,'unexpected unstructured error: '+label)
            results.append({'label':label,'exit_code':r.returncode,'structured_json_error':structured})
        valid=[]
        for label,bounds in [('minimum',(2,1,1,1)),('maximum',(100,100,100,12))]:
            obj=copy.deepcopy(original)
            for key,v in zip(['energy_max_terms','landau_max_index','fejer_max_index','rudin_shapiro_max_depth'],bounds):
                obj[key]=v
            r=subprocess.run(cmd,input=json.dumps(obj).encode(),capture_output=True,timeout=45)
            require(r.returncode==0 and json.loads(r.stdout)['ok'] is True,'valid boundary failed')
            valid.append({'label':label,'counts':json.loads(r.stdout)['counts']})
        modes.append({'mode':mode,'malformed_rejections':results,'valid_boundaries':valid})
    return modes

def main():
    require(len(sys.argv)==2,'usage: independent_checks.py PACKET_DIRECTORY')
    root=Path(sys.argv[1]).resolve()
    all_files={**{'public/'+n:(root/'public'/n).read_bytes() for n in PUBLIC},**{'external/'+n:(root/'external'/n).read_bytes() for n in EXTERNAL}}
    before={n:sha(b) for n,b in all_files.items()}
    require(sha((root/'bounded_partial_sums_2304003_frozen.tar.gz').read_bytes())==ARCHIVE_SHA,'archive pin')
    require(before['external/MANIFEST.json']==MANIFEST_SHA,'manifest pin')
    require(before['external/bootstrap.py']==BOOTSTRAP_SHA,'bootstrap pin')
    require(before['external/PINS.json']==PINS_SHA,'pins pin')
    with tarfile.open(root/'bounded_partial_sums_2304003_frozen.tar.gz','r:gz') as archive:
        members=archive.getmembers()
        require(len(members)==len(all_files),'archive member count')
        require({m.name for m in members}==set(all_files),'archive allowlist')
        for member in members:
            require(member.isfile() and not member.issym() and not member.islnk(),'archive nonregular entry')
            require(archive.extractfile(member).read()==all_files[member.name],'archive mismatch')
    computed=identities()
    rejections=rejection_tests(root)
    require(all(sha((root/n).read_bytes())==v for n,v in before.items()),'original modified')
    print(json.dumps({'ok':True,'source_documents_redistributed':False,'original_files_unchanged':True,
          'frozen_archive_sha256':ARCHIVE_SHA,'archive_members':len(all_files),'independent_identity_counts':computed,
          'modes':rejections,'known_diagnostic_limit':'Deep nesting is rejected with nonzero exit and no stdout; CPython RecursionError is not converted to JSON.',
          'analytic_proof_mechanized':False},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
