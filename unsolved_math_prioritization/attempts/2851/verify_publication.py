#!/usr/bin/env python3
"""Fail-closed publication integrity and replay controls, not a formal proof checker."""
import argparse,copy,hashlib,io,json,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
STEM='STRONG_HEEGAARD_2851_'
PINS={
 'AUTHOR_SAFE_FREEZE.zip':(14473,'0b194b2b9ee859709b8e668f881aeb2db4939cc3939b2a99a6d79bfebbc02dda'),
 'AUTHOR_EXTERNAL_MANIFEST.json':(1825,'fee2951571dfc9e040fb822d077d10eead948d6ab60abc93a62f0936ec59004d'),
 'INDEPENDENT_AUDIT_SAFE.zip':(36501,'b19799aa5ef869be3e8b9310ea9d5170c00848e3da0c85cfc2ec19e09e0cbd9a'),
 'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(2862,'ff2f3c3468e20ea4dbf61e10f76e8067a28e08d560a34cc89b6c18561ea4608e'),
 'INDEPENDENT_AUDIT_RECEIPT.json':(1576,'a4f57c1c729ec12bcc7544e0520076ae0221a66c8b6794935e2957dceb6b3aee')}
PINS={'archives/'+STEM+k:v for k,v in PINS.items()}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_INPUT_REPLAY.json','verify_publication.py'}
TAGS=[('AUTHOR','original_author','SAFE_FREEZE.zip',10),('INDEPENDENT_AUDIT','independent_audit','SAFE.zip',15)]
FALSE=['full_problem_solved','full_problem_refuted','manifold_counterexample_constructed','novelty_claim','formal_proof_claim','human_peer_review_claim','source_contents_included','dataset_contents_included','new_proof_search_performed','new_source_retrieval_or_inspection_claimed','correction_required']
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def enc(o):return (json.dumps(o,indent=2,sort_keys=True)+'\n').encode()
def pin(b,size,digest):need(type(size) is int and (len(b),sha(b))==(size,digest),'size/hash pin mismatch')
def safe(n):
 need(type(n) is str and bool(n),'invalid path type');p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and str(p)==n and '\\' not in n,'unsafe path')
def unpack(raw,ext,count):
 pin(raw,ext['archive_bytes'],ext['archive_sha256']);rows=ext['files'];need(len(rows)==count and len({r['path'] for r in rows})==count,'external manifest duplicates/count');z=zipfile.ZipFile(io.BytesIO(raw));need(len(z.namelist())==len(set(z.namelist()))==count and set(z.namelist())=={r['path'] for r in rows},'archive exact inventory');need(z.testzip() is None,'archive CRC');pack={}
 for i in z.infolist():
  safe(i.filename);need('/' not in i.filename and stat.S_ISREG(i.external_attr>>16),'flat regular members required');pack[i.filename]=z.read(i.filename)
 for row in rows:
  need(set(row)=={'path','bytes','sha256'},'manifest row schema');pin(pack[row['path']],row['bytes'],row['sha256'])
 need(json.loads(pack['MANIFEST.json'])['allowed_files']==[r for r in rows if r['path']!='MANIFEST.json'],'internal/external manifest consistency')
 return pack

