#!/usr/bin/env python3
"""Fail-closed integrity and exact replay; no source-free source-validation claim."""
import argparse,hashlib,io,json,os,re,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
STEM='STRONG_RATIONAL_8500009_'
PINS={
'AUTHOR_SAFE_FREEZE.zip':(15851,'026cecc87b82627bf471ed37ee920ec2203ec8e94cd14f7e1fb0a629469c111c'),
'AUTHOR_EXTERNAL_MANIFEST.json':(1500,'0fcc1d4e600a73113c40b708df26f9aa4d754a7d493af61f499a0c09f6e32342'),
'INDEPENDENT_AUDIT_SAFE.zip':(36039,'c818ef2021df6ca31314472317bdcbbf52594a3783f31863463392d8f7967956'),
'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(3664,'265e46a8c0c78bdda54c9ca6d963464d8631321b67bf25dd515acdde7c306635'),
'INDEPENDENT_AUDIT_RECEIPT.json':(1010,'1ac739a1e3ffd190e6b2af00491171a310ec2a826f6e4fa4b6706e4864343926')}
PINS={'archives/'+STEM+k:v for k,v in PINS.items()}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_INPUT_REPLAY.json','verify_publication.py'}
TAGS=[('AUTHOR','original_author','SAFE_FREEZE.zip',7),('INDEPENDENT_AUDIT','independent_audit','SAFE.zip',17)]
FALSE=['full_resolution','quadruple_constructed','nonexistence_proved','rational_points_classified','novelty_claim','source_contents_included','corpus_contents_included','private_coordination_included','author_patch_required','new_proof_search_performed']
MODES=[[],['-O'],['-I'],['-I','-O']]
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def enc(o):return (json.dumps(o,indent=2,sort_keys=True)+'\n').encode()
def pin(b,size,digest):need(type(size) is int and len(b)==size and sha(b)==digest,'size/hash mismatch')
def safe(n):
 p=PurePosixPath(n);need(bool(n) and not p.is_absolute() and '..' not in p.parts and str(p)==n and '\\' not in n,'unsafe path')
def unpack(raw,ext,count):
 pin(raw,ext['archive']['bytes'],ext['archive']['sha256']);rows=ext['files'];need(len(rows)==count and len({r['path'] for r in rows})==count,'manifest inventory');z=zipfile.ZipFile(io.BytesIO(raw));need(len(z.namelist())==len(set(z.namelist()))==count and set(z.namelist())=={r['path'] for r in rows},'archive exact inventory');need(z.testzip() is None,'CRC');d={}
 for i in z.infolist():
  safe(i.filename);need(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'regular members');d[i.filename]=z.read(i.filename)
 for r in rows:pin(d[r['path']],r['bytes'],r['sha256'])
 return d

