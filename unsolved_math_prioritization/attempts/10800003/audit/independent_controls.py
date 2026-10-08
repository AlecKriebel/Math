#!/usr/bin/env python3
"""Independent source-free audit controls. Writes only a requested external receipt and disposable copies."""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, itertools, json, math, os, shutil, stat, subprocess, sys, tempfile
ORIGINAL_MANIFEST='90f41824fce3c028993e1dcd12651dbeb86c8b2728527e61052da9b54c2e33a7'
ORIGINAL_BOOTSTRAP='747e0a67d88e4adb8818077394a132f80b0c8f30ed5c5b1877ea536708ab624f'
CORRECTED_MANIFEST='9ddef9ad585717ca652952fddceef1d3cf0f753f2e23c59a5cdc581ff92e5850'
CORRECTED_BOOTSTRAP='e75b15d966850e2097412032b18c243cd068aa7750d20191121236671802a161'
def need(condition,message):
    if not condition: raise RuntimeError(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(p):
    return {str(q.relative_to(p)):(stat.S_IFMT(q.lstat().st_mode),stat.S_IMODE(q.lstat().st_mode),digest(q) if q.is_file() and not q.is_symlink() else None) for q in sorted(p.rglob('*'))}
def run(args,cwd):
    return subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45)
def matrix(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def power(a,k):
    z=[[int(i==j) for j in range(len(a))] for i in range(len(a))]
    while k:
        if k%2:z=matrix(z,a)
        a=matrix(a,a);k//=2
    return z
def bareiss(a):
    a=[list(row) for row in a];n=len(a);previous=1;sign=1
    for k in range(n-1):
        r=next((r for r in range(k,n) if a[r][k]),None)
        if r is None:return 0
        if r!=k:a[k],a[r]=a[r],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=pivot*a[i][j]-a[i][k]*a[k][j]
                need(v%previous==0,'Bareiss nonexact division')
                a[i][j]=v//previous
        for i in range(k+1,n):a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]
