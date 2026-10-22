#!/usr/bin/env python3
"""Unprivileged adversarial controls; mutate only disposable copies."""
import copy,hashlib,json,os,shutil,stat,subprocess,sys,tempfile
from pathlib import Path
class Failure(Exception):pass
def need(ok,msg):
    if not ok:raise Failure(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def files(root):
    return {str(p.relative_to(root)):sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
def writable(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def readonly(root):
    for p in root.rglob('*'):
        if not p.is_symlink():p.chmod(0o555 if p.is_dir() else 0o444)
    root.chmod(0o555)
def copyfreeze(base,d):
    shutil.copytree(base,d);writable(d)
def run(base,mode,pin,cwd,env=None):
    p=base/'bootstrap.py';st=p.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or sha(p.read_bytes())!=pin:
        return subprocess.CompletedProcess([],1,b'',b'REJECT: external bootstrap pin mismatch')
    return subprocess.run([sys.executable,'-I','-S','-B',*mode,str(p)],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
def direct(base,mode,option,p,cwd):
    return subprocess.run([sys.executable,'-I','-S','-B',*mode,str(base/'packet/verify.py'),option,str(p)],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
def main():
    need(len(sys.argv)==3,'usage: test_bootstrap.py EXPECTED_BOOTSTRAP_SHA256 EXPECTED_MANIFEST_SHA256')
    pin,mpin=sys.argv[1:];base=Path(__file__).absolute().parents[1];need(os.getuid()!=0,'must run as non-root')
    need(sha((base/'bootstrap.py').read_bytes())==pin,'initial bootstrap pin');need(sha((base/'AUTHOR_MANIFEST.json').read_bytes())==mpin,'initial manifest pin')
    before=files(base);modes=[[],['-O'],['-OO']];pos=[];neg=[];semantic=[]
    need(all((p.stat().st_mode&0o222)==0 for p in base.rglob('*')) and (base.stat().st_mode&0o222)==0,'original freeze must be genuinely mode-read-only')
    write_denied=False
    try:(base/'packet/CLAIMS.json').open('ab').close()
    except PermissionError:write_denied=True
    need(write_denied,'original write not denied')
    with tempfile.TemporaryDirectory(prefix='positive-twist-controls-') as temp:
        t=Path(temp);expected=None
        for mode in modes:
            r=run(base,mode,pin,t);need(r.returncode==0,'original failed '+r.stderr.decode());expected=expected or r.stdout;need(r.stdout==expected,'mode-dependent original');pos.append({'layout':'original-read-only','mode':mode})
        d=t/'relocated';copyfreeze(base,d);readonly(d);d_before=files(d)
        try:(d/'packet/forbidden').write_bytes(b'x');raise Failure('relocated directory writable')
        except PermissionError:pass
        for mode in modes:
            r=run(d,mode,pin,t);need(r.returncode==0 and r.stdout==expected,'relocated replay');pos.append({'layout':'relocated-read-only','mode':mode})
        need(files(d)==d_before,'relocated bytes changed');writable(d)
        host=t/'hostile-import';host.mkdir();marker=t/'IMPORT_EXECUTED'
        code="from pathlib import Path\nPath("+repr(str(marker))+").write_text('bad')\nraise RuntimeError('hostile')\n"
        for name in ['json.py','hashlib.py','tempfile.py','subprocess.py','sitecustomize.py','usercustomize.py']:(host/name).write_text(code)
        env=dict(os.environ);env['PYTHONPATH']=str(host)
        for mode in modes:
            r=run(base,mode,pin,host,env);need(r.returncode==0 and r.stdout==expected and not marker.exists(),'hostile imports executed');pos.append({'layout':'hostile-cwd-and-pythonpath-isolated','mode':mode})
        cases=[]
        for name in sorted(p.name for p in (base/'packet').iterdir()):
            cases.append(('payload-drift-'+name,lambda d,name=name:(d/'packet'/name).write_bytes((d/'packet'/name).read_bytes()+b'!')))
            cases.append(('payload-missing-'+name,lambda d,name=name:(d/'packet'/name).unlink()))
        cases.extend([
            ('extra-file',lambda d:(d/'packet/extra').write_text('x')),
            ('extra-directory',lambda d:(d/'packet/extra').mkdir()),
            ('outer-extra-file',lambda d:(d/'extra').write_text('x')),
            ('outer-extra-directory',lambda d:(d/'extra').mkdir()),
            ('extra-import-module',lambda d:(d/'packet/json.py').write_text(code)),
            ('malformed-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').write_text('{bad')),
            ('missing-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').unlink()),
            ('empty-manifest',lambda d:(d/'AUTHOR_MANIFEST.json').write_bytes(b'')),
            ('bootstrap-code-replacement',lambda d:(d/'bootstrap.py').write_text(code)),
            ('payload-code-replacement',lambda d:(d/'packet/verify.py').write_text(code)),
        ])
        def link(d,name,kind):
            p=d/name;content=p.read_bytes();p.unlink();target=d.parent/('outside-'+d.name);target.write_bytes(content)
            if kind=='symbolic':p.symlink_to(target)
            else:os.link(target,p)
        for name in ['packet/CLAIMS.json','AUTHOR_MANIFEST.json','bootstrap.py']:
            for kind in ['symbolic','hard']:cases.append((kind+'-link-'+name,lambda d,name=name,kind=kind:link(d,name,kind)))
        def fifo(d):p=d/'packet/CLAIMS.json';p.unlink();os.mkfifo(p)
        cases.append(('fifo-payload',fifo))
        def directory_payload(d):p=d/'packet/CLAIMS.json';p.unlink();p.mkdir()
        cases.append(('directory-payload',directory_payload))
        def root_link(d):p=d/'packet';p.rename(d.parent/('moved-'+d.name));p.symlink_to(d.parent/('moved-'+d.name),target_is_directory=True)
        cases.append(('symlink-packet',root_link))
        def forge(d):
            p=d/'packet/CLAIMS.json';x=json.loads(p.read_text());x['quotient_rank']=3;p.write_text(json.dumps(x))
            m=json.loads((d/'AUTHOR_MANIFEST.json').read_text())
            for e in m['files']:
                if e['path']=='CLAIMS.json':e['bytes']=p.stat().st_size;e['sha256']=sha(p.read_bytes())
            (d/'AUTHOR_MANIFEST.json').write_text(json.dumps(m))
        cases.append(('self-consistent-forged-payload-manifest',forge))
        def manifest_mut(d,kind):
            p=d/'AUTHOR_MANIFEST.json';m=json.loads(p.read_text())
            if kind=='traversal':m['files'][0]['path']='../escape'
            elif kind=='absolute':m['files'][0]['path']='/tmp/escape'
            elif kind=='duplicate':m['files'].append(m['files'][0])
            elif kind=='bool-size':m['files'][0]['bytes']=True
            elif kind=='negative-size':m['files'][0]['bytes']=-1
            elif kind=='nonhex-hash':m['files'][0]['sha256']='z'*64
            elif kind=='bool-approaches':m['approaches']=False
            p.write_text(json.dumps(m))
        for kind in ['traversal','absolute','duplicate','bool-size','negative-size','nonhex-hash','bool-approaches']:cases.append(('untrusted-manifest-'+kind,lambda d,kind=kind:manifest_mut(d,kind)))
        for i,(label,mutate) in enumerate(cases):
            d=t/('mutation-'+str(i));copyfreeze(base,d);mutate(d)
            for mode in modes:
                r=run(d,mode,pin,host,env);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'accepted mutation '+label+': '+r.stderr.decode());need(not marker.exists(),'hostile code executed');neg.append({'case':label,'mode':mode})
        good=json.loads((base/'packet/CLAIMS.json').read_text());cert=json.loads((base/'packet/CERTIFICATE.json').read_text());bad=[]
        for k,val in [('novelty_claimed',True),('formal_verification',True),('approaches',5),('genus',4),('quotient_rank',3),('positive_factors',0),('target_answer','yes'),('independent_review_performed',True),('finite_checks_certify_mapping_class_identity',True),('approaches',False),('problem_id',11000113)]:
            x=copy.deepcopy(good);x[k]=val;bad.append(('claim-'+k+'-'+str(val),'--claims',json.dumps(x)))
        for name,body in [('malformed','{bad'),('duplicate','{"schema":1,"schema":2}'),('nonfinite','{"schema":NaN}'),('null','null'),('list','[]'),('string','"bad"'),('invalid-utf8',b'\xff'),('deep',b'['*2000+b']'*2000),('oversized',b' '*1000001)]:bad.append((name,'--claims',body))
        x=copy.deepcopy(good);x['extra']=0;bad.append(('extra-key','--claims',json.dumps(x)))
        x=copy.deepcopy(good);del x['status'];bad.append(('missing-key','--claims',json.dumps(x)))
        for key in ['lattice_basis','quotient_map','section']:
            for kind in ['entry','boolean','row-shape','column-shape','large']:
                x=copy.deepcopy(cert)
                if kind=='entry':x[key][0][0]+=1
                elif kind=='boolean':x[key][0][0]=True
                elif kind=='row-shape':x[key].pop()
                elif kind=='column-shape':x[key][0].pop()
                elif kind=='large':x[key][0][0]=10**10
                bad.append((key+'-'+kind,'--certificate',json.dumps(x)))
        for i,(label,opt,body) in enumerate(bad):
            p=t/('input-'+str(i));p.write_bytes(body if type(body) is bytes else body.encode())
            for mode in modes:
                r=direct(base,mode,opt,p,host);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'semantic accepted '+label+': '+r.stderr.decode());semantic.append({'case':label,'mode':mode})
        for kind in ['symlink','fifo']:
            p=t/('input-'+kind)
            if kind=='symlink':p.symlink_to(base/'packet/CLAIMS.json')
            else:os.mkfifo(p)
            for mode in modes:
                r=direct(base,mode,'--claims',p,host);need(r.returncode==1 and r.stderr.startswith(b'REJECT:'),'nonregular semantic input accepted');semantic.append({'case':kind,'mode':mode})
        need(files(base)==before,'original bytes changed');need(not marker.exists(),'hostile execution marker')
    return {'schema':'positive-twist-control-results-v1','status':'PASS','uid':os.getuid(),'bootstrap_sha256':pin,'manifest_sha256':mpin,'original_write_denied':write_denied,'original_bytes_unchanged':True,'readonly_relocated_bytes_unchanged':True,'hostile_code_executed':False,'positives':pos,'integrity_rejections':neg,'semantic_rejections':semantic,'positive_count':len(pos),'integrity_rejection_count':len(neg),'semantic_rejection_count':len(semantic),'integrity_case_count':len(cases),'semantic_case_count':len(bad)+2,'scope':'Integrity and finite algebra controls; not a topology proof checker or independent mathematical review.'}
if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except (Failure,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
