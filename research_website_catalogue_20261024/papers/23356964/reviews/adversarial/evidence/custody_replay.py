#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import hashlib,io,json,zipfile,stat,shutil,subprocess,sys,datetime
O=Path(__file__).resolve().parent;B=O.parents[2];R=O.parent;S=B/'sources';P=S/'published-source/generic-wreath-hyperfiniteness-verification'
def sha(x):return hashlib.sha256(x).hexdigest()
receipt=json.loads((S/'receipt.json').read_text());assets=[]
for row in receipt['files']:
 raw=(S/row['name']).read_bytes()
 assert sha(raw)==row['sha256'] and len(raw)==row['bytes'] and hashlib.md5(raw).hexdigest()==row['md5']
 assets.append({k:row[k] for k in ['name','url','bytes','md5','sha256']})
allmembers=[];nested=[]
def verifyzip(raw,label,base):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None
  seen=set()
  for item in z.infolist():
   q=PurePosixPath(item.filename)
   assert not q.is_absolute() and '..' not in q.parts and '\\' not in item.filename and item.filename not in seen
   seen.add(item.filename)
   if item.is_dir():continue
   assert not stat.S_ISLNK(item.external_attr>>16)
   body=z.read(item);assert body==(base/item.filename).read_bytes()
   allmembers.append({'archive':label,'member':item.filename,'source_path':str((base/item.filename).relative_to(S)),'bytes':len(body),'sha256':sha(body),'crc32':f'{item.CRC:08x}'})
   if item.filename.endswith('.zip'):nested.append((body,item.filename))
verifyzip((S/'generic-wreath-hyperfiniteness-verification.zip').read_bytes(),'public_outer_zip',P)
outer_count=len(allmembers);assert outer_count==121 and len(nested)==3
for raw,label in list(nested):
 if label.endswith('INDEPENDENT_AUDIT_SAFE.zip'):base=P/'source/audit_bundle'
 elif label.endswith('INDEPENDENT_REVIEW_2_SAFE_FREEZE.zip'):base=P/'source/independent_review_2'
 elif label.endswith('AUTHOR_SAFE_FREEZE.zip'):base=P/'source'
 else:raise AssertionError(label)
 verifyzip(raw,label,base)
assert len(allmembers)==172
readers=[m for m in allmembers if m['member'].endswith('.pdf')]
assert len(readers)==1 and readers[0]['sha256']==assets[0]['sha256']
prim=[]
for row in json.loads((B/'reviews/scope/primary-source-receipts.json').read_text()):
 if row['status']!='acquired':continue
 src=B/'reviews/scope/cache/primary-sources'/row['name'];raw=src.read_bytes()
 assert sha(raw)==row['sha256'] and len(raw)==row['bytes']
 dest=R/'cache'/('primary-'+src.stem+'.txt')
 subprocess.run(['pdftotext','-layout',str(src),str(dest)],check=True)
 assert dest.read_bytes()==src.with_suffix('.txt').read_bytes()
 prim.append({k:row[k] for k in ['name','url','version','bytes','sha256']}|{'fresh_text_sha256':sha(dest.read_bytes()),'fresh_text_matches_text_read':True})
assert len(prim)==7
record=json.loads((S/'record.json').read_text())
c={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'receipt_sha256':sha((S/'receipt.json').read_bytes()),'record_sha256':sha((S/'record.json').read_bytes()),'metadata':{k:record['metadata'].get(k) for k in ['title','version','publication_date']},'record_created':record['created'],'record_updated':record['updated'],'public_assets':assets,'outer_regular_members':outer_count,'nested_regular_members':len(allmembers)-outer_count,'total_regular_members':len(allmembers),'nested_archives':len(nested),'members':allmembers,'reader_map':readers,'primary_sources':prim,'historical_handling':'Archive/member names and opaque bytes only, not assessment bodies. Full wrapper historical acceptance path not run.'}
(O/'custody.json').write_text(json.dumps(c,indent=2)+'\n')
work=R/'replay-work';work.mkdir(exist_ok=True);copy=work/'published-copy'
assert not copy.exists(),'Do not restart existing replay blindly'
shutil.copytree(P,copy)
for row in allmembers:assert sha((S/row['source_path']).read_bytes())==row['sha256']
indexhash=sha((P/'package_index.json').read_bytes());runs=[]
commands=[('package-integrity',[sys.executable,'-I','-B',str(copy/'verify_package.py'),indexhash])]
for name,member in [('author-math','source/author/checks.py'),('independent-diagnostics','source/independent_review_2/independent_diagnostics.py'),('current-boundary','audits/slab/boundary_diagnostics.py')]:
 commands.append((name,[sys.executable,'-I','-B',str(O/'helper_runner.py'),str(copy/member)]))
for name,cmd in commands:
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=180,cwd=work)
 (O/(name+'.stdout.json')).write_text(p.stdout);(O/(name+'.stderr.log')).write_text(p.stderr)
 runs.append({'name':name,'command':cmd,'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'stdout_sha256':sha(p.stdout.encode()),'stderr_sha256':sha(p.stderr.encode())})
 assert p.returncode==0,(name,p.stderr)
 data=json.loads(p.stdout)
 if name=='package-integrity':assert data['regular_files']==121 and data['infinite_theorem_verified_by_program'] is False
 if name in ['author-math','current-boundary']:assert data['all_checks_passed'] is True
 if name=='current-boundary':assert data['infinite_theorem_verified'] is False
for row in assets:assert sha((S/row['name']).read_bytes())==row['sha256']
for row in allmembers:assert sha((S/row['source_path']).read_bytes())==row['sha256']
(O/'selective-replay-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'package_index_sha256':indexhash,'full_wrapper_executed':False,'historical_acceptance_bodies_read':False,'all_public_and_extracted_source_bytes_unchanged_after_replay':True,'scope':'Integrity plus three unchanged finite mathematical programs. No inherited acceptance or priority assertion is a premise.'},indent=2)+'\n')
print(json.dumps({'runs':[(x['name'],x['returncode']) for x in runs],'member_count':len(allmembers),'primary_files':len(prim),'all_sources_unchanged':True},indent=2))