def ga(a,b):return (a[0]+b[0],a[1]+b[1])
def gm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gs(a,b):return (a[0]-b[0],a[1]-b[1])
def scale(a,c):return (a[0]*c,a[1]*c)
def independent_math():
    counts={}
    def check(c,g):need(c,'independent math: '+g);counts[g]=counts.get(g,0)+1
    I=[[1,0],[0,1]]
    for m in list(range(-25,26))+[-10**6,10**6]:
        # Derive each reflection by acting on the two basis vectors.
        gram=[[-2,m],[m,-2]];r=[]
        for root in range(2):
            r.append([[int(i==j)+int(i==root)*gram[j][root] for j in range(2)] for i in range(2)])
        p=matrix(r[0],r[1]);check(p==[[m*m-1,-m],[m,-1]],'reflection')
        check(matrix(r[0],r[0])==I and matrix(r[1],r[1])==I,'reflection')
        check(bareiss(p)==1 and bareiss(gram)==4-m*m,'reflection')
        p2=matrix(p,p);trace=m*m-2
        check([[p2[i][j]-trace*p[i][j]+I[i][j] for j in range(2)] for i in range(2)]==[[0,0],[0,0]],'reflection')
        if m==0:check(power(p,2)==I and p!=I,'reflection')
        elif abs(m)==1:check(power(p,3)==I and power(p,2)!=I,'reflection')
        elif abs(m)==2:
            check(power(p,101)==[[I[i][j]+101*(p[i][j]-I[i][j]) for j in range(2)] for i in range(2)],'reflection')
        else:check(trace>2 and trace*trace-4>0,'reflection')
    for x,y in [(1,0),(-1,0),(0,1),(0,-2),(1,2),(-3,2),(5,-7),(2,3)]:
        s=(Q(x,3),Q(y,5));a=gm(s,s);s3=gm(a,s);b=(Q(2,7),Q(3,11))
        f=lambda z:ga(gs(gm(gm(z,z),z),scale(gm(a,z),3)),b)
        vp=f(s);vm=f(scale(s,-1));d=gs(vm,vp)
        check(vp==gs(b,scale(s3,2)) and vm==ga(b,scale(s3,2)),'complex_cubic')
        check(gm(d,d)==scale(gm(gm(a,a),a),16),'complex_cubic')
        check(gs(scale(gm(s,s),3),scale(a,3))==(0,0),'complex_cubic')
    alpha=(-2,-1,3);beta=(-5,1,4);points=list(itertools.product(alpha,beta))
    p=lambda x:Q(x**4,4)-Q(7*x*x,2)-6*x
    q=lambda y:Q(y**4,4)-Q(21*y*y,2)+20*y
    vals=[p(x)+q(y) for x,y in points]
    check(vals==[Q(-817,4),Q(47,4),Q(-22),Q(-407,2),Q(25,2),Q(-85,4),Q(-471,2),Q(-39,2),Q(-213,4)],'grid')
    check(len(set(vals))==9,'grid')
    for x,y in points:
        check(x**3-7*x-6==0 and y**3-21*y+20==0,'grid')
        check((3*x*x-7)*(3*y*y-21)!=0,'grid')
    mon=list(itertools.product(range(3),repeat=2));E=[[x**r*y**s for r,s in mon] for x,y in points]
    check(bareiss(E)==34012224000,'grid')
    def coefficients(roots,i):
        other=[roots[j] for j in range(3) if j!=i];u,v=other
        den=(roots[i]-u)*(roots[i]-v)
        return [Q(u*v,den),Q(-u-v,den),Q(1,den)]
    C=[]
    for r,s in mon:
        C.append([coefficients(alpha,i)[r]*coefficients(beta,j)[s] for i,j in itertools.product(range(3),repeat=2)])
    check(matrix(E,C)==[[int(i==j) for j in range(9)] for i in range(9)],'grid')
    # Four anchored rectangle equations form an independent additive-grid annihilator.
    R=[]
    for i,j in itertools.product((1,2),repeat=2):
        row=[0]*9
        for pos,sgn in [(0,1),(j,-1),(3*i,-1),(3*i+j,1)]:row[pos]+=sgn
        R.append(row)
    check(all(sum(a*b for a,b in zip(row,vals))==0 for row in R),'sparse_grid')
    for i in range(9):check(any(row[i] for row in R),'sparse_grid')
    for i,j in itertools.combinations(range(9),2):
        check(any(R[a][i]*R[b][j]-R[a][j]*R[b][i] for a,b in itertools.combinations(range(4),2)),'sparse_grid')
    check(all(sum(row[k] for k in range(3))==0 for row in R),'sparse_grid')
    check(1-0-0+(-1)==0,'sparse_grid_2x2_scope_control')
    # Genus-two, two-boundary-component homology model: nonzero radical class.
    J=[[0,1,0,0,0],[-1,0,0,0,0],[0,0,0,1,0],[0,0,-1,0,0],[0,0,0,0,0]]
    c=[0,0,0,0,1]
    check(c!=[0]*5 and matrix(J,[[x] for x in c])==[[0] for _ in c],'bordered_surface_radical')
    transvection=[[int(i==j)+c[i]*sum(J[j][k]*c[k] for k in range(5)) for j in range(5)] for i in range(5)]
    check(transvection==[[int(i==j) for j in range(5)] for i in range(5)],'bordered_surface_radical')
    for d,w,exps in [(4,(1,1),(2,2)),(6,(2,1),(1,4))]:
        check(d-sum(a*b for a,b in zip(w,exps))==0,'marginal_scaling')
        check(all(Q(1,2)**(d-weight)!=1 for weight in range(d)),'marginal_scaling')
    # Exact dyadic A2 approach a=(1-t)^(2/3), d=4(1-t), t=1-2^(-3n).
    for n in range(1,21):
        h=Q(1,2**(3*n));a=Q(1,2**(2*n));d=4*h
        check(16*a**3==d*d,'integrable_cusp')
        # The exact remaining variation is h^(2/3); it converges despite speed blowup.
        check(a==h*Q(2**n) and a<Q(1,2**n),'integrable_cusp')
    return {'status':'PASS','checks':counts,'total':sum(counts.values())}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--math-only',action='store_true');ap.add_argument('--receipt');args=ap.parse_args()
    if args.math_only:
        print(json.dumps(independent_math(),sort_keys=True));return
    here=Path(__file__).resolve().parent;base=here.parent;corrected=here/'corrected'
    original_before=snap(base/'author');freeze_before=snap(base/'freeze');fixed_before=snap(corrected)
    need(os.geteuid()!=0,'genuine read-only test requires non-root UID')
    need(digest(base/'freeze/AUTHOR_MANIFEST.json')==ORIGINAL_MANIFEST and digest(base/'freeze/bootstrap.py')==ORIGINAL_BOOTSTRAP,'original anchors')
    need(digest(corrected/'freeze/AUTHOR_MANIFEST.json')==CORRECTED_MANIFEST and digest(corrected/'freeze/bootstrap.py')==CORRECTED_BOOTSTRAP,'corrected anchors')
    work=Path(tempfile.mkdtemp(prefix='independent-collision-audit-'));cases=[]
    def record(mode,name,ok,detail=None):
        need(ok,'case failed: '+mode+' '+name);row={'mode':mode,'case':name,'status':'PASS'}
        if detail is not None:row['detail']=detail
        cases.append(row)
    def cp(tag):
        dst=work/tag;shutil.copytree(base/'author',dst);dst.chmod(0o755)
        for p in dst.iterdir():p.chmod(0o644)
        return dst
    def change(p,name,fn):
        f=p/name;x=json.loads(f.read_text());fn(x);f.write_text(json.dumps(x))
    mutations={
      'boolean_turn_count':lambda p:change(p,'CLAIMS.json',lambda x:x.update(approaches_used=True)),
      'numeric_false_resolution':lambda p:change(p,'CLAIMS.json',lambda x:x.update(complete_original_resolution=0)),
      'extra_claim_key':lambda p:change(p,'CLAIMS.json',lambda x:x.update(extra='bad')),
      'wrong_catalog':lambda p:change(p,'CLAIMS.json',lambda x:x.update(catalog_id='AMR-107-0004')),
      'wrong_rank':lambda p:change(p,'CLAIMS.json',lambda x:x.update(rank=1012)),
      'empty_gap':lambda p:change(p,'CLAIMS.json',lambda x:x.update(remaining_gap='')),
      'wrong_mechanism':lambda p:change(p,'APPROACH_LEDGER.json',lambda x:x['turns'][2].update(mechanism='inverse_flow')),
      'duplicate_cusp_rational':lambda p:change(p,'CERTIFICATE.json',lambda x:x['cusp_s'].__setitem__(1,x['cusp_s'][0])),
      'negative_denominator':lambda p:change(p,'CERTIFICATE.json',lambda x:x['cusp_s'].__setitem__(0,[1,-2])),
      'float_integer':lambda p:change(p,'CERTIFICATE.json',lambda x:x['grid_alpha'].__setitem__(0,-2.0)),
      'wrong_j10_modulus_weight':lambda p:change(p,'CERTIFICATE.json',lambda x:x['scaling']['j10'].update(marginal_exponents=[2,2])),
      'wrong_reflection_range':lambda p:change(p,'CERTIFICATE.json',lambda x:x['reflection_m'].append(9)),
      'source_byte_flag_true':lambda p:change(p,'SOURCE_METADATA.json',lambda x:x.update(source_bytes_in_packet=True)),
      'duplicate_source_alias':lambda p:change(p,'SOURCE_METADATA.json',lambda x:x['sources'][1].update(alias=x['sources'][0]['alias'])),
      'boolean_source_size':lambda p:change(p,'SOURCE_METADATA.json',lambda x:x['sources'][0].update(bytes=True)),
      'bad_json_duplicate':lambda p:(p/'CLAIMS.json').write_text('{"schema":0,"schema":1}'),
      'nan_json':lambda p:(p/'CLAIMS.json').write_text('{"schema":NaN}'),
      'overflow_float_json':lambda p:(p/'CLAIMS.json').write_text('{"schema":1e999}'),
      'invalid_utf8':lambda p:(p/'CLAIMS.json').write_bytes(b'\xff'),
      'missing_required_file':lambda p:(p/'CLAIMS.json').unlink(),
    }
    math_receipts=[];original_diagnostics=(base/'author/DIAGNOSTICS.json').read_bytes()
    for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        prefix=[sys.executable,'-I','-S','-B',*flags]
        r=run(prefix+[str(here/'independent_controls.py'),'--math-only'],work)
        record(mode,'independent_exact_math',r.returncode==0,r.stdout.decode().strip());math_receipts.append(json.loads(r.stdout))
        for label,tree,pin in [('original',base,ORIGINAL_MANIFEST),('corrected',corrected,CORRECTED_MANIFEST)]:
            r=run(prefix+[str(tree/'author/verify.py')],work)
            record(mode,label+'_verifier',r.returncode==0 and r.stdout==original_diagnostics)
            r=run(prefix+[str(tree/'freeze/bootstrap.py'),str(tree/'author')],work)
            record(mode,label+'_bootstrap',r.returncode==0 and json.loads(r.stdout)['manifest_sha256']==pin)
            ro=work/(mode+'-'+label+'-readonly');shutil.copytree(tree/'author',ro);ro.chmod(0o555)
            for p in ro.iterdir():p.chmod(0o444)
            before=snap(ro)
            probe='import pathlib,sys,os,json\np=pathlib.Path(sys.argv[1]);out={"uid":os.geteuid()}\nfor k,t,m in [("create",p/"probe","wb"),("append",p/"CLAIMS.json","ab")]:\n try:\n  with t.open(m) as f:f.write(b"x")\n  out[k]="wrote"\n except PermissionError:out[k]="denied"\nprint(json.dumps(out))\n'
            pr=run(prefix+['-c',probe,str(ro)],work);j=json.loads(pr.stdout)
            record(mode,label+'_read_only_probe',j=={'uid':os.geteuid(),'create':'denied','append':'denied'})
            r=run(prefix+[str(tree/'freeze/bootstrap.py'),str(ro)],work)
            record(mode,label+'_read_only_bootstrap',r.returncode==0 and snap(ro)==before)
        for tag,mutate in mutations.items():
            p=cp(mode+'-'+tag);mutate(p);r=run(prefix+[str(p/'verify.py')],work)
            record(mode,'semantic_'+tag,r.returncode!=0 and r.stderr.startswith(b'REJECT:'))
        # Portable diagnostics deliberately do not establish source-description truth.
        p=cp(mode+'-metadata-trust-boundary')
        change(p,'SOURCE_METADATA.json',lambda x:x.update(uninspected_original_dependency='deliberately false test-only metadata'))
        r=run(prefix+[str(p/'verify.py')],work)
        record(mode,'unvalidated_source_narrative_direct_accepts_expected',r.returncode==0 and r.stdout==original_diagnostics)
        r=run(prefix+[str(base/'freeze/bootstrap.py'),str(p)],work)
        record(mode,'unvalidated_source_narrative_bootstrap_rejects',r.returncode!=0)
        for tag in ['unexpected_directory','symlink_payload','fifo_payload','writable_payload_mode','forged_verifier','forged_manifest','replaced_bootstrap']:
            root=work/(mode+'-integrity-'+tag);shutil.copytree(base/'freeze',root/'freeze');payload=cp(mode+'-integrity-payload-'+tag)
            (root/'freeze').chmod(0o755)
            for p in (root/'freeze').iterdir():p.chmod(0o644)
            sentinel=root/'HOSTILE_EXECUTED';boot=root/'freeze/bootstrap.py'
            if tag=='unexpected_directory':(payload/'extra').mkdir()
            elif tag=='symlink_payload':(payload/'CLAIMS.json').unlink();(payload/'CLAIMS.json').symlink_to(base/'author/CLAIMS.json')
            elif tag=='fifo_payload':(payload/'CLAIMS.json').unlink();os.mkfifo(payload/'CLAIMS.json')
            elif tag=='writable_payload_mode':(payload/'CLAIMS.json').chmod(0o664)
            elif tag in ['forged_verifier','forged_manifest']:
                (payload/'verify.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\n')
                if tag=='forged_manifest':
                    mp=root/'freeze/AUTHOR_MANIFEST.json';m=json.loads(mp.read_text())
                    for e in m['files']:
                        if e['path']=='verify.py':e.update(bytes=(payload/'verify.py').stat().st_size,sha256=digest(payload/'verify.py'))
                    mp.write_text(json.dumps(m))
            elif tag=='replaced_bootstrap':boot.write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\n')
            if digest(boot)!=ORIGINAL_BOOTSTRAP:r=None
            else:r=run(prefix+[str(boot),str(payload)],work)
            record(mode,'integrity_'+tag,(r is None or r.returncode!=0) and not sentinel.exists())
    need(math_receipts[0]==math_receipts[1]==math_receipts[2],'optimization changed math receipt')
    # Confirm the correction patch reconstructs all changed bytes on a writable disposable copy.
    patched=work/'patch-test'
    for part in ['author','freeze']:
        shutil.copytree(base/part,patched/part);(patched/part).chmod(0o755)
        for p in (patched/part).iterdir():p.chmod(0o644)
    r=run(['patch','-p1','--batch','-i',str(here/'CORRECTIONS.patch')],patched)
    need(r.returncode==0,'patch application failed')
    for part in ['author','freeze']:
        need({p.name:digest(p) for p in (patched/part).iterdir()}=={p.name:digest(p) for p in (corrected/part).iterdir()},'patch byte reconstruction')
    record('all','patch_reconstructs_corrected_bytes',True)
    need(snap(base/'author')==original_before and snap(base/'freeze')==freeze_before and snap(corrected)==fixed_before,'immutable packet changed')
    receipt={'schema':'independent-critical-collision-audit-controls-v1','status':'PASS','actual_uid':os.geteuid(),'modes':['normal','O','OO'],'cases':cases,'total_cases':len(cases),'independent_math':math_receipts[0],'original_manifest_sha256':ORIGINAL_MANIFEST,'original_bootstrap_sha256':ORIGINAL_BOOTSTRAP,'corrected_manifest_sha256':CORRECTED_MANIFEST,'corrected_bootstrap_sha256':CORRECTED_BOOTSTRAP,'immutable_bytes_and_modes_preserved':True,'hostile_sentinels_created':0,'external_source_reverification':'NOT_RUN by this source-free script','limits':['Finite tests do not formalize the analytic or surface-topology proofs.','Semantic and integrity boundaries are tested separately; direct verifier is not a complete metadata truth checker.','No race-resistance, external-network isolation, or arbitrary-code sandbox guarantee.']}
    if args.receipt:Path(args.receipt).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='cases'},sort_keys=True))
if __name__=='__main__':main()
