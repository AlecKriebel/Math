#!/usr/bin/env python3
"""Fresh PR411 administration-only adversarial tests; all service calls modeled.

Raw metadata fixtures and all state/evidence outputs stay in this reviewer's
private directory. No Production transport is instantiated. No asset is read.
"""
import base64
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import traceback
import unittest
import uuid

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[2]
PRIVATE = CASE / "private_sources/publication_admin_helper_v3/publication_v3_software_adversary1"
SOURCE = HERE.parent / "publication_admin_v3.py"
REVIEWED = "536844c63eedf31934e686d44a32c3e8564ba9aaa9c078f204ffe5488bfdea53"
ADOPTION = HERE.parent / "PROPOSED_RECOVERY_ADOPTION.json"
ADOPTION_SHA = "8edb48b705627c97e6390e05e63879924920fb2d1d590e83a61d18542f44155b"
raw = (PRIVATE / "REVIEWED_536.py").read_bytes()
assert hashlib.sha256(raw).hexdigest() == REVIEWED
spec = importlib.util.spec_from_file_location("independent_v3", SOURCE)
v = importlib.util.module_from_spec(spec)
exec(compile(raw, str(SOURCE), "exec"), v.__dict__)
v.PRIVATE = PRIVATE
RUN = PRIVATE / ("tests_" + uuid.uuid4().hex)
RUN.mkdir()
FIX = v.MAPPING_DIR
fixtures = {i: json.loads((FIX / f"{i:04d}_response.json").read_bytes()) for i in range(8)}
native_receipts = {i: json.loads((FIX / f"{i:04d}_native.json").read_bytes()) for i in (3, 4)}
originals = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (v.v2.ORIGINAL_STATE, v.V2_STATE)}

class Model:
    def __init__(self):
        self.data = copy.deepcopy(fixtures)
        self.calls, self.rows = [], []
        self.last_native = None
        self.append_mode = "normal"
        self.header = v.v1.HEADERS[:]
        self.gid, self.title = v.v1.GID, v.v1.TITLE
        self.bad_return = False
        self.readback_bad = False
        self.before_remote = None
    def zenodo(self, method, endpoint, payload=None, file=None, **params):
        self.calls.append(("zenodo", method, endpoint))
        assert method == "GET" and payload is None and file is None
        self.last_native = None
        i = 0 if endpoint.startswith("/api/deposit/") else 2 if endpoint.endswith("/files") else 1
        return copy.deepcopy(self.data[i])
    def public_json(self, record_id, native=False):
        self.calls.append(("public_json", "GET", native))
        self.last_native = copy.deepcopy(native_receipts[4 if native else 3])
        return copy.deepcopy(self.data[4 if native else 3])
    def public_hash(self, record_id, name):
        self.calls.append(("public_hash", "GET", name))
        # Matches pinned Production a425 line174: no download native decoration.
        self.last_native = None
        for i in (5, 6, 7):
            d = self.data[i]
            if d["url"].endswith("/" + v.v1.quote(name, safe="") + "/content"):
                return copy.deepcopy(d)
        raise AssertionError("unknown positive asset identifier")
    def sheet(self, method, params, payload=None):
        self.calls.append(("sheet", method, copy.deepcopy(params)))
        self.last_native = None
        if method == "get":
            return {"spreadsheetId": v.v1.SHEET, "sheets": [{"properties": {"sheetId": self.gid, "title": self.title}}]}
        if method == "batchGet":
            out = []
            for rr in params["ranges"]:
                cr = v.v1.canonical_range(rr)
                if cr == "A1:D1": values = [self.header]
                elif cr == "C2:C": values = [[r[2]] for r in self.rows]
                else:
                    row = int(cr.split(":")[0][1:]) - 2
                    values = [copy.deepcopy(self.rows[row])] if row < len(self.rows) else []
                    if self.readback_bad and values: values[0][0] = "tampered"
                out.append({"range": rr, "majorDimension": "ROWS", "values": values})
            return {"spreadsheetId": v.v1.SHEET, "valueRanges": out}
        assert method == "append"
        if self.before_remote: self.before_remote()
        if self.append_mode == "before":
            self.last_native = {"service":"gws","method":"append","returncode":None,"stdout_base64":"","stderr_base64":base64.b64encode(b"modeled native timeout").decode()}
            raise TimeoutError("offline timeout before modeled commit")
        self.rows.extend(copy.deepcopy(payload["values"]))
        if self.append_mode == "after":
            self.last_native = {"service":"gws","method":"append","returncode":None,"stdout_base64":"","stderr_base64":base64.b64encode(b"modeled native timeout").decode()}
            raise TimeoutError("offline timeout after modeled commit")
        rr = v.v1.TAB + f"A{len(self.rows)+1}:D{len(self.rows)+1}"
        if self.bad_return: rr = "'Wrong'!A2:D2"
        return {"spreadsheetId": v.v1.SHEET, "updates": {"spreadsheetId": v.v1.SHEET, "updatedRows": 1, "updatedColumns": 4, "updatedCells": 4, "updatedRange": rr, "updatedData": {"values": copy.deepcopy(payload["values"])}}}

