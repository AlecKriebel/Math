#!/usr/bin/env python3
"""R2 independent detached integrity, metadata, and provenance checks.
All scratch and fabricated service state remain within this review family.
No original source body or provider excerpt is emitted.
"""
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent; A=R.parents[1]; S=R/'scratch';S.mkdir(exist_ok=True)
os.environ['TMPDIR']=str(S);os.environ['PYTHONDONTWRITEBYTECODE']='1'
import copy,datetime,hashlib,importlib.util,json,re,shutil,subprocess,types,zipfile
ENV=dict(os.environ);ENV.pop('PYTHONOPTIMIZE',None)
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 sp=importlib.util.spec_from_file_location('r2_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def run(p,flags=(),args=()):
 x=subprocess.run([sys.executable,'-B',*flags,str(p),*args],cwd=S,env=ENV,text=True,capture_output=True,timeout=240)
 return {'flags':list(flags),'returncode':x.returncode,'stdout':x.stdout,'stderr':x.stderr}
def archive():
 d=S/'extracted';d.mkdir(exist_ok=True)
 zpath=A/'publication/Prime_Difference_Counterexample_Verification_v1.0.zip'
 with zipfile.ZipFile(zpath) as z:
  names=z.namelist();need(len(names)==len(set(names))==178,'178 unique archive members')
  for i in z.infolist():
   need(not Path(i.filename).is_absolute() and '..' not in Path(i.filename).parts and '\\' not in i.filename,'unsafe archive member')
   need((i.external_attr>>16)&0o170000!=0o120000,'archive symlink')
  z.extractall(d)
 need(all((d/n).read_bytes()==(A/'publication/verification'/n).read_bytes() for n in names),'actual ZIP/local tree differs')
 b=json.loads((A/'publication/BUILD_RECEIPT.json').read_text()); anchors=b['verification_anchors'];args=[s for k,v in anchors.items() for s in ['--expected-'+k+'-sha256',v]]
 baseline=[run(d/'verify.py',f,args) for f in [[],['-O'],['-OO']]];need(all(x['returncode']==0 for x in baseline),'archive baseline rejected')
 negative=[]
 def test(label,mutate,restore,arguments=args):
  mutate()
  try:
   for f in [[],['-O'],['-OO']]:
    x=run(d/'verify.py',f,arguments);need(x['returncode']!=0,'accepted corruption '+label)
    negative.append({'case':label,'flags':f,'returncode':x['returncode'],'error':x['stderr'].splitlines()[-1]})
  finally:restore()
 p=d/'current_edition/PROOF.md';old=p.read_bytes()
 test('altered_current_proof',lambda:p.write_bytes(old+b'\nR2 TAMPER'),lambda:p.write_bytes(old))
 test('missing_current_proof',p.unlink,lambda:p.write_bytes(old))
 q=d/'extra.txt';test('unlisted_extra',lambda:q.write_text('EXTRA'),q.unlink)
 man=d/'MANIFEST.json';oldman=man.read_bytes();test('changed_root_manifest',lambda:man.write_bytes(oldman+b'\n'),lambda:man.write_bytes(oldman))
 for k in anchors:
  bad=[s for key,val in anchors.items() for s in ['--expected-'+key+'-sha256','0'*64 if key==k else val]]
  test('false_outside_'+k,lambda:None,lambda:None,bad)
 payload=d/'reviews/source_question_family/SOURCE_ONLY_RECONSTRUCTION.md';oldpayload=payload.read_bytes();payload.write_bytes(oldpayload+b'\nR2 TAMPER')
 outer=json.loads(oldman)
 for e in outer['files']:
  if e['path']==payload.relative_to(d).as_posix():e.update(bytes=payload.stat().st_size,sha256=sha(payload))
 save(man,outer);bad=[s for k,v in anchors.items() for s in ['--expected-'+k+'-sha256',sha(man) if k=='manifest' else v]]
 test('outer_resigned_nested_payload',lambda:None,lambda:(payload.write_bytes(oldpayload),man.write_bytes(oldman)),bad)
 # A real symlink to an identical source cannot be passed as a regular member.
 test('same_bytes_symlink',lambda:(p.unlink(),p.symlink_to(A/'submitted/PROOF.md')),lambda:(p.unlink(),p.write_bytes(old)))
 return {'zip_sha256':sha(zpath),'bytes':zpath.stat().st_size,'members':178,'all_members_match_tree':True,'outside_anchors':anchors,'baseline':baseline,'negative_controls':negative}
def provenance():
 s=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());checks=[]
 for e in s['files']:
  b=(A/e['local']).read_bytes()
  x=subprocess.run(['git','-c','gc.auto=0','show',s['head']+':'+e['path']],cwd=A.parents[2],env=dict(ENV,GIT_OPTIONAL_LOCKS='0'),capture_output=True,timeout=60)
  need(x.returncode==0 and x.stdout==b,'actual original Git blob differs '+e['path'])
  need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'original blob OID differs')
  n=Path(e['path']).name;need((A/'current_edition'/n).read_bytes()==b,'current original copy differs')
  checks.append({'name':n,'git_blob':e['blob'],'sha256':hashlib.sha256(b).hexdigest(),'actual_git_bytes_equal':True,'current_equal':True})
 # Explicit current membership registry, not source receipt guessing.
 v=load(S/'extracted/verify.py');c=json.loads((A/'CURRENT_PR1268_CONTEXT.json').read_text());nested=v.authenticate_nested_manifests(A,c['authored_freezes']);need(len(nested)==12,'expected12 explicit frozen families')
 a=json.loads((A/'priority/primary_lineage/QUERY_LEDGER.json').read_text());b=json.loads((A/'priority/graph_literature_public/QUERY_LEDGER.json').read_text());raw=json.loads((A/'priority/graph_literature/QUERY_LEDGER.json').read_text());r=json.loads((A/'priority/root_extension/QUERY_LEDGER.json').read_text())
 q=[x['literal_query'] for x in a['queries']]+[x['literal_query'] for x in b['queries']]+[x['query'] for x in r['entries']]
 need(len(q)==111 and len(set(q))==107,'query counts differ')
 def strip_titles(x):
  if isinstance(x,dict):return {k:strip_titles(y) for k,y in x.items() if k!='title'}
  if isinstance(x,list):return [strip_titles(y) for y in x]
  return x
 need(strip_titles(raw['queries'])==b['queries'],'public query records are not exact non-title projection')
 entries=[y for x in b['queries'] for y in x['returned_entries']];rawentries=[y for x in raw['queries'] for y in x['returned_entries']]
 need(len(entries)==893 and sum('title'in x for x in rawentries)==893 and all('title'not in x for x in entries),'893 omitted titles')
 # Count serialized/visible search surface without reproducing raw body.
 from html.parser import HTMLParser
 class Visible(HTMLParser):
  def __init__(self):super().__init__();self.hidden=0;self.data=[]
  def handle_starttag(self,t,attrs):
   if t in {'script','style'}:self.hidden+=1
  def handle_endtag(self,t):
   if t in {'script','style'}:self.hidden=max(0,self.hidden-1)
  def handle_data(self,d):
   if not self.hidden:self.data.append(d)
 html=(A/'priority/graph_literature/ignored_local/capuano2026.html').read_text();parser=Visible();parser.feed(html)
 counts={'raw_substring':len(re.findall('clique',html,re.I)),'visible_substring':len(re.findall('clique',' '.join(parser.data),re.I)),'raw_singular_whole_word':len(re.findall(r'\bclique\b',html,re.I))};need(counts=={'raw_substring':4,'visible_substring':1,'raw_singular_whole_word':0},'surface correction differs')
 return {'actual_original_git_checks':checks,'nested_registry':nested,'query_entries':111,'distinct_literal_queries':107,'A_B_root_counts':[36,59,16],'public_B_non_title_records_exact':True,'omitted_title_fields':893,'retained_URL_rows':893,'surface_counts':counts,'limits':'No raw source or search-provider body is redistributed. Count consistency does not attest historical searches or priority absence.'}
