#!/usr/bin/env python3
"""Replay original frozen author packet plus independently designed adversarial checks.
Optional --catalog/--problems/--reports and --source-dir are read-only external inputs.
No source or corpus contents are emitted. No network access is used.
"""
import argparse,copy,hashlib,io,json,os,pathlib,shutil,subprocess,sys,tempfile,zipfile,warnings
P='REGULAR_PENTAGON_5500072_AUTHOR_'
PINS={
 P+'SAFE_FREEZE.zip':(14851,'da58c09682631f3455d7ef0047ff20b137f2c8b14640752f9886bb4dfc4bfb62'),
 P+'EXTERNAL_MANIFEST.json':(1680,'88771594f5b6c2aabe33513345ca2b70786984448cfa17d5ed7bbc5ffe122f95'),
 P+'BOOTSTRAP.py':(3419,'590cf2095337c31144dc04bff20baf9fede8a6d8ea96fdf4fc92aea3205c9841')}
CORPORA={
 'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566',15458),
 'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf',15458),
 'reports':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b',6701)}
def fp(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def require(x,msg):
 if not x:raise ValueError(msg)
def packed(rows):
 b=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED) as z:
   for n,r in rows:z.writestr(n,r)
 return b.getvalue()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author-dir',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
 for n in CORPORA:ap.add_argument('--'+n,type=pathlib.Path)
 ap.add_argument('--source-dir',type=pathlib.Path);args=ap.parse_args();tests=[]
 def ok(label,x):require(x,label);tests.append({'test':label,'passed':True})
 blobs={n:(args.author_dir/n).read_bytes() for n in PINS}
 for n,(size,digest) in PINS.items():ok('trusted_pin:'+n,fp(blobs[n])=={'bytes':size,'sha256':digest})
 manifest=json.loads(blobs[P+'EXTERNAL_MANIFEST.json'])
 with zipfile.ZipFile(io.BytesIO(blobs[P+'SAFE_FREEZE.zip'])) as z:
  names=z.namelist();ok('eight_unique_safe_members',len(names)==8 and len(set(names))==8 and set(names)==set(manifest['files']) and all(pathlib.PurePosixPath(n).name==n for n in names))
  ok('zip_crc',z.testzip() is None);members={n:z.read(n) for n in names}
  for n,r in members.items():ok('member_pin:'+n,fp(r)==manifest['files'][n])
 corpus_report={'verified':False};supplied=[getattr(args,n) is not None for n in CORPORA]
 require(not any(supplied) or all(supplied),'supply all three corpora')
 forwarded=[]
 if all(supplied):
  data={};cr={}
  for n,(size,digest,count) in CORPORA.items():
   p=getattr(args,n).resolve();raw=p.read_bytes();ok('independent_full_corpus:'+n,fp(raw)=={'bytes':size,'sha256':digest});data[n]=json.loads(raw);ok('corpus_records:'+n,len(data[n])==count);cr[n]={**fp(raw),'records':count};forwarded+=['--'+n,str(p)]
  r=[x for x in data['problems'] if str(x.get('id'))=='5500072'];c=[x for x in data['catalog'] if str(x.get('id'))=='5500072'];ok('unique_identity',len(r)==len(c)==1)
  r,c=r[0],c[0];rr=data['reports'].get(r['problem_number'],{});pair=json.dumps([r,rr],sort_keys=True).encode();ph=hashlib.sha256(pair).hexdigest()
  ok('whole_pair_not_projection',len(pair)==3943 and ph==c['review_hash']=='8b339393cebf5ccaee4df9fcd5290875ff54c34aa811cee58f9041e9d54df4c5')
  ok('rank_number_title',c['rank']==929 and r['problem_number']==c['problem_number']=='AMR-054-0072' and r['title']==c['title']=='Polyhedron with Regular Pentagon Faces')
  sh=hashlib.sha256(r['statement'].encode()).hexdigest();ok('statement_hash',sh==c['statement_hash']=='ec51f78f7a8e69659f97579b1a600cd42a60fbb069718357dbc2bf46f808f045')
  rh=hashlib.sha256(json.dumps(rr,sort_keys=True).encode()).hexdigest();ok('inherited_whole_report_hash',rh=='d9242514a6fd82934ead5264a76d719aa2d12cb852076f7b922022d671bab893')
  altered=copy.deepcopy(r);altered['view_count']=int(altered['view_count'])+1
  ok('nonstatement_field_mutation_detected',hashlib.sha256(json.dumps([altered,rr],sort_keys=True).encode()).hexdigest()!=ph)
  corpus_report={'verified':True,'corpora':cr,'pair_bytes':len(pair),'pair_sha256':ph,'statement_sha256':sh,'report_sha256':rh,'prior_work_gate':'Independent AI inspection of inherited report: literature triage only; no proof attempt.'}
 if args.source_dir is not None:forwarded+=['--source-dir',str(args.source_dir.resolve())]
 outputs=[];bootstrap_outputs=[]
 with tempfile.TemporaryDirectory(prefix='pentagon independent unrelated ') as root:
  root=pathlib.Path(root);unrelated=root/'unrelated working directory';unrelated.mkdir()
  for optimized in [False,True]:
   mode='optimized' if optimized else 'normal';flags=['-I']+(['-O'] if optimized else []);run_dir=root/mode;run_dir.mkdir()
   for n,b in blobs.items():(run_dir/n).write_bytes(b)
   extracted=run_dir/'extracted';extracted.mkdir()
   for n,b in members.items():(extracted/n).write_bytes(b)
   def run(script,extra=()):return subprocess.run([sys.executable]+flags+[str(script)]+list(extra),cwd=unrelated,capture_output=True,text=True,timeout=120)
   x=run(extracted/'diagnostics.py');ok('isolated_no_input_'+mode,x.returncode==0);j=json.loads(x.stdout);ok('honest_missing_input_'+mode,j['input_provenance']['verified'] is False and j['source_bytes']['verified'] is False)
   x=run(extracted/'diagnostics.py',forwarded);ok('isolated_full_replay_'+mode,x.returncode==0);outputs.append(json.loads(x.stdout))
   if all(supplied) and args.source_dir:ok('recorded_result_reproduced_'+mode,outputs[-1]==json.loads(members['validation_results.json']))
   x=run(run_dir/(P+'BOOTSTRAP.py'),forwarded);ok('relocated_bootstrap_'+mode,x.returncode==0);bootstrap_outputs.append(json.loads(x.stdout))
   # Status and exact algebra mutations are checked directly, without envelope hashes.
   for key,value in [('full_resolution',True),('novelty_claim',True),('problem_id',5500073),('approaches_used',5),('approach_limit',6),('outcome','solved')]:
    s=json.loads(members['status.json']);s[key]=value;(extracted/'status.json').write_text(json.dumps(s));x=run(extracted/'diagnostics.py');ok('reject_status_'+key+'_'+mode,x.returncode!=0)
   (extracted/'status.json').write_bytes(members['status.json'])
   script=members['diagnostics.py'].replace(b'q = Q5(F(-1, 4), F(1, 4))',b'q = Q5(F(-1, 4), F(1, 3))');require(script!=members['diagnostics.py'],'mutation target')
   (extracted/'diagnostics.py').write_bytes(script);ok('reject_constant_'+mode,run(extracted/'diagnostics.py').returncode!=0);(extracted/'diagnostics.py').write_bytes(members['diagnostics.py'])
   if all(supplied):
    bad=root/('bad corpus '+mode+'.json');bad.write_bytes(b'[]');ok('reject_corpus_bytes_'+mode,run(extracted/'diagnostics.py',['--catalog',str(bad),'--problems',str(args.problems.resolve()),'--reports',str(args.reports.resolve())]).returncode!=0)
    ok('reject_partial_corpora_'+mode,run(extracted/'diagnostics.py',['--catalog',str(args.catalog.resolve())]).returncode!=0)
   if args.source_dir:
    bad=root/('bad source '+mode);bad.mkdir()
    rows=json.loads(members['verification_metadata.json'])['retrieved_sources']
    for row in rows:shutil.copyfile(args.source_dir/row['file'],bad/row['file'])
    p=bad/'rote2009.pdf';p.write_bytes(p.read_bytes()+b'X');ok('reject_source_bytes_'+mode,run(extracted/'diagnostics.py',['--source-dir',str(bad)]).returncode!=0)
   archive=run_dir/(P+'SAFE_FREEZE.zip');mf=run_dir/(P+'EXTERNAL_MANIFEST.json');boot=run_dir/(P+'BOOTSTRAP.py')
   archive.write_bytes(blobs[P+'SAFE_FREEZE.zip']+b'X');ok('reject_archive_append_'+mode,run(boot).returncode!=0);archive.write_bytes(blobs[P+'SAFE_FREEZE.zip'])
   boot.write_bytes(blobs[P+'BOOTSTRAP.py']+b'\n# changed\n');ok('reject_bootstrap_bytes_'+mode,run(boot).returncode!=0);boot.write_bytes(blobs[P+'BOOTSTRAP.py'])
   # Update only outer ZIP hash, so deeper checks are actually reached.
   for name,rows in [('member_tamper',[(n,b+b'X' if n=='proof_note.md' else b) for n,b in members.items()]),('missing_member',[(n,b) for n,b in members.items() if n!='proof_note.md']),('extra_member',list(members.items())+[('unexpected.txt',b'x')]),('duplicate_member',list(members.items())+[('README.md',members['README.md'])])]:
    raw=packed(rows);m=copy.deepcopy(manifest);m['archive']=fp(raw);archive.write_bytes(raw);mf.write_text(json.dumps(m));ok('reject_'+name+'_'+mode,run(boot).returncode!=0)
   for badname in ['../escape.txt','/absolute.txt']:
    rows=[(badname if n=='README.md' else n,b) for n,b in members.items()];raw=packed(rows);m=copy.deepcopy(manifest);m['files'][badname]=m['files'].pop('README.md');m['archive']=fp(raw);archive.write_bytes(raw);mf.write_text(json.dumps(m));ok('reject_unsafe_path_'+('relative' if badname.startswith('..') else 'absolute')+'_'+mode,run(boot).returncode!=0)
   # Coordinated rewrite is rejected by the audit's immutable external reference.
   changed=dict(members);changed['proof_note.md']+=b'\nchanged\n';raw=packed(changed.items());m=copy.deepcopy(manifest);m['archive']=fp(raw);m['files']['proof_note.md']=fp(changed['proof_note.md']);mraw=json.dumps(m).encode()
   ok('coordinated_rewrite_fails_trusted_pins_'+mode,fp(raw)['sha256']!=PINS[P+'SAFE_FREEZE.zip'][1] and fp(mraw)['sha256']!=PINS[P+'EXTERNAL_MANIFEST.json'][1])
   for n,b in blobs.items():(run_dir/n).write_bytes(b)
  ok('author_normal_optimized_equal',outputs[0]==outputs[1]);ok('bootstrap_normal_optimized_equal',bootstrap_outputs[0]==bootstrap_outputs[1])
  # Execute independently authored exact arithmetic from another directory.
  exact=pathlib.Path(__file__).with_name('independent_exact_checks.py');raw=exact.read_bytes();dest=root/'independent relocated.py';dest.write_bytes(raw);res=[]
  for flags,label in [(['-I'],'normal'),(['-I','-O'],'optimized')]:
   x=subprocess.run([sys.executable]+flags+[str(dest)],cwd=unrelated,capture_output=True,text=True,timeout=120);ok('independent_relocated_'+label,x.returncode==0);res.append(json.loads(x.stdout))
  ok('independent_normal_optimized_equal',res[0]==res[1])
  expected=json.loads(exact.with_name('independent_exact_results.json').read_text());ok('independent_recorded_result_equal',res[0]==expected)
  bad=raw.replace(b'F(1,8),F(1,8)',b'F(1,7),F(1,8)');require(bad!=raw,'independent mutation target');dest.write_bytes(bad)
  for flags,label in [(['-I'],'normal'),(['-I','-O'],'optimized')]:
   x=subprocess.run([sys.executable]+flags+[str(dest)],cwd=unrelated,capture_output=True,text=True,timeout=120);ok('independent_wrong_determinant_rejected_'+label,x.returncode!=0)
 out={'problem_id':5500072,'accepted_original_unchanged':True,'outcome':'stalled_partial','approaches_used':3,'full_resolution':False,'tests_passed':len(tests),'tests':tests,'independent_corpus_verification':corpus_report,'author_diagnostic_result_sha256':hashlib.sha256((json.dumps(outputs[0],indent=2,sort_keys=True)+'\n').encode()).hexdigest(),'source_bytes_verified':bool(args.source_dir),'scope':'Algebra and artifact tests supplement independent AI mathematical/source review; not human peer review, formal verification, or a global solver.'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
