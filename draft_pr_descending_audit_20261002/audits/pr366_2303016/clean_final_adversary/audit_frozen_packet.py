from pathlib import Path
import datetime,hashlib,json,subprocess,sys,shutil
R=Path(__file__).resolve().parent
F=R.parent/'snapshot';P=F/'unsolved_math_prioritization/attempts/2303016'
BASE='efd29c05204703acca9a0860812f54b94fae54b1';HEAD='f4039c9c093b10e651ee7fd2e6379073b84238c7';AUTHOR='2a14016d7e62d1b044bb63cad51a25e5747e7cd1'
S=json.loads((R.parent/'snapshot_manifest.json').read_text())
assert S['head']==HEAD and S['base']==BASE
OUT=R/'streams';OUT.mkdir(exist_ok=True)
commands=[]
def run(label,args,cwd=None):
    z=subprocess.run(args,cwd=cwd,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(z.stdout);(OUT/(label+'.stderr')).write_bytes(z.stderr)
    row={'label':label,'argv':args,'cwd':str(cwd) if cwd else None,'exit':z.returncode,'stdout_bytes':len(z.stdout),'stderr_bytes':len(z.stderr),'stdout_sha256':hashlib.sha256(z.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(z.stderr).hexdigest()}
    commands.append(row);return z
files=[]
for e in S['files']:
    path=F/e['path'];b=path.read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    git=run('original_blob_'+str(len(files)),['git','show',HEAD+':'+e['path']])
    assert git.returncode==0 and git.stdout==b
    blob=hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest();assert blob==e['git_blob_sha']
    files.append({'path':e['path'],'bytes':len(b),'sha256':e['sha256'],'git_blob_sha':blob,'original_head_bytes_match':True})
assert len(files)==22 and len(list(P.rglob('*.*')))==21
nested=[]
for name in ['TURN_1_MANIFEST.json','FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','final_review/REVIEW_MANIFEST.json']:
    mp=P/name;m=json.loads(mp.read_text())
    for e in m['files']:
        file=mp.parent/e['path'];b=file.read_bytes()
        assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(name,e['path'])
        nested.append({'manifest':name,'path':e['path'],'bytes':len(b),'sha256':e['sha256']})
assert len(nested)==48
pub=json.loads((P/'PUBLICATION_MANIFEST.json').read_text())
assert pub['author_manifest_sha256']==hashlib.sha256((P/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()
assert pub['review_manifest_sha256']==hashlib.sha256((P/'final_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()
author=run('author_tree',['git','ls-tree','-r','--name-only',AUTHOR,'--','unsolved_math_prioritization/attempts/2303016'])
author_paths=author.stdout.decode().splitlines();assert len(author_paths)==14
for i,path in enumerate(author_paths):
    z=run('author_blob_'+str(i),['git','show',AUTHOR+':'+path]);assert z.returncode==0 and z.stdout==(F/path).read_bytes()
ancestry=run('author_ancestry',['git','merge-base','--is-ancestor',AUTHOR,HEAD]);assert ancestry.returncode==0
changed=run('changed_files',['git','diff','--name-status',BASE,HEAD]);assert changed.returncode==0
assert {x.split('\t')[-1] for x in changed.stdout.decode().splitlines()}=={e['path'] for e in S['files']}
queue=run('queue_diff',['git','diff','--unified=2',BASE,HEAD,'--','unsolved_math_prioritization/QUEUE.md']);assert queue.returncode==0
bq=run('base_queue',['git','show',BASE+':unsolved_math_prioritization/QUEUE.md']);assert bq.returncode==0
old=bq.stdout.decode().splitlines();new=(F/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines()
assert len(old)==len(new)
changes=[(i+1,a,b) for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert len(changes)==1
line,a,b=changes[0];assert '2303016 / AMR-022-3016' in a
assert b==a.replace('| queued | 0/5 |','| already_solved | 1/5 |')
author_check=run('author_checks',[sys.executable,str(P/'verify_turn1.py')]);assert author_check.returncode==0 and not author_check.stderr
assert author_check.stdout==(P/'TURN_1_CHECKS.json').read_bytes();assert json.loads(author_check.stdout)['assertions']==2690
historical=run('historical_review',[sys.executable,str(P/'final_review/check.py'),str(P)]);assert historical.returncode==0 and not historical.stderr
assert historical.stdout==(P/'final_review/CHECKS.json').read_bytes();assert json.loads(historical.stdout)['independent_assertions']==1909
# Deliberate in-memory binding failure: distinguish evidence integrity from a trusted label.
mutated=(P/'TURN_1.md').read_bytes()+b'\n';assert hashlib.sha256(mutated).hexdigest()!=next(e['sha256'] for e in S['files'] if e['path'].endswith('/TURN_1.md'))
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_head':HEAD,'base':BASE,'author_checkpoint':AUTHOR,'snapshot_file_bindings':files,'nested_bindings':nested,'nested_binding_count':len(nested),'author_checkpoint_files':14,'author_checkpoint_byte_preservation':True,'queue_changed_line':line,'queue_only_status_and_turn_cells':True,'author_output_exact':True,'historical_review_output_exact':True,'one_byte_mutation_rejected':True,'commands':commands,'limitations':['Local exact original-head evidence; live prepared head and remote identity require a fresh later review.','Historical duplicate-search narrative is read and bounded by its own stated inaccessible-object limitation; not independently exhaustive.','Finite controls do not certify the all-set analytical theorem.']}
(R/'FROZEN_PACKET_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','snapshot_files':22,'nested_bindings':48,'author_checkpoint_files':14,'author_assertions':2690,'historical_review_assertions':1909,'queue_line':line,'commands':len(commands),'gap':'live prepared exact-head audit remains'},indent=2))
