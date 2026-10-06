#!/usr/bin/env python3
"""Pinned fail-closed publication audit. No source-free source-validation claim."""
import argparse,hashlib,io,json,os,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
STEM='ASYMMETRIC_EXCLUSION_9600004_'
PINS={
'AUTHOR_SAFE_FREEZE.zip':(18052,'733056f2e46581e6082d1cc320273ecccad48e62efdb1063ebafdad60adf502b'),
'AUTHOR_EXTERNAL_MANIFEST.json':(2000,'a0d7aa3a6e4feaccdb9dde972f3d5456d860a7baf6301c683c1a9c9ec5a21b44'),
'INDEPENDENT_AUDIT_SAFE.zip':(37349,'ea5d96f09003ea21bdc1ebef30e2cb3c8ed020794c0d35be6c2bd903091499ae'),
'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(4935,'2422de8763b36541b1455838ad174544bd50b1165d92694532de3250e0055fae'),
'INDEPENDENT_AUDIT_RECEIPT.json':(1771,'f0223a8f88fe9c6c7e7f55de171e6ace9ab7aa5b71c9e0ef3bf577450102758e')}
PINS={'archives/'+STEM+k:v for k,v in PINS.items()}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_INPUT_REPLAY.json','verify_publication.py'}
TAGS=[('AUTHOR','author_original','SAFE_FREEZE.zip',8,'asymmetric_exclusion_9600004/'),('INDEPENDENT_AUDIT','independent_audit','SAFE.zip',19,'')]
FALSE=['full_resolution','novelty_claim','human_peer_review','formal_verification','source_contents_included','corpus_contents_included','private_coordination_included','author_patch_required','new_proof_search_performed']
MODES=[[],['-O'],['-I','-S'],['-I','-S','-O']]
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def enc(o):return (json.dumps(o,indent=2,sort_keys=True)+'\n').encode()
def pin(b,size,digest):need(type(size) is int and len(b)==size and sha(b)==digest,'size/hash mismatch')
def safe(n):
 p=PurePosixPath(n);need(bool(n) and not p.is_absolute() and '..' not in p.parts and str(p)==n and '\\' not in n,'unsafe path')
def unpack(raw,ext,count,prefix=''):
 pin(raw,ext['archive']['bytes'],ext['archive']['sha256']);rows=ext['members'];need(len(rows)==count and len({r['path'] for r in rows})==count,'manifest inventory');z=zipfile.ZipFile(io.BytesIO(raw));need(len(z.namelist())==len(set(z.namelist()))==count and set(z.namelist())=={prefix+r['path'] for r in rows},'archive exact inventory');need(z.testzip() is None,'CRC');d={}
 for i in z.infolist():
  safe(i.filename);need(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'regular members');d[i.filename]=z.read(i.filename)
 for r in rows:pin(d[prefix+r['path']],r['bytes'],r['sha256'])
 return d