def metadata():
 d=S/'actual_metadata';d.mkdir(exist_ok=True)
 for n in ['zenodo-deposit.json','Prime_Difference_Counterexample_Note_v1.0.pdf','Prime_Difference_Counterexample_Verification_v1.0.zip','append_tracker.py','check_public_downloads.py','verification/verify.py']:
  out=d/n;out.parent.mkdir(exist_ok=True);shutil.copyfile(A/'publication'/n,out)
 cpath=A.parents[1]/'publication_coordinators/pr1268.py';cp=d/'coordinator.py';shutil.copyfile(cpath,cp);c=load(cp);c.P=d
 kit=c.load_exact_kit();kit.STATE_DIR=d/'kitstate';kit.doi_status=lambda doi:{'status':'resolved','http_status':200,'synthetic_fixture_only':True}
 meta,files=kit.load_manifest(d/'zenodo-deposit.json');need(meta==json.loads((A/'CURRENT_PR1268_CONTEXT.json').read_text())['metadata'],'actual metadata context')
 v=load(d/'verification/verify.py');v.metadata_contract(meta)
 pub=load(d/'check_public_downloads.py');actual=copy.deepcopy(meta);actual['resource_type']={'type':actual.pop('upload_type'),'subtype':actual.pop('publication_type')};actual['license']={'id':actual['license']};good=pub.verify_public_metadata(actual,meta);badfields=[]
 for k in meta:
  wrong=copy.deepcopy(actual)
  if k in {'upload_type','publication_type'}:wrong['resource_type']['type'if k=='upload_type'else'subtype']='CORRUPTED'
  elif k=='license':wrong['license']['id']='CORRUPTED'
  else:wrong[k]=None
  try:pub.verify_public_metadata(wrong,meta)
  except RuntimeError:badfields.append(k)
  else:raise RuntimeError('public field corruption accepted '+k)
 # Actual current metadata/files through genuine shared-kit run and strict wrapper.
 # Only external client methods, gate/preflight and state destinations are mocked.
 events=[];remote={'id':73123456,'submitted':False,'metadata':copy.deepcopy(meta),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':'md5:'+f['md5']} for f in files]};state={'manifest':str((d/'zenodo-deposit.json').resolve()),'environment':'production','id':remote['id']};kit.save_state(kit.state_path((d/'zenodo-deposit.json').resolve(),'production'),state)
 class Client:
  def get(self,i):events.append('GET');need(i==remote['id'],'wrong ID');return copy.deepcopy(remote)
  def publish(self,i):events.append('POST publish');remote['submitted']=True;remote['doi']='10.5281/zenodo.'+str(i)
 client=Client();args=types.SimpleNamespace(command='publish',manifest=d/'zenodo-deposit.json',sandbox=False,confirm_id=remote['id'],check_doi=False)
 rejected=[]
 for k in meta:
  original=copy.deepcopy(remote['metadata'][k]);remote['metadata'][k]=None
  try:kit.run(args,client=client)
  except (kit.DepositError,RuntimeError):rejected.append(k)
  else:raise RuntimeError('real kit accepted altered metadata '+k)
  remote['metadata'][k]=original
 need('POST publish'not in events,'metadata rejection happened after POST')
 result=kit.run(args,client=client);need(events.count('POST publish')==1 and result['metadata_normalizations']==[] and result['state']=='published','actual metadata mock publish failed')
 kit.run(args,client=client);need(events.count('POST publish')==1,'known published ID repeated POST')
 return {'actual_manifest_sha256':sha(d/'zenodo-deposit.json'),'actual_metadata_fields':good,'actual_files':[{'name':f['name'],'bytes':f['size'],'sha256':f['sha256']} for f in files],'all11_schema_projection_corruptions_rejected':badfields,'all11_actual_kit_metadata_corruptions_rejected_before_POST':rejected,'genuine_shared_kit_run_and_strict_wrapper':True,'mock_publish_POST_count':1,'known_published_ID_repeat_readonly':True,'events':events,'limits':'Actual bytes and metadata; synthetic production ID, all service methods mocked. No real release gate or production integration clearance.'}
def main():
 out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive(),'provenance':provenance(),'metadata':metadata()};save(R/'DETACHED_CHECKS.json',out);print(json.dumps({k:'PASS'for k in ['archive','provenance','metadata']}))
if __name__=='__main__':main()
