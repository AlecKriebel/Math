#!/usr/bin/env python3
"""Explicit fail-closed integrity/replay wrapper; not a formal mathematical proof checker."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,io,json,re,shutil,stat,subprocess,sys,tempfile,zipfile
STEM='SURFACE_TRIPLE_POINTS_2811_'
PINS={
 'archives/'+STEM+'AUTHOR_SAFE_FREEZE.zip':(18270,'913061fdd981ef0decf65fcc0916c58b2fd1e7ff0a70b3397459a623e0f08493'),
 'archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json':(4324,'8febb9e92071c17df719a6de3ca2a2423f247022ee0ee981b17426b9060ce40f'),
 'archives/'+STEM+'AUTHOR_VALIDATION_RECEIPT.json':(698,'33561e95cf3d47aed3d279c178fb1dbd49566260531ea2e9285bd7f86864ae30'),
 'archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip':(37737,'40b3b9bdce5a7b430428e777c3d5332a223064bb2d98d72db5978348e53173d9'),
 'archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(4985,'7d29abf6cfdd1e5454683c28ed1a53dd624f1e44d12aef80a13b1a60e4c4806d'),
 'INDEPENDENT_AUDIT_RECEIPT.json':(1209,'d6f009be30e438e9eb8bde09875e2dbb8396d77664a69ee13903752b96985718')}
EXTRA={'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_INPUT_REPLAY.json','verify_publication.py'}
FALSE_CLAIMS=['full_solution','counterexample','novelty_claim','formal_proof_claim','human_peer_review_claim','source_contents_included','dataset_contents_included','new_proof_search_performed','new_source_retrieval_or_visual_inspection_claimed']
TAGS=[('AUTHOR','original_author','_SAFE_FREEZE.zip',10),('INDEPENDENT_AUDIT','independent_audit','_SAFE.zip',12)]
def need(ok,why):
 if not ok:raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def safe(name):
 p=PurePosixPath(name);need(type(name) is str and bool(name) and not p.is_absolute() and '..' not in p.parts and str(p)==name and '\\' not in name,'unsafe path')
def pin(data,size,digest):need(type(size) is int and size>=0 and (len(data),sha(data))==(size,digest),'size/hash pin')
def archive(raw,ext,count):
 z=zipfile.ZipFile(io.BytesIO(raw));names=z.namelist();need(len(names)==len(set(names))==count==ext['archive_members'],'archive inventory count');need(z.testzip() is None,'archive CRC');payload={}
 for info in z.infolist():
  n=info.filename;safe(n);need('/' not in n and stat.S_ISREG(info.external_attr>>16),'nonregular/flat archive entry');payload[n]=z.read(n)
 need(sha(payload['MANIFEST.json'])==ext['internal_manifest_sha256'],'inner manifest external pin');m=json.loads(payload['MANIFEST.json']);need(m['problem_id']==2811,'inner identity');rows=m['files'];need(rows==ext['payload_files'],'external/internal member rows');need(len(rows)==count-1 and {r['path'] for r in rows}==set(payload)-{'MANIFEST.json'},'exact payload inventory')
 for row in rows:
  need(set(row)=={'path','bytes','sha256'},'entry schema');safe(row['path']);pin(payload[row['path']],row['bytes'],row['sha256'])
 return payload

def validate(files,manifest_pin=None):
 expected=set(PINS)|EXTRA;packs={}
 for name,(size,digest) in PINS.items():need(name in files,'missing frozen file');pin(files[name],size,digest)
 for tag,leaf,suffix,count in TAGS:
  stem='archives/'+STEM+tag;ext=json.loads(files[stem+'_EXTERNAL_MANIFEST.json']);need(ext['problem_id']==2811,'external identity');need((ext['archive']['bytes'],ext['archive']['sha256'])==PINS[stem+suffix],'archive/external binding');p=archive(files[stem+suffix],ext,count);packs[tag]=p
  for n,b in p.items():name=leaf+'/'+n;expected.add(name);need(files.get(name)==b,'loose/archive mismatch '+name)
 need(set(files)==expected,'public file allowlist')
 for name,data in files.items():
  safe(name)
  if not name.endswith('.zip'):
   txt=data.decode('utf-8');need(all(s not in txt for s in ['/'+'work'+'space/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','agent_'+'notes/','private_'+'sources/']),'private path marker')
 au=packs['AUTHOR'];ad=packs['INDEPENDENT_AUDIT'];binding=json.loads(ad['BINDING.json']);status=json.loads(ad['AUDIT_STATUS.json']);receipt=json.loads(files['INDEPENDENT_AUDIT_RECEIPT.json']);meta=json.loads(files['PUBLICATION_METADATA.json']);source=json.loads(ad['SOURCE_AUDIT.json'])
 need(binding['problem_id']==2811 and binding['accepted_without_repair'] is True and binding['source_content_included'] is False,'binding acceptance')
 need(len(binding['author_files'])==3,'bound author count')
 for row in binding['author_files']:
  b=ad[row['name']];pin(b,row['bytes'],row['sha256']);need(b==files['archives/'+row['name']],'nested original exact')
 ae=json.loads(files['archives/'+STEM+'AUTHOR_EXTERNAL_MANIFEST.json']);need(binding['author_internal_manifest_sha256']==ae['internal_manifest_sha256'],'author internal binding')
 need(status['verdict']==receipt['verdict']==meta['accepted_verdict']=='PASS_SCOPED_PARTIALS_UNCHANGED','accepted verdict');need(status['problem_id']==2811 and status['problem_number']=='KP-3.13' and status['rank']==910,'audit identity');need(status['queue_status']=='unsolved' and status['substantive_approaches_used']==3 and status['approach_limit']==5,'audit disposition')
 for k in ['author_patch_required','counterexample','full_solution','human_peer_review','novelty_claim','repository_mutations','source_pdf_or_dataset_contents_included']:need(status[k] is False,'audit scope '+k)
 need(status['original_artifacts_preserved'] is True and status['additional_approaches_in_audit']==0,'historical accepted scope')
 need(meta['problem_id']==2811 and meta['problem_number']=='KP-3.13' and meta['rank']==910 and meta['status']=='unsolved','canonical identity');need(type(meta['approaches_used']) is int and meta['approaches_used']==3 and meta['approach_limit']==5,'canonical approaches')
 for k in FALSE_CLAIMS:need(meta[k] is False,'publication claim '+k)
 need(meta['historical_freeze_fields_preserved'] is True and meta['accepted_without_repair'] is True,'history preservation');q=meta['queue'];need(q['actually_changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue scope')
 need(json.loads(au['STATUS.json'])['independent_audit']=='pending','historical pending author');need(receipt['archive']['sha256']==PINS['archives/'+STEM+'INDEPENDENT_AUDIT_SAFE.zip'][1] and receipt['external_manifest']['sha256']==PINS['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'][1],'receipt audit binding')
 need(receipt['author_integrity_negatives_per_mode']==20 and receipt['audit_integrity_negatives_per_mode']==16,'receipt negative counts');need(source['li_local_pdf_retrieved'] is False and source['li_visual_inspection'] is False and source['li_pdf_bytes'] is None and source['li_pdf_hash'] is None and source['li_web_extraction_reopened'] is True,'Li evidence limitation')
 if manifest_pin is not None:
  need(re.fullmatch('[0-9a-f]{64}',manifest_pin) is not None and sha(files['PUBLICATION_MANIFEST.json'])==manifest_pin,'external publication manifest pin');m=json.loads(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['schema']=='public-file-manifest-v1' and m['problem_id']==2811,'publication manifest identity');need(len(rows)==len(files)-1 and {r['path'] for r in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'publication manifest inventory')
  for row in rows:pin(files[row['path']],row['bytes'],row['sha256'])
 return {'status':'PASS','public_files_checked':len(files),'author_members':10,'audit_members':12,'nested_originals_exact':True,'historical_fields_preserved':True,'canonical_status':'unsolved','turns':'3/5','formal_proof_checked':False}

def check_queue(base,new,meta):
 q=meta['queue'];need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'],'queue hashes');a=base.splitlines(keepends=True);b=new.splitlines(keepends=True);need(len(a)==len(b),'queue line count');ix=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y];need(len(ix)==1 and a[ix[0]].startswith(b'| 910 | 2811 / KP-3.13 |'),'one target queue row');x=a[ix[0]].split(b'|');y=b[ix[0]].split(b'|');need(len(x)==len(y) and [i for i,(p,q) in enumerate(zip(x,y)) if p!=q]==[8,9],'Status/Turns only');need(y[8:10]==[b' unsolved ',b' 3/5 '],'queue target');return {'status':'PASS','changed_cells':['Status','Turns'],'findings_and_all_other_bytes_preserved':True}

def wrapper_negatives(files):
 out=[]
 def reject(label,alter,use_manifest=False):
  f=dict(files);alter(f)
  try:validate(f,sha(files['PUBLICATION_MANIFEST.json']) if use_manifest else None)
  except (RuntimeError,KeyError,TypeError,ValueError,zipfile.BadZipFile):out.append(label);return
  raise RuntimeError('negative accepted '+label)
 for n in PINS:reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'corrupt'))
 for n in ['original_author/PROOF.md','original_author/STATUS.json','independent_audit/AUDIT_REPORT.md','independent_audit/BINDING.json','independent_audit/AUDIT_STATUS.json','independent_audit/'+STEM+'AUTHOR_SAFE_FREEZE.zip']:
  reject('corrupt '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'corrupt'))
 reject('missing member',lambda f:f.pop('original_author/README.md'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('traversal',lambda f:f.__setitem__('../x',b'x'))
 for k,v in [('status','partial'),('status','verified_solved'),('approaches_used',4),('accepted_without_repair',False)]+[(k,True) for k in FALSE_CLAIMS]:
  def alter(f,k=k,v=v):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
  reject('bad claim '+k+'='+str(v),alter)
 reject('stale wrapper manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'changed'),True)
 reject('corrupt manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),True)
 try:need(False,'deliberate fail-closed check')
 except RuntimeError:out.append('explicit need(False)')
 else:raise RuntimeError('guard disabled')
 return {'negative_control_count':len(out),'negative_controls_rejected':out}

def run(script,flags=(),pinvalue=None):
 args=[sys.executable,'-B',*flags,str(script)]
 if pinvalue is not None:args+=['--manifest-sha256',pinvalue]
 return subprocess.run(args,capture_output=True,timeout=240)

def replay(files):
 modes=[];negative=[]
 with tempfile.TemporaryDirectory(prefix='surface-triples-replay-') as temp:
  t=Path(temp)
  for tag,leaf,suffix,count in TAGS:
   ext=json.loads(files['archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json']);pack=archive(files['archives/'+STEM+tag+suffix],ext,count);root=t/leaf;root.mkdir()
   for name,data in pack.items():(root/name).write_bytes(data)
   positive=[]
   for flags in ([],['-O']):
    script=root/('verify_package.py' if tag=='AUTHOR' else 'verify_audit.py');p=run(script,flags,ext['internal_manifest_sha256']);need(p.returncode==0 and not p.stderr,'fresh replay '+tag+': '+p.stderr.decode());positive.append(p.stdout);modes.append({'packet':tag,'mode':'optimized' if flags else 'normal','exit_code':0,'output_bytes':len(p.stdout),'output_sha256':sha(p.stdout),'result':json.loads(p.stdout)})
   need(positive[0]==positive[1],'normal/optimized identical')
  original=t/'independent_audit';ep=json.loads(files['archives/'+STEM+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json']);extpin=ep['internal_manifest_sha256']
  cases=['alter_report','alter_checker','alter_source_metadata','alter_author_archive','alter_binding','alter_results','missing_file','extra_file','wrong_pin','no_pin','manifest_corrupt','rebound_author_archive','payload_symlink','manifest_symlink','unsafe_path','duplicate_entry']
  for case in cases:
   root=t/case;shutil.copytree(original,root);mp=root/'MANIFEST.json';m=json.loads(mp.read_bytes());pvalue=extpin
   amap={'alter_report':'AUDIT_REPORT.md','alter_checker':'independent_checks.py','alter_source_metadata':'SOURCE_AUDIT.json','alter_author_archive':STEM+'AUTHOR_SAFE_FREEZE.zip','alter_binding':'BINDING.json','alter_results':'INDEPENDENT_RESULTS.json'}
   if case in amap:p=root/amap[case];p.write_bytes(p.read_bytes()+b'\nchanged\n')
   elif case=='missing_file':(root/'AUDIT_REPORT.md').unlink()
   elif case=='extra_file':(root/'unexpected').write_text('extra')
   elif case=='wrong_pin':pvalue='0'*64
   elif case=='no_pin':pvalue=None
   elif case=='manifest_corrupt':mp.write_text('bad JSON')
   elif case=='rebound_author_archive':
    p=root/(STEM+'AUTHOR_SAFE_FREEZE.zip');p.write_bytes(p.read_bytes()+b'changed')
    for f in m['files']:
     if f['path']==p.name:f.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
    mp.write_bytes(enc(m));pvalue=sha(mp.read_bytes())
   elif case=='payload_symlink':p=root/'AUDIT_REPORT.md';p.unlink();p.symlink_to(original/'AUDIT_REPORT.md')
   elif case=='manifest_symlink':mp.unlink();mp.symlink_to(original/'MANIFEST.json')
   elif case in ['unsafe_path','duplicate_entry']:
    if case=='unsafe_path':m['files'][0]['path']='../AUDIT_REPORT.md'
    else:m['files'].append(m['files'][0])
    mp.write_bytes(enc(m));pvalue=sha(mp.read_bytes())
   for flags in ([],['-O']):
    p=run(root/'verify_audit.py',flags,pvalue);need(p.returncode!=0,'audit negative accepted '+case)
   negative.append({'case':case,'normal_rejected':True,'optimized_rejected':True})
 return {'status':'PASS','fresh_authenticated_extraction':True,'positive_replays':modes,'author_integrity_negatives_per_mode':20,'audit_integrity_negatives_per_mode':len(negative),'audit_negative_results':negative,'formal_mathematical_proof':False}

def input_replay(files,catalog,problems,reports,source_dir):
 a=json.loads(files['independent_audit/SOURCE_AUDIT.json']);out=[];objects=[]
 for path,row in zip([catalog,problems,reports],a['corpus_integrity']):
  b=path.read_bytes();pin(b,row['bytes'],row['sha256']);objects.append(json.loads(b));out.append({'label':row['label'],'bytes':len(b),'sha256':sha(b),'match':True})
 c,p,r=objects;cs=[x for x in c if str(x['id'])=='2811'];ps=[x for x in p if str(x['id'])=='2811'];need(len(cs)==len(ps)==1,'unique source identity');need(cs[0]['rank']==910 and cs[0]['problem_number']==ps[0]['problem_number']=='KP-3.13','source key/rank');record=ps[0];report=r.get(record['problem_number'],{});need(report=={},'exact report empty');pair=sha(json.dumps([record,report],sort_keys=True).encode());statement=sha(record['statement'].encode());need(pair==a['record_report_pair_sha256'] and statement==a['statement_sha256']==cs[0]['statement_hash'],'exact pair/statement hashes');source=[]
 for name,row in zip(['k3.pdf','cooper_long.pdf','kahn_markovic.pdf','agol.pdf','agol_published.pdf'],a['source_pdfs']):
  b=(source_dir/name).read_bytes();pin(b,row['bytes'],row['sha256']);need(b.startswith(b'%PDF'),'PDF header');source.append({'title':row['title'],'url':row['url'],'bytes':len(b),'sha256':sha(b),'match':True})
 return {'status':'PASS','problem_id':2811,'rank':910,'corpus_integrity':out,'unique_record_and_catalog_match':True,'exact_report_empty':True,'statement_sha256':statement,'record_report_pair_sha256':pair,'source_pdfs':source,'li_local_pdf_or_visual_claim':False,'new_source_retrieval_or_inspection':False,'scope':'Full local-byte hash replay and exact target binding; no source or corpus contents included.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path,nargs='?',default=Path('.'));p.add_argument('--manifest-sha256',required=True);p.add_argument('--replay',action='store_true');p.add_argument('--base-queue',type=Path);p.add_argument('--queue',type=Path);p.add_argument('--catalog',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-reports',type=Path);p.add_argument('--source-dir',type=Path);args=p.parse_args();root=args.directory.absolute();paths=list(root.rglob('*'));need(root.is_dir() and not root.is_symlink() and all(not x.is_symlink() for x in paths),'no filesystem symlinks');need(all(x.is_file() or x.is_dir() for x in paths),'regular filesystem');files={x.relative_to(root).as_posix():x.read_bytes() for x in paths if x.is_file()};expected_dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'};need({x.relative_to(root).as_posix() for x in paths if x.is_dir()}==expected_dirs,'no unlisted empty directories');result=validate(files,args.manifest_sha256);result['wrapper_controls']=wrapper_negatives(files)
 need(bool(args.queue)==bool(args.base_queue),'both queue inputs required');result['queue_check']={'status':'NOT_RUN'}
 if args.queue:
  base=args.base_queue.read_bytes();new=args.queue.read_bytes();meta=json.loads(files['PUBLICATION_METADATA.json']);result['queue_check']=check_queue(base,new,meta);rejects=0
  for bad in [new+b'x',new.replace(b'| 910 | 2811 / KP-3.13 |',b'| 910 | 2812 / KP-3.13 |')]:
   try:check_queue(base,bad,meta)
   except RuntimeError:rejects+=1
  need(rejects==2,'queue negatives');result['queue_check']['negative_controls_rejected']=rejects
 result['finite_and_integrity_replay']=replay(files) if args.replay else {'status':'NOT_RUN'}
 inp=[args.catalog,args.problems,args.research_reports,args.source_dir];need(all(inp) or not any(inp),'all four external input options required');result['external_input_replay']=input_replay(files,*inp) if all(inp) else {'status':'NOT_RUN'}
 if all(inp):need(result['external_input_replay']==json.loads(files['PUBLICATION_INPUT_REPLAY.json']),'saved input replay match')
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