def validate(files,manifest_pin=None):
 expected=set(PINS)|EXTRA;packs={}
 for n,(size,digest) in PINS.items():need(n in files,'missing frozen input');pin(files[n],size,digest)
 for tag,leaf,suffix,count in TAGS:
  pre='archives/'+STEM+tag+'_';ext=json.loads(files[pre+'EXTERNAL_MANIFEST.json']);need(ext['problem_id']==8500009 and ext['rank']==932,'external identity');pack=unpack(files[pre+suffix],ext,count);packs[tag]=pack
  for n,b in pack.items():expected.add(leaf+'/'+n);need(files.get(leaf+'/'+n)==b,'loose/archive equality '+n)
 need(set(files)==expected,'publication allowlist')
 for n,b in files.items():
  safe(n)
  if not n.endswith('.zip'):
   t=b.decode('utf-8');need(all(x not in t for x in ['/'+'workspace/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','private_'+'sources/','agent_'+'notes/']),'private marker')
 au,ad=packs['AUTHOR'],packs['INDEPENDENT_AUDIT'];need(ad['author_external_manifest.json']==files['archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json'],'nested author manifest')
 for n,b in au.items():need(ad['author/'+n]==b,'nested author exact')
 ac=json.loads(ad['ACCEPTANCE.json']);meta=json.loads(files['PUBLICATION_METADATA.json']);receipt=json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_RECEIPT.json']);need(ac['decision']==receipt['decision']==meta['decision']=='ACCEPT PARTIAL','decision');need(meta['status']=='unsolved' and meta['mathematical_status']=='partial','disposition');need(meta['problem_id']==8500009 and meta['rank']==932 and meta['problem_code']=='AMR-084-0009' and type(meta['turns_used']) is int and meta['turns_used']==3 and meta['turn_limit']==5,'identity/budget');need(meta['original_and_accepted_bytes_preserved'] is True,'preserve originals')
 for k in FALSE:need(meta[k] is False,'overclaim '+k)
 need(ac['full_resolution'] is False and ac['novelty_or_priority_claim'] is False and ac['correction_required'] is False and ac['author_files_changed'] is False and ac['approaches_used']==3,'acceptance scope')
 for key,name in [('accepted_author_archive','AUTHOR_SAFE_FREEZE.zip'),('accepted_author_external_manifest','AUTHOR_EXTERNAL_MANIFEST.json')]:need((ac[key]['bytes'],ac[key]['sha256'])==PINS['archives/'+STEM+name],'acceptance pins')
 need(ac['audit_report']['sha256']==sha(ad['AUDIT_REPORT.md']) and ac['audit_report']['bytes']==len(ad['AUDIT_REPORT.md']),'accepted report');need(receipt['archive']['sha256']==PINS['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'][1],'receipt archive')
 q=meta['queue'];need(q['changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 if manifest_pin is not None:
  need(re.fullmatch('[0-9a-f]{64}',manifest_pin) and sha(files['PUBLICATION_MANIFEST.json'])==manifest_pin,'external publication manifest pin');m=json.loads(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['problem_id']==8500009 and len(rows)==len(files)-1 and len({r['path'] for r in rows})==len(rows) and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'publication manifest inventory')
  for r in rows:pin(files[r['path']],r['bytes'],r['sha256'])
 return {'status':'PASS','public_files_checked':len(files),'author_members':7,'audit_members':17,'originals_and_nested_author_bytes_exact':True,'canonical_status':'unsolved','turns':'3/5','formal_proof_check':False}

def check_queue(base,new,meta):
 q=meta['queue'];need(len(base)==q['base_bytes'] and len(new)==q['new_bytes'] and sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'] and git(base)==q['base_git_blob_sha'] and git(new)==q['new_git_blob_sha'],'queue pins');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'line count');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 932 | 8500009 / AMR-084-0009 |'),'target row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y) and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9],'only Status/Turns');need(x[8:10]==[b' queued ',b' 0/5 '] and y[8:10]==[b' unsolved ',b' 3/5 '],'cells');return {'status':'PASS','changed_cells':['Status','Turns'],'findings_and_unrelated_bytes_preserved':True}

def negatives(files):
 labels=[]
 def reject(label,mutate,manifest=False):
  f=dict(files);mutate(f)
  try:validate(f,sha(files['PUBLICATION_MANIFEST.json']) if manifest else None)
  except Exception:labels.append(label);return
  raise RuntimeError('control accepted '+label)
 for n in PINS:reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 for n in ['original_author/REPORT.md','original_author/verify_exact.py','independent_audit/AUDIT_REPORT.md','independent_audit/ACCEPTANCE.json','independent_audit/replay_all.py','independent_audit/independent_exact.py']:
  reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
 reject('missing member',lambda f:f.pop('original_author/exact_certificate.json'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('traversal',lambda f:f.__setitem__('../x',b'x'))
 for k,v in [(k,True) for k in FALSE]+[('status','solved'),('turns_used',True),('turns_used',4),('original_and_accepted_bytes_preserved',False)]:
  def alter(f,k=k,v=v):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('invalid '+k,alter)
 reject('stale README manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),True);reject('corrupt publication manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),True)
 try:need(False,'intentional false guard')
 except RuntimeError:labels.append('explicit false guard')
 else:raise RuntimeError('guard disabled')
 return {'rejected_count':len(labels),'rejected':labels}

def replay(files):
 records=[]
 with tempfile.TemporaryDirectory(prefix='strong-rational-public-replay-') as td:
  w=Path(td);d=w/'audit';other=w/'unrelated';d.mkdir();other.mkdir();ext=json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json']);pack=unpack(files['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'],ext,17)
  for n,b in pack.items():p=d/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  env={'PATH':os.environ.get('PATH',''),'HOME':td,'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
  for flags in MODES:
   p=subprocess.run([sys.executable,*flags,str(d/'replay_all.py')],cwd=other,env=env,capture_output=True,timeout=180);need(p.returncode==0 and not p.stderr,'outer replay failed');r=json.loads(p.stdout);need(r['outcome']=='PASS' and r['problem_id']==8500009 and len(r['runs'])==12,'replay outputs');need({tuple(v['flags']) for v in r['runs']}=={tuple(v) for v in MODES},'all inner modes');need(all(v['returncode']==0 for v in r['runs']),'inner genuine')
   for v in r['runs']:
    if v['label']=='independent_exact':need(v['log'].encode()==pack['independent_exact_results.json'],'independent exact output')
    elif v['label']=='author_certificate':need(v['log'].encode()==pack['author/exact_certificate.json'],'author certificate')
    elif v['label']=='author_tests':need('Ran 9 tests' in v['log'] and '\nOK\n' in v['log'],'genuine test count')
    else:raise RuntimeError('unknown genuine run')
   m=r['author_mutation_replay'];need(m['original_sha256']==sha(pack['author/verify_exact.py']) and m['certificate_sha256']==sha(pack['author/exact_certificate.json']),'mutant inputs');need(len(m['runs'])==4 and all(v['returncode']==0 and 'Ran 9 tests' in v['log'] for v in m['runs']),'mutation genuine controls');need(len(m['mutations'])==8 and len({v['name'] for v in m['mutations']})==8,'mutation count')
   for v in m['mutations']:need(v['killed'] is True and v['returncode']!=0 and ('FAIL:' in v['log'] or 'ERROR:' in v['log']) and 'SyntaxError' not in v['log'],'nonvacuous mutant')
   records.append({'flags':flags,'exit_code':0,'inner_genuine_runs':12,'extra_author_genuine_test_modes':4,'mathematical_mutants_killed':8,'nonvacuous_mutants':True,'independent_output_sha256':sha(pack['independent_exact_results.json']),'certificate_sha256':sha(pack['author/exact_certificate.json'])})
 return {'status':'PASS','relocated_fresh_archive_extraction':True,'unrelated_working_directory':True,'outer_runs':records,'source_or_corpus_inputs_validated':False,'abstract_proof_machine_checked':False}

def inputs(files,catalog,problems,research,sources):
 verification=json.loads(files['original_author/verification_metadata.json']);datasets={};rows=[]
 for p,pinrow in zip([catalog,problems,research],verification['whole_corpora']):
  b=p.read_bytes();pin(b,pinrow['bytes'],pinrow['sha256']);d=json.loads(b);need(len(d)==pinrow['records'],'record count');datasets[pinrow['dataset']]=d;rows.append(dict(pinrow,matches=True))
 cs=[x for x in datasets['catalog.json'] if str(x['id'])=='8500009'];ps=[x for x in datasets['problems.json'] if str(x['id'])=='8500009'];need(len(cs)==len(ps)==1,'unique exact ID');c,p=cs[0],ps[0];need(c['rank']==932 and c['problem_number']==p['problem_number']=='AMR-084-0009','identity');b=json.dumps([p,datasets['research_results.json'].get(p['problem_number'],{})],sort_keys=True).encode();cp=verification['canonical_pair'];pin(b,cp['bytes'],cp['sha256']);need(sha(b)==c['review_hash']==cp['catalog_review_hash'],'strict canonical pair');source_pins=json.loads(files['independent_audit/source_hash_replay.json']);need(len(source_pins)==9,'source object count');out={}
 for n,row in source_pins.items():safe(n);b=(sources/n).read_bytes();pin(b,row['bytes'],row['sha256']);out[n]={'bytes':len(b),'sha256':sha(b),'matches':True}
 return {'status':'PASS','whole_corpora':rows,'canonical_pair':{'bytes':len(json.dumps([p,datasets['research_results.json'].get(p['problem_number'],{})],sort_keys=True).encode()),'sha256':cp['sha256'],'matches':True},'source_objects':out,'source_objects_hashed':9,'whole_corpora_hashed':3,'new_source_retrieval_or_inspection':False,'raw_source_or_corpus_text_included':False}

def load_files(root):
 need(root.is_dir() and not root.is_symlink(),'regular root');paths=list(root.rglob('*'));need(all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths),'regular files');files={p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()};dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need({p.relative_to(root).as_posix() for p in paths if p.is_dir()}==dirs,'no unlisted empty directories');return files

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--manifest-sha256',required=True);p.add_argument('--replay',action='store_true');p.add_argument('--base-queue',type=Path);p.add_argument('--queue',type=Path);p.add_argument('--catalog',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research',type=Path);p.add_argument('--sources',type=Path);a=p.parse_args();f=load_files(a.directory);r=validate(f,a.manifest_sha256);r['wrapper_negative_controls']=negatives(f);need(bool(a.base_queue)==bool(a.queue),'both queues required');r['queue_check']=check_queue(a.base_queue.read_bytes(),a.queue.read_bytes(),json.loads(f['PUBLICATION_METADATA.json'])) if a.queue else {'status':'NOT_RUN'};r['mathematical_replay']=replay(f) if a.replay else {'status':'NOT_RUN'};opts=[a.catalog,a.problems,a.research,a.sources];need(all(opts) or not any(opts),'all external input options required');r['external_input_replay']=inputs(f,*opts) if all(opts) else {'status':'NOT_RUN','reason':'Original source/corpus inputs intentionally absent from safe packet'}
 if all(opts):need(r['external_input_replay']==json.loads(f['PUBLICATION_INPUT_REPLAY.json']),'source replay record match')
 print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