def validate(files,manifest_pin=None):
 expected=set(PINS)|EXTRA;packs={}
 for n,(size,digest) in PINS.items():need(n in files,'missing frozen file');pin(files[n],size,digest)
 for tag,leaf,suffix,count in TAGS:
  pre='archives/'+STEM+tag+'_';ext=json.loads(files[pre+'EXTERNAL_MANIFEST.json']);need(ext['problem_id']==2851,'external identity');p=unpack(files[pre+suffix],ext,count);packs[tag]=p
  for n,b in p.items():expected.add(leaf+'/'+n);need(files.get(leaf+'/'+n)==b,'loose/archive mismatch '+n)
 need(set(files)==expected,'public allowlist mismatch')
 for n,b in files.items():
  safe(n)
  if not n.endswith('.zip'):need(all(t not in b.decode() for t in ['/'+'workspace/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','private_'+'sources/','agent_'+'notes/']),'private path marker')
 au=packs['AUTHOR'];ad=packs['INDEPENDENT_AUDIT'];ac=json.loads(ad['ACCEPTANCE.json']);meta=json.loads(files['PUBLICATION_METADATA.json']);receipt=json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_RECEIPT.json'])
 need(ad['AUTHOR_SAFE_FREEZE.zip']==files['archives/'+STEM+'AUTHOR_SAFE_FREEZE.zip'] and ad['AUTHOR_EXTERNAL_MANIFEST.json']==files['archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json'],'nested originals exact')
 need(ac['decision']==receipt['decision']==meta['decision']=='ACCEPT_UNCHANGED_RESTRICTED_PARTIAL','acceptance decision')
 for x in [ac,meta,receipt]:need(x['problem_id']==2851 and x['problem_number']=='KP-3.53' and x['rank']==914 and type(x['turns_used']) is int and x['turns_used']==3 and x['turn_limit']==5,'identity and disposition')
 need(meta['status']=='unsolved','canonical status');need(meta['historical_freeze_fields_preserved'] is True,'preserve history')
 for k in FALSE:need(meta[k] is False,'publication overclaim '+k)
 for k in ['full_problem_solved','full_problem_refuted','manifold_counterexample_constructed','novelty_claim','correction_required','publication_performed']:need(ac[k] is False,'acceptance scope '+k)
 need(ac['original_archive_preserved'] is True and ac['accepted_author_archive_bytes']==14473 and ac['accepted_author_archive_sha256']==PINS['archives/'+STEM+'AUTHOR_SAFE_FREEZE.zip'][1],'exact accepted author')
 need(meta['accepted_scope']==ac['accepted_scope'] and meta['excluded_generalizations']==ac['excluded_generalizations'],'exact acceptance scope')
 need(receipt['audit_archive_sha256']==PINS['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'][1] and receipt['audit_external_manifest_sha256']==PINS['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'][1],'receipt pins')
 old=json.loads(au['STATUS.json']);need(old['audit_status']=='pending independent audit' and old['publication_status']=='not published','historical author fields')
 ir=json.loads(ad['INDEPENDENT_RESULTS.json']);need(ir['boundary_histogram']=={'1':2688,'3':11680,'5':2016},'independent histogram')
 q=meta['queue'];need(q['actually_changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 if manifest_pin is not None:
  need(re.fullmatch('[0-9a-f]{64}',manifest_pin) is not None and sha(files['PUBLICATION_MANIFEST.json'])==manifest_pin,'external publication manifest pin');m=json.loads(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['schema']=='public-file-manifest-v1' and m['problem_id']==2851,'manifest identity');need(len(rows)==len(files)-1 and len({r['path'] for r in rows})==len(rows) and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'manifest inventory')
  for r in rows:need(set(r)=={'path','bytes','sha256'},'manifest row');pin(files[r['path']],r['bytes'],r['sha256'])
 return {'status':'PASS','public_files_checked':len(files),'author_members':10,'audit_members':15,'nested_originals_exact':True,'historical_fields_preserved':True,'canonical_status':'unsolved','turns':'3/5','formal_proof_checked':False}

def check_queue(base,new,meta):
 q=meta['queue'];need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'] and git(base)==q['base_git_blob_sha'] and git(new)==q['new_git_blob_sha'],'queue hashes');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'queue line count');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 914 | 2851 / KP-3.53 |'),'unique target row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y) and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9],'Status/Turns only');need(y[8:10]==[b' unsolved ',b' 3/5 '],'new queue cells');return {'status':'PASS','changed_cells':['Status','Turns'],'findings_and_all_unrelated_bytes_preserved':True}

def wrapper_negatives(files):
 rejected=[]
 def reject(label,mutate,manifest=False):
  f=dict(files);mutate(f)
  try:validate(f,sha(files['PUBLICATION_MANIFEST.json']) if manifest else None)
  except Exception:rejected.append(label);return
  raise RuntimeError('negative accepted '+label)
 for n in PINS:reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'changed'))
 for n in ['original_author/REPORT.md','original_author/STATUS.json','independent_audit/INDEPENDENT_AUDIT.md','independent_audit/ACCEPTANCE.json','independent_audit/replay.py','independent_audit/AUTHOR_SAFE_FREEZE.zip']:
  reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'changed'))
 reject('missing member',lambda f:f.pop('original_author/README.md'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('traversal',lambda f:f.__setitem__('../x',b'x'))
 for k,v in [('status','partial'),('status','verified_solved'),('turns_used',4),('turns_used',True),('historical_freeze_fields_preserved',False),('accepted_scope','all diagrams'),('excluded_generalizations',[])]+[(k,True) for k in FALSE]:
  def alter(f,k=k,v=v):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('bad claim '+k+'='+str(v),alter)
 reject('stale wrapper manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),True);reject('corrupt manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),True)
 try:need(False,'intentional false guard')
 except RuntimeError:rejected.append('explicit need(False)')
 else:raise RuntimeError('guard disabled')
 return {'count':len(rejected),'rejected':rejected}

def command(script,flags=(),extra=(),cwd=None):return subprocess.run([sys.executable,'-B',*flags,str(script),*map(str,extra)],cwd=cwd,capture_output=True,timeout=240)
def replay(files):
 out=[]
 with tempfile.TemporaryDirectory(prefix='strong-heegaard-public-replay-') as td:
  t=Path(td);a=t/'audit';a.mkdir();other=t/'unrelated';other.mkdir()
  for n,b in unpack(files['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'],json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json']),15).items():(a/n).write_bytes(b)
  for script,expected in [('replay.py','REPLAY_RESULTS.json'),('test_artifact_integrity.py','ARTIFACT_INTEGRITY_TESTS.json'),('independent_check.py','INDEPENDENT_RESULTS.json')]:
   outputs=[]
   for flags in [[],['-O']]:
    p=command(a/script,flags,cwd=other);need(p.returncode==0 and not p.stderr,'replay failed '+script+': '+p.stderr.decode());need(p.stdout==files['independent_audit/'+expected],'replay record mismatch '+script);outputs.append(p.stdout);out.append({'script':script,'mode':'optimized' if flags else 'normal','exit_code':0,'exact_record_match':True,'output_sha256':sha(p.stdout)})
   need(outputs[0]==outputs[1],'normal/optimized agreement')
 return {'status':'PASS','fresh_authenticated_extraction':True,'unrelated_working_directory':True,'runs':out,'fixture_rejections_per_outer_replay':50,'artifact_integrity_rejections_per_run':14,'independent_cyclic_orders':16384,'independent_mirror_cases':16384,'formal_proof':False}

def inputs(files,catalog,problems,research,pdfdir):
 out=[]
 with tempfile.TemporaryDirectory(prefix='strong-heegaard-inputs-') as td:
  p=Path(td)/'verify_source_pins.py';p.write_bytes(files['independent_audit/verify_source_pins.py'])
  for flags in [[],['-O']]:
   r=command(p,flags,['--catalog',catalog,'--problems',problems,'--research',research,'--pdf-dir',pdfdir],td);need(r.returncode==0 and not r.stderr,'source/corpus replay failed');need(r.stdout==files['independent_audit/SOURCE_PIN_RESULTS.json'],'source/corpus saved record mismatch');out.append(r.stdout)
 need(out[0]==out[1],'source/corpus modes match')
 return {'status':'PASS','normal_optimized_match':True,'three_full_corpora':True,'five_pdf_pins':True,'exact_record_report_and_statement':True,'output_sha256':sha(out[0]),'new_source_retrieval_or_inspection':False}

def load_files(root):
 need(root.is_dir() and not root.is_symlink(),'regular root directory');paths=list(root.rglob('*'));need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths),'regular files only, no symlinks');files={p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()};dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need({p.relative_to(root).as_posix() for p in paths if p.is_dir()}==dirs,'unlisted empty directory');return files

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path,nargs='?',default=Path('.'));p.add_argument('--manifest-sha256',required=True);p.add_argument('--replay',action='store_true');p.add_argument('--base-queue',type=Path);p.add_argument('--queue',type=Path);p.add_argument('--catalog',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research',type=Path);p.add_argument('--pdf-dir',type=Path);a=p.parse_args();files=load_files(a.directory);r=validate(files,a.manifest_sha256);r['wrapper_controls']=wrapper_negatives(files);need(bool(a.base_queue)==bool(a.queue),'both queue inputs required');r['queue_check']=check_queue(a.base_queue.read_bytes(),a.queue.read_bytes(),json.loads(files['PUBLICATION_METADATA.json'])) if a.queue else {'status':'NOT_RUN'};r['computational_replay']=replay(files) if a.replay else {'status':'NOT_RUN'};opts=[a.catalog,a.problems,a.research,a.pdf_dir];need(all(opts) or not any(opts),'all four source input options required');r['external_input_replay']=inputs(files,*opts) if all(opts) else {'status':'NOT_RUN'}
 if all(opts):need(r['external_input_replay']==json.loads(files['PUBLICATION_INPUT_REPLAY.json']),'publication input replay match')
 print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
