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
    def test_zero_validity_has_zero_lower_bound(self):
        q.write(q.ROOT/'assessments.json',{'1':{'review_hash':self.row()['review_hash'],'p_valid_open':0}})
        q.rank(None);self.assertEqual(self.row()['ev_low'],0);self.assertEqual(self.row()['ev'],0)
    def test_stale_assessment_file_rejected(self):
        path=q.ROOT/'review.json';q.write(path,{'review_hash':'old'})
        with self.assertRaises(ValueError):q.assess(types.SimpleNamespace(id='1',file=str(path)))
        self.assertEqual(q.read(q.ROOT/'assessments.json',{}),{})
    def test_stale_readiness_rejected(self):
        path=q.ROOT/'ready.json';q.write(path,{'review_hash':'old'})
        with self.assertRaises(ValueError):q.status(types.SimpleNamespace(id='1',status='ready',evidence=str(path),note='test'))
        self.assertEqual(q.read(q.ROOT/'state.json',{}),{})
    def test_retired_status_exported(self):
        self.install([])
        q.status(types.SimpleNamespace(id='1',status='deferred',evidence=None,note='Keep for later'))
        self.assertEqual(self.row()['local_status'],'deferred')
    def setup_five_turn_attempt(self):
        cfg={**POLICY,'turn_limit':5,'version':'2.0-five-turn-proof','age_modifier':{'maximum_bonus':.15,'saturation_years':100}}
        q.write(q.ROOT/'policy.json',cfg)
        rev={'review_hash':self.row()['review_hash'],'review_policy':cfg['version'],'route':'proof','decision':'candidate','impact':3,'p_solve':.03,'p_valid_open':.6}
        q.write(q.ROOT/'assessments.json',{'1':rev})
        q.write(q.ROOT/'state.json',{'1':{'status':'in_progress','review_hash':self.row()['review_hash'],'turns_used':0}})
        q.rank(None)
    def test_five_turn_stop(self):
        self.setup_five_turn_attempt()
        for i in range(5):q.record_turn(types.SimpleNamespace(id='1',note='Substantive proof turn',outcome='continue'))
        self.assertEqual(q.read(q.ROOT/'state.json',{})['1']['status'],'exhausted')
        self.assertFalse(self.row()['eligible']);self.assertIn('5/5',(q.ROOT/'QUEUE.md').read_text())
        with self.assertRaises(ValueError):q.record_turn(types.SimpleNamespace(id='1',note='Sixth turn',outcome='continue'))
    def test_candidate_on_fifth_turn_preserved(self):
        self.setup_five_turn_attempt()
        for i in range(4):q.record_turn(types.SimpleNamespace(id='1',note='Work',outcome='continue'))
        q.record_turn(types.SimpleNamespace(id='1',note='Proof candidate',outcome='candidate'))
        self.assertEqual(q.read(q.ROOT/'state.json',{})['1']['status'],'candidate_result')
    def test_status_change_cannot_reset_budget(self):
        self.setup_five_turn_attempt()
        q.record_turn(types.SimpleNamespace(id='1',note='First turn',outcome='continue'))
        q.status(types.SimpleNamespace(id='1',status='partial',note='Partial result',evidence=None))
        self.assertEqual(q.read(q.ROOT/'state.json',{})['1']['turns_used'],1)
    def test_large_search_never_admitted(self):
        self.setup_five_turn_attempt()
        a=q.read(q.ROOT/'assessments.json',{});a['1']['route']='large_search';q.write(q.ROOT/'assessments.json',a)
        q.rank(None);self.assertIn('large_exhaustive_search',self.row()['holds'])
    def test_age_only_uses_proposal_year(self):
        self.setup_five_turn_attempt();self.assertEqual(self.row()['age_multiplier'],1)
        self.install([{**self.p,'proposed_year':1926}]);self.assertEqual(self.row()['age_multiplier'],1.15)
    def test_reproducibility(self):
        before=(q.ROOT/'catalog.json').read_bytes();q.rank(None);self.assertEqual(before,(q.ROOT/'catalog.json').read_bytes())
if __name__=='__main__':unittest.main()
