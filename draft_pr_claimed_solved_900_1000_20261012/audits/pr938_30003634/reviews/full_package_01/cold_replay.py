"""Offline cold release replay; all execution/scratch remains in this review."""
import ast, datetime, hashlib, json, os, pathlib, shutil, subprocess, tempfile, zipfile
from authenticate import A,C,O,MANIFEST,require,sha
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def main(output=None):
    work=O/'private/cold';work.mkdir(parents=True,exist_ok=True)
    root=pathlib.Path(tempfile.mkdtemp(prefix='extracted_',dir=work))
    z=zipfile.ZipFile(C/'deep-derived-pure-braids-source-verification-v1.0.zip')
    z.extractall(root)
    require(sha((root/'verify_package.py').read_bytes())=='61cac923d484f8a7fed8f48358eda1182f771ae61e02aecd75a1e0e24e2c10ae','external verifier pin')
    require(sha((root/'PACKAGE_MANIFEST.json').read_bytes())==MANIFEST,'external package pin')
    rows=[]
    for label,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
        if opt:env['PYTHONOPTIMIZE']=opt
        probe=subprocess.run([PY,*flags,'-c','import sys;print(sys.flags.optimize)'],env=env,capture_output=True,text=True,check=True)
        result=subprocess.run([PY,*flags,str(root/'verify_package.py'),'--expected-manifest',MANIFEST,'--pdf',str(C/'output/pdf/note.pdf'),'--workdir',str(work/'scratch')],cwd=work,env=env,capture_output=True,text=True,timeout=1800)
        (work/(label+'.stdout')).write_text(result.stdout);(work/(label+'.stderr')).write_text(result.stderr)
        require(result.returncode==0,label+' failed '+result.stderr)
        receipt=json.loads(result.stdout);require(receipt['status']=='PASS','Cold status')
        rows.append({'mode':label,'observed_outer_optimization':int(probe.stdout),'receipt':receipt})
    require(all(r['receipt']==rows[0]['receipt'] for r in rows),'Replay mode difference')
    # Execute only inspected challenge drivers from private copies: the inventory
    # driver places scratch relative to itself. They never mutate the authentic root.
    challenges=[]
    for script,tail in [('package_guard_challenges.py',[]),('copy_guard_challenge.py',['--expected-manifest',MANIFEST,'--workdir',str(work/'copy_scratch')])]:
        shutil.copyfile(C/script,work/script)
        dest=work/('COLD_'+script.replace('.py','').upper()+'.json')
        p=subprocess.run([PY,'-B',str(work/script),'--bundle',str(root),'--python',PY,'--output',str(dest),*tail],cwd=work,capture_output=True,text=True,timeout=600)
        (work/(script+'.stdout')).write_text(p.stdout);(work/(script+'.stderr')).write_text(p.stderr)
        require(p.returncode==0,'Challenge failed '+p.stderr);challenges.append(json.loads(dest.read_text()))
    builder=ast.parse((C/'build_package.py').read_text())
    families=next(ast.literal_eval(n.value) for n in builder.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FAMILIES' for t in n.targets))
    seals={}
    for family,(name,pin) in families.items():
        folder=A/'reviews'/family;raw=(folder/name).read_bytes();require(sha(raw)==pin,'Family pin '+family)
        mapping=json.loads(raw);entries=mapping.get('files',mapping.get('public_files',mapping.get('records')))
        if isinstance(entries,list):entries={r['path']:{'bytes':r.get('bytes',r.get('size')),'sha256':r['sha256']} for r in entries}
        require(name not in entries,'Self-included family manifest')
        for path,meta in entries.items():
            b=(folder/path).read_bytes();require({'bytes':len(b),'sha256':sha(b)}==meta,'Family payload '+family+'/'+path)
            require(z.read('reviews/'+family+'/'+path)==b,'Archive family mismatch')
        seals[family]={'manifest':name,'sha256':pin,'payloads':len(entries),'all_disk_archive_fingerprints_match':True}
    out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','cold_extraction':True,'externally_pinned_verifier_sha256':'61cac923d484f8a7fed8f48358eda1182f771ae61e02aecd75a1e0e24e2c10ae','package_manifest_sha256':MANIFEST,'modes':rows,'family_seals':seals,'challenges':[{k:v for k,v in c.items() if k!='rows'} for c in challenges],'scope':'Finite reproducibility and bounded transport controls, not universal mathematics or historical priority.'}
    if output:pathlib.Path(output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();main(args.output)
