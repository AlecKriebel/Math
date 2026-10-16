"""Independent V2 review: synthetic protocol faults and opaque actual GET custody.

No production transport, state, asset bytes, or external mutation is used.
Every generated fixture and evidence directory belongs to this review only.
"""
import base64
import copy
from contextlib import ExitStack
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
PUBLIC_PARENT = HERE.parent
CASE = PUBLIC_PARENT.parents[1]
PRIVATE = CASE / 'private_sources/publication_admin_helper_v2/publication_v2_software_adversary1'
loader = importlib.util.spec_from_file_location('review_baseline_v2', PUBLIC_PARENT / 'test_publication_admin_v2.py')
t = importlib.util.module_from_spec(loader); loader.loader.exec_module(t)
m = t.m


class IndependentTests(t.V2Tests):
    def setUp(self):
        self.outer = ExitStack()
        self.outer.enter_context(patch.object(m, 'HERE', HERE))
        self.outer.enter_context(patch.object(m, 'PRIVATE', PRIVATE))
        super().setUp()

    def tearDown(self):
        try: super().tearDown()
        finally: self.outer.close()

    def call_stops_without_transport(self, e, *args, **kwargs):
        count=len(self.api.calls)
        with self.assertRaises(m.Stop): e.request(*args, **kwargs)
        self.assertEqual(len(self.api.calls),count)

    def test_independent_lowlevel_methods_flags_and_foreign_target_boundary(self):
        e=self.engine()
        for service,op,params,payload,write in (
            ('zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish',None,None,False),
            ('zenodo',f'GET /api/deposit/depositions/{m.ID}',None,None,True),
            ('zenodo',f'GET /api/deposit/depositions/{m.ID}',None,None,1),
            ('zenodo',f'DELETE /api/deposit/depositions/{m.ID}',None,None,True),
            ('zenodo',f'GET /api/deposit/depositions/{m.ID+1}',None,None,False),
            ('zenodo',f'GET /api/records/{m.ID}/draft',None,None,False),
            ('zenodo',f'GET /api/deposit/depositions/{m.ID}',{'accept':'anything'},None,False),
            ('zenodo',f'GET /api/deposit/depositions/{m.ID}',None,{},False),
            ('public_json','GET',{'id':m.ID+1,'native':False},None,False),
            ('public_json','GET',{'id':True,'native':False},None,False),
            ('public_json','GET',{'id':m.ID,'native':1},None,False),
            ('public_json','GET',{'id':m.ID,'native':False,'url':'https://elsewhere.invalid'},None,False),
            ('public_hash','GET',{'id':m.ID,'name':'preprint.pdf'},None,False),
            ('sheet','append',{},None,False),
            ('sheet','update',{},None,True),
            ('foreign','GET',{},None,False)):
            self.call_stops_without_transport(e,service,op,params,payload,write=write)
        self.call_stops_without_transport(e,'zenodo',f'GET /api/deposit/depositions/{m.ID}',file=self.source)

    def test_independent_sheet_read_scope_and_options(self):
        e=self.engine(); params={'spreadsheetId':m.v1.SHEET,'ranges':[m.v1.TAB+'C2:C'],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'}
        for delta in ({'spreadsheetId':'foreign'},{'ranges':[m.v1.TAB+'A2:D1000']},{'ranges':[m.v1.TAB+'A1:D1',m.v1.TAB+'A2:D3']},
                      {'ranges':[m.v1.TAB+'A1:D1',"'Elsewhere'!A2:D2"]},{'majorDimension':'COLUMNS'},{'valueRenderOption':'FORMATTED_VALUE'},
                      {'ranges':[m.v1.TAB+'A1:D1',m.v1.TAB+'A1:D1']},{'extra':'parameter'}):
            self.call_stops_without_transport(e,'sheet','batchGet',{**params,**delta})
        self.call_stops_without_transport(e,'sheet','get',{'spreadsheetId':m.v1.SHEET,'fields':'*'})
        self.call_stops_without_transport(e,'sheet','get',{'spreadsheetId':m.v1.SHEET,'fields':'spreadsheetId,sheets.properties'},payload={})

    def test_independent_direct_mutation_requires_active_guarded_phase(self):
        self.recover();e=self.engine();e.read_state(m.SPEC_SHA)
        self.call_stops_without_transport(e,'zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish',write=True)
        e.state['publish_intent']=True;e.state['approved_native_sha256']=m.ROOT_SNAPSHOT_SHA
        self.call_stops_without_transport(e,'zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish',write=True)
        e._active_phase='tracker';e.state['phase']='unknown_write';e.state['append_intent']=True
        self.call_stops_without_transport(e,'sheet','append',{}, {},write=True)

    def test_independent_baseclass_publish_cannot_omit_v2_active_phase(self):
        self.recover();e=self.engine()
        with self.assertRaises(m.Stop):m.v1.Admin.publish(e,m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertFalse(self.writes());self.assertTrue(json.loads(self.state.read_bytes())['publish_intent'])

    def test_independent_adopted_native_copy_and_source_copy_tampering_stop(self):
        self.recover();j=json.loads(self.state.read_bytes());Path(j['native_snapshot_path']).write_bytes(b'{}')
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertFalse(self.writes())
        self.source_copy.write_bytes(b'changed copy')
        with self.assertRaises(m.Stop):self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
        self.assertFalse(self.writes());self.assertEqual(self.source_copy.read_bytes(),b'changed copy')

    def test_independent_state_adoption_join_and_dependency_binding(self):
        self.recover();good=json.loads(self.state.read_bytes())
        for field,bad in (('case','other'),('revision',1),('id',m.ID+1),('v1_helper_sha256','0'*64),
                          ('dependencies',{'guards':'0'*64,'zenodo':m.v1.KIT_SHA}),('adoption',{**good['adoption'],'publisher':'other'})):
            j=copy.deepcopy(good);j[field]=bad;self.state.write_bytes(m.encoded(j))
            with self.assertRaises((m.Stop,m.z.DepositError)):
                self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
            self.assertFalse(self.writes())
        self.state.write_bytes(m.encoded(good))

    def test_independent_root_acceptance_snapshot_hash_join(self):
        a=json.loads(self.acceptance.read_bytes());a['approved_native_snapshot_sha256']='0'*64
        raw=m.encoded(a);self.acceptance.write_bytes(raw)
        with patch.object(m,'ROOT_ACCEPTANCE_SHA',m.sha(raw)):
            self.adoption['root_acceptance']['sha256']=m.ROOT_ACCEPTANCE_SHA;self.write_adoption()
            with self.assertRaises(m.Stop):self.engine().load_adoption(self.adoption_path,self.adoption_sha)
        self.assertFalse(self.api.calls);self.assertFalse(self.writes())

    def test_independent_native_hidden_disabled_mismatched_parent_flags_and_listing(self):
        orig=self.api.native_record
        def alter(fn):
            def fault():
                n=orig();fn(n);return n
            return fault
        changes=[lambda n:n['files'].update(enabled=False),lambda n:n['files'].update(count=2),
                 lambda n:n['files']['entries']['preprint.pdf']['access'].update(hidden=True),
                 lambda n:n['files']['entries']['preprint.pdf'].update(key='foreign.pdf'),
                 lambda n:n['parent'].update(id=str(m.ID)),lambda n:n.update(is_draft=False),
                 lambda n:n.update(is_published=True),lambda n:n.update(id=str(m.ID+1)),
                 lambda n:n.update(created='2026-10-13T01:00:00Z',updated='2026-10-13T00:00:00Z')]
        for fn in changes:
            with patch.object(self.api,'native_record',alter(fn)):
                with self.assertRaises((m.Stop,m.z.DepositError)):self.recover()
            self.assertFalse(self.state.exists());self.assertFalse(self.writes())
        original=self.api.zenodo
        def listingfault(method,ep,*args,**kwargs):
            r=original(method,ep,*args,**kwargs)
            if ep.endswith('/files'):r['entries'][0]['access']['hidden']=True
            return r
        with patch.object(self.api,'zenodo',listingfault):
            with self.assertRaises(m.Stop):self.recover()
        self.assertFalse(self.state.exists());self.assertFalse(self.writes())

    def test_independent_unattested_relations_stop_after_one_publish_no_append(self):
        self.recover();original=self.api.deposit
        def changed():
            d=original()
            if self.api.submitted:d['metadata']['relations']={}
            return d
        with patch.object(self.api,'deposit',changed):
            with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
            before=len(self.writes());self.assertEqual(before,1)
            with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
            with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
            with self.assertRaises(m.Stop):self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
            self.assertEqual(len(self.writes()),before)

    def test_independent_unknown_publish_not_applied_and_stale_get_never_retries(self):
        self.recover();self.api.fail=('zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish');self.api.applied_before_error=False
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        state_before=self.state.read_bytes();self.api.fail=None;count=len(self.writes())
        r=self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(r['status'],'draft_observed_publication_unconfirmed');self.assertEqual(self.state.read_bytes(),state_before)
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),count)

    def test_independent_unknown_append_not_applied_get_absence_no_retry(self):
        self.publish();self.api.fail=('sheet','append');self.api.applied_before_error=False
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        state_before=self.state.read_bytes();self.api.fail=None;count=len(self.writes())
        r=self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(r['status'],'publication_verified_tracker_absent_observed');self.assertEqual(self.state.read_bytes(),state_before)
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),count)

    def test_independent_postpublish_hash_corruption_does_not_promote_phase(self):
        self.recover();self.api.hash_change=True
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        j=json.loads(self.state.read_bytes());self.assertEqual(j['phase'],'intent_recorded');self.assertTrue(j['publish_intent'])
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),1)

    def test_independent_append_call_options_exact_under_active_phase(self):
        self.publish();e=self.engine();e.read_state(m.SPEC_SHA);e._active_phase='tracker';e.state['append_intent']=True
        params={'spreadsheetId':m.v1.SHEET,'range':m.v1.TAB+'A:D','valueInputOption':'RAW','insertDataOption':'INSERT_ROWS',
                'includeValuesInResponse':True,'responseValueRenderOption':'UNFORMATTED_VALUE'}
        row=[self.spec['tracker']['original_problem'],self.spec['tracker']['solution_chat'],f'https://doi.org/10.5281/zenodo.{m.ID}',self.spec['tracker']['notes']]
        for delta in ({'range':m.v1.TAB+'A2:D2'},{'valueInputOption':'USER_ENTERED'},{'insertDataOption':'OVERWRITE'},
                      {'includeValuesInResponse':1},{'responseValueRenderOption':'FORMATTED_VALUE'},{'spreadsheetId':'foreign'}):
            self.call_stops_without_transport(e,'sheet','append',{**params,**delta},{'majorDimension':'ROWS','values':[row]},write=True)
        for bad in ([row+['fifth']], [row,row], [[*row[:3],'changed note']]):
            self.call_stops_without_transport(e,'sheet','append',params,{'majorDimension':'ROWS','values':bad},write=True)


    def test_independent_schema_type_rejection_is_local_and_side_effect_free(self):
        good=copy.deepcopy(self.spec)
        variants=[]
        for key,bad in (("schema",True),("assets",{}),("metadata",[]),("tracker",{})):
            d=copy.deepcopy(good);d[key]=bad;variants.append(d)
        for key,bad in (("size",True),("sha256","0"*63),("md5",7),("name","../foreign"),("mode","120000")):
            d=copy.deepcopy(good);d["assets"][0][key]=bad;variants.append(d)
        for key,bad in (("title",True),("creators",[]),("keywords",[7]),("access_right","restricted")):
            d=copy.deepcopy(good);d["metadata"][key]=bad;variants.append(d)
        e=self.engine()
        for d in variants:
            with self.assertRaises((m.Stop,TypeError)):e.validate_spec(d)
        self.assertFalse(self.api.calls);self.assertFalse(self.state.exists())

    def test_independent_local_lock_and_private_path_boundary(self):
        with m.local_lock():
            with self.assertRaises(m.Stop):
                with m.local_lock():pass
        for p in (self.tmp/'state.json',m.PRIVATE,self.priv/'..'/'escape'):
            with self.assertRaises(m.Stop):m.Admin(self.api,self.priv/'outside_evidence',p)
        symlink=self.priv/'source_link.json';symlink.symlink_to(self.source)
        with self.assertRaises(m.Stop):m.g.read_regular(symlink,private=True)
        self.assertFalse(self.api.calls)

    def test_independent_native_bool_fields_are_not_truthy_coercions(self):
        original=self.api.native_record
        for field in ('is_draft','is_published'):
            def fault():
                n=original();n[field]=int(n[field]);return n
            with patch.object(self.api,'native_record',fault):
                with self.assertRaises(m.Stop):self.recover()
            self.assertFalse(self.state.exists())
        def fault():
            n=original();n['files']['entries']['preprint.pdf']['access']['hidden']=0;return n
        with patch.object(self.api,'native_record',fault):
            with self.assertRaises(m.Stop):self.recover()
        self.assertFalse(self.state.exists());self.assertFalse(self.writes())


