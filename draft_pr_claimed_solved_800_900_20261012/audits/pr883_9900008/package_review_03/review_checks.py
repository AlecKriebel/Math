#!/usr/bin/env python3
"""Independent, bounded review: read sealed input; write only this review's receipts/copies.
No network; no Git mutations; no source corpus writes; all executed candidate bodies
were authenticated and fully read before this harness was written.
"""
import hashlib, io, json, os, shutil, stat, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
A=HERE.parent
ROOT=A/'replay/revision_r2'
PACKAGE=ROOT/'preprint/verification_package'
REPO=A.parents[2]
OUTER='4d3697ad4c38f37528b313626dc072c08c806d27c2a92316d63f4bcc522cfefa'
INDEX='9c547acc859c79b26704df0d9d278aaa469d02e22093b3ab7d199d6b50e2c49b'
VERIFIER='e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8'
ZIP='5fd482efb102cb5cddb85e87d67e4446a35306b7a3c649ed409e46439a531adc'
SOURCE='53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab'
HEAD='af25d26e21945a1a132aace5e600485152777070'
PREPARED='83a9565aa3588dc33abbc293e9f416d1da422bc6'
PREFIX='unsolved_math_prioritization/attempts/9900008/'
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok,label):
 if not ok: raise RuntimeError(label)
