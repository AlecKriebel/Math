"""Independent synthetic attacks. All fixtures and evidence stay in review custody."""
import copy
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[2]
PRIVATE = CASE / "private_sources/publication_admin_helper_v2/publication_v2_software_adversary0"
spec = importlib.util.spec_from_file_location("parent_tests", HERE.parent / "test_publication_admin_v2.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
m = t.m

class ReviewTests(t.V2Tests):
    def setUp(self):
        self.review_roots = [patch.object(m, "HERE", HERE), patch.object(m, "PRIVATE", PRIVATE)]
        for item in self.review_roots: item.start()
        try: super().setUp()
        except Exception:
            for item in reversed(self.review_roots): item.stop()
            raise
    def tearDown(self):
        try: super().tearDown()
        finally:
            for item in reversed(self.review_roots): item.stop()

    def test_mutation_cannot_disguise_as_read_by_omitting_write_flag(self):
        e=self.engine()
        with self.assertRaises(m.Stop):
            e.request("zenodo", "POST /api/deposit/depositions", payload={"metadata": self.spec["metadata"]})
        self.assertFalse(self.api.calls)
        self.assertFalse(self.state.exists())

    def test_append_low_level_rejects_other_sheet_or_unapproved_cells(self):
        self.recover();e=self.engine();e.read_state(m.SPEC_SHA)
        params={"spreadsheetId": "other spreadsheet", "range": "Other!A:D", "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"}
        payload={"majorDimension": "ROWS", "values": [["arbitrary", "other", "10.5281/zenodo.999", "cells"]]}
        before=len(self.writes())
        with self.assertRaises(m.Stop):e.request("sheet", "append", params, payload, write=True)
        self.assertEqual(len(self.writes()),before)

    def test_low_level_publish_requires_protocol_intent_and_native_approval(self):
        self.recover();e=self.engine();e.read_state(m.SPEC_SHA)
        before=len(self.writes())
        with self.assertRaises(m.Stop):e.request("zenodo",f"POST /api/deposit/depositions/{m.ID}/actions/publish",write=True)
        self.assertEqual(len(self.writes()),before)

    def test_generated_relations_unobserved_shape_cannot_be_assumed(self):
        self.recover();e=self.engine();e.read_state(m.SPEC_SHA)
        d=self.api.deposit();d["metadata"]["relations"]={"version": [{"index":0,"is_last":False,
           "parent":{"pid_type":"recid","pid_value":e.contract["concept_id"]}}]}
        with self.assertRaises(m.Stop):e.legacy(d,self.spec,m.ID)

    def test_missing_or_bad_native_completed_visibility_or_concept_stops(self):
        old=self.api.zenodo
        variants=("native_enabled", "native_count", "native_hidden", "native_key", "listing_enabled", "listing_hidden", "listing_status", "parent")
        for variant in variants:
            def mutated(method,ep,*args,**kwargs):
                value=old(method,ep,*args,**kwargs)
                if ep.endswith("/files"):
                    if variant=="listing_enabled":value["enabled"]=False
                    if variant=="listing_hidden":value["entries"][0]["access"]["hidden"]=True
                    if variant=="listing_status":value["entries"][0]["status"]="pending"
                elif "/records/" in ep:
                    if variant=="native_enabled":value["files"]["enabled"]=False
                    if variant=="native_count":value["files"]["count"]=4
                    if variant=="native_hidden":next(iter(value["files"]["entries"].values()))["access"]["hidden"]=True
                    if variant=="native_key":next(iter(value["files"]["entries"].values()))["key"]="wrong"
                    if variant=="parent":value["parent"]["id"]="wrong"
                return value
            with self.subTest(variant=variant),patch.object(self.api,"zenodo",mutated):
                with self.assertRaises((m.Stop,m.z.DepositError)):self.recover()
            self.assertFalse(self.state.exists());self.assertFalse(self.writes())

    def test_wrong_generated_doi_and_editable_extra_stop(self):
        self.recover();e=self.engine();e.read_state(m.SPEC_SHA)
        for variation in ("top_doi", "reserved_doi", "reserved_id", "editable_extra", "publisher_missing", "publisher_other"):
            d=self.api.deposit()
            if variation=="top_doi":d["doi"]="10.5281/zenodo.999"
            if variation=="reserved_doi":d["metadata"]["prereserve_doi"]["doi"]="10.5281/zenodo.999"
            if variation=="reserved_id":d["metadata"]["prereserve_doi"]["recid"]="999"
            if variation=="editable_extra":d["metadata"]["unrequested_editable"]="extra"
            if variation=="publisher_missing":del d["metadata"]["imprint_publisher"]
            if variation=="publisher_other":d["metadata"]["imprint_publisher"]="Other"
            with self.subTest(variation=variation):
                with self.assertRaises(m.Stop):e.legacy(d,self.spec,m.ID)
        self.assertFalse(self.writes())

    def test_wrong_returned_append_row_and_duplicate_doi_stops(self):
        self.publish();self.api.returned_range="Other!A2:D2"
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),2)
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),2)

    def test_unknown_publish_not_applied_remains_get_only_no_retry(self):
        self.recover();self.api.fail=("zenodo",f"POST /api/deposit/depositions/{m.ID}/actions/publish")
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.api.fail=None;before=len(self.writes())
        self.assertEqual(self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)["status"],"draft_observed_publication_unconfirmed")
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_doi_column_holes_exact_existing_and_duplicate_rows(self):
        self.publish();doi=f"10.5281/zenodo.{m.ID}"
        row=[self.spec["tracker"]["original_problem"],self.spec["tracker"]["solution_chat"],"https://doi.org/"+doi,self.spec["tracker"]["notes"]]
        self.api.rows[7]=row[:];e=self.engine()
        self.assertEqual(e.doi_rows(doi),[7]);before=len(self.writes())
        self.assertEqual(e.tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)["status"],"tracker_already_exact")
        self.assertEqual(len(self.writes()),before)
        self.api.rows[12]=row[:]
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_unknown_append_not_applied_no_second_append_or_state_rewrite(self):
        self.publish();self.api.fail=("sheet","append")
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.api.fail=None;before=len(self.writes());state_before=self.state.read_bytes()
        result=self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(result["status"],"publication_verified_tracker_absent_observed")
        self.assertEqual(self.state.read_bytes(),state_before)
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_native_accepted_copy_tamper_blocks_publish_before_mutation(self):
        self.recover();j=json.loads(self.state.read_bytes());snapshot=Path(j["native_snapshot_path"])
        snapshot.write_bytes(b"tampered accepted snapshot")
        before=len(self.writes())
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_positive_dispatch_rejects_unknown_services_targets_and_types(self):
        e=self.engine()
        cases=[("zenodo","GET /api/deposit/depositions/1",None,None,None,False),
               ("zenodo",f"GET /api/deposit/depositions/{m.ID}",{},None,None,False),
               ("zenodo",f"POST /api/deposit/depositions/{m.ID}/actions/publish",None,None,None,False),
               ("sheet","append",{},None,None,False),
               ("sheet","update",{},None,None,False),
               ("sheet","get",{"spreadsheetId":"other","fields":"spreadsheetId,sheets.properties"},None,None,False),
               ("public_json","GET",{"id":m.ID,"native":"true"},None,None,False),
               ("public_json","GET",{"id":m.ID+1,"native":False},None,None,False),
               ("public_hash","GET",{"id":m.ID,"name":"unapproved.bin"},None,None,False),
               ("arbitrary","GET",None,None,None,False),
               ("zenodo",f"GET /api/deposit/depositions/{m.ID}",None,None,None,1),
               ("zenodo",f"GET /api/deposit/depositions/{m.ID}",None,None,self.tmp/"opaque.bin",False)]
        for service,operation,params,payload,file,write in cases:
            with self.subTest(service=service,operation=operation,params=params):
                with self.assertRaises(m.Stop):e.request(service,operation,params,payload,file,write)
        self.assertFalse(self.api.calls);self.assertFalse(self.state.exists())

    def test_active_tracker_wrong_target_options_or_cells_still_stop(self):
        self.publish();e=self.engine();j=e.read_state(m.SPEC_SHA);e._active_phase="tracker";j["append_intent"]=True
        p={"spreadsheetId":m.v1.SHEET,"range":m.v1.TAB+"A:D","valueInputOption":"RAW","insertDataOption":"INSERT_ROWS",
           "includeValuesInResponse":True,"responseValueRenderOption":"UNFORMATTED_VALUE"}
        payload={"majorDimension":"ROWS","values":[[self.spec["tracker"]["original_problem"],self.spec["tracker"]["solution_chat"],
                  f"https://doi.org/10.5281/zenodo.{m.ID}",self.spec["tracker"]["notes"]]]}
        before=len(self.writes())
        for key,wrong in (("spreadsheetId","other"),("range","Other!A:D"),("valueInputOption","USER_ENTERED"),
                          ("insertDataOption","OVERWRITE"),("includeValuesInResponse",1),("responseValueRenderOption","FORMATTED_VALUE")):
            variant=copy.deepcopy(p);variant[key]=wrong
            with self.subTest(key=key):
                with self.assertRaises(m.Stop):e.request("sheet","append",variant,payload,write=True)
        for index in range(4):
            variant=copy.deepcopy(payload);variant["values"][0][index]="unapproved cell"
            with self.subTest(cell=index):
                with self.assertRaises(m.Stop):e.request("sheet","append",p,variant,write=True)
        self.assertEqual(len(self.writes()),before)

