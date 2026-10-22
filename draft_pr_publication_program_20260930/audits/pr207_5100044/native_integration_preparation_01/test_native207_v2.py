"""Offline fixtures only: no gh, Git, network, global views, or real acceptance.
Temporary files are small, owned, and removed beneath this preparation folder.
"""
import base64, copy, importlib.util, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

HERE=Path(__file__).absolute().parent
spec=importlib.util.spec_from_file_location('native207_test_subject',HERE/'native207_v2.py')
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
c=n.core()

class FakeAPI:
 """Independent immediate native object store; no service implementation used."""
 def __init__(self):
  self.trees={};self.blobs={};self.commits={};self.calls=[];self.main='1'*40;self.pr_merged=False
 def blob(self,raw):
  oid=c.native('blob',raw);self.blobs[oid]=raw;return oid
 def tree(self,entries):
  rows=sorted([(name,*entry) for name,entry in entries.items()],key=lambda x:x[0].encode()+(b'/' if x[1]=='040000' else b''))
  oid=c.tree_hash(rows);self.trees[oid]=entries.copy();return oid
 def insert(self,root,path,entry):
  parts=path.split('/');d=dict(self.trees[root]) if root else {};name=parts[0]
  if len(parts)==1:d[name]=entry
  else:
   old=d.get(name);assert old is None or old[:2]==('040000','tree')
   d[name]=('040000','tree',self.insert(old[2] if old else None,'/'.join(parts[1:]),entry))
  return self.tree(d)
 def setup(self,overlay,pre):
  empty=self.tree({})
  root=self.tree({'empty':('040000','tree',empty),'executable':('100755','blob',self.blob(b'exec\n')),'symlink':('120000','blob',self.blob(b'target')),'submodule':('160000','commit','b'*40),'opaque_foreign':('040000','tree','f'*40)})
  for path,old in pre.items():
   if old is not None:
    raw=overlay[path] if c.native('blob',overlay[path])==old[2] else b'old '+path.encode()+b'\n'
    if path==n.QUEUE:raw=QUEUE_OLD if c.native('blob',QUEUE_OLD)==old[2] else QUEUE_NEW
    assert self.blob(raw)==old[2];root=self.insert(root,path,old)
  self.commits[self.main]={'sha':self.main,'tree':{'sha':root},'parents':[{'sha':n.ANCHOR}],'message':'fixture parent'}
  self.commits[n.HEAD]={'sha':n.HEAD,'tree':{'sha':n.HEAD_TREE},'parents':[],'message':'original fixture identity only'}
  return root
 def __call__(self,method,path,body=None):
  self.calls.append((method,path,copy.deepcopy(body)))
  if method=='GET':
   if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
   if path=='pulls/207':return {'number':207,'head':{'sha':n.HEAD},'base':{'ref':'main'},'draft':False,'merged':self.pr_merged,'state':'closed' if self.pr_merged else 'open','merge_commit_sha':self.main if self.pr_merged else None}
   if path.startswith('compare/'):
    base,end=path[8:].split('...');return {'status':'ahead','merge_base_commit':{'sha':base}}
   kind,oid=path.rsplit('/',1)
   if kind=='git/commits':return copy.deepcopy(self.commits[oid])
   if kind=='git/trees':
    entries=self.trees[oid]
    rows=sorted(entries.items(),key=lambda x:x[0].encode()+(b'/' if x[1][0]=='040000' else b''))
    return {'sha':oid,'truncated':False,'tree':[dict(path=name,mode=e[0],type=e[1],sha=e[2]) for name,e in rows]}
   if kind=='git/blobs':
    raw=self.blobs[oid];return {'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
  assert method=='POST'
  if path=='git/blobs':
   assert body['encoding']=='base64';return {'sha':self.blob(base64.b64decode(body['content'],validate=True))}
  if path=='git/trees':
   root=body['base_tree']
   for row in body['tree']:
    assert ('content' in row) != ('sha' in row)
    oid=self.blob(row['content'].encode()) if 'content' in row else row['sha']
    root=self.insert(root,row['path'],(row['mode'],row['type'],oid))
   return {'sha':root}
  if path=='git/commits':
   oid=('%040x'%(4096+len(self.commits)));self.commits[oid]={'sha':oid,'tree':{'sha':body['tree']},'parents':[{'sha':x} for x in body['parents']],'message':body['message']};return {'sha':oid}
  raise AssertionError('Unexpected fake endpoint '+path)

QUEUED_ROW=b'| 225 | 5100044 / AMR-050-0044 | Elliptic-billiard invariant k_{804,a} | 0.1905 | 5.0 | 3 | 2021 | queued | 0/5 |  |  |  |\n'
assert n.pin(QUEUED_ROW)==n.QUEUED_ROW_PIN
QUEUE_OLD=b'heading\n| 1 | 999 / OTHER | foreign | 1 | 2 | 3 | 4 | untouched | 0/5 |  | foreign bytes |  |\n'+QUEUED_ROW+b'footer\n'
QUEUE_NEW=QUEUE_OLD.replace(b'| queued | 0/5 |  |  |  |',b'| claimed_solved | 1/5 |  | actual fixture review | fixture DOI |')

class Tests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=HERE,prefix='OFFLINE_FIXTURE_');self.d=Path(self.temp.name)
  self.base=n.BASE;self.repo=n.C;self.program=n.P;n.BASE=self.d;n.C=self.d/'fixture_repository';n.P=n.C/'draft_pr_publication_program_20260930';n.P.mkdir(parents=True)
  for name in ('archive206_verified_reference.py','CUSTODY_INVENTORY.json','CUSTODY_DELTA.json'):self.write(name,(HERE/name).read_bytes())
  self.m,self.overlay=self.manifest();self.manifest_path=self.d/'MANIFEST.json';self.save()
 def tearDown(self):
  n.BASE=self.base;n.C=self.repo;n.P=self.program;self.temp.cleanup()
 def write(self,name,raw):
  path=self.d/name;path.parent.mkdir(parents=True,exist_ok=True)
  if path.exists():path.chmod(0o644)
  path.write_bytes(raw);path.chmod(0o444);return path
 def save(self):
  if self.manifest_path.exists():self.manifest_path.chmod(0o644)
  self.manifest_path.write_bytes(n.enc(self.m));self.manifest_path.chmod(0o444)
 def load(self):return n.inputs(self.manifest_path,n.pin(self.manifest_path.read_bytes()))
 def manifest(self,phase='merge95'):
  inventory=n.decode((HERE/'CUSTODY_INVENTORY.json').read_bytes());overlay={}
  for name in inventory:
   overlay[n.ATTEMPT+name]=b'corrected current fixture '+name.encode()+b'\n'
   overlay[n.CASE+'submitted_snapshot/'+name]=(HERE.parent/'submitted_snapshot'/name).read_bytes()
  overlay[n.ATTEMPT+'requirements.txt']=b'fixture dependency\n'
  overlay[n.ATTEMPT+'current_execution_receipt.json']=b'{"fixture_only":true}\n'
  facts=n.phase_facts(phase)
  for path in n.VIEWS:overlay[path]=n.enc(facts) if path.endswith('.json') else b'fixture current view\n'+n.marker(facts)+b'\n'
  progress={**facts,'published_PRs':list(range(1,34))+[207],'fully_completed_eligible_PRs':list(range(1,50))+([207] if phase=='completion100' else []),'dated_eligible_total':99,'current_case_percent':facts['case_workflow_estimate_percent'],'current_publication_ready':True,'fully_completed_fraction_percent':100*facts['fully_completed_count']/99};overlay[n.VIEWS[2]]=n.enc(progress)
  roles={'scientific','whole_package_review','publication','tracker'}|({'ready_PR_merge'} if phase=='completion100' else set())
  receipts={}
  for role in roles:
   path=n.CASE+'fixture_evidence/'+role+'.json';overlay[path]=n.enc({'fixture_only':True,'role':role});receipts[role]={'path':path,**n.pin(overlay[path])}
  gate=n.CASE+'fixture_evidence/GATES.json'
  overlay[gate]=n.enc({'schema':'pr207-root-native-phase-gates-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':phase,'accepted':True,'original_head':n.HEAD,'facts':facts,'scientific_accepted':True,'whole_package_accepted':True,'actual_publication_verified':True,'actual_tracker_verified':True,'ready_for_merge':True,'receipts':receipts,'fixture_only':True})
  overlay[n.QUEUE]=QUEUE_NEW
  overlay[n.CASE+'fixture_evidence/paper.pdf']=b'%PDF-1.7\x00\xffbinary fixture\n'
  overlay[n.CASE+'fixture_evidence/package.zip']=overlay[n.CASE+'fixture_evidence/paper.pdf']
  rows=[];local=[]
  for index,(path,raw) in enumerate(overlay.items()):
   name='sources/'+str(index);self.write(name,raw)
   old=(QUEUE_NEW if phase=='completion100' else QUEUE_OLD) if path==n.QUEUE else b'old '+path.encode()+b'\n'
   pre={'mode':'100644','type':'blob','sha':c.native('blob',old)} if path in n.VIEWS or path==n.QUEUE else None
   rows.append({'path':path,'source':name,**n.pin(raw),'git_blob':c.native('blob',raw),'preimage':pre})
  for path in n.VIEWS:
   old=b'old '+path.encode()+b'\n';local.append({'path':path,'preimage':n.pin(old)});p=n.C/path;p.parent.mkdir(parents=True,exist_ok=True)
   if p.exists():p.chmod(0o644)
   p.write_bytes(old);p.chmod(0o444)
  m={'schema':'pr207-native-integration-inputs-v1','PR':207,'phase':phase,'anchor':n.ANCHOR,'original_head':n.HEAD,'original_head_tree':n.HEAD_TREE,'expected_parent':'1'*40,'helper_pin':n.pin((HERE/'native207_v2.py').read_bytes()),'core_pin':n.CORE_PIN,'facts':facts,'files':rows,'total_files':len(rows),'total_bytes':sum(map(len,overlay.values())),'local_views':local,'gate_receipt':gate,'commit_message':'Offline fixture only '+phase}
  return m,overlay
 def setup_api(self):
  cc,m,overlay,pre,pins=self.load();api=FakeAPI();api.setup(overlay,pre);return cc,m,overlay,pre,pins,api
 def make_candidate(self):
  cc,m,overlay,pre,pins,api=self.setup_api();j=n.journal_new('candidate_fixture');result=n.candidate(cc,m,overlay,pre,pins,api,j);return cc,m,overlay,pre,pins,api,result
 def mutate_body(self,path,body):
  row=next(x for x in self.m['files'] if x['path']==path);p=self.d/row['source'];p.chmod(0o644);p.write_bytes(body);p.chmod(0o444);row.update(n.pin(body));row['git_blob']=c.native('blob',body);self.m['total_bytes']=sum(x['bytes'] for x in self.m['files']);self.save()

 def test_full_candidate_binary_dedup_and_independent_verify(self):
  cc,m,overlay,pre,pins,api,result=self.make_candidate()
  self.assertTrue(result['full_scope_verified']);self.assertEqual(result['parents'],['1'*40,n.HEAD]);self.assertEqual(api.main,'1'*40)
  self.assertEqual(len([x for x in api.calls if x[:2]==('POST','git/blobs')]),1)
  self.assertFalse(any(x[1]=='git/trees/'+'f'*40 for x in api.calls))
  root=result['tree'];foreign={k:v for k,v in api.trees[root].items() if k in ('empty','executable','symlink','submodule','opaque_foreign')}
  old=api.trees[api.commits['1'*40]['tree']['sha']];self.assertEqual(foreign,{k:old[k] for k in foreign})
  api.calls=[];again=n.verify(cc,m,overlay,pre,pins,api,'1'*40,result['candidate']);self.assertTrue(again['full_scope_verified']);self.assertTrue(all(x[0]=='GET' for x in api.calls))
 def test_get_only_plan(self):
  cc,m,overlay,pre,pins,api=self.setup_api();r=n.plan(cc,m,overlay,pre,pins,api);self.assertEqual(r['status'],'GET_ONLY_PLAN');self.assertTrue(all(x[0]=='GET' for x in api.calls))
 def test_same_sha_corrupt_tree_rejected(self):
  cc,m,overlay,pre,pins,api=self.setup_api();root=api.commits[api.main]['tree']['sha'];api.trees[root]['symlink']=('100644','blob',api.blob(b'target'))
  with self.assertRaisesRegex(RuntimeError,'SHA1'):n.plan(cc,m,overlay,pre,pins,api)
 def test_authenticated_mode_preimage_rejected(self):
  cc,m,overlay,pre,pins,api=self.setup_api();root=api.commits[api.main]['tree']['sha'];entry=api.trees[root]
  path=n.VIEWS[0];root=api.insert(root,path,('100755','blob',pre[path][2]));api.commits[api.main]['tree']['sha']=root
  with self.assertRaisesRegex(RuntimeError,'preimage'):n.plan(cc,m,overlay,pre,pins,api)
 def test_deleted_preimage_rejected(self):
  cc,m,overlay,pre,pins,api=self.setup_api();pre[n.VIEWS[0]]=('100644','blob','c'*40)
  with self.assertRaisesRegex(RuntimeError,'preimage'):n.plan(cc,m,overlay,pre,pins,api)
 def test_overlay_ancestor_collision_rejected(self):
  cc,m,overlay,pre,pins,api=self.setup_api();overlay[n.CASE.rstrip('/')]=b'collision';pre[n.CASE.rstrip('/')]=None
  with self.assertRaisesRegex(RuntimeError,'collision'):n.plan(cc,m,overlay,pre,pins,api)
 def test_foreign_overlay_rejected(self):
  self.m['files'][0]['path']='FOREIGN.md';self.save()
  with self.assertRaisesRegex(RuntimeError,'Foreign overlay'):self.load()
 def test_native_attempt_missing_file_rejected(self):
  self.m['files']=[x for x in self.m['files'] if x['path']!=n.ATTEMPT+'requirements.txt'];self.m['total_files']=len(self.m['files']);self.m['total_bytes']=sum(x['bytes'] for x in self.m['files']);self.save()
  with self.assertRaisesRegex(RuntimeError,'twenty'):self.load()
 def test_foreign_queue_line_rejected(self):
  self.mutate_body(n.QUEUE,QUEUE_NEW.replace(b'foreign bytes',b'changed foreign'))
  cc,m,overlay,pre,pins,api=self.setup_api()
  with self.assertRaisesRegex(RuntimeError,'Foreign QUEUE'):n.plan(cc,m,overlay,pre,pins,api)
 def test_queue_status_or_rank_change_rejected(self):
  for raw in (QUEUE_NEW.replace(b'claimed_solved',b'published'),QUEUE_NEW.replace(b'| 225 |',b'| 224 |')):
   with self.assertRaises(RuntimeError):n.queue_change(QUEUE_OLD,raw,'merge95')
 def test_duplicate_json_and_nonfinite_rejected(self):
  for raw in (b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}'):
   with self.assertRaises(RuntimeError):n.decode(raw)
 def test_stale_parent_rejected(self):
  cc,m,overlay,pre,pins,api=self.setup_api();api.main='3'*40
  with self.assertRaisesRegex(RuntimeError,'lease'):n.plan(cc,m,overlay,pre,pins,api)
 def test_wrong_commit_parents_rejected(self):
  cc,m,overlay,pre,pins,api,r=self.make_candidate();api.commits[r['candidate']]['parents']=[{'sha':'1'*40}]
  with self.assertRaisesRegex(RuntimeError,'parents'):n.verify(cc,m,overlay,pre,pins,api,'1'*40,r['candidate'])
 def test_wrong_native_body_rejected(self):
  cc,m,overlay,pre,pins,api,r=self.make_candidate();api.blobs[next(iter(pins.values()))['git_blob']]=b'wrong body'
  with self.assertRaisesRegex(RuntimeError,'body identity'):n.verify(cc,m,overlay,pre,pins,api,'1'*40,r['candidate'])
 def test_missing_publication_tracker_gate_rejected(self):
  gate=self.m['gate_receipt'];raw=n.decode(self.overlay[gate]);del raw['receipts']['tracker'];self.mutate_body(gate,n.enc(raw))
  with self.assertRaisesRegex(RuntimeError,'roles'):self.load()
 def test_false_actual_gate_rejected(self):
  gate=self.m['gate_receipt'];raw=n.decode(self.overlay[gate]);raw['actual_publication_verified']=False;self.mutate_body(gate,n.enc(raw))
  with self.assertRaisesRegex(RuntimeError,'actual_publication_verified'):self.load()
 def test_phase_count_and_bool_alias_rejected(self):
  self.m['facts']['fully_completed_count']=50;self.save()
  with self.assertRaisesRegex(RuntimeError,'counters'):self.load()
  self.m['facts']=n.phase_facts('merge95');self.m['facts']['advance_to_next_PR_authorized_now']=0;self.save()
  with self.assertRaisesRegex(RuntimeError,'counters'):self.load()
 def test_completion_requires_native_merge(self):
  self.m,self.overlay=self.manifest('completion100');self.save();cc,m,overlay,pre,pins,api=self.setup_api()
  with self.assertRaisesRegex(RuntimeError,'merge required'):n.plan(cc,m,overlay,pre,pins,api)
  api.pr_merged=True;r=n.plan(cc,m,overlay,pre,pins,api);self.assertEqual(r['parents'],['1'*40]);self.assertEqual(r['facts']['next_numeric_intake_cursor'],208)
 def test_after_cas_explicit_readonly_mode(self):
  cc,m,overlay,pre,pins,api,r=self.make_candidate();api.main=r['candidate'];api.pr_merged=True
  with self.assertRaisesRegex(RuntimeError,'lease'):n.verify(cc,m,overlay,pre,pins,api,'1'*40,r['candidate'])
  api.calls=[];verified=n.verify(cc,m,overlay,pre,pins,api,'1'*40,r['candidate'],after_cas=True);self.assertFalse(verified['fresh_parent_lease_required']);self.assertTrue(all(x[0]=='GET' for x in api.calls))
 def test_sync_without_actual_acceptance_does_not_write(self):
  cc,m,overlay,pre,pins,api=self.setup_api();path=self.write('PREPARATION_NOT_ACCEPTANCE.json',n.enc({'schema':'preparation','accepted':False}));before={x:n.local_pin(n.C/x) for x in n.VIEWS};j=n.journal_new('denied_sync')
  with self.assertRaisesRegex(RuntimeError,'actual Root acceptance'):n.sync(cc,m,overlay,pre,pins,api,j,n.pin(self.manifest_path.read_bytes()),path,n.pin(path.read_bytes()))
  self.assertEqual(before,{x:n.local_pin(n.C/x) for x in n.VIEWS});self.assertEqual(api.calls,[])
 def test_sync_fake_actual_acceptance_and_stable_lock_resume(self):
  cc,m,overlay,pre,pins,api,r=self.make_candidate();api.main=r['candidate'];api.pr_merged=True
  wp=n.pin(self.manifest_path.read_bytes());a={'schema':'pr207-root-native-integration-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':207,'phase':m['phase'],'accepted':True,'full_scope_verified':True,'all_selected_native_bodies_verified':True,'manifest_pin':wp,'helper_pin':n.pin((HERE/'native207_v2.py').read_bytes()),'facts':m['facts'],'parent':m['expected_parent'],'original_head':n.HEAD,'original_head_tree':n.HEAD_TREE,'candidate':r['candidate'],'tree':r['tree'],'actual_MAIN_observed':r['candidate'],'Root_ref_update':{'expected_sha':m['expected_parent'],'sha':r['candidate'],'force':False,'success_confirmed_by_actual_native_readback':True},'fixture_only':True}
  path=self.write('FAKE_ACTUAL_ACCEPTANCE.json',n.enc(a));lock=n.P/'ROOT_GLOBAL_FIVE_WRITER.lock';lock.write_bytes(n.LOCK_BYTES);lock.chmod(0o444);inode=lock.stat().st_ino
  # One postimage represents a previous interrupted per-file sync; explicit resume accepts it.
  first=n.C/n.VIEWS[0];first.chmod(0o644);first.write_bytes(overlay[n.VIEWS[0]]);first.chmod(0o444)
  api.calls=[];result=n.sync(cc,m,overlay,pre,pins,api,n.journal_new('sync_fixture'),wp,path,n.pin(path.read_bytes()))
  self.assertTrue(result['all_five_local_files_match_actual_checkpoint']);self.assertEqual(inode,lock.stat().st_ino);self.assertTrue(all(x[0]=='GET' for x in api.calls));self.assertTrue((self.d/'ROOT_ACTUAL_MERGE95_POINTER.json').is_file())
 def test_api_ref_route_and_no_retry_uncertainty(self):
  api=n.API(n.journal_new('api_fixture'),mutate=True)
  for method,path in (('PATCH','git/refs/heads/main'),('POST','pulls'),('GET','repos')):
   with self.assertRaisesRegex(RuntimeError,'No ref'):api(method,path,{})
  def fail(*args,**kwargs):
   self.assertTrue(any(api.journal.glob('*.OBJECT_INTENT.json')));raise TimeoutError('fixture timeout')
  with patch.object(n.subprocess,'run',side_effect=fail) as called:
   with self.assertRaisesRegex(RuntimeError,'Attempt stopped'):api('POST','git/blobs',{'content':'AA==','encoding':'base64'})
   with self.assertRaisesRegex(RuntimeError,'Attempt stopped'):api('POST','git/blobs',{'content':'AA==','encoding':'base64'})
   self.assertEqual(called.call_count,1)
 def test_required_queue_selection_both_phases(self):
  for phase in ('merge95','completion100'):
   if phase!='merge95':self.m,self.overlay=self.manifest(phase)
   self.m['files']=[x for x in self.m['files'] if x['path']!=n.QUEUE];self.m['total_files']=len(self.m['files']);self.m['total_bytes']=sum(x['bytes'] for x in self.m['files']);self.save()
   with self.assertRaisesRegex(RuntimeError,'QUEUE selection required'):self.load()
 def test_one_byte_actual_event_bool_bytecount_rejected(self):
  gate=self.m['gate_receipt'];obj=n.decode(self.overlay[gate]);event=obj['receipts']['scientific']['path'];self.mutate_body(event,b'x');obj['receipts']['scientific'].update({'bytes':True,'sha256':n.pin(b'x')['sha256']});self.mutate_body(gate,n.enc(obj))
  with self.assertRaisesRegex(RuntimeError,'Exact bounded byte pin'):self.load()
 def test_ordinary_cli_and_optimization_rejection(self):
  ordinary=subprocess.run([sys.executable,'-E','-S','-B','-P',str(HERE/'native207_v2.py'),'--help'],capture_output=True)
  self.assertEqual(ordinary.returncode,0,ordinary.stderr.decode());self.assertIn(b'--manifest',ordinary.stdout)
  optimized=subprocess.run([sys.executable,'-E','-S','-B','-P','-O',str(HERE/'native207_v2.py'),'--help'],capture_output=True)
  self.assertNotEqual(optimized.returncode,0);self.assertIn(b'Ordinary Python -E -S -B -P required',optimized.stderr)
 def test_sources_canonical_readonly_and_bytepin(self):
  row=self.m['files'][0];path=self.d/row['source'];path.chmod(0o644)
  with self.assertRaisesRegex(RuntimeError,'Readonly'):self.load()
  path.chmod(0o444);alias=self.d/'alias';alias.symlink_to(path)
  with self.assertRaisesRegex(RuntimeError,'Canonical'):n.sealed(alias,n.pin(path.read_bytes()))
  with self.assertRaisesRegex(RuntimeError,'changed'):n.sealed(path,{'bytes':0,'sha256':'0'*64})

if __name__=='__main__':unittest.main(verbosity=2)
