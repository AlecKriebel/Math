#!/usr/bin/env python3
"""Independent source-free exact algebra and frozen-artifact controls.
Not a mapping-class-group proof checker; published geometry remains an input.
Run: python3 -I -S -B independent_checks.py /path/to/freeze /path/to/archive.zip
"""
import copy, hashlib, itertools, json, math, os, pathlib, shutil, stat, subprocess, sys, tempfile, zipfile
P=pathlib.Path
PIN_B='3c892dc01523d9c75f28b41efe0de500407ae02bc21ea13208771dcc91dec817'
PIN_M='45f641b37f6e58df37729e194076c2512cdc77ce12faa7c7c937dd6fc09195fa'
PIN_Z='383ccc35f8a5230570b411ac5809c6b477d0b341ce09bed3b6d6a34a0133d25d'
MODES=[[],['-O'],['-OO']]
def need(t,m):
    if not t: raise RuntimeError(m)
def h(b):return hashlib.sha256(b).hexdigest()
def inv(p):return {str(x.relative_to(p)):{'bytes':x.stat().st_size,'sha256':h(x.read_bytes())} for x in sorted(p.rglob('*')) if x.is_file()}
def run(cmd,cwd,env=None):return subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
def matrix(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def tr(a):return [list(x) for x in zip(*a)]
def modes_run(script,args,cwd,env=None):
    return [run([sys.executable,'-I','-S','-B',*m,str(script),*args],cwd,env) for m in MODES]
def rw(p):
    p.chmod(0o755)
    for q in p.rglob('*'):
        if not q.is_symlink():q.chmod(0o755 if q.is_dir() else 0o644)
def ro(p):
    for q in p.rglob('*'):
        if not q.is_symlink():q.chmod(0o555 if q.is_dir() else 0o444)
    p.chmod(0o555)
def main():
    need(len(sys.argv)==3,'provide freeze and ZIP');base=P(sys.argv[1]).resolve();archive=P(sys.argv[2]).resolve()
    need(os.getuid()!=0,'must run unprivileged')
    for p,d in [(base/'bootstrap.py',PIN_B),(base/'AUTHOR_MANIFEST.json',PIN_M),(archive,PIN_Z)]:need(h(p.read_bytes())==d,'external pin mismatch '+p.name)
    before=inv(base);need(len(before)==13,'exact expected freeze inventory')
    need(all((q.stat().st_mode&0o222)==0 for q in [base,*base.rglob('*')]),'freeze not mode-read-only')
    denied=False
    try:(base/'packet/CLAIMS.json').open('ab').close()
    except PermissionError:denied=True
    need(denied,'write not denied')
    m=json.loads((base/'AUTHOR_MANIFEST.json').read_bytes())
    need({x['path'] for x in m['files']}=={p.name for p in (base/'packet').iterdir()},'manifest inventory')
    for x in m['files']:need(before['packet/'+x['path']]=={'bytes':x['bytes'],'sha256':x['sha256']},'manifest payload mismatch')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();need(len(names)==len(set(names))==13 and set(names)==set(before),'ZIP inventory')
        need(z.testzip() is None,'ZIP CRC')
        for name in names:need(z.read(name)==(base/name).read_bytes(),'ZIP byte mismatch')
    u=[1,0,0,0,1,0];v=[0,1,0,-1,0,1]
    # Independently derived exponent sums, in source factor order (equations 48--59).
    coeffs=[[1,0],[1,-1],[0,-1],[1,0],[1,-1],[0,-1],[1,0],[1,-1],[0,1],[1,0],[1,-1],[0,-1]]
    rows=[[a*x+b*y for x,y in zip(u,v)] for a,b in coeffs]
    minors=[rows[i][a]*rows[j][b]-rows[i][b]*rows[j][a] for i,j in itertools.combinations(range(12),2) for a,b in itertools.combinations(range(6),2)]
    need(math.gcd(*minors)==1,'nonsaturated lattice')
    need(all(math.gcd(*r)==1 for r in rows),'nonprimitive curve class')
    need(rows[0]==u and rows[8]==v,'missing lattice generators')
    c=json.loads((base/'packet/CERTIFICATE.json').read_bytes());q=c['quotient_map'];s=c['section']
    need(c['lattice_basis']==[u,v],'certificate/source mismatch')
    need(matrix(q,tr(rows))==[[0]*12 for _ in range(4)],'q fails source rows')
    need(matrix(q,s)==eye(4),'section')
    decomposition=[[int(i==j)-matrix(s,q)[i][j] for j in range(6)] for i in range(6)]
    need(decomposition==[[u[i]*int(j==0)+v[i]*int(j==1) for j in range(6)] for i in range(6)],'exact kernel identity')
    J=[[0]*6 for _ in range(6)]
    for i in range(3):J[2*i][2*i+1]=1;J[2*i+1][2*i]=-1
    product=eye(6)
    for r in rows:
        dual=matrix([r],J)[0];t=[[int(i==j)+r[i]*dual[j] for j in range(6)] for i in range(6)]
        need(matrix(matrix(tr(t),J),t)==J,'nonsymplectic transvection')
        product=matrix(product,t)
    need(product==eye(6),'homological monodromy is not identity')
    positives=[];rejections=[];semantic=[];output=None
    with tempfile.TemporaryDirectory(prefix='positive-twist-independent-') as tmp:
        tmp=P(tmp);host=tmp/'hostile';host.mkdir();marker=tmp/'BAD_IMPORT'
        badcode='from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\nraise RuntimeError("hostile")\n'
        for name in ['json.py','hashlib.py','tempfile.py','subprocess.py','sitecustomize.py','usercustomize.py']:(host/name).write_text(badcode)
        env=dict(os.environ,PYTHONPATH=str(host),PYTHONSTARTUP=str(host/'sitecustomize.py'))
        for mode,r in zip(MODES,modes_run(base/'bootstrap.py',[],host,env)):
            need(r.returncode==0,'original replay '+r.stderr.decode());output=output or r.stdout;need(r.stdout==output,'mode drift');positives.append({'case':'actual-readonly-hostile-cwd','mode':mode})
        ext=tmp/'zip';ext.mkdir()
        with zipfile.ZipFile(archive) as z:z.extractall(ext)
        ro(ext);ext_before=inv(ext)
        for mode,r in zip(MODES,modes_run(ext/'bootstrap.py',[],host,env)):
            need(r.returncode==0 and r.stdout==output,'archive replay');positives.append({'case':'archive-readonly','mode':mode})
        need(inv(ext)==ext_before,'archive changed');rw(ext)
        muts=[]
        for name in sorted(before):
            muts.append(('alter-'+name,lambda d,n=name:(d/n).write_bytes((d/n).read_bytes()+b'\n!')))
            muts.append(('remove-'+name,lambda d,n=name:(d/n).unlink()))
        muts.extend([('extra-root',lambda d:(d/'extra').write_text('x')),('extra-packet',lambda d:(d/'packet/extra').write_text('x')),('extra-directory',lambda d:(d/'packet/extra').mkdir())])
        def replace_type(d,kind):
            p=d/'packet/CERTIFICATE.json';b=p.read_bytes();p.unlink();out=tmp/('external-'+d.name);out.write_bytes(b)
            if kind=='symlink':p.symlink_to(out)
            elif kind=='hardlink':os.link(out,p)
            elif kind=='fifo':os.mkfifo(p)
            else:p.mkdir()
        for kind in ['symlink','hardlink','fifo','directory']:muts.append((kind,lambda d,k=kind:replace_type(d,k)))
        def forge(d):
            p=d/'packet/CLAIMS.json';a=json.loads(p.read_bytes());a['quotient_rank']=3;p.write_text(json.dumps(a));mm=json.loads((d/'AUTHOR_MANIFEST.json').read_bytes())
            for e in mm['files']:
                if e['path']==p.name:e.update(bytes=p.stat().st_size,sha256=h(p.read_bytes()))
            (d/'AUTHOR_MANIFEST.json').write_text(json.dumps(mm))
        muts.append(('self-consistent-forgery',forge))
        for idx,(name,mut) in enumerate(muts):
            d=tmp/('mutation-'+str(idx));shutil.copytree(base,d);rw(d);mut(d)
            for mode in MODES:
                script=d/'bootstrap.py'
                if not script.is_file() or script.is_symlink() or script.stat().st_nlink!=1 or h(script.read_bytes())!=PIN_B:
                    rejections.append({'case':name,'mode':mode,'layer':'external-bootstrap-pin'});continue
                r=run([sys.executable,'-I','-S','-B',*mode,str(script)],host,env)
                need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'accepted integrity mutation '+name);rejections.append({'case':name,'mode':mode,'layer':'bootstrap'})
        cases=[];claims=json.loads((base/'packet/CLAIMS.json').read_bytes())
        for key,val in [('novelty_claimed',True),('approaches',1),('approaches',False),('rank',1013),('quotient_rank',3),('positive_factors',0),('finite_checks_certify_mapping_class_identity',True),('formal_verification',True),('independent_review_performed',True)]:
            x=copy.deepcopy(claims);x[key]=val;cases.append(('claim-'+key+'-'+str(val),'--claims',json.dumps(x).encode()))
        for key in ['lattice_basis','quotient_map','section']:
            for i,row in enumerate(c[key]):
                for j in range(len(row)):
                    x=copy.deepcopy(c);x[key][i][j]+=1;cases.append((key+'-'+str(i)+'-'+str(j),'--certificate',json.dumps(x).encode()))
            for name,value in [('boolean',True),('float',0.0),('huge',10**9),('string','1'),('null',None)]:
                x=copy.deepcopy(c);x[key][0][0]=value;cases.append((key+'-'+name,'--certificate',json.dumps(x).encode()))
            x=copy.deepcopy(c);x[key].pop();cases.append((key+'-rows','--certificate',json.dumps(x).encode()))
            x=copy.deepcopy(c);x[key][0].pop();cases.append((key+'-columns','--certificate',json.dumps(x).encode()))
        for name,b in [('malformed',b'{'),('duplicate-key',b'{"x":1,"x":2}'),('nan',b'{"x":NaN}'),('invalid-utf8',b'\xff'),('deep',b'['*2000+b']'*2000),('oversized',b' '*1000001),('null',b'null')]:cases.append((name,'--certificate',b))
        for idx,(name,opt,b) in enumerate(cases):
            p=tmp/('semantic-'+str(idx));p.write_bytes(b)
            for mode,r in zip(MODES,modes_run(base/'packet/verify.py',[opt,str(p)],host,env)):
                need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'accepted semantic mutation '+name);semantic.append({'case':name,'mode':mode})
        need(not marker.exists(),'hostile code executed')
    need(inv(base)==before,'original freeze changed')
    return {'schema':'positive-twist-independent-audit-controls-v1','status':'PASS','uid':os.getuid(),'original_write_denied':denied,'original_bytes_unchanged':True,'archive_members':13,'archive_bytes_match':True,'pins':{'bootstrap':PIN_B,'manifest':PIN_M,'archive':PIN_Z},'source_derived_coefficients':coeffs,'source_derived_rows':rows,'minor_count':len(minors),'gcd_rank_two_minors':math.gcd(*minors),'all_curve_vectors_primitive':True,'rank':2,'integral_quotient':'Z^4','symplectic_product_identity':True,'symplectic_check_is_not_mapping_class_proof':True,'positive_count':len(positives),'integrity_case_count':len(muts),'integrity_rejection_count':len(rejections),'semantic_case_count':len(cases),'semantic_rejection_count':len(semantic),'positives':positives,'integrity_rejections':rejections,'semantic_rejections':semantic,'source_rehash':'NOT_RUN_BY_THIS_SOURCE_FREE_SCRIPT','corpus_rehash':'NOT_RUN_BY_THIS_SOURCE_FREE_SCRIPT'}
if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
