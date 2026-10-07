#!/usr/bin/env python3
"""Non-mutating audit of the frozen input, with mutations confined to temp copies."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,zipfile
BASE=pathlib.Path(__file__).resolve().parent.parent
PACKET=BASE/'packet';OUT=BASE/'independent_audit'
def need(x,m):
    if not x:raise RuntimeError(m)
def digest(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def snapshot(p):return {x.relative_to(p).as_posix():digest(x) for x in sorted(p.rglob('*')) if x.is_file()}
def run(script,mode='normal',cwd='/tmp'):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    flag=[]
    if mode=='dash_O':flag=['-O']
    elif mode=='env_2':env['PYTHONOPTIMIZE']='2'
    return subprocess.run([sys.executable,*flag,'-B',str(script)],env=env,cwd=cwd,capture_output=True)
def rebind(p):
    m=json.loads((p/'AUTHOR_MANIFEST.json').read_text())
    m['files']={f.relative_to(p).as_posix():digest(f) for f in sorted(p.rglob('*')) if f.is_file() and f.name!='AUTHOR_MANIFEST.json'}
    (p/'AUTHOR_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
before=snapshot(PACKET)
need(digest(PACKET/'AUTHOR_MANIFEST.json')['sha256']=='cfa02b87b3cd03463d68912a12b621c7603cd00b86143edf3562055c1a933407','manifest anchor')
need(digest(BASE/'AUTHOR_PACKET_30001052.zip')['sha256']=='c8ca75803bd021bdd988128eae16a46dcee00ae1211a0507e2b635de1f49a3d4','ZIP anchor')
rep={'status':'PASS','python':sys.version,'input_manifest':digest(PACKET/'AUTHOR_MANIFEST.json'),'input_zip':digest(BASE/'AUTHOR_PACKET_30001052.zip'),'positive':[],'negative':[],'source_pdf_hashes':[]}
with zipfile.ZipFile(BASE/'AUTHOR_PACKET_30001052.zip') as z:
    need(set(z.namelist())==set(before),'ZIP inventory')
    need(len(z.namelist())==len(set(z.namelist())),'ZIP duplicate entries')
    need(all(z.read(n)==(PACKET/n).read_bytes() for n in z.namelist()),'ZIP member bytes')
rep['zip_members_match_packet']=True
jobs=[(PACKET/'check_fusion.py',PACKET/'FUSION_CHECKS.json'),(PACKET/'check_obstructions.py',PACKET/'OBSTRUCTION_CHECKS.json'),(OUT/'independent_fusion_check.py',OUT/'INDEPENDENT_FUSION_CHECKS.json'),(OUT/'independent_obstruction_check.py',OUT/'INDEPENDENT_OBSTRUCTION_CHECKS.json')]
for mode in ['normal','dash_O','env_2']:
    r=run(PACKET/'verify.py',mode);need(r.returncode==0,'packet verifier '+mode+': '+r.stderr.decode())
    rep['positive'].append({'check':'author packet verifier','mode':mode,'status':'PASS','stdout_sha256':hashlib.sha256(r.stdout).hexdigest()})
    for script,expected in jobs:
        r=run(script,mode);need(r.returncode==0,str(script)+': '+r.stderr.decode());need(r.stdout==expected.read_bytes(),'bytes differ '+str(script))
        rep['positive'].append({'check':script.name,'mode':mode,'status':'PASS','output_sha256':hashlib.sha256(r.stdout).hexdigest()})
with tempfile.TemporaryDirectory() as t:
    b=pathlib.Path(t)/'fully relocated case';p=b/'packet';a=b/'independent_audit'
    shutil.copytree(PACKET,p);shutil.copytree(OUT,a)
    for mode in ['normal','dash_O','env_2']:
        r=run(p/'verify.py',mode);need(r.returncode==0,'relocated verifier '+r.stderr.decode())
        rep['positive'].append({'check':'relocated author verifier','mode':mode,'status':'PASS'})
        for script,expected in jobs:
            q=(p if script.parent==PACKET else a)/script.name
            r=run(q,mode);need(r.returncode==0,'relocated checker '+r.stderr.decode());need(r.stdout==expected.read_bytes(),'relocated output')
            rep['positive'].append({'check':'relocated '+script.name,'mode':mode,'status':'PASS'})
for case in ['changed_proof','changed_results','missing_member','extra_member','rebound_bad_hom_count','rebound_bad_carry','symlink_member','rebound_bad_output']:
    with tempfile.TemporaryDirectory() as t:
        p=pathlib.Path(t)/'packet';shutil.copytree(PACKET,p)
        if case=='changed_proof':(p/'PROOF.md').write_bytes((p/'PROOF.md').read_bytes()+b'\nchanged\n')
        elif case=='changed_results':(p/'FUSION_CHECKS.json').write_text('{}\n')
        elif case=='missing_member':(p/'README.md').unlink()
        elif case=='extra_member':(p/'unexpected.txt').write_text('unexpected')
        elif case=='symlink_member':
            (p/'README.md').unlink();(p/'README.md').symlink_to(PACKET/'README.md')
        elif case=='rebound_bad_output':
            (p/'FUSION_CHECKS.json').write_text('{}\n');rebind(p)
        else:
            file,old,new=(('check_fusion.py','len(homs)==len(set(homs))==36','len(homs)==len(set(homs))==35') if case=='rebound_bad_hom_count' else ('check_obstructions.py','carry=[(i+j)//p for i,j in two]','carry=[((i+j)//p+1)%p for i,j in two]'))
            f=p/file;txt=f.read_text();need(old in txt,'mutation target');f.write_text(txt.replace(old,new));rebind(p)
        for mode in ['normal','dash_O','env_2']:
            r=run(p/'verify.py',mode);need(r.returncode!=0,'accepted mutant '+case)
            err=r.stderr.decode()
            if case in ['rebound_bad_hom_count','rebound_bad_carry']:need('checker failed:' in err,'not reached mathematical checker')
            if case=='rebound_bad_output':need('checker output differs:' in err,'not reached output comparison')
            rep['negative'].append({'case':case,'mode':mode,'status':'REJECTED','error_summary':[x for x in err.splitlines() if x.startswith('RuntimeError:')]})
metadata=json.loads((PACKET/'SOURCE_METADATA.json').read_text())
filenames=['owr.pdf','blo.pdf','extensions.pdf','ragnarsson.pdf','henke.pdf','puig2015.pdf','oliver.pdf']
for item,name in zip(metadata['pdfs'],filenames):
    d=digest(BASE/'private_sources'/name);need(all(d[k]==item[k] for k in ['bytes','sha256']),'source PDF hash '+name)
    rep['source_pdf_hashes'].append({'title':item['title'],'url':item['url'],**d,'matches_author_metadata':True})
# Optional command-line argument: directory containing the two authorized corpus files.
corpus=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else None
rep['corpus_hashes']={}
ready=json.loads((PACKET/'READINESS.json').read_text())
for name in (['problems.json','research_results.json'] if corpus is not None else []):
    p=corpus/name;d=digest(p);need(d==ready['corpus'][name],'corpus hash '+name)
    data=json.loads(p.read_text());rep['corpus_hashes'][name]={**d,'matches_author_metadata':True,'top_level_count':len(data)}
need(snapshot(PACKET)==before,'original packet changed')
rep['original_packet_unchanged']=True
(OUT/'AUDIT_CHECKS.json').write_text(json.dumps(rep,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','positive_runs':len(rep['positive']),'negative_runs':len(rep['negative']),'input_preserved':True},sort_keys=True))
