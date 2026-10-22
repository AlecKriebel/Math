from pathlib import Path
import ast,datetime,hashlib,json,os,runpy,shutil,subprocess,sys,tempfile,zipfile
H=Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication';os.environ['TMPDIR']=str(H/'_local');tempfile.tempdir=str(H/'_local')
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def rejected(fn,label):
 try:fn()
 except Exception as e:return {'case':label,'rejected':True,'reason':str(e)}
 raise RuntimeError('Unexpectedly accepted '+label)
build=json.loads((P/'BUILD_RECEIPT.json').read_text());zpath=P/build['verification_zip']['path'];pdf=P/build['pdf']['path'];ctx=json.loads((A/'CURRENT_PR1280_CONTEXT.json').read_text());results={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_archive_sha256':sha(zpath.read_bytes()),'actual_pdf_sha256':sha(pdf.read_bytes()),'program_ast_assert_counts':{},'replays':[],'corruptions':[]}
need(results['actual_archive_sha256']=='7c9956d47bc31f1a26176ab4fc2ab3b9fe99098d0d012963cc7a51fed34d0c09','zip anchor');need(results['actual_pdf_sha256']=='e06c466e33fc4f78ee8e8a6b7c0b930925ae806563c8f5d52f3a5ee5719cce06','PDF anchor')
with tempfile.TemporaryDirectory(prefix='actual-archive-',dir=H/'_local') as scratch:
 root=Path(scratch)
 with zipfile.ZipFile(zpath) as z:
  names=z.namelist();need(len(names)==205 and len(set(names))==205,'205unique');need(all(not n.startswith('/') and '..' not in Path(n).parts for n in names),'safezip');z.extractall(root)
 v=runpy.run_path(str(root/'verify.py'));anchors=build['verification_anchors'];registries=ctx['authored_freezes'];need(len(registries)==17,'17registries');members=0
 for reg in registries:
  doc=json.loads((root/reg['path']).read_text());entries=doc[reg['entries_key']];members+=len(entries)
  for e in entries:
   rel=e[reg['path_key']];b=(root/reg['base']/rel).read_bytes();need(len(b)==e[reg['size_key']] and sha(b)==e['sha256'],'familybinding')
 results['registry_count']=len(registries);results['explicit_authored_member_records']=members;need(members==137,'137 explicit family members');results['portable_record_count']=len(ctx['portable_files']);need(len(ctx['portable_files'])==177,'177portable records')
 for spec in ctx['diagnostic_replays']:
  b=(root/spec['program']).read_bytes();count=sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(b)));results['program_ast_assert_counts'][spec['program']]=count;need(count==0,'durable assert')
 for flags in [[],['-O'],['-OO']]:
  args=[x for k,val in anchors.items() for x in ['--expected-'+k+'-sha256',val]];r=subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py'),*args],capture_output=True,text=True,timeout=600);need(r.returncode==0,r.stderr);d=json.loads(r.stdout);need(d['status']=='PASS' and d['authenticated_members']==204,'replayresult');results['replays'].append({'flags':flags,'result':d})
 call=lambda:v['verify'](root,anchors['manifest'],anchors['context'],anchors['snapshot'])
 results['corruptions'].append(rejected(lambda:v['verify'](root,'0'*64,anchors['context'],anchors['snapshot']),'wrong_external_manifest_anchor'))
 for raw in ['current_edition/PROOF.md','original_submitted/ACCEPTANCE.json','manuscript/main.tex','provenance/CURRENT_PR1280_CONTEXT.json','provenance/MATH_GATE.json',registries[0]['path'],ctx['diagnostic_replays'][0]['program']]:
  p=root/raw;b=p.read_bytes();p.write_bytes(b+b'CORRUPT');results['corruptions'].append(rejected(call,'payload_corruption:'+raw));p.write_bytes(b)
 p=root/'UNLISTED.txt';p.write_text('extra');results['corruptions'].append(rejected(call,'extra_member'));p.unlink()
 p=root/'current_edition/README.md';b=p.read_bytes();p.unlink();results['corruptions'].append(rejected(call,'missing_member'));p.write_bytes(b)
 # Defeat a recomputed outer manifest: nested outside context anchor still rejects.
 reg=registries[0];p=root/reg['base']/json.loads((root/reg['path']).read_text())[reg['entries_key']][0][reg['path_key']];b=p.read_bytes();p.write_bytes(b+b'CORRUPT');mp=root/'MANIFEST.json';mb=mp.read_bytes();md=json.loads(mb)
 for e in md['files']:
  if e['path']==p.relative_to(root).as_posix():e['bytes']=p.stat().st_size;e['sha256']=sha(p.read_bytes())
 mp.write_text(json.dumps(md));results['corruptions'].append(rejected(lambda:v['verify'](root,sha(mp.read_bytes()),anchors['context'],anchors['snapshot']),'coupled_outer_rewrite_nested_binding'));p.write_bytes(b);mp.write_bytes(mb)
 # Replay output mismatch must fail under each interpreter optimization setting.
 for flags in [[],['-O'],['-OO']]:
  script="import runpy,json;from pathlib import Path;v=runpy.run_path("+repr(str(root/'verify.py'))+");c=json.loads(Path("+repr(str(root/'provenance/CURRENT_PR1280_CONTEXT.json'))+").read_text());v['replay_diagnostics'](Path("+repr(str(root))+"),c)"
  spec=ctx['diagnostic_replays'][0];p=root/spec['result'];b=p.read_bytes();obj=json.loads(b);obj['ADVERSARIAL_EXTRA']='mismatch';p.write_text(json.dumps(obj));r=subprocess.run([sys.executable,'-B',*flags,'-c',script],capture_output=True,text=True,timeout=300);need(r.returncode!=0 and 'finite replay differs' in r.stderr,'optimized replay negative');results['corruptions'].append({'case':'replay_output_mismatch','flags':flags,'rejected':True});p.write_bytes(b)
results['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();results['status']='PASS';(H/'ARCHIVE_CHECKS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({k:v for k,v in results.items() if k not in ['replays','corruptions','program_ast_assert_counts']}))
