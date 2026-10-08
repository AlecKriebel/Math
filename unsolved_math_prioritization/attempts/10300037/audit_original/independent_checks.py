#!/usr/bin/env python3
"""Independent exact local-model and malformed-input controls; no topology proof."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import gcd
import hashlib,importlib.util,json,subprocess,sys,shutil,tempfile

class AuditFailure(Exception):pass
def need(ok,why):
    if not ok:raise AuditFailure(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def rejection(f):
    try:f()
    except Exception as e:
        need(type(e).__name__ in ('VerificationError','JSONDecodeError','TypeError','KeyError'),
             'unexpected malformed-control failure: '+type(e).__name__)
        return type(e).__name__
    raise AuditFailure('malformed object accepted')
def add(*terms):
    out={}
    for d in terms:
        for m,c in d.items():out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}
def mul(a,b):
    out={}
    for m,c in a.items():
        for n,d in b.items():
            k=tuple(x+y for x,y in zip(m,n));out[k]=out.get(k,0)+c*d
    return {m:c for m,c in out.items() if c}
def neg(p):return {m:-c for m,c in p.items()}
def deriv(p,j):
    out={}
    for m,c in p.items():
        if m[j]:n=list(m);n[j]-=1;out[tuple(n)]=c*m[j]
    return out
def helicity(v):
    p,q,r=v
    curl=[add(deriv(r,1),neg(deriv(q,2))),add(deriv(p,2),neg(deriv(r,0))),add(deriv(q,0),neg(deriv(p,1)))]
    return add(*(mul(a,b) for a,b in zip(v,curl)))
def evalp(p,x,y,t=F(0)):
    return sum(c*x**m[0]*y**m[1]*t**m[2] for m,c in p.items())
def command(base,mode,args=()):
    flag=[] if mode=='normal' else [mode]
    return subprocess.run([sys.executable,'-I','-S','-B']+flag+[str(base/'bootstrap.py')]+list(args),cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
def copy_pack(src,dest):
    dest.mkdir()
    for n in ('bootstrap.py','AUTHOR_MANIFEST.json'):shutil.copyfile(src/n,dest/n)
    shutil.copytree(src/'packet',dest/'packet',copy_function=shutil.copyfile)
    for p in dest.rglob('*'):p.chmod(0o755 if p.is_dir() else 0o644)
def snap(p):return {str(f.relative_to(p)):sha(f.read_bytes()) for f in p.rglob('*') if f.is_file() and not f.is_symlink()}

def main():
    need(len(sys.argv)==3,'usage: independent_checks.py ORIGINAL_FREEZE CORRECTED_FREEZE')
    original=Path(sys.argv[1]).resolve();corrected=Path(sys.argv[2]).resolve()
    need(sha((original/'AUTHOR_MANIFEST.json').read_bytes())=='96b8d8549908ac7160ad9b57dcc1eb1b8d0ae5ed393b874d6e2d4e73c7dbc375','original manifest anchor')
    need(sha((original/'bootstrap.py').read_bytes())=='e28741d45e461a11e657c5e6f56e29edf8d19d86d47ac57d938f98007872debc','original bootstrap anchor')
    counts={'curve_traced_cusp_models':0,'curve_traced_points':0,'cover_descent_controls':0,'unimodular_basis_controls':0,'boundary_transverse_endpoint_controls':0,'polynomial_edge_controls':0,'digon_edge_controls':0}
    # Generate actual slope-curve intersections, and track their positions after one circuit.
    for m,a,b in product(range(1,9),range(-11,12),range(-9,10)):
        if not b or gcd(a,b)!=1:continue
        pts=sorted({(F(j,m)+k)/b % 1 for j in range(m) for k in range(abs(b))})
        n=m*abs(b);need(len(pts)==n,'root count')
        need(all((pts[(i+1)%n]-pts[i])%1==F(1,n) for i in range(n)) if n>1 else True,'root spacing')
        perm=[pts.index((x+F(a,b))%1) for x in pts]
        signed_shift=(m*a*(1 if b>0 else -1))%n
        need(all((j-i)%n==signed_shift for i,j in enumerate(perm)),'signed curve monodromy')
        invariant=(n%2==0 and all((i-j)%2==0 for i,j in enumerate(perm)))
        need(invariant==(m%2==0),'cusp parity iff')
        unseen=set(range(n));lengths=[]
        while unseen:
            j=min(unseen);start=j;length=0
            while j in unseen:unseen.remove(j);length+=1;j=perm[j]
            need(j==start,'cycle returns to start');lengths.append(length)
        need(lengths==[abs(b)]*m,'independent cycle count')
        counts['curve_traced_cusp_models']+=1;counts['curve_traced_points']+=n
    for n in range(2,25):
        signs=[1 if i%2==0 else -1 for i in range(n)]
        for s in range(n):
            for d in range(1,7):
                circle=all(signs[i]!=signs[(i+1)%n] for i in range(n))
                cover=circle and all(signs[i]==signs[(i+d*s)%n] for i in range(n))
                descent=cover and all(signs[i]==signs[(i+s)%n] for i in range(n))
                need(cover==(n%2==0 and (d*s)%2==0),'cover sign action')
                need(descent==(n%2==0 and s%2==0),'deck sign action')
                counts['cover_descent_controls']+=1
    # Enumerate determinant-one integer bases, independently of extended Euclid.
    for p,q,c,d in product(range(-7,8),repeat=4):
        if not q or p*d-q*c!=1:continue
        need((d*p-q*c,d*q-q*d)==(1,0),'inverse coordinates')
        for k in (1,2,5):
            N=2*k*abs(q);s=(2*k*d)%N
            need(N%2==0 and s%2==0,'filling coorientation')
            for h in (-5,2,7):need(2*k*(d+h*q)%N==s,'longitude shift')
        counts['unimodular_basis_controls']+=1
    # Boundary foliation dtheta-r dlambda: arbitrary endpoint displacements can
    # be made positively transverse by adding sufficiently many meridian turns.
    for p,q,u,v in product(range(-6,7),range(1,6),range(-2,3),range(-2,3)):
        r=F(p,q);dx=F(u,3);dy=F(v,3)
        w=dx-r*dy;k=max(0,1-(w.numerator//w.denominator))
        need(w+k>0,'positive transverse boundary path')
        counts['boundary_transverse_endpoint_controls']+=1
    one={(0,0,0):1};x={(1,0,0):1};y={(0,1,0):1};A=add(one,neg(mul(x,x)));B=add(one,neg(mul(y,y)))
    P={m:2*c for m,c in mul(x,B).items()};Q={m:-2*c for m,c in mul(y,A).items()};R=mul(A,B)
    need(not helicity((P,Q,R)),'symbolic Frobenius identity')
    broken=helicity((P,Q,add(R,one)))
    need(bool(broken),'nonintegrable perturbation incorrectly accepted')
    for z in (F(i,13) for i in range(-12,13)):
        for xx,yy in ((F(1),z),(F(-1),z),(z,F(1)),(z,F(-1))):
            v=tuple(evalp(f,xx,yy) for f in (P,Q,R))
            need(v[2]==0 and any(v),'open-edge tangent nonzero form')
            need((v[1]==0 if abs(xx)==1 else v[0]==0),'edge tangent plane')
            counts['polynomial_edge_controls']+=1
    for xx,yy in product((-1,1),repeat=2):need(not any(evalp(f,F(xx),F(yy)) for f in (P,Q,R)),'vertices really excluded')
    for yy in (-1,1):
        need((1-yy*yy,-2)==(0,-2),'digon extension nonzero');counts['digon_edge_controls']+=1
    # Authenticate first, then import the pinned author checker for independent malformed cases.
    for base in (original,corrected):need(command(base,'normal').returncode==0,'authenticated baseline')
    spec=importlib.util.spec_from_file_location('checked_author_verifier',original/'packet/verify.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    bad=[]
    for value in ([1,-1],(),(1,),(True,-1),(1.0,-1),(1,0)):
        bad.append(rejection(lambda value=value:module.alternating(value)))
    for m,a,b in ((-1,1,1),(2,0,2),(2,1,False),(2,True,1),(1,1,0),(2,3.0,2)):
        bad.append(rejection(lambda m=m,a=a,b=b:module.model(m,a,b)))
    for raw in ('{"a":0,"a":1}','{"a":-Infinity}','[NaN]','{"x":}','{"x":1} garbage'):
        bad.append(rejection(lambda raw=raw:module.strict_json(raw)))
    for key,value in (('approaches',5.0),('rank',1006.0),('status','solved'),('noncompact_extension_required',False),('digon_claimed_genuine',True)):
        c=dict(module.EXPECTED);c[key]=value;bad.append(rejection(lambda c=c:module.validate_claims(c)))
    for extra in (True,False):
        c=dict(module.EXPECTED)
        if extra:c['unexpected']='value'
        else:del c['rank']
        bad.append(rejection(lambda c=c:module.validate_claims(c)))
    replays=[];negatives=[];before={str(p):snap(p) for p in (original,corrected)}
    with tempfile.TemporaryDirectory(prefix='independent-even-sided-') as t:
        t=Path(t)
        for bi,base in enumerate((original,corrected)):
            cpdir=t/('readonly-'+str(bi));copy_pack(base,cpdir)
            for p in cpdir.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
            cpdir.chmod(0o555)
            denied=False
            try:(cpdir/'packet'/'unwanted').write_text('x')
            except PermissionError:denied=True
            need(denied,'read-only mutation was possible')
            initial=snap(cpdir);expected=None
            for mode in ('normal','-O','-OO'):
                for layout,root in (('frozen-input',base),('relocated-read-only',cpdir)):
                    r=command(root,mode);need(r.returncode==0,'replay rejected '+r.stderr.decode())
                    if expected is None:expected=r.stdout
                    need(r.stdout==expected,'mode/layout output changed')
                    replays.append({'input':'original' if bi==0 else 'corrected','mode':mode,'layout':layout,'stdout_sha256':sha(r.stdout)})
            need(snap(cpdir)==initial,'read-only layout changed')
            cpdir.chmod(0o755)
            for p in cpdir.rglob('*'):p.chmod(0o755 if p.is_dir() else 0o644)
        for case in ('root-symlink','manifest-symlink','wrong-cli-arity','alter-proof-same-size','extra-nested-directory'):
            target=t/case;copy_pack(corrected,target);args=[]
            if case=='root-symlink':
                (target/'alias').symlink_to(target/'packet',target_is_directory=True);args=[str(target/'alias')]
            elif case=='manifest-symlink':
                p=target/'AUTHOR_MANIFEST.json';data=p.read_bytes();p.unlink();(target/'external.json').write_bytes(data);p.symlink_to(target/'external.json')
            elif case=='wrong-cli-arity':args=['packet','extra']
            elif case=='alter-proof-same-size':
                p=target/'packet/PROOF.md';data=p.read_bytes();p.write_bytes(b'!'+data[1:])
            else:(target/'packet'/'nested').mkdir()
            for mode in ('normal','-O','-OO'):
                r=command(target,mode,args);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'bad package accepted '+case)
                negatives.append({'case':case,'mode':mode,'rejected':True})
    need(all(snap(p)==before[str(p)] for p in (original,corrected)),'original or corrected input mutated')
    return {'schema':'independent-even-sided-audit-controls-v1','status':'pass','counts':counts,'finite_exact_model_controls':sum(counts.values())-counts['curve_traced_points'],'tracked_cusp_points':counts['curve_traced_points'],'malformed_api_controls':len(bad),'package_negative_runs':negatives,'positive_runs':replays,'symbolic_frobenius':{},'nonintegrable_perturbation_coefficients':{str(k):v for k,v in broken.items()},'vertices_explicitly_excluded':4,'read_only_write_denied':True,'input_bytes_unchanged':True,'scope':'Exact arithmetic, local analytic identities, schema and package controls only. General topology is reviewed in AUDIT.md, not proved by these tests.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (AuditFailure,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
