"""Protect exhaustive review activation from partial or mismatched source inputs."""
import contextlib, hashlib, importlib.util, io, json, pathlib, sqlite3, tempfile, unittest

spec=importlib.util.spec_from_file_location('review_merge',pathlib.Path(__file__).parent/'review_v2/merge.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class MergeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old=m.ROOT,m.HERE
  m.ROOT=pathlib.Path(self.tmp.name);m.HERE=m.ROOT/'review_v2';m.HERE.mkdir();(m.ROOT/'cache').mkdir()
  self.put(m.ROOT/'manifest.json',{'revision':'pinned','records':1})
  self.put(m.HERE/'assignments.json',{'source_revision':'pinned','shards':[['1']]})
  self.review={'id':'1','impact':3,'p_solve':.08,'p_valid_open':.7,'route':'proof','decision':'candidate','note':'An explicit normal form suggests a proof; singular cases remain unresolved.'}
  self.put(m.HERE/'reviews_0.json',[self.review]);self.put(m.HERE/'policy_v2.json',{'version':'2.0-five-turn-proof','turn_limit':5})
  self.put(m.ROOT/'assessments.json',{'1':{'holds':['prior_evidence_hold']}})
  self.put(m.ROOT/'policy.json',{'version':'old'})
  self.payload={'id':1,'statement':'Exact reviewed statement'}
  with sqlite3.connect(m.ROOT/'cache/catalog.sqlite') as c:
   c.execute('create table metadata (revision text)');c.execute("insert into metadata values ('pinned')")
   c.execute('create table records (key text primary key,payload text,report text)')
   c.execute('insert into records values (?,?,?)',('1',json.dumps(self.payload),'{}'))
 def tearDown(self):m.ROOT,m.HERE=self.old;self.tmp.cleanup()
 def put(self,p,obj):p.write_text(json.dumps(obj))
 def assert_rejected_without_mutation(self):
  before={p:p.read_bytes() for p in [m.ROOT/'assessments.json',m.ROOT/'policy.json']}
  with self.assertRaises(ValueError):m.merge('exclude_resolved')
  for p,data in before.items():self.assertEqual(p.read_bytes(),data)
  self.assertFalse((m.HERE/'merge_manifest.json').exists())
 def test_incomplete_reviews_cannot_activate(self):
  self.put(m.HERE/'reviews_0.json',[]);self.assert_rejected_without_mutation()
 def test_wrong_cache_revision_cannot_rebind_reviews(self):
  with sqlite3.connect(m.ROOT/'cache/catalog.sqlite') as c:c.execute("update metadata set revision='different'")
  self.assert_rejected_without_mutation()
 def test_wrong_cache_ids_cannot_drop_reviews(self):
  with sqlite3.connect(m.ROOT/'cache/catalog.sqlite') as c:c.execute("update records set key='2'")
  self.assert_rejected_without_mutation()
 def test_duplicate_assignments_rejected(self):
  self.put(m.HERE/'assignments.json',{'source_revision':'pinned','shards':[['1','1']]});self.assert_rejected_without_mutation()
 def test_invalid_or_unknown_override_rejected_before_activation(self):
  for override in [{'1':{'p_solve':2}},{'11':{'decision':'exclude'}},{'1':{'id':'11'}}]:
   self.put(m.HERE/'adversarial_overrides.json',override);self.assert_rejected_without_mutation()
 def test_missing_policy_cannot_partially_replace_assessments(self):
  (m.HERE/'policy_v2.json').unlink();self.assert_rejected_without_mutation()
 def test_rerun_cannot_erase_later_assessment(self):
  with contextlib.redirect_stdout(io.StringIO()):m.merge('exclude_resolved')
  a=m.read(m.ROOT/'assessments.json');a['1'].update(p_solve=.001,note='A later source review records a new obstacle and lower probability.')
  self.put(m.ROOT/'assessments.json',a);before=(m.ROOT/'assessments.json').read_bytes()
  with self.assertRaises(ValueError):m.merge('exclude_resolved')
  self.assertEqual(before,(m.ROOT/'assessments.json').read_bytes())
 def test_full_merge_preserves_holds_overrides_and_source_binding(self):
  self.put(m.HERE/'adversarial_overrides.json',{'1':{'decision':'repair','note':'The source omits an essential hypothesis, so repair the target before proceeding.','holds':['source_scope_repair_required']}})
  with contextlib.redirect_stdout(io.StringIO()):m.merge('exclude_resolved')
  a=m.read(m.ROOT/'assessments.json')['1']
  self.assertEqual(a['decision'],'repair');self.assertIn('prior_evidence_hold',a['holds']);self.assertIn('source_scope_repair_required',a['holds']);self.assertIn('desk_review_repair',a['holds'])
  self.assertEqual(a['review_hash'],hashlib.sha256(json.dumps([self.payload,{}],sort_keys=True).encode()).hexdigest())
  self.assertEqual(m.read(m.HERE/'reviews_0.json'),[self.review])
  self.assertEqual(m.read(m.HERE/'merge_manifest.json')['records_reviewed'],1)

if __name__=='__main__':unittest.main()