def validate(files,manifest_pin=None):
 expected=set(PINS)|EXTRA;packs={}
 for n,(size,digest) in PINS.items():need(n in files,'missing frozen input');pin(files[n],size,digest)
 for tag,leaf,suffix,count,prefix in TAGS:
  pre='archives/'+STEM+tag+'_';ext=json.loads(files[pre+'EXTERNAL_MANIFEST.json']);need(ext['problem_id']==9600004 and ext['rank']==933,'external identity');pack=unpack(files[pre+suffix],ext,count,prefix);packs[tag]=pack
  for n,b in pack.items():expected.add(leaf+'/'+n);need(files.get(leaf+'/'+n)==b,'loose/archive equality '+n)
 need(set(files)==expected,'publication allowlist')
 for n,b in files.items():
  safe(n)
  if not n.endswith('.zip'):
   t=b.decode('utf-8');need(all(x not in t for x in ['/'+'workspace/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','private_'+'sources/','agent_'+'notes/']),'private marker')
 au,ad=packs['AUTHOR'],packs['INDEPENDENT_AUDIT'];need(ad['audit/FROZEN_AUTHOR_MANIFEST.json']==files['archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json'],'nested author manifest')
 for n,b in au.items():need(ad['original/'+n]==b,'nested author exact')
 ac=json.loads(ad['audit/ACCEPTANCE.json']);meta=json.loads(files['PUBLICATION_METADATA.json']);receipt=json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_RECEIPT.json']);need(ac['decision']==receipt['decision']==meta['decision']=='ACCEPT AS PROVED LOCAL PARTIAL ONLY','decision');need(meta['status']=='unsolved','disposition');need(meta['problem_id']==9600004 and meta['rank']==933 and meta['problem_code']=='AMR-095-0004' and type(meta['turns_used']) is int and meta['turns_used']==3 and meta['turn_limit']==5,'identity/budget');need(meta['original_and_accepted_bytes_preserved'] is True,'preserve originals')
 for k in FALSE:need(meta[k] is False,'overclaim '+k)
 for k in ['full_problem_solved','novelty_claim','human_peer_review','formally_verified','original_correction_required']:need(ac[k] is False,'acceptance scope')
 need((ac['author_archive_bytes'],ac['author_archive_sha256'])==PINS['archives/'+STEM+'AUTHOR_SAFE_FREEZE.zip'],'acceptance pin');need(meta['accepted_theorem']==ac['accepted_theorem'],'theorem scope');need(meta['strict_covariance_for_positive_time_and_nonconstant_functions'] is True and meta['all_disjoint_increasing_event_tests']==174 and meta['distinct_lifted_pairs']==78,'event coverage')
 need(receipt['safe_zip']['sha256']==PINS['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'][1],'receipt archive')
 q=meta['queue'];need(q['changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 if manifest_pin is not None:
  need(re.fullmatch('[0-9a-f]{64}',manifest_pin) and sha(files['PUBLICATION_MANIFEST.json'])==manifest_pin,'external publication manifest pin');m=json.loads(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['problem_id']==9600004 and len(rows)==len(files)-1 and len({r['path'] for r in rows})==len(rows) and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'publication manifest inventory')
  for r in rows:pin(files[r['path']],r['bytes'],r['sha256'])
 return {'status':'PASS','public_files_checked':len(files),'author_members':8,'audit_members':19,'originals_and_nested_author_bytes_exact':True,'canonical_status':'unsolved','turns':'3/5','formal_proof_check':False}

def check_queue(base,new,meta):
 q=meta['queue'];need(len(base)==q['base_bytes'] and len(new)==q['new_bytes'] and sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'] and git(base)==q['base_git_blob_sha'] and git(new)==q['new_git_blob_sha'],'queue pins');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'line count');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 933 | 9600004 / AMR-095-0004 |'),'target row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y) and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9],'only Status/Turns');need(x[8:10]==[b' queued ',b' 0/5 '] and y[8:10]==[b' unsolved ',b' 3/5 '],'cells');return {'status':'PASS','changed_cells':['Status','Turns'],'findings_and_unrelated_bytes_preserved':True,'literal_prefix_preserved':base.splitlines()[0]==new.splitlines()[0]}

def negatives(files):
 labels=[]
 def reject(label,mutate,manifest=False):
  f=dict(files);mutate(f)
  try:validate(f,sha(files['PUBLICATION_MANIFEST.json']) if manifest else None)
  except Exception:labels.append(label);return
  raise RuntimeError('control accepted '+label)
 for n in PINS:reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 for n in ['author_original/asymmetric_exclusion_9600004/PROOF.md','author_original/asymmetric_exclusion_9600004/check_certificate.py','independent_audit/audit/REPORT.md','independent_audit/audit/ACCEPTANCE.json','independent_audit/audit/test_independent.py','independent_audit/audit/independent_recompute.py']:
  reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 reject('missing member',lambda f:f.pop('author_original/asymmetric_exclusion_9600004/certificate.json'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('traversal',lambda f:f.__setitem__('../x',b'x'))
 for k,v in [(k,True) for k in FALSE]+[('status','solved'),('turns_used',True),('turns_used',4),('original_and_accepted_bytes_preserved',False),('accepted_theorem','Full all-time result'),('all_disjoint_increasing_event_tests',6)]:
  def alter(f,k=k,v=v):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('invalid '+k,alter)
 reject('stale README manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),True);reject('corrupt publication manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),True)
 try:need(False,'intentional false guard')
 except RuntimeError:labels.append('explicit false guard')
 else:raise RuntimeError('guard disabled')
 return {'rejected_count':len(labels),'rejected':labels}

def replay(files):
 records=[]
 with tempfile.TemporaryDirectory(prefix='asep public replay ') as td:
  w=Path(td);d=w/'audit packet';other=w/'unrelated working directory';d.mkdir();other.mkdir();ext=json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json']);pack=unpack(files['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'],ext,19)
  for n,b in pack.items():p=d/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  env={'PATH':os.environ.get('PATH',''),'HOME':td,'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
  for flags in MODES:
   outcomes=[]
   runs=[('author_exact','original/asymmetric_exclusion_9600004/check_certificate.py',['--cross-window'],None),('author_controls','original/asymmetric_exclusion_9600004/test_mutations.py',[],'audit/AUTHOR_REPLAY.json'),('independent_exact','audit/independent_recompute.py',[],'audit/INDEPENDENT_RECOMPUTATION.json'),('independent_controls','audit/test_independent.py',[],'audit/INDEPENDENT_CONTROLS.json')]
   for label,script,args,reference in runs:
    p=subprocess.run([sys.executable,*flags,str(d/script),*args],cwd=other,env=env,capture_output=True,timeout=600);need(p.returncode==0 and not p.stderr,'replay failed '+label);r=json.loads(p.stdout)
    if reference:need(p.stdout==pack[reference],'exact saved replay differs '+label)
    if label=='author_controls':need(len(r['negative'])==12 and all(x['rejected'] for x in r['negative']) and len(r['positive'])==4 and all(x['returncode']==0 for x in r['positive']),'author controls count')
    if label=='independent_exact':need(r['ok'] is True and r['cases']==174 and r['distinct_lifted_event_pairs']==78 and r['delta']=='1/10837981440','independent theorem data')
    if label=='independent_controls':need(len(r['certificate_controls'])==18 and len(r['dynamics_controls'])==4 and all(x['rejected'] for x in r['certificate_controls']+r['dynamics_controls']) and len(r['positive'])==4 and all(x['ok'] is True for x in r['positive']) and r['adversarial_distribution']['witness_covariance']=='1/8','independent nonvacuous controls')
    outcomes.append({'label':label,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'exact_reference_match':bool(reference)})
   records.append({'flags':flags,'runs':outcomes,'author_negative_executions_rejected':12,'independent_negative_executions_rejected':22,'total_nonvacuous_negative_executions':34})
 return {'status':'PASS','relocated_fresh_archive_extraction':True,'unrelated_working_directory':True,'outer_runs':records,'source_or_corpus_inputs_validated':False,'analytic_proof_formally_verified':False}

def inputs(files,corpus,pdfs):
 sources=json.loads(files['author_original/asymmetric_exclusion_9600004/SOURCES.json']);datasets={};rows=[]
 for r in sources['public_corpus_verification']:
  b=(corpus/r['name']).read_bytes();pin(b,r['bytes'],r['sha256']);datasets[r['name']]=json.loads(b);rows.append({'name':r['name'],'bytes':len(b),'sha256':sha(b),'match':True})
 cs=[x for x in datasets['catalog.json'] if str(x['id'])=='9600004'];ps=[x for x in datasets['problems.json'] if str(x['id'])=='9600004'];need(len(cs)==len(ps)==1,'unique exact ID');c,p=cs[0],ps[0];need(c['rank']==933 and c['turns_used']==0 and c['problem_number']==p['problem_number']=='AMR-095-0004','corpus gate');b=json.dumps([p,datasets['research_results.json'].get(p['problem_number'],{})],sort_keys=True).encode();cp=sources['canonical_pair'];pin(b,cp['bytes'],cp['sha256']);need(sha(b)==c['review_hash']==cp['catalog_review_hash'],'strict canonical pair');out=[]
 for name,r in zip(['liggett_archive','bbl_arxiv','conroy_sethuraman','conroy2025_k','conroy2025_d'],sources['sources']):
  b=(pdfs/(name+'.pdf')).read_bytes();pin(b,r['bytes'],r['sha256']);out.append({'title':r['title'],'url':r['url'],'bytes':len(b),'sha256':sha(b),'match':True})
 need(len(rows)==3 and len(out)==5,'complete source pin set');return {'status':'PASS','whole_corpora':rows,'canonical_pair':{'bytes':cp['bytes'],'sha256':cp['sha256'],'match':True},'source_pdfs':out,'source_pdfs_hashed':5,'whole_corpora_hashed':3,'new_source_retrieval_or_inspection':False,'raw_source_or_corpus_text_included':False}

def load_files(root):
 need(root.is_dir() and not root.is_symlink(),'regular root');paths=list(root.rglob('*'));need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths),'regular files');files={p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()};dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need({p.relative_to(root).as_posix() for p in paths if p.is_dir()}==dirs,'no unlisted empty directories');return files

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--manifest-sha256',required=True);p.add_argument('--replay',action='store_true');p.add_argument('--base-queue',type=Path);p.add_argument('--queue',type=Path);p.add_argument('--corpus-dir',type=Path);p.add_argument('--pdf-dir',type=Path);a=p.parse_args();f=load_files(a.directory);r=validate(f,a.manifest_sha256);r['wrapper_negative_controls']=negatives(f);need(bool(a.base_queue)==bool(a.queue),'both queues required');r['queue_check']=check_queue(a.base_queue.read_bytes(),a.queue.read_bytes(),json.loads(f['PUBLICATION_METADATA.json'])) if a.queue else {'status':'NOT_RUN'};r['mathematical_replay']=replay(f) if a.replay else {'status':'NOT_RUN'};need(bool(a.corpus_dir)==bool(a.pdf_dir),'all external input options required');r['external_input_replay']=inputs(f,a.corpus_dir,a.pdf_dir) if a.corpus_dir else {'status':'NOT_RUN','reason':'Original source/corpus inputs intentionally absent from safe packet'}
 if a.corpus_dir:need(r['external_input_replay']==json.loads(f['PUBLICATION_INPUT_REPLAY.json']),'source replay record match')
 print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
