#!/usr/bin/env python3
"""Fail-closed static integrity and patch-derivation checks, not a mathematical proof checker."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,re,stat,subprocess,sys,tempfile,zipfile
PINS={'UNIFORM_HEEGAARD_2832_AUTHOR_VALIDATION_RECEIPT.json': [567, '6988810a0896ad99e3e0bc4da129e74479d75d9bea47930e0a3e02697387ce36'], 'UNIFORM_HEEGAARD_2832_INDEPENDENT_AUDIT_RECEIPT.json': [2502, '86530c25c2912f5c6d333d2d7e1dd4bfc9af5ec680a3bdef8860d4de8c8cb361'], 'archives/UNIFORM_HEEGAARD_2832_AUTHOR_EXTERNAL_MANIFEST.json': [1376, '1dcc35bc15ef26eca2791af98d1554dda4500da9290f7051e3c8959e17039db8'], 'archives/UNIFORM_HEEGAARD_2832_AUTHOR_SAFE_FREEZE.zip': [9711, 'f6fa08d1a90fbb0b44f4098b260a7e22e99d2fd72f24f6e62df0f62791648244'], 'archives/UNIFORM_HEEGAARD_2832_CORRECTED_EXTERNAL_MANIFEST.json': [2147, 'f23a8c8979de833ff5e122475e2c74a29ad9eda832bffe0d97f4d6f4ca7aaacf'], 'archives/UNIFORM_HEEGAARD_2832_CORRECTED_SAFE.zip': [10087, '7e3dae1948520099fb9cf90daf8a56ee3aae828bf21c8d593658c583157aed3f'], 'archives/UNIFORM_HEEGAARD_2832_EXACT_ACCEPTANCE_EXTERNAL_MANIFEST.json': [851, 'bbb1e28116166b1d7119873af3e2f1e3f1ec2047803f7b59bc7284041be19983'], 'archives/UNIFORM_HEEGAARD_2832_EXACT_ACCEPTANCE_SAFE.zip': [3001, 'e65782c6581cf11d0e7f83eca36108e59256721f500c8aa73a76ff5e546c094a'], 'archives/UNIFORM_HEEGAARD_2832_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': [4275, '6828a05ae9c4346530782d067030df802b2a1a7bc5084be532dda488b2e96bb8'], 'archives/UNIFORM_HEEGAARD_2832_INDEPENDENT_AUDIT_SAFE.zip': [40393, '08d7f1daea6ac3ea9d6f02c31ea940846122b5f618a72da73293d5ea29033936']}
STEM='UNIFORM_HEEGAARD_2832_'
TAGS=[('AUTHOR','_SAFE_FREEZE.zip',6),('CORRECTED','_SAFE.zip',6),('INDEPENDENT_AUDIT','_SAFE.zip',23),('EXACT_ACCEPTANCE','_SAFE.zip',2)]
EXTRAS={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_INPUT_REPLAY.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_MANIFEST.json','verify_publication.py'}
FALSE_CLAIMS=['full_solution','counterexample','novelty_claim','formal_proof_claim','source_contents_included','dataset_contents_included','new_proof_search_performed','new_source_retrieval_or_visual_inspection_claimed','original_unconditionally_accepted']
def need(ok,why):
 if not ok:raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
def safe(n):
 need(type(n) is str and bool(n),'path type');p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts and str(p)==n and '\\' not in n,'safe path')
def pin(b,size,digest):need(type(size) is int and size>=0 and type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest) is not None and (len(b),sha(b))==(size,digest),'byte/hash pin')
def archive(raw,ext,count):
 need(ext['problem_id']==2832 and ext['problem_number']=='KP-3.34' and ext['executable_files']==[],'archive identity/scope');pin(raw,ext['archive']['bytes'],ext['archive']['sha256']);rows=ext['files'];need(len(rows)==count and len({r['path'] for r in rows})==count,'manifest members');z=zipfile.ZipFile(io.BytesIO(raw));names=z.namelist();need(len(names)==len(set(names))==count and set(names)=={r['path'] for r in rows},'ZIP inventory');need(z.testzip() is None,'CRC');out={}
 for row in rows:
  n=row['path'];safe(n);info=z.getinfo(n);mode=info.external_attr>>16;need(stat.S_ISREG(mode) and not mode&0o111,'regular non-executable ZIP members');b=z.read(n);pin(b,row['bytes'],row['sha256']);b.decode('utf8');need(PurePosixPath(n).suffix in ['.json','.md','.patch'],'data suffix');out[n]=b
 return out

def validate(files,manifest_pin=None):
 for n in files:safe(n)
 for n,(size,digest) in PINS.items():pin(files[n],size,digest)
 packets={};expected=set(PINS)|EXTRAS
 for tag,suffix,count in TAGS:
  ext=json.loads(files['archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json']);pack=archive(files['archives/'+STEM+tag+suffix],ext,count);packets[tag]=pack
  leaf={'INDEPENDENT_AUDIT':'independent_audit','EXACT_ACCEPTANCE':'exact_acceptance'}.get(tag)
  if leaf:
   for n,b in pack.items():need(files[leaf+'/'+n]==b,'extracted member match');expected.add(leaf+'/'+n)
 need(set(files)==expected,'exact public inventory')
 original=packets['AUTHOR'];corrected=packets['CORRECTED'];audit=packets['INDEPENDENT_AUDIT'];accept=packets['EXACT_ACCEPTANCE']
 for n,b in original.items():need(audit['author_original/'+n]==b,'audit original match')
 for n,b in corrected.items():need(audit['corrected/'+n]==b,'audit corrected match')
 for n,b in accept.items():need(audit['audit/'+n]==b,'audit exact acceptance match')
 for tag,n in [('AUTHOR','author'),('CORRECTED','corrected')]:need(audit['metadata/'+n+'_external_manifest.json']==files['archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json'],'nested external manifest')
 a=json.loads(accept['acceptance_report.json']);need(a['decision']=='accept_corrected_stopped_partial' and a['problem_id']==2832 and a['catalog_rank']==912,'exact acceptance identity')
 for key,tag,suffix in [('original_archive','AUTHOR','_SAFE_FREEZE.zip'),('original_external_manifest','AUTHOR','_EXTERNAL_MANIFEST.json'),('accepted_archive','CORRECTED','_SAFE.zip'),('accepted_external_manifest','CORRECTED','_EXTERNAL_MANIFEST.json')]:
  row=a[key];b=files['archives/'+STEM+tag+suffix];pin(b,row['bytes'],row['sha256']);need(row['filename']==STEM+tag+suffix,'acceptance filename')
 for key,n in [('correction_patch','correction.patch'),('derivation_replay','replay_verification.json'),('analytic_audit_report','audit_report.md')]:row=a[key];pin(audit['audit/'+n],row['bytes'],row['sha256'])
 for key,tag in [('original_members','AUTHOR'),('accepted_members','CORRECTED')]:need(a[key]==json.loads(files['archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json'])['files'],'acceptance full inventory')
 need(len(a['verified_mathematical_propositions'])==4 and all(x['decision']=='pass_unchanged' for x in a['verified_mathematical_propositions']),'four unchanged propositions')
 for k in ['full_conjecture_proved','counterexample_constructed','novelty_claimed','cited_literature_full_proofs_independently_audited','finite_computation_is_theorem_proof']:need(a[k] is False,'acceptance limit '+k)
 need(a['approaches_used']==4 and a['approach_limit']==5,'approaches')
 need(json.loads(original['checks.json'])['independent_audit_completed'] is False,'historical pending author');need(json.loads(corrected['checks.json'])['independent_audit_completed'] is True,'corrected acceptance')
 need(original['approach_log.md']==corrected['approach_log.md'] and original['source_metadata.json']==corrected['source_metadata.json'],'unchanged original members')
 old=b'[JF], Theorem 1, bounds the final flip genus';new=b'For initial genus g >= 2, [JF], Theorem 1, bounds the final flip genus';need(original['proof.md'].count(old)==1 and original['proof.md'].replace(old,new)==corrected['proof.md'],'sole proof citation correction')
 meta=json.loads(files['PUBLICATION_METADATA.json']);need(meta['problem_id']==2832 and meta['problem_number']=='KP-3.34' and meta['rank']==912 and meta['status']=='unsolved' and type(meta['approaches_used']) is int and meta['approaches_used']==4 and meta['approach_limit']==5,'publication identity/status')
 for k in FALSE_CLAIMS:need(meta[k] is False,'publication claim '+k)
 need(meta['historical_freeze_fields_preserved'] is True and meta['four_structural_proofs_unchanged'] is True,'publication history');q=meta['queue'];need(q['actually_changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='4/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 if manifest_pin is not None:
  need(type(manifest_pin) is str and re.fullmatch('[0-9a-f]{64}',manifest_pin) is not None and sha(files['PUBLICATION_MANIFEST.json'])==manifest_pin,'external manifest pin');m=json.loads(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['problem_id']==2832 and len(rows)==len(files)-1 and len({r['path'] for r in rows})==len(rows) and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'public manifest inventory')
  for r in rows:pin(files[r['path']],r['bytes'],r['sha256'])
 return packets

def replay(packets):
 original=packets['AUTHOR'];corrected=packets['CORRECTED'];patch=packets['INDEPENDENT_AUDIT']['audit/correction.patch']
 with tempfile.TemporaryDirectory(prefix='heegaard-patch-') as t:
  root=Path(t)
  for n,b in original.items():(root/n).write_bytes(b)
  proc=subprocess.run(['patch','--batch','--fuzz=0','-p1'],input=patch,cwd=root,capture_output=True,timeout=30);need(proc.returncode==0 and not proc.stderr and b'fuzz' not in proc.stdout.lower() and b'offset' not in proc.stdout.lower(),'zero-fuzz exact patch replay');need({x.name:x.read_bytes() for x in root.iterdir()}==corrected,'all six patched members byte-identical')
 return {'status':'PASS','patch_exit_code':0,'fuzz':0,'offsets':False,'all_six_corrected_members_exact':True,'mathematical_proof_checked':False}

def check_queue(base,new,meta):
 q=meta['queue'];need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'],'queue pins');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'queue line count');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 912 | 2832 / KP-3.34 |'),'one target queue row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y) and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9] and y[8:10]==[b' unsolved ',b' 4/5 '],'Status/Turns only');return {'status':'PASS','changed_cells':['Status','Turns'],'findings_and_all_other_bytes_preserved':True}

def input_replay(files,catalog,problems,reports,source_dir):
 iv=json.loads(files['independent_audit/audit/input_verification.json']);objects=[];out=[]
 for path,row in zip([catalog,problems,reports],iv['datasets']):
  b=path.read_bytes();pin(b,row['bytes'],row['sha256']);objects.append(json.loads(b));out.append({'label':row['source_label'],'bytes':len(b),'sha256':sha(b),'match':True})
 c,p,r=objects;need(len(c)==15458 and len(p)==15458 and len(r)==6701,'full corpus counts');cs=[x for x in c if str(x['id'])=='2832'];ps=[x for x in p if str(x['id'])=='2832'];need(len(cs)==len(ps)==1 and cs[0]['rank']==912,'unique rank/ID');record=ps[0];need(record['problem_number']==cs[0]['problem_number']=='KP-3.34' and record['problem_number'] not in r,'absent report key');pair=sha(json.dumps([record,r.get(record['problem_number'],{})],sort_keys=True).encode());statement=sha(record['statement'].encode());need(pair==iv['record_report_pair_sha256'] and statement==iv['statement_sha256']==cs[0]['statement_hash'],'exact pair/statement');sv=json.loads(files['independent_audit/audit/source_verification.json']);sources=[]
 for name,row in zip(['k3.pdf','johnson_upper.pdf','hass_thompson_thurston.pdf','johnson_flipping.pdf'],sv['primary_sources']):
  b=(source_dir/name).read_bytes();pin(b,row['retained_pdf_bytes'],row['retained_pdf_sha256']);need(b.startswith(b'%PDF'),'PDF header');sources.append({'title':row['title'],'url':row['url'],'bytes':len(b),'sha256':sha(b),'match':True})
 return {'status':'PASS','problem_id':2832,'rank':912,'full_corpus_integrity':out,'unique_record_and_catalog_match':True,'report_key_present':False,'record_report_pair_sha256':pair,'statement_sha256':statement,'source_pdfs':sources,'new_source_retrieval_or_visual_inspection':False,'scope':'Full local-byte integrity and target-identity replay only; no source or corpus contents included.'}

def negatives(files):
 out=[]
 def reject(label,alter,mp=None):
  f=dict(files);alter(f)
  try:validate(f,mp)
  except (RuntimeError,KeyError,ValueError,TypeError,zipfile.BadZipFile):out.append(label);return
  raise RuntimeError('negative accepted '+label)
 for n in PINS:reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 for n in ['independent_audit/author_original/proof.md','independent_audit/corrected/proof.md','independent_audit/audit/audit_report.md','independent_audit/audit/correction.patch','exact_acceptance/acceptance_report.json']:
  reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 reject('missing member',lambda f:f.pop('independent_audit/corrected/README.md'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('unsafe path',lambda f:f.__setitem__('../x',b'x'))
 for k,v in [('status','solved'),('approaches_used',5),('four_structural_proofs_unchanged',False)]+[(k,True) for k in FALSE_CLAIMS]:
  def alter(f,k=k,v=v):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('bad claim '+k,alter)
 reject('stale README',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),sha(files['PUBLICATION_MANIFEST.json']));reject('wrong manifest pin',lambda f:None,'0'*64);reject('corrupt manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),sha(files['PUBLICATION_MANIFEST.json']))
 try:need(False,'deliberate false guard')
 except RuntimeError:out.append('explicit false guard')
 else:raise RuntimeError('fail-closed guard disabled')
 return {'count':len(out),'rejected':out}

def load_files(root):
 need(not root.is_symlink(),'root symlink');paths=list(root.rglob('*'));need(all(not p.is_symlink() for p in paths),'filesystem symlinks');need(all(p.is_file() or p.is_dir() for p in paths),'nonregular filesystem');return {p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path,nargs='?',default=Path('.'));p.add_argument('--manifest-sha256',required=True);p.add_argument('--base-queue',type=Path);p.add_argument('--queue',type=Path);p.add_argument('--catalog',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-reports',type=Path);p.add_argument('--source-dir',type=Path);args=p.parse_args();f=load_files(args.directory);packets=validate(f,args.manifest_sha256);result={'status':'PASS','public_files_checked':len(f),'archive_member_counts':{k:len(v) for k,v in packets.items()},'patch_replay':replay(packets),'wrapper_negative_controls':negatives(f),'mathematical_proof_checked':False,'queue_check':{'status':'NOT_RUN'},'external_input_replay':{'status':'NOT_RUN'}}
 need(bool(args.base_queue)==bool(args.queue),'both queue paths required')
 if args.queue:result['queue_check']=check_queue(args.base_queue.read_bytes(),args.queue.read_bytes(),json.loads(f['PUBLICATION_METADATA.json']))
 inp=[args.catalog,args.problems,args.research_reports,args.source_dir];need(all(inp) or not any(inp),'all four external input paths required')
 if all(inp):result['external_input_replay']=input_replay(f,*inp);need(result['external_input_replay']==json.loads(f['PUBLICATION_INPUT_REPLAY.json']),'saved input replay match')
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
