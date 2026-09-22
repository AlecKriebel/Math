"""Regression tests for lost-work and false-solution failure modes."""
import contextlib, importlib.util, io, json, pathlib, sqlite3, tempfile, types, unittest
spec=importlib.util.spec_from_file_location('research_queue',pathlib.Path(__file__).with_name('queue.py'))
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
POLICY=q.read(q.ROOT/'policy.json',{})
class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.old=q.ROOT;q.ROOT=pathlib.Path(self.tmp.name)
        q.write(q.ROOT/'policy.json',POLICY);q.write(q.ROOT/'state.json',{});q.write(q.ROOT/'assessments.json',{})
        self.p={'id':1,'problem_number':'TEST-1','title':'A finite graph construction','statement':'Does there exist a finite graph satisfying the following explicitly specified conditions?', 'statement_status':'exact','status':'open'}
        self.install([self.p])
    def tearDown(self):q.ROOT=self.old;self.tmp.cleanup()
    def install(self,problems):
        db=q.connect();db.execute('DELETE FROM records')
        db.executemany('INSERT INTO records VALUES (?,?,?)',[(str(p['id']),json.dumps(p),'{}') for p in problems])
        db.execute('CREATE TABLE IF NOT EXISTS metadata (revision TEXT)');db.execute('DELETE FROM metadata');db.execute("INSERT INTO metadata VALUES ('test')");db.commit();db.close()
        q.write(q.ROOT/'manifest.json',{'revision':'test','records':len(problems)})
        with contextlib.redirect_stdout(io.StringIO()):q.rank(None)
    def row(self):return q.read(q.ROOT/'catalog.json',[])[0]
    def test_cache_loss_cannot_erase_catalog(self):
        before=(q.ROOT/'catalog.json').read_bytes();(q.ROOT/'cache/catalog.sqlite').unlink()
        with self.assertRaises(ValueError):q.rank(None)
        self.assertEqual(before,(q.ROOT/'catalog.json').read_bytes())
    def test_partial_not_solved(self):
        for status in ['open','partially_solved','not solved']:
            p={**self.p,'background':'<!-- LITERATURE-TRIAGE:BEGIN --> **Status:** '+status}
            self.assertNotIn('upstream_resolution_claim',q.score(p,{},POLICY)['holds'])
        p={**self.p,'background':'<!-- LITERATURE-TRIAGE:BEGIN --> **Status:** solved'}
        self.assertIn('upstream_resolution_claim',q.score(p,{},POLICY)['holds'])
    def test_malformed_low_difficulty_held(self):
        a=q.score({**self.p,'difficulty_level_id':2,'statement_status':'unrecoverable'},{},POLICY)
        self.assertIn('statement_repair_required',a['holds'])
    def test_metadata_change_preserves_but_invalidates_state(self):
        q.write(q.ROOT/'state.json',{'1':{'status':'in_progress','note':'Do not lose this','review_hash':self.row()['review_hash']}})
        self.install([{**self.p,'status':'solved'}])
        self.assertEqual(q.read(q.ROOT/'state.json',{})['1']['note'],'Do not lose this')
        self.assertIn('status_review_stale',self.row()['holds']);self.assertFalse(self.row()['eligible'])
    def test_removed_record_preserved(self):
        self.install([]);self.assertFalse(self.row()['present']);self.assertIn('removed_upstream',self.row()['holds'])
    def test_duplicate_is_only_suspicion(self):
        self.install([self.p,{**self.p,'id':2,'problem_number':'TEST-2'}]);rows=q.read(q.ROOT/'catalog.json',[])
        self.assertEqual(len(rows),2);self.assertTrue(any('possible_duplicate_of:1' in x['holds'] for x in rows))
    def test_stale_verification_rejected(self):
        q.write(q.ROOT/'state.json',{'1':{'status':'independent_verification','review_hash':'old'}})
        ev=q.ROOT/'evidence.json';q.write(ev,{k:'artifact' for k in ['proof_artifact','independent_review','novelty_check','exact_claim']})
        with self.assertRaises(ValueError):q.status(types.SimpleNamespace(id='1',status='verified_solved',evidence=str(ev),note='test'))
    def test_hold_clearance_and_invalid_scores(self):
        p={**self.p,'statement_status':'reconstructed_unverified'};self.install([p]);r=self.row()
        a={'1':{'review_hash':r['review_hash'],'clear_holds':{'statement_repair_required':'Evidence: recovered primary formulation in local note'}}}
        q.write(q.ROOT/'assessments.json',a);q.rank(None);self.assertTrue(self.row()['eligible'])
        a['1']['p_solve']=2;q.write(q.ROOT/'assessments.json',a)
        with self.assertRaises(ValueError):q.rank(None)
    def test_statement_change_invalidates_review(self):
        q.write(q.ROOT/'assessments.json',{'1':{'review_hash':self.row()['review_hash'],'p_solve':0.1}})
        self.install([{**self.p,'statement':self.p['statement']+' Additional quantifier.'}])
        self.assertIn('assessment_stale',self.row()['holds'])
    def test_unrecorded_cache_rejected(self):
        (q.ROOT/'manifest.json').unlink()
        with self.assertRaises(ValueError):q.sync(types.SimpleNamespace(use_cache=True,revision='a'*40))
    def test_reproducibility(self):
        before=(q.ROOT/'catalog.json').read_bytes();q.rank(None);self.assertEqual(before,(q.ROOT/'catalog.json').read_bytes())
if __name__=='__main__':unittest.main()