class ActualOpaqueReplay(unittest.TestCase):
    def test_independent_actual_three_get_replay_byte_pins_original_immutable(self):
        originals={p:m.g.read_regular(p,private=True)[0] for p in (m.ORIGINAL_STATE,m.STATE_COPY,m.ROOT_ACCEPTANCE,m.ROOT_SNAPSHOT)}
        self.assertEqual(m.sha(originals[m.ORIGINAL_STATE]),m.ORIGINAL_STATE_SHA)
        self.assertEqual(originals[m.ORIGINAL_STATE],originals[m.STATE_COPY]);self.assertEqual(m.sha(originals[m.ROOT_SNAPSHOT]),m.ROOT_SNAPSHOT_SHA)
        class Replay:
            def __init__(self):self.calls=[]
            def zenodo(self,method,ep,*args,**kwargs):
                self.calls.append((method,ep));assert method=='GET'
                name='0002_response.json' if ep.endswith('/files') else '0001_response.json' if '/records/' in ep else '0000_response.json'
                return json.loads(m.g.read_regular(m.ROOT_SNAPSHOT.parent/name,private=True)[0])
        with patch.object(m,'PRIVATE',PRIVATE),tempfile.TemporaryDirectory(prefix='actual_opaque_',dir=PRIVATE) as directory:
            root=Path(directory);api=Replay();e=m.Admin(api,root/'evidence',root/'ephemeral_state.json')
            adoption=PUBLIC_PARENT/'PROPOSED_RECOVERY_ADOPTION.json';approval=m.sha(m.g.read_regular(adoption)[0])
            r=e.recover(adoption,approval,m.SPEC_SHA,m.ROOT_SNAPSHOT_SHA)
            self.assertEqual(r['status'],'existing_stage_get_verified_adopted');self.assertEqual(e.kind,'offline_model');self.assertEqual(len(api.calls),3)
            saved=json.loads((root/'ephemeral_state.json').read_bytes())
            self.assertEqual(m.g.read_regular(saved['native_snapshot_path'],private=True)[0],originals[m.ROOT_SNAPSHOT])
        for p,raw in originals.items():self.assertEqual(m.g.read_regular(p,private=True)[0],raw)


if __name__=='__main__': unittest.main(verbosity=2)
