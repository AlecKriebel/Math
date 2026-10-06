#!/usr/bin/env python3
"""Static publication integrity and hostile-mutation controls, not a proof checker."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,io,json,stat,zipfile
PINS={
 'INDEPENDENT_AUDIT_RECEIPT.json':(1275,'89a644cdec736b2d25a8138ca345083f2a4e17be8e354aeecf610727af86c480'),
 'PUBLICATION_INPUT_REPLAY.json':(8971,'9685c2c0c4df7208682423ed119d3a0b6b2cb5a3bc71527c6fa82b0f7fac1cca'),
 'archives/TANGLE_STABILIZER_2756_AUTHOR_SAFE_FREEZE.zip':(13913,'72f9afea11f77de85242d98b32b8769beafdf33599ea939a93ba923bf897f652'),
 'archives/TANGLE_STABILIZER_2756_AUTHOR_EXTERNAL_MANIFEST.json':(1774,'2c07eb0303f15e18f7937bc7ec554d0b2384fae38395fa8475334478288a8606'),
 'archives/TANGLE_STABILIZER_2756_INDEPENDENT_AUDIT_SAFE.zip':(30176,'553f0b08a830ea2a1d94d2fd118217b695c022c9f4c7cb8da9e1ed31352cccdc'),
 'archives/TANGLE_STABILIZER_2756_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(2840,'0a2edfa2aef9f5e4ed8352325287711483e3232d0ea87947b97c8570f311de7d')}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_INPUT_REPLAY.json','INDEPENDENT_AUDIT_RECEIPT.json','verify_publication.py'}
FALSE_CLAIMS=['full_solution','new_mathematical_novelty_claimed','general_n_at_least_4_resolved','entire_K_extension_split_claimed','abstract_intersection_example_is_wicket_counterexample','new_correction_patch_needed','formal_verification_claimed','human_peer_review_claimed','mathematical_checker','source_downloads_during_publication','corpus_contents_published']
def need(condition,message):
 if not condition:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(obj):return (json.dumps(obj,indent=2)+'\n').encode()
def safe_path(name):
 p=PurePosixPath(name);need(name and not p.is_absolute() and '..' not in p.parts and '\\' not in name and str(p)==name,'unsafe path')
def validate(files,check_manifest=True):
 for name,(size,digest) in PINS.items():need(name in files and (len(files[name]),sha(files[name]))==(size,digest),'outer pin: '+name)
 expected=set(PINS)|EXTRA;counts=[]
 for tag,leaf,suffix,prefix in [('AUTHOR','original_author','_SAFE_FREEZE.zip','tangle_stabilizer_2756/'),('INDEPENDENT_AUDIT','independent_audit','_SAFE.zip','tangle_stabilizer_2756_independent_audit/')]:
  stem='archives/TANGLE_STABILIZER_2756_'+tag;zn=stem+suffix;m=json.loads(files[stem+'_EXTERNAL_MANIFEST.json']);need(m['problem_id']==2756 and (m['bytes'],m['sha256'])==PINS[zn],'external manifest identity')
  with zipfile.ZipFile(io.BytesIO(files[zn])) as z:
   names=z.namelist();rows=m['archive_members'];need(z.testzip() is None,'archive CRC');need(len(names)==len(set(names))==len(rows) and set(names)=={r['path'] for r in rows},'exact archive inventory')
   for row in rows:
    n=row['path'];safe_path(n);need(n.startswith(prefix),'archive root');info=z.getinfo(n);need(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'nonregular archive member');data=z.read(n);need((len(data),sha(data))==(row['bytes'],row['sha256']),'member pin');dest=leaf+'/'+n[len(prefix):];need(files.get(dest)==data,'loose member mismatch: '+dest);expected.add(dest)
   inner=json.loads(z.read(prefix+'MANIFEST.json'));ir=inner['files'];need(len(ir)==len(names)-1 and {prefix+r['path'] for r in ir}==set(names)-{prefix+'MANIFEST.json'},'inner manifest inventory')
   for row in ir:
    data=z.read(prefix+row['path']);need((len(data),sha(data))==(row['bytes'],row['sha256']),'inner manifest pin')
  counts.append(len(names))
 need(counts==[7,11] and set(files)==expected,'complete public file allowlist')
 for name,data in files.items():
  safe_path(name)
  if not name.endswith('.zip'):
   text=data.decode('utf-8');need(all(marker not in text for marker in ['/'+'work'+'space/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','agent_'+'notes/','private_'+'sources/']),'private path/coordination marker')
 meta=json.loads(files['PUBLICATION_METADATA.json']);need(meta['problem_id']==2756 and meta['problem_number']=='KP-2.8' and meta['rank']==908 and meta['status']=='unsolved','canonical identity/status');need(type(meta['approaches_used']) is int and meta['approaches_used']==3 and meta['approach_limit']==5,'turn count')
 for key in FALSE_CLAIMS:need(meta[key] is False,'forbidden claim: '+key)
 need(meta['historical_freeze_fields_preserved'] is True,'historical bytes');q=meta['queue'];need(q['actually_changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 a=json.loads(files['independent_audit/EXACT_ACCEPTANCE.json']);need(a['decision']=='accept_exact_original_as_partial' and a['problem_id']==2756 and a['required_corrections']==[] and a['full_solution'] is False and a['queue_scope']=={'Status':'partial','Turns':'3/5'},'exact historical acceptance');need(a['checks']=={'source_corpus_archive_pin_checks':45,'author_builder_cases':24,'validator_suite_cases_per_harness':19,'validator_harness_modes':['normal','optimized'],'all_pass':True,'mathematical_checker':False},'audit scope checks')
 receipt=json.loads(files['INDEPENDENT_AUDIT_RECEIPT.json']);need(receipt['decision']==a['decision'] and (receipt['audit_bundle']['bytes'],receipt['audit_bundle']['sha256'])==PINS['archives/TANGLE_STABILIZER_2756_INDEPENDENT_AUDIT_SAFE.zip'],'receipt binding');need(receipt['required_corrections']==[] and receipt['full_solution'] is False,'receipt scope')
 if check_manifest:
  manifest=json.loads(files['PUBLICATION_MANIFEST.json']);rows=manifest['files'];need(manifest['schema']=='public-file-manifest-v1','manifest schema');need(len(rows)==len(files)-1 and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'manifest inventory')
  for row in rows:need((len(files[row['path']]),sha(files[row['path']]))==(row['bytes'],row['sha256']),'manifest file pin')
 return {'status':'PASS','public_files_checked':len(files),'author_archive_members':7,'audit_archive_members':11,'nested_originals_exact':True,'historical_acceptance_preserved':True,'canonical_status':'unsolved','turns':'3/5','mathematical_proof_checked':False,'archive_code_executed':False}
def check_queue(base,new,meta):
 q=meta['queue'];need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'],'queue SHA256 pins');bl=base.splitlines(keepends=True);nl=new.splitlines(keepends=True);need(len(bl)==len(nl),'queue line count');changed=[i for i,(b,n) in enumerate(zip(bl,nl)) if b!=n];need(len(changed)==1,'one queue row only');i=changed[0];need(bl[i].startswith(b'| 908 | 2756 / KP-2.8 |'),'queue identity');bc=bl[i].split(b'|');nc=nl[i].split(b'|');need(len(bc)==len(nc) and [j for j,(b,n) in enumerate(zip(bc,nc)) if b!=n]==[8,9],'Status/Turns only');need(nc[8]==b' unsolved ' and nc[9]==b' 3/5 ','queue disposition');return {'status':'PASS','only_changed_cells':['Status','Turns'],'findings_and_all_unrelated_bytes_preserved':True}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path,nargs='?',default=Path('.'));p.add_argument('--base-queue',type=Path);p.add_argument('--queue',type=Path);args=p.parse_args();root=args.directory.resolve();paths=list(root.rglob('*'));need(not any(x.is_symlink() for x in paths),'no symlinks');files={x.relative_to(root).as_posix():x.read_bytes() for x in paths if x.is_file()};result=validate(files);controls=[]
 def reject(label,alter,manifest=False):
  f=dict(files);alter(f)
  try:validate(f,manifest)
  except (ValueError,KeyError,TypeError,UnicodeDecodeError,zipfile.BadZipFile):controls.append(label);return
  raise ValueError('negative control accepted: '+label)
 for name in PINS:reject('changed pin '+name,lambda f,n=name:f.__setitem__(n,f[n]+b'changed'))
 for name in ['original_author/PROOF.md','independent_audit/AUDIT.md','independent_audit/EXACT_ACCEPTANCE.json','independent_audit/original/TANGLE_STABILIZER_2756_AUTHOR_SAFE_FREEZE.zip']:
  reject('changed loose member '+name,lambda f,n=name:f.__setitem__(n,f[n]+b'changed'))
 reject('missing member',lambda f:f.pop('original_author/README.md'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('traversal',lambda f:f.__setitem__('../extra',b'x'))
 for key,value in [('status','partial'),('status','verified_solved'),('approaches_used',4)]+[(k,True) for k in FALSE_CLAIMS]:
  def alter(f,k=key,v=value):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=encoded(m)
  reject('bad claim '+key+'='+str(value),alter)
 reject('changed wrapper with stale manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'changed'),True)
 def bad_manifest(f):m=json.loads(f['PUBLICATION_MANIFEST.json']);m['files'].pop();f['PUBLICATION_MANIFEST.json']=encoded(m)
 reject('missing manifest entry',bad_manifest,True)
 need(bool(args.base_queue)==bool(args.queue),'both queue inputs required')
 result['queue_check']={'status':'NOT_RUN','reason':'Supply both --base-queue and --queue to check the complete queue delta.'}
 if args.queue:
  base=args.base_queue.read_bytes();new=args.queue.read_bytes();meta=json.loads(files['PUBLICATION_METADATA.json']);result['queue_check']=check_queue(base,new,meta)
  for label,bad in [('unrelated queue byte',new+b'x'),('wrong queue status',new.replace(b'| unsolved | 3/5 |',b'| partial | 3/5 |'))]:
   try:check_queue(base,bad,meta)
   except ValueError:controls.append(label)
   else:raise ValueError('bad queue accepted')
 try:need(False,'deliberate fail-closed control')
 except ValueError:controls.append('explicit need(False)')
 else:raise ValueError('fail-closed guard disabled')
 result['negative_controls_rejected']=controls;result['negative_control_count']=len(controls);print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