class ActualCustodyReplay(unittest.TestCase):
    def test_actual_administrative_custody_replay_keeps_native_label_offline(self):
        class Replay:
            def __init__(self):self.calls=[]
            def zenodo(self,method,endpoint,*args,**kwargs):
                self.calls.append((method,endpoint))
                if method != "GET":raise AssertionError("Actual replay permits GET only")
                root=m.ROOT_SNAPSHOT.parent
                name="0002_response.json" if endpoint.endswith("/files") else "0001_response.json" if "/records/" in endpoint else "0000_response.json"
                return json.loads(m.g.read_regular(root/name,private=True)[0])
        PRIVATE.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="actual_replay_",dir=PRIVATE) as directory,patch.object(m,"PRIVATE",PRIVATE):
            d=Path(directory);api=Replay();e=m.Admin(api,d/"evidence",d/"temporary_state.json")
            adoption=HERE.parent/"PROPOSED_RECOVERY_ADOPTION.json";digest=m.sha(m.g.read_regular(adoption)[0])
            before=m.g.read_regular(m.ORIGINAL_STATE,private=True)[0]
            result=e.recover(adoption,digest,m.SPEC_SHA,m.ROOT_SNAPSHOT_SHA)
            self.assertEqual(result["status"],"existing_stage_get_verified_adopted")
            self.assertEqual(api.calls,[("GET",f"/api/deposit/depositions/{m.ID}"),("GET",f"/api/records/{m.ID}/draft"),("GET",f"/api/records/{m.ID}/draft/files")])
            self.assertEqual(e.kind,"offline_model")
            self.assertEqual(m.g.read_regular(m.ORIGINAL_STATE,private=True)[0],before)

if __name__=="__main__":unittest.main(verbosity=2)