def js(p): return json.loads(p.read_bytes())
def emit(name,obj):
 (HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def normalized(x):
 if isinstance(x,str):
  for p,role in sorted([(str(ROOT),'$CANDIDATE'),(str(PACKAGE),'$PACKAGE'),(str(HERE),'$REVIEW'),(str(A),'$AUDIT'),(str(REPO),'$REPOSITORY')],key=lambda t:-len(t[0])): x=x.replace(p,role)
  return x
 if isinstance(x,list): return [normalized(v) for v in x]
 if isinstance(x,dict): return {k:normalized(v) for k,v in x.items()}
 return x
def run(label,argv,cwd,expect=0):
 start=datetime.now(timezone.utc).isoformat()
 p=subprocess.run(argv,cwd=cwd,capture_output=True,timeout=600)
 raw={'label':label,'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'argv':argv,'cwd':str(cwd),'returncode':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()}
 emit('private/'+label+'.json',raw)
 need((p.returncode==0)==(expect==0),label+' wrong exit')
 data=json.loads(p.stdout) if p.stdout else None
 return {'label':label,'started_utc':start,'finished_utc':raw['finished_utc'],'command':normalized(argv),'cwd':'$REVIEW/unrelated','returncode':p.returncode,'raw_stdout_sha256':sha(p.stdout),'raw_stdout_bytes':len(p.stdout),'raw_stderr_sha256':sha(p.stderr),'stderr_bytes':len(p.stderr),'result':normalized(data)}
def inventory():
 seal=js(A/'revision_r2_SEAL.json')
 need(sha((ROOT/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes())==OUTER,'outer seal')
 rows=js(ROOT/'CURRENT_PUBLICATION_MANIFEST.json')['files']
 expected={r['path'] for r in rows}|{'CURRENT_PUBLICATION_MANIFEST.json'}
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
 need(actual==expected and len(actual)==244,'closed244')
 for row in rows:
  b=(ROOT/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'outer '+row['path'])
 for p in ROOT.rglob('*'): need(not p.is_symlink(),'symbolic link')
 need(sha((PACKAGE/'package_index.json').read_bytes())==INDEX,'portable index seal')
 prows=js(PACKAGE/'package_index.json')['files']
 pnames={r['path'] for r in prows}|{'package_index.json'}
 need(len(pnames)==204 and pnames=={p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()},'closed204')
 for row in prows:
  b=(PACKAGE/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'portable '+row['path'])
 core=[]
 for row in seal['core_files']:
  b=(ROOT/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'external core '+row['path']);core.append(row)
 archive=(ROOT/'preprint/verification.zip').read_bytes();need(sha(archive)==ZIP and len(archive)==558456,'zip seal')
 with zipfile.ZipFile(io.BytesIO(archive)) as z:
  need(z.namelist()==sorted(pnames) and len(z.namelist())==204,'closed zip names')
  for name in z.namelist():
   info=z.getinfo(name);need(info.date_time==(2026,10,15,0,0,0) and info.external_attr>>16==(stat.S_IFREG|0o644),'zip metadata')
   need(z.read(name)==(PACKAGE/name).read_bytes(),'zip data')
 sraw=(PACKAGE/'root_evidence/SOURCE_MANIFEST.json').read_bytes();need(sha(sraw)==SOURCE,'source manifest')
 source=json.loads(sraw);need(len(source['files'])==26 and sum(r['bytes'] for r in source['files'])==211771,'source totals')
 gitrows=[]
 for r in source['files']:
  b=(PACKAGE/'source'/r['path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  need(sha(b)==r['sha256'] and len(b)==r['bytes'] and blob==r['git_blob'],'source pin')
  old=subprocess.run(['git','cat-file','blob',HEAD+':'+PREFIX+r['path']],cwd=REPO,capture_output=True,check=True).stdout
  need(old==b,'original actual Git object '+r['path']);gitrows.append({'path':r['path'],'git_blob':blob,'same_as_frozen_git_object':True})
 config=js(ROOT/'CURRENT_PUBLICATION.json')['tooling_layout']
 need(len(config['preserved_source_paths'])==24 and len(config['copy_pairs'])==10,'copy counts')
 for p in config['preserved_source_paths']: need((ROOT/p).read_bytes()==(PACKAGE/'source'/p).read_bytes(),'preserved copy')
 for p in config['copy_pairs']: need((ROOT/p['outer_path']).read_bytes()==(PACKAGE/p['portable_path']).read_bytes(),'copy pair')
 metadata=js(ROOT/'preprint/metadata.json');deposit=js(ROOT/'preprint/zenodo-deposit.json')
 need(metadata==deposit['metadata'],'whole nested metadata')
 need(deposit['files']==[{'path':'output/pdf/note.pdf','name':'diffuse-allocation-note.pdf'},{'path':'verification.zip','name':'diffuse-allocation-verification.zip'}],'exact ordered deposit files')
 prepared=[]
 for name in sorted(actual):
  b=(ROOT/name).read_bytes()
  p=subprocess.run(['git','ls-tree',PREPARED,'--',PREFIX+name],cwd=REPO,capture_output=True,check=True).stdout.decode().strip()
  mode,typ,tail=p.split(' ',2);blob,fn=tail.split('\t',1)
  need(mode=='100644' and typ=='blob' and fn==PREFIX+name,'prepared mode')
  content=subprocess.run(['git','cat-file','blob',blob],cwd=REPO,capture_output=True,check=True).stdout
  need(content==b,'prepared actual blob');prepared.append({'path':name,'mode':mode,'git_blob':blob})
 families=[]
 for row in seal['audit_families']:
  d=PACKAGE/'audits'/row['family'];manifest=js(d/'PUBLIC_MANIFEST.json')
  need(sha((d/'PUBLIC_MANIFEST.json').read_bytes())==row['manifest_sha256'],'family manifest seal')
  mrows=manifest.get('files',manifest.get('allowed_public_files'));names={r['path'] for r in mrows};need(len(names)==row['payload_count'],'family count')
  need({p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()}==names|{'PUBLIC_MANIFEST.json'},'family closed')
  for r in mrows:
   b=(d/r['path']).read_bytes();need(len(b)==r.get('bytes',len(b)) and sha(b)==r['sha256'],'family payload')
  families.append(row)
 result={'status':'PASS','outer_sha256':OUTER,'outer_files':244,'portable_index_sha256':INDEX,'portable_members':204,'archive_sha256':ZIP,'archive_bytes':558456,'core_files':core,'source_manifest_sha256':SOURCE,'source_originals':gitrows,'source_original_total_bytes':211771,'preserved_outer_count':24,'copy_binding_count':10,'whole_nested_deposit_metadata_equal':True,'exact_two_ordered_deposit_files':True,'audit_families':families,'prepared_commit':PREPARED,'prepared_candidate_blobs':prepared,'prepared_scope':'Read-only local object preview; not live PR approval.'}
 emit('INVENTORY_CHECKS.json',result)
 print('inventory PASS',flush=True)
def replays():
 unrelated=HERE/'private/unrelated';unrelated.mkdir(exist_ok=True)
 receipts=[]
 flags=[sys.executable,'-I','-S','-B']
 for optimized in (False,True):
  mode='optimized' if optimized else 'normal';f=flags+(['-O'] if optimized else [])
  r=run('current_'+mode,f+[str(ROOT/'verify_current_publication.py'),OUTER,'--root',str(ROOT)],unrelated)
  need(r['result']['status']=='PASS','current pass');o=r['result']['portable_result']['originals'];need((o['direct_subprocess_count'],o['nested_author_subprocess_count'],o['total_archival_subprocess_count'])==(6,16,22),'default counts');receipts.append(r)
  r=run('verify_only_'+mode,f+[str(ROOT/'verify_current_publication.py'),OUTER,'--root',str(ROOT),'--verify-only'],unrelated)
  o=r['result']['portable_result']['originals'];need((o['direct_subprocess_count'],o['nested_author_subprocess_count'],o['total_archival_subprocess_count'])==(0,0,0),'verify-only counts');receipts.append(r)
  output=HERE/'private'/('build_'+mode)
  r=run('builder_'+mode,f+[str(PACKAGE/'build_verification.py'),str(PACKAGE),INDEX,VERIFIER,str(output)],unrelated)
  need(r['result']['status']=='PASS' and sha((output/'verification.zip').read_bytes())==ZIP and (output/'verification.zip').read_bytes()==(ROOT/'preprint/verification.zip').read_bytes(),'deterministic archive bytes')
  receipts.append(r);shutil.rmtree(output)
  print(mode+' replay + verify-only + builder PASS',flush=True)
 emit('REPLAY_RESULTS.json',{'status':'PASS','receipts':receipts,'raw_receipts_private':True,'normal_optimized_archive_byte_identical':True})
def controls():
 unrelated=HERE/'private/unrelated';flags=[sys.executable,'-I','-S','-B'];out=[]
 with tempfile.TemporaryDirectory(prefix='bounded_controls_',dir=HERE/'private') as td:
  copy=Path(td)/'candidate';shutil.copytree(ROOT,copy,copy_function=shutil.copyfile)
  for optimized in (False,True):
   mode='optimized' if optimized else 'normal';f=flags+(['-O'] if optimized else [])
   command=f+[str(copy/'verify_current_publication.py'),OUTER,'--root',str(copy),'--verify-only']
   out.append(run('bad_outer_pin_'+mode,f+[str(copy/'verify_current_publication.py'),'0'*64,'--root',str(copy),'--verify-only'],unrelated,1))
   target=copy/'preprint/note.tex';before=target.read_bytes();target.write_bytes(before+b'\n')
   out.append(run('changed_core_'+mode,command,unrelated,1));target.write_bytes(before)
   extra=copy/'extra.txt';extra.write_text('bounded control\n');out.append(run('extra_outer_file_'+mode,command,unrelated,1));extra.unlink()
   extra=copy/'unlisted_empty';extra.mkdir();out.append(run('extra_outer_directory_'+mode,command,unrelated,1));extra.rmdir()
   pack=copy/'preprint/verification_package';build=f+[str(pack/'build_verification.py'),str(pack)]
   output=Path(td)/'output'
   out.append(run('bad_builder_index_'+mode,build+['0'*64,VERIFIER,str(output)],unrelated,1))
   out.append(run('bad_verifier_pin_'+mode,build+[INDEX,'0'*64,str(output)],unrelated,1))
   target=pack/'source/author/PROOF.md';before=target.read_bytes();target.write_bytes(before+b'\n')
   out.append(run('changed_portable_member_'+mode,build+[INDEX,VERIFIER,str(output)],unrelated,1));target.write_bytes(before)
   extra=pack/'unlisted_empty';extra.mkdir();out.append(run('extra_portable_directory_'+mode,build+[INDEX,VERIFIER,str(output)],unrelated,1));extra.rmdir()
   need(not output.exists(),'rejected build created output')
   print(mode+' bounded controls PASS',flush=True)
 emit('MUTATION_CONTROLS.json',{'status':'PASS','count':len(out),'scope':'Ordinary pin, changed-artifact and closed-tree controls; no hostile exploitation scope. Rejections precede replay and build output.','receipts':out})
if __name__=='__main__':
 inventory();replays();controls()
