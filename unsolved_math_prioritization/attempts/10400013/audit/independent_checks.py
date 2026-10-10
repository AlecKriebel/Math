#!/usr/bin/env python3
"""Source-free independent exact algebra and adversarial replay; not a proof assistant."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile, zipfile

class AuditError(Exception): pass
COUNTS=Counter()
def check(ok,label):
    if not ok: raise AuditError(label)
    COUNTS[label.split(':')[0]]+=1

def digest(b): return hashlib.sha256(b).hexdigest()
def snap(p): return {str(f.relative_to(p)):(digest(f.read_bytes()),f.stat().st_mode & 0o777) for f in sorted(p.rglob('*')) if f.is_file()}
def freeze(p):
    for f in p.rglob('*'): f.chmod(0o555 if f.is_dir() else 0o444)
    p.chmod(0o555)
def thaw(p):
    p.chmod(0o755)
    for f in p.rglob('*'):
        if not f.is_symlink():f.chmod(0o755 if f.is_dir() else 0o644)
def invoke(base,mode,args=(),direct=False):
    flags=[] if mode=='normal' else [mode]
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(base/('packet/verify.py' if direct else 'bootstrap.py')),*map(str,args)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=90)

def poly(terms):
    out={}
    for e,c in terms:
        if not isinstance(e,tuple) or not all(type(j) is int for j in e):raise AuditError('Noninteger exponent')
        if type(c) not in (int,F):raise AuditError('Nonexact coefficient')
        out[e]=out.get(e,F(0))+F(c)
    return {e:c for e,c in out.items() if c}
def m(*e,c=1):return poly([(e,c)])
def add(*ps):return poly([(e,c) for p in ps for e,c in p.items()])
def scale(p,c):return poly([(e,c*v) for e,v in p.items()])
def mul(p,q):return poly([(tuple(x+y for x,y in zip(a,b)),c*d) for a,c in p.items() for b,d in q.items()])
def power(p,n):
    if n<0:
        if len(p)!=1:raise AuditError('Nonmonomial inversion')
        e,c=next(iter(p.items()));return poly([(tuple(x*n for x in e),c**n)])
    ans=m(*([0]*len(next(iter(p)))))
    for _ in range(n):ans=mul(ans,p)
    return ans
def subst(p,ims):
    out={}
    for e,c in p.items():
        r=m(*([0]*len(next(iter(ims[0])))),c=c)
        for x,im in zip(e,ims):r=mul(r,power(im,x))
        out=add(out,r)
    return out
def sp(p,k=0):return max(e[k] for e in p)-min(e[k] for e in p)
def ev(p,x):return sum(c*F(x)**e[0] for e,c in p.items())
def der(p,n=1):
    out=F(0)
    for e,c in p.items():
        for k in range(n):c*=e[0]-k
        out+=c
    return out

def exact_algebra():
    one=m(0);t=m(1)
    h=one
    for p in [add(t,scale(one,-1)),add(t,one),add(power(t,2),one),add(power(t,2),t,one),add(power(t,2),scale(t,-1),one)]:
        h=mul(h,power(p,2) if p in [add(t,scale(one,-1)),add(t,one)] else p)
    check(h==add(m(10),m(6,c=-1),m(4,c=-1),one),'formal:factorization')
    for n in [1,2,7,53,10**80]:
        j=add(one,scale(h,n))
        check(sp(j)==10 and ev(j,1)==1 and der(j)==0 and der(j,2)==48*n,'formal:large_exact_jones')
        check(ev(j,-1)==1,'formal:determinant')
    for a in [(1,),(-2,1,2),(10**90,1,-10**90),(1,-7,11,-4)]:
        shift=-sum(i*v for i,v in enumerate(a));p=poly([((shift+i,),v) for i,v in enumerate(a)])
        check(sum(a)==1 and ev(p,1)==1 and der(p)==0,'normalization:large_shifts')
        check(abs(shift)<=max(map(abs,a))*len(a)*(len(a)-1)//2,'normalization:bound')
    # Exact Burau replay covers inverse powers as well as positive powers.
    def mm(a,b):return [[add(*(mul(a[i][k],b[k][j]) for k in range(2))) for j in range(2)] for i in range(2)]
    ident=[[one,{}],[{},one]];s1=[[scale(t,-1),one],[{},one]];s2=[[one,{}],[t,scale(t,-1)]]
    delta=mm(mm(s1,s2),s1);check(delta==mm(mm(s2,s1),s2),'burau:relation')
    di=[[scale(x,1) for x in row] for row in delta];di=[[mul(x,m(-3)) for x in row] for row in di]
    check(mm(delta,di)==ident,'burau:inverse')
    for n in range(-13,14):
        powern=2*n+1;r=ident
        for _ in range(abs(powern)):r=mm(r,delta if powern>=0 else di)
        check(add(r[0][0],r[1][1])=={},'burau:all_odd_trace')
        v=add(m(6*n+1,c=-1),m(6*n+5,c=-1))
        check(sp(v)==4,'burau:half_integer_span_two')
    perm=(2,1,0);seen=set();cycles=0
    for i in range(3):
        if i in seen:continue
        cycles+=1
        while i not in seen:seen.add(i);i=perm[i]
    check(cycles==2,'burau:components')
    for s in range(45):
        for r in range(3,s+4):
            for q in range(r+1,s+4):
                gap=F(1,r)-F(1,q)
                check(F(1,(s+2)*(s+3))<=gap<=F(1,3),'interpolation:separation')
    for s in range(11):
        p=poly([((j,),(-1)**j*(10**35+j)) for j in range(s+1)]);out={};nodes=[F(2*j+1,3) for j in range(s+1)]
        for r in nodes:
            basis=one;den=F(1)
            for q in nodes:
                if q!=r:basis=mul(basis,add(t,scale(one,-q)));den*=r-q
            out=add(out,scale(basis,ev(p,r)/den))
        check(out==p,'interpolation:independent_rational_nodes')
    for c in range(1,31):
        for va in range(1,c+2):
            for vb in range(1,c+2):
                g=F(2+c-va-vb,2)
                if g<0 or g.denominator!=1:continue
                check(F(2*c+2*va+2*vb-4,4)==c-g,'adequate:span_genus')
        for j in range(1,c+1):
            check(c-2*j+2*(c+j-2-1)==c+2*c-6,'adequate:state_drop')
    d=add(m(2,c=-1),m(-2,c=-1));T=(t,m(-1));Ti=(m(-1),t)
    def tm(x,y):return (mul(x[0],y[0]),add(mul(x[0],y[1]),mul(x[1],y[0]),mul(mul(x[1],y[1]),d)))
    check(tm(T,Ti)==(one,{}),'twist:inverse')
    for n in range(-15,16):
        r=(one,{})
        for _ in range(2*abs(n)):r=tm(r,T if n>=0 else Ti)
        check(mul(d,r[0])==mul(d,m(2*n)) and mul(d,r[1])==add(m(-6*n),m(2*n,c=-1)),'twist:spectral')
    l=m(1,0);z=m(0,1);o=m(0,0)
    R=add(power(z,4),scale(power(z,2),4),scale(o,2),scale(power(l,2),-1),scale(power(l,-2),-1))
    S=add(power(z,2),scale(power(add(l,scale(power(l,-1),-1)),2),-1))
    hp=mul(mul(add(power(l,2),scale(o,-1)),power(z,2)),mul(R,S))
    TT=add(power(z,3),scale(z,-3),l,power(l,-1))
    fp=mul(mul(power(add(l,scale(power(l,-1),-1)),2),power(z,2)),power(TT,2))
    for n in (1,19,10**100):
        hpoly=add(o,scale(hp,n));fpoly=add(o,scale(fp,n))
        check((sp(hpoly),sp(hpoly,1))==(10,8),'specializations:homfly_support')
        check((sp(fpoly),sp(fpoly,1))==(8,8),'specializations:kauffman_support')
        check(subst(hpoly,[m(2),add(t,m(-1,c=-1))])==one,'specializations:homfly_jones')
        check(subst(hpoly,[one,t])==one,'specializations:homfly_alexander')
        check(subst(hpoly,[t,add(m(-1),scale(t,-1))])==one,'specializations:homfly_unit')
        check(subst(fpoly,[m(-3,c=-1),add(t,m(-1))])==one,'specializations:kauffman_jones')
        check(subst(fpoly,[one,t])==one,'specializations:kauffman_q')
        check(all(i%2==0 and j%2==0 for i,j in hpoly),'specializations:homfly_parity')
        check(all((i+j)%2==0 for i,j in fpoly),'specializations:kauffman_parity')
    for malformed in [[((0,),1.0)],[((0.5,),1)],[((True,),1)]]:
        caught=False
        try:poly(malformed)
        except AuditError:caught=True
        check(caught,'independent_engine:malformed')

def loadverifier(path):
    spec=importlib.util.spec_from_file_location('frozen_verifier',path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);return v

def replay(original,corrected):
    pins={'AUTHOR_MANIFEST.json':'a8e8ce66abc1366122e72cd8086b9cba999e04e05b9f8d1b7b41111d3a2fbcd6','bootstrap.py':'152ab44196e87e7660de8b4c16faf2c1475b5416c83fd3fdfbc520f57660e4ef','test_bootstrap.py':'011f4a4e76bcd40b0aa1fe79163f116d7d28df03c28468e3f315b69bf626c114'}
    for name,pin in pins.items():check(digest((original/name).read_bytes())==pin,'integrity:external_original_pin')
    check(os.getuid()!=0,'read_only:nonroot')
    modes=('normal','-O','-OO');receipts=[];snapshots=[snap(original),snap(corrected)]
    for label,base in [('original',original),('corrected',corrected)]:
        check(not (base.stat().st_mode&0o222),'read_only:directory_modes')
        denied=False
        try:(base/'packet'/'audit-write-probe').write_text('must fail')
        except PermissionError:denied=True
        check(denied,'read_only:write_denied')
        for mode in modes:
            r=invoke(base,mode);check(r.returncode==0,'replay:'+label+':'+mode);j=json.loads(r.stdout)
            check(j['status']=='PASS','replay:status');receipts.append({'layout':label,'mode':mode,'stdout_sha256':digest(r.stdout),'returncode':r.returncode})
    vo=loadverifier(original/'packet/verify.py');vc=loadverifier(corrected/'packet/verify.py')
    defects=0
    for sign in [-1,1]:
        for n in [-17,-2,-1]:
            a=vo.power({(1,):sign},n);b=vc.power({(1,):sign},n)
            check(any(type(x) is float for x in a.values()),'regression:original_float_reproduced');defects+=1
            check(all(type(x) is int for x in b.values()) and a==b,'regression:correction_exact_and_equal')
    # Instrument all cleaned polynomial arithmetic to reject nonexact values.
    oldclean=vc.clean
    def typedclean(p):
        check(all(type(c) in (int,F) for c in p.values()),'regression:exact_runtime_coefficients')
        return oldclean(p)
    vc.clean=typedclean;oldargs=sys.argv;sys.argv=['verify.py']
    try:result=vc.main()
    finally:sys.argv=oldargs
    check(result['checks']==32681,'regression:unchanged_diagnostic_count')
    claims=json.loads((corrected/'packet/CLAIMS.json').read_text());negatives=[]
    with tempfile.TemporaryDirectory(prefix='independent-fixed-span-') as td:
        td=Path(td);cases=[]
        for key,val in claims.items():
            altered=dict(claims);altered[key]=not val if type(val) is bool else None;cases.append(('wrong-'+key,json.dumps(altered)))
        cases += [('top-array','[]'),('top-null','null'),('bad-json','{'),('duplicate-key','{"schema":1,"schema":1}'),('nan','{"schema":NaN}'),('infinity','{"schema":Infinity}')]
        c=dict(claims);c['approaches']=5.0;cases.append(('float-as-integer',json.dumps(c)))
        c=dict(claims);c['traczyk_components']=True;cases.append(('boolean-as-integer',json.dumps(c)))
        c=dict(claims);c['new_field']=1;cases.append(('extra-key',json.dumps(c)))
        c=dict(claims);del c['rank'];cases.append(('missing-key',json.dumps(c)))
        for label,body in cases:
            p=td/'input.json';p.write_text(body)
            for mode in modes:
                r=invoke(corrected,mode,('--claims',p),True)
                check(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'malformed_claims:'+label+':'+mode);negatives.append({'case':label,'mode':mode})
        for label in ['packet-symlink','manifest-symlink','hidden-file','forged-proof','forged-executable']:
            base=td/label;shutil.copytree(corrected,base);thaw(base)
            if label=='packet-symlink':
                (base/'packet').rename(base/'actual');(base/'packet').symlink_to(base/'actual',target_is_directory=True)
            elif label=='manifest-symlink':
                (base/'AUTHOR_MANIFEST.json').rename(base/'actual.json');(base/'AUTHOR_MANIFEST.json').symlink_to(base/'actual.json')
            elif label=='hidden-file':(base/'packet/.hidden').write_text('extra')
            else:
                target=base/'packet'/('PROOF.md' if label=='forged-proof' else 'verify.py')
                target.write_text('False claim' if label=='forged-proof' else "raise RuntimeError('EXECUTED UNAUTHENTICATED')\n")
                manifest=json.loads((base/'AUTHOR_MANIFEST.json').read_text())
                for item in manifest['files']:
                    if item['path']==target.name:item.update(bytes=target.stat().st_size,sha256=digest(target.read_bytes()))
                (base/'AUTHOR_MANIFEST.json').write_text(json.dumps(manifest))
            for mode in modes:
                r=invoke(base,mode);check(r.returncode==1 and r.stderr.startswith(b'REJECT:') and b'EXECUTED UNAUTHENTICATED' not in r.stderr,'adversarial:'+label+':'+mode)
                negatives.append({'case':label,'mode':mode})
        rel=td/'relocated';shutil.copytree(corrected,rel);freeze(rel);before=snap(rel)
        try:
            for mode in modes:
                r=invoke(rel,mode);check(r.returncode==0,'relocated:'+mode)
                receipts.append({'layout':'corrected-relocated-read-only','mode':mode,'stdout_sha256':digest(r.stdout),'returncode':r.returncode})
            check(before==snap(rel),'relocated:bytes_modes_unchanged')
        finally:thaw(rel)
    check(snapshots==[snap(original),snap(corrected)],'integrity:both_freezes_unchanged')
    return {'original_float_regression_cases':defects,'positive_replays':receipts,'negative_replays':negatives,'negative_replay_count':len(negatives),'uid':os.getuid(),'read_only_write_denied':True,'both_freezes_unchanged':True}

def main():
    if len(sys.argv)!=3:raise AuditError('usage: independent_checks.py ORIGINAL_FREEZE CORRECTED_FREEZE')
    original,corrected=map(lambda x:Path(x).resolve(),sys.argv[1:]);exact_algebra();results=replay(original,corrected)
    return {'schema':'fixed-span-independent-checks-v1','status':'PASS','problem_id':10400013,'optimization':sys.flags.optimize,'checks':sum(COUNTS.values()),'categories':dict(COUNTS),**results,'scope':'Finite exact algebra, type regression, claim-boundary rejection and pinned replay. Not a general theorem prover, knot-realization certificate, or hostile concurrent-writer sandbox.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (AuditError,OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError) as e:print('AUDIT REJECT: '+str(e),file=sys.stderr);sys.exit(1)
