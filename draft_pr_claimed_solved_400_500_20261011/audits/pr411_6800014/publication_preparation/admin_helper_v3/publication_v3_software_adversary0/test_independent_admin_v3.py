"""Independent bounded administrative review; captured root DTOs, fake Sheet, API calls zero."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CASE = HERE.parents[2]
PRIVATE = CASE / 'private_sources/publication_admin_helper_v3/publication_v3_software_adversary0'
spec = importlib.util.spec_from_file_location('baseline_fixture', HERE.parent/'test_publication_admin_v3.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
m = t.m


class Review(t.Tests):
    """Reuse actual captured DTO replay; override all inherited test custody."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='independent_offline_', dir=PRIVATE)
        self.tmp=Path(self.temp.name); self.state=self.tmp/'MODEL_STATE.json'; self.api=t.Replay(); self.counter=0
        self.adoption=m.HERE/'PROPOSED_RECOVERY_ADOPTION.json'; self.digest=m.sha(m.g.read_regular(self.adoption)[0])
        self.original_v2_sha=m.sha(m.g.read_regular(m.V2_STATE,private=True)[0])
        self.original_v1_sha=m.sha(m.g.read_regular(m.v2.ORIGINAL_STATE,private=True)[0])

    def tearDown(self):
        self.assertEqual(m.sha(m.g.read_regular(m.v2.ORIGINAL_STATE,private=True)[0]),self.original_v1_sha)
        super().tearDown()

    def attack(self,name,fn):
        self.api.changes={name:fn}
        with self.assertRaises(m.Stop): self.recover()
        self.assertFalse(self.state.exists()); self.assertFalse(self.writes())

    def test_routes_under_v3_and_v2_dispatch_default_and_true(self):
        self.recover();e=self.engine();e.read_state(m.SPEC_SHA)
        operations=['POST /api/deposit/depositions',f'POST /api/deposit/depositions/{m.ID}/actions/publish',
                    f'PUT /api/deposit/depositions/{m.ID}',f'DELETE /api/deposit/depositions/{m.ID}','PUT /api/files/a/file']
        before=len(self.api.calls)
        for request in (e.request,lambda *a,**kw:m.v2.Admin.request(e,*a,**kw)):
            for op in operations:
                for flag in (False,True):
                    with self.assertRaises(m.Stop):request('zenodo',op,write=flag)
        for publish in (e.publish,lambda *a:m.v2.Admin.publish(e,*a),lambda *a:m.v1.Admin.publish(e,*a)):
            with self.assertRaises(m.Stop):publish(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.assertEqual(len(self.api.calls),before);self.assertFalse(self.writes())

    def test_v1_base_dispatch_cannot_send_zenodo_mutations(self):
        e=self.engine();before=len(self.api.calls)
        with self.assertRaises(m.Stop):m.v1.Admin.request(e,'zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish')
        self.assertEqual(len(self.api.calls),before,'base dispatcher reached backend POST')

    def test_v1_base_dispatch_cannot_send_unphased_wrong_sheet_append(self):
        e=self.engine();before=len(self.api.calls)
        with self.assertRaises(m.Stop):m.v1.Admin.request(e,'sheet','append',{'spreadsheetId':'wrong','range':'Other!A:D'},
                                                       {'values':[['wrong']*4]})
        self.assertEqual(len(self.api.calls),before,'base dispatcher reached backend append')

    def test_mutation_write_type_and_file_flags(self):
        e=self.engine()
        for flag in (0,1,None,'true'):
            with self.assertRaises(m.Stop):e.request('zenodo',f'GET /api/deposit/depositions/{m.ID}',write=flag)
        with self.assertRaises(m.Stop):e.request('zenodo',f'GET /api/deposit/depositions/{m.ID}',file=self.tmp/'never_read')
        self.assertFalse(self.api.calls)

    def test_exact_public_snapshot_false_is_not_integer_zero(self):
        self.attack('0004_response.json',lambda d:d['access']['embargo'].update(active=0))

    def test_public_projection_rejects_additional_access_and_custom_fields(self):
        self.attack('0004_response.json',lambda d:d['access'].update(evil=True))
        self.attack('0004_response.json',lambda d:d['custom_fields'].update(evil=True))

    def test_private_parent_public_projection_rejects_all_unobserved_omissions(self):
        self.attack('0004_response.json',lambda d:d['parent']['access'].pop('settings'))
        self.attack('0004_response.json',lambda d:d['parent']['access'].update(links=[]))
        self.attack('0004_response.json',lambda d:d['parent']['access']['settings'].update(allow_user_requests=0))

    def test_exact_auth_version_and_acl_types(self):
        self.attack('0001_response.json',lambda d:d['versions'].update(index=True))
        self.attack('0001_response.json',lambda d:d['versions'].update(is_latest=1))
        self.attack('0001_response.json',lambda d:d['parent']['access'].update(links=['nonempty']))

    def test_native_file_visibility_completion_identity_and_count(self):
        self.attack('0001_response.json',lambda d:d['files'].update(enabled=1))
        self.attack('0001_response.json',lambda d:next(iter(d['files']['entries'].values()))['access'].update(hidden=0))
        self.attack('0004_response.json',lambda d:next(iter(d['files']['entries'].values())).update(key='wrong'))
        self.attack('0002_response.json',lambda d:d['entries'][0].update(status='failed'))

    def test_public_hash_status_url_md5_size_and_sha(self):
        for delta in ({'http_status':302},{'url':'https://example.invalid/content'},{'md5':'0'*32},{'size':0},{'sha256':'0'*64}):
            self.attack('hash',lambda d,delta=delta:d.update(delta))

    def test_doi_and_native_flags_and_relation_types(self):
        self.attack('0000_response.json',lambda d:d.update(doi='10.5281/zenodo.1'))
        self.attack('0004_response.json',lambda d:d.update(is_published=1))
        self.attack('0004_response.json',lambda d:d.update(is_draft=0))
        self.attack('0003_response.json',lambda d:d['metadata']['relations']['version'][0].update(index=False))

    def test_copied_native_bytes_and_revision_binding(self):
        self.recover();j=json.loads(self.state.read_text());copy_path=Path(j['native_snapshot_path'])
        copy_path.write_bytes(copy_path.read_bytes()+b' ')
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.assertFalse(self.writes())
        self.state.write_text(json.dumps({**j,'revision':2}))
        with self.assertRaises(m.Stop):self.engine().read_state(m.SPEC_SHA)

    def test_state_spec_and_native_and_adoption_pins(self):
        self.recover();original=json.loads(self.state.read_text())
        for key,value in (('spec_sha256','0'*64),('v2_helper_sha256','0'*64),('native_snapshot_sha256','0'*64)):
            altered=copy.deepcopy(original);altered[key]=value;self.state.write_text(json.dumps(altered))
            with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.assertFalse(self.writes())

    def test_symlink_state_and_custody_destinations_rejected(self):
        target=self.tmp/'target';target.write_text('{}');link=self.tmp/'alias';link.symlink_to(target)
        with self.assertRaises(m.Stop):m.Admin(self.api,self.tmp/'new',link)
        for wrong in (m.V2_STATE,m.v2.ORIGINAL_STATE,m.MAPPING):
            with self.assertRaises(m.Stop):m.Admin(self.api,self.tmp/'new2',wrong)
        self.assertFalse(self.api.calls)

    def test_unphased_append_cannot_use_exact_payload(self):
        self.recover();e=self.engine();j=e.read_state(m.SPEC_SHA);row=[j['spec']['tracker']['original_problem'],j['spec']['tracker']['solution_chat'],j['publication']['doi_url'],j['spec']['tracker']['notes']]
        params={'spreadsheetId':m.v1.SHEET,'range':m.v1.TAB+'A:D','valueInputOption':'RAW','insertDataOption':'INSERT_ROWS',
                'includeValuesInResponse':True,'responseValueRenderOption':'UNFORMATTED_VALUE'}
        with self.assertRaises(m.Stop):e.request('sheet','append',params,{'majorDimension':'ROWS','values':[row]},write=True)
        self.assertFalse(self.writes())

    def test_exact_fixed_append_payload_and_one_durable_intent(self):
        self.recover();e=self.engine();r=e.tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA);self.assertEqual(r['status'],'tracker_verified')
        calls=self.writes();self.assertEqual(len(calls),1);call=calls[0]
        self.assertEqual(call[2]['spreadsheetId'],m.v1.SHEET);self.assertEqual(call[2]['range'],m.v1.TAB+'A:D')
        j=json.loads(self.state.read_text());self.assertEqual(len(j['intents']),1);self.assertTrue(j['append_intent'])
        self.assertEqual(call[3],{'majorDimension':'ROWS','values':[[j['spec']['tracker']['original_problem'],j['spec']['tracker']['solution_chat'],j['publication']['doi_url'],j['spec']['tracker']['notes']]]})
        before=len(calls);self.engine().reconcile(m.SPEC_SHA,native_approval=m.NATIVE_SHA);self.assertEqual(len(self.writes()),before)

    def test_existing_exact_doi_row_prevents_append(self):
        self.recover();j=json.loads(self.state.read_text());self.api.rows[2]=[j['spec']['tracker']['original_problem'],j['spec']['tracker']['solution_chat'],j['publication']['doi_url'],j['spec']['tracker']['notes']]
        self.assertEqual(self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)['status'],'tracker_already_exact');self.assertFalse(self.writes())

    def test_duplicate_doi_and_wrong_existing_row_prevent_append(self):
        self.recover();j=json.loads(self.state.read_text());row=[j['spec']['tracker']['original_problem'],j['spec']['tracker']['solution_chat'],j['publication']['doi_url'],j['spec']['tracker']['notes']]
        self.api.rows[2]=row;self.api.rows[3]=row
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        del self.api.rows[3];self.api.rows[2]=['wrong',*row[1:]]
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.assertFalse(self.writes())

    def test_reconcile_leaves_durable_state_unchanged_and_uses_get_only(self):
        self.recover();before=self.state.read_bytes();r=self.engine().reconcile(m.SPEC_SHA,native_approval=m.NATIVE_SHA)
        self.assertEqual(r['status'],'publication_verified_tracker_absent_observed');self.assertEqual(self.state.read_bytes(),before)
        self.assertFalse(self.writes());self.assertTrue(all(c[1] in ('GET','get','batchGet') for c in self.api.calls))


if __name__=='__main__':unittest.main(verbosity=2)