class Review(unittest.TestCase):
    def engine(self, model=None, recover=True):
        model = model or Model()
        d = RUN / uuid.uuid4().hex
        e = v.Admin(model, d / "evidence", d / "state.json")
        if recover: e.recover(ADOPTION, ADOPTION_SHA, v.SPEC_SHA, v.NATIVE_SHA)
        return e, model
    def published(self, model):
        e, model = self.engine(model, False)
        original = e.load_adoption(ADOPTION, ADOPTION_SHA)
        e.state = original
        snapshot = json.loads(v.v2.ROOT_SNAPSHOT.read_bytes())
        return e.published(original["spec"], v.ID, snapshot)
    def reject_model(self, mutate):
        m = Model(); mutate(m)
        with self.assertRaises(Exception): self.published(m)
        self.assertFalse(any(x[1] in ("POST", "PUT", "append") for x in m.calls))
    def row(self, e):
        t = e.state["spec"]["tracker"]
        return [t["original_problem"], t["solution_chat"], v.DOI and "https://doi.org/" + v.DOI, t["notes"]]
    def append_args(self, e):
        return {"spreadsheetId": v.v1.SHEET, "range": v.v1.TAB + "A:D", "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS", "includeValuesInResponse": True, "responseValueRenderOption": "UNFORMATTED_VALUE"}, {"majorDimension": "ROWS", "values": [self.row(e)]}
    def guard_ready(self):
        e, m = self.engine(); e._active_phase = "tracker";e.state["append_intent"] = True
        return e, m
    def test_01_actual_shape_recovery(self):
        e, m = self.engine()
        self.assertEqual(e.state["phase"], "published_verified")
        self.assertEqual(e.state["revision"], 3)
        self.assertEqual(len(m.calls), 8)
        self.assertTrue(all(c[1] == "GET" for c in m.calls))
        self.assertFalse(e.state["append_intent"])
        self.assertTrue(e.state["publish_intent"])
        self.assertEqual(e.state["intents"], [])
    def test_02_positive_source_seals(self):
        e, m = self.engine(recover=False)
        e.load_adoption(ADOPTION, ADOPTION_SHA)
        self.assertEqual(m.calls, [])
        self.assertEqual(hashlib.sha256((CASE / "publication_preparation/ROOT_ACTUAL_PUBLICATION_RESPONSE_TYPES.json").read_bytes()).hexdigest(), "d4f56a5b66c19bf7a3190604b89f3980e5070b20e59d840141207a8b4c0cdbd8")
        self.assertEqual(e.contract["concept_id"], "23331231")
    def test_03_wrong_recovery_approvals(self):
        for index in (0,1,2):
            e, m = self.engine(recover=False); args = [ADOPTION_SHA,v.SPEC_SHA,v.NATIVE_SHA];args[index] = "0"*64
            with self.assertRaises(Exception): e.recover(ADOPTION,*args)
            self.assertEqual(m.calls, [])
        e, m = self.engine()
        with self.assertRaises(v.Stop): e.recover(ADOPTION,ADOPTION_SHA,v.SPEC_SHA,v.NATIVE_SHA)
    def test_04_stage_and_publish_unavailable(self):
        e,m=self.engine()
        for fn in (e.stage,e.publish):
            with self.assertRaises(v.Stop): fn(None,None,None)
        self.assertEqual(len(m.calls),8)
    def test_05_zenodo_write_and_target_denied(self):
        e,m=self.engine()
        for op in ("POST /api/deposit/depositions",f"POST /api/deposit/depositions/{v.ID}/actions/publish",f"PUT /api/deposit/depositions/{v.ID}","GET /api/records/1"):
            with self.assertRaises(v.Stop): e.request("zenodo",op,write=op.startswith(("POST","PUT")))
        self.assertEqual(len(m.calls),8)
    def test_06_explicit_inherited_dispatch_denied(self):
        for cls in (v.v1.Admin,v.v2.Admin):
            for svc,op,params,payload in (("zenodo",f"POST /api/deposit/depositions/{v.ID}/actions/publish",None,None),("sheet","append",{},{})):
                e,m=self.guard_ready()
                with self.assertRaises(v.Stop): cls.request(e,svc,op,params,payload,write=True)
                self.assertEqual(len(m.calls),8)
    def test_07_transport_grant_exact_and_onecall(self):
        e,m=self.engine()
        with self.assertRaises(v.Stop): e.api.zenodo("GET",f"/api/deposit/depositions/{v.ID}")
        exact=["zenodo",f"GET /api/deposit/depositions/{v.ID}",None,None,None]
        e._dispatch_grant=v.encoded(exact)
        with self.assertRaises(v.Stop): e.api.zenodo("GET","/api/records/1")
        e.api.zenodo("GET",f"/api/deposit/depositions/{v.ID}")
        with self.assertRaises(v.Stop): e.api.zenodo("GET",f"/api/deposit/depositions/{v.ID}")
        self.assertEqual(len(m.calls),9)
    def test_08_sheet_dispatch_requires_mutation_mark(self):
        e,m=self.guard_ready();p,b=self.append_args(e)
        for op,write in (("append",False),("update",True),("clear",True)):
            with self.assertRaises(v.Stop): e.request("sheet",op,p,b,write=write)
        self.assertEqual(len(m.calls),8)
    def test_09_exact_sheet_target_options(self):
        for key,value in (("spreadsheetId","wrong"),("range","'Wrong'!A:D"),("valueInputOption","USER_ENTERED"),("insertDataOption","OVERWRITE"),("includeValuesInResponse",False)):
            e,m=self.guard_ready();p,b=self.append_args(e);p[key]=value
            with self.assertRaises(v.Stop): e.request("sheet","append",p,b,write=True)
            self.assertEqual(len(m.calls),8)
    def test_10_exact_sheet_payload(self):
        for cell in range(4):
            e,m=self.guard_ready();p,b=self.append_args(e);b["values"][0][cell]="altered"
            with self.assertRaises(v.Stop): e.request("sheet","append",p,b,write=True)
            self.assertEqual(len(m.calls),8)
    def test_11_append_phase_binding(self):
        for key,value in (("phase","unknown_write"),("append_intent",False),("approved_native_sha256","0"*64)):
            e,m=self.guard_ready();p,b=self.append_args(e);e.state[key]=value
            with self.assertRaises(v.Stop): e.request("sheet","append",p,b,write=True)
            self.assertEqual(len(m.calls),8)
        e,m=self.guard_ready();e._active_phase=None;p,b=self.append_args(e)
        with self.assertRaises(v.Stop): e.request("sheet","append",p,b,write=True)
    def test_12_auth_requested_exact12(self):
        self.reject_model(lambda m:m.data[0]["metadata"].update(title="altered"))
        self.reject_model(lambda m:m.data[0]["metadata"].update(extra="injected"))
    def test_13_auth_publisher_and_reservation_types(self):
        self.reject_model(lambda m:m.data[0]["metadata"].update(imprint_publisher="Other"))
        self.reject_model(lambda m:m.data[0]["metadata"]["prereserve_doi"].update(recid=str(v.ID)))
        self.reject_model(lambda m:m.data[0].update(submitted=False))
    def test_14_public_exact13_projection(self):
        self.reject_model(lambda m:m.data[3]["metadata"].update(extra="injected"))
        self.reject_model(lambda m:m.data[3]["metadata"].update(license={"id":"other"}))
        self.reject_model(lambda m:m.data[3]["metadata"].update(resource_type={"type":"publication","subtype":"article","title":"Article"}))
        self.reject_model(lambda m:m.data[3]["metadata"]["relations"]["version"][0]["parent"].update(pid_value="1"))
    def test_15_native_exact_snapshot_and_types(self):
        self.reject_model(lambda m:m.data[1]["metadata"].update(publisher="Other"))
        self.reject_model(lambda m:m.data[1]["access"]["embargo"].update(active=0))
        self.reject_model(lambda m:m.data[4]["custom_fields"].update(extra="injected"))
    def test_16_parent_acl_omission_only(self):
        self.reject_model(lambda m:m.data[1]["parent"]["access"].update(grants=[{}]))
        self.reject_model(lambda m:m.data[4]["parent"]["access"].update(grants=[]))
        self.reject_model(lambda m:m.data[4]["parent"].update(id="1"))
    def test_17_version_exact_flags_types(self):
        self.reject_model(lambda m:m.data[1]["versions"].update(index=True))
        self.reject_model(lambda m:m.data[1]["versions"].pop("is_latest_draft"))
        self.reject_model(lambda m:m.data[4]["versions"].update(is_latest_draft=True))
    def test_18_publication_pids(self):
        self.reject_model(lambda m:m.data[4]["pids"]["doi"].update(identifier="10.5281/zenodo.1"))
        self.reject_model(lambda m:m.data[4].update(is_published=False))
        self.reject_model(lambda m:m.data[4].update(is_draft=True))
    def test_19_files_completed_visible_exact_three(self):
        self.reject_model(lambda m:m.data[2]["entries"][0].update(status="pending"))
        self.reject_model(lambda m:m.data[2]["entries"][0]["access"].update(hidden=True))
        self.reject_model(lambda m:m.data[4]["files"].update(count=2))
        self.reject_model(lambda m:next(iter(m.data[4]["files"]["entries"].values())).update(checksum="md5:"+"0"*32))
    def test_20_download_status_hash_size_url(self):
        for key,value in (("http_status",404),("sha256","0"*64),("md5","0"*32),("size",1)):
            self.reject_model(lambda m,k=key,x=value:m.data[5].update({k:x}))
        self.reject_model(lambda m:m.data[5].update(url="https://example.invalid/content"))
    def test_21_normal_sheet_append_durable_intent(self):
        e,m=self.engine()
        def at_backend():
            j=json.loads(e.state_path.read_bytes())
            self.assertEqual(j["phase"],"intent_recorded")
            self.assertTrue(j["append_intent"])
            self.assertEqual(len(j["intents"]),1)
            self.assertEqual(j["last_intent"]["service"],"sheet")
        m.before_remote=at_backend
        result=e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertEqual(result["status"],"tracker_verified")
        self.assertEqual(m.rows,[self.row(e)])
        self.assertEqual(sum(x[1]=="append" for x in m.calls),1)
        self.assertEqual(e.state["phase"],"tracker_verified")
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertEqual(sum(x[1]=="append" for x in m.calls),1)
    def test_22_existing_doi_exact_no_append(self):
        e,m=self.engine();m.rows=[self.row(e)]
        result=e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertEqual(result["status"],"tracker_already_exact")
        self.assertFalse(any(x[1]=="append" for x in m.calls))
        for value in (v.DOI," HTTPS://DOI.ORG/"+v.DOI.upper()+" ","http://dx.doi.org/"+v.DOI):
            self.assertEqual(v.v1.doi_key(value),v.DOI)
    def test_23_doi_only_scan_and_duplicates(self):
        e,m=self.engine();r=self.row(e);m.rows=[["https://doi.org/"+v.DOI,"unrelated","10.5281/zenodo.1","unrelated"]]
        self.assertEqual(e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)["status"],"tracker_verified")
        e,m=self.engine();m.rows=[self.row(e),self.row(e)]
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertFalse(any(x[1]=="append" for x in m.calls))
    def test_24_gid_title_header_drift(self):
        for name,val in (("gid",1),("title","Wrong"),("header",["wrong"]*4)):
            e,m=self.engine();setattr(m,name,val)
            with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
            self.assertFalse(any(x[1]=="append" for x in m.calls))
    def test_25_malformed_return_blocks_repeat(self):
        e,m=self.engine();m.bad_return=True
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertTrue(e.state["append_intent"])
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertEqual(sum(x[1]=="append" for x in m.calls),1)
    def test_26_readback_and_postappend_duplicates(self):
        e,m=self.engine();m.readback_bad=True
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertNotEqual(e.state["phase"],"tracker_verified")
        e,m=self.engine();m.before_remote=lambda:m.rows.append(self.row(e))
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertEqual(sum(x[1]=="append" for x in m.calls),1)
    def timeout_test(self,when,status):
        e,m=self.engine();m.append_mode=when
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        self.assertEqual(e.state["phase"],"unknown_write")
        self.assertTrue(e.state["append_intent"])
        self.assertNotIn("append_range",e.state)
        append_index=next(i for i in range(e.count) if json.loads((e.evidence/f"{i:04d}_intent.json").read_bytes())["intent"]["operation"]=="append")
        self.assertFalse((e.evidence/f"{append_index:04d}_response.json").exists())
        native=json.loads((e.evidence/f"{append_index:04d}_native.json").read_bytes())
        self.assertEqual(native["service"],"gws")
        self.assertEqual(base64.b64decode(native["stderr_base64"]),b"modeled native timeout")
        with self.assertRaises(v.Stop):e.tracker(v.SPEC_SHA,v.ID,v.NATIVE_SHA)
        before=len(m.calls);r=e.reconcile(v.SPEC_SHA,native_approval=v.NATIVE_SHA)
        self.assertEqual(r["status"],status)
        self.assertTrue(r["read_only"])
        self.assertTrue(all(x[1] in ("GET","get","batchGet") for x in m.calls[before:]))
        self.assertEqual(sum(x[1]=="append" for x in m.calls),1)
        if when=="after":self.assertFalse(r["append_response_available"])
    def test_27_timeout_before_append(self):self.timeout_test("before","publication_verified_tracker_absent_observed")
    def test_28_timeout_after_append(self):self.timeout_test("after","publication_and_tracker_observed_exact")
    def test_29_repaired_native_receipt_association(self):
        e,m=self.engine()
        for i in (5,6,7):
            self.assertFalse((e.evidence/f"{i:04d}_native.json").exists())
            intent=json.loads((e.evidence/f"{i:04d}_intent.json").read_bytes())["intent"]
            self.assertEqual(intent["service"],"public_hash")
        e.request("public_json","GET",{"id":v.ID,"native":True})
        genuine=json.loads((e.evidence/"0008_native.json").read_bytes())
        self.assertEqual(genuine["url"],f"https://zenodo.org/api/records/{v.ID}")
        # A denied inherited dispatcher must not retain prior response custody.
        with self.assertRaises(v.Stop):v.v1.Admin.request(e,"zenodo",f"POST /api/deposit/depositions/{v.ID}/actions/publish",write=True)
        self.assertFalse((e.evidence/"0009_native.json").exists())
        self.assertEqual(len(m.calls),9)
    def test_30_original_states_unchanged(self):
        for p,digest in originals.items():self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),digest)

