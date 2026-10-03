from pathlib import Path
import hashlib,json,subprocess,shutil,datetime,sys

p=Path(__file__).resolve().parent;b=p.parent;repo=Path('/Users/alec/Documents/Math')
old=b/'snapshot/unsolved_math_prioritization/attempts/30002200';copy=p/'tmp/original_packet'
shutil.copytree(old,copy,dirs_exist_ok=True)
r=subprocess.run([sys.executable,'-B',str(copy/'verify_publication.py')],capture_output=True,cwd=copy)
(p/'original_verify_publication.stdout').write_bytes(r.stdout);(p/'original_verify_publication.stderr').write_bytes(r.stderr)
assert r.returncode==0 and len(r.stdout)==147 and not r.stderr
oldrep=json.loads((b/'root_original_reproduction_receipt.json').read_text())
assert hashlib.sha256(r.stdout).hexdigest()==oldrep['complete_streams'][2]['sha256']
sm=json.loads((b/'snapshot_manifest.json').read_text())
for e in sm['files']:
    r=subprocess.run(['git','show',sm['head']+':'+e['path']],capture_output=True,cwd=repo);assert r.returncode==0
    assert len(r.stdout)==e['bytes'] and hashlib.sha256(r.stdout).hexdigest()==e['sha256']
    blob=hashlib.sha1(b'blob '+str(len(r.stdout)).encode()+b'\0'+r.stdout).hexdigest();assert blob==e['git_blob_sha']
checks=[]
for folder,manifest in [('geometry_morse_review','FAMILY_ARTIFACT_MANIFEST.json'),('geometry_morse_review','independent_seal_manifest.json'),('koszul_depth_review','FINAL_AUDIT_MANIFEST.json'),('koszul_depth_review','INDEPENDENT_SEAL.json'),('priority_sources_review','PUBLIC_ARTIFACT_MANIFEST.json'),('priority_sources_review','source_first_seal.json')]:
    obj=json.loads((b/folder/manifest).read_text());entries=obj['files']
    if isinstance(entries,dict):entries=[{'path':k,'sha256':v} for k,v in entries.items()]
    for e in entries:
        d=(b/folder/e['path']).read_bytes()
        assert hashlib.sha256(d).hexdigest()==e['sha256'] and len(d)==e.get('bytes',len(d))
    checks.append({'folder':folder,'manifest':manifest,'bindings':len(entries)})
runs=[]
for folder,script,outname in [('geometry_morse_review','independent_local_controls.py','independent_local_controls.stdout.txt'),('koszul_depth_review','independent_koszul_controls.py','independent_koszul_controls.stdout.txt'),('koszul_depth_review','frozen_comparison_controls.py','frozen_comparison_controls.stdout.txt'),('priority_sources_review','independent_source_controls.py','source_controls_full.stdout')]:
    r=subprocess.run([sys.executable,'-B',str(b/folder/script)],capture_output=True,cwd=b/folder)
    assert r.returncode==0 and not r.stderr
    stem='family_'+folder+'_'+script[:-3]
    (p/(stem+'.stdout')).write_bytes(r.stdout);(p/(stem+'.stderr')).write_bytes(r.stderr)
    old=(b/folder/outname).read_bytes()
    if folder=='priority_sources_review':
        a=[json.loads(x) for x in r.stdout.splitlines()];o=[json.loads(x) for x in old.splitlines()]
        for rows in [a,o]:
            rows[0].pop('started_utc');rows[-1].pop('completed_utc')
        assert a==o;match='All JSON fields exact except explicit started_utc/completed_utc'
    else:assert r.stdout==old;match='Full stdout byte exact'
    runs.append({'folder':folder,'script':script,'match':match,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':0})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_old20_git_objects_verified':True,'old_publication_stdout_bytes':147,'old_publication_stdout_sha256':oldrep['complete_streams'][2]['sha256'],'family_manifest_bindings':checks,'family_runs':runs,'no_final_actual_publication_gate_claimed':True}
(p/'postseal_comparison_reproduction.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