class Record(unittest.TestResult):
    def __init__(self):super().__init__();self.records=[]
    def addSuccess(self,test):super().addSuccess(test);self.records.append({"test":test._testMethodName,"outcome":"PASS"})
    def addFailure(self,test,err):super().addFailure(test,err);self.bad(test,err)
    def addError(self,test,err):super().addError(test,err);self.bad(test,err)
    def bad(self,test,err):
        self.records.append({"test":test._testMethodName,"outcome":"FAIL","exception_type":err[0].__name__})
        (RUN/(test._testMethodName+"_failure.txt")).write_text("".join(traceback.format_exception(*err)))

if __name__=="__main__":
    result=Record();unittest.defaultTestLoader.loadTestsFromTestCase(Review).run(result)
    report={"source_sha256":REVIEWED,"adoption_sha256":ADOPTION_SHA,"offline_only":True,"tests_run":result.testsRun,"tests_passed":sum(r["outcome"]=="PASS" for r in result.records),"records":result.records,"custody_regression":"no stale native decoration on hash or denied ancestor; genuine modeled GWS timeout retained","acceptance":result.wasSuccessful(),"original_states_unchanged":all(hashlib.sha256(p.read_bytes()).hexdigest()==d for p,d in originals.items())}
    (HERE/"OFFLINE_TEST_RESULTS.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("tests_run","tests_passed","offline_only","acceptance","original_states_unchanged")},sort_keys=True))
