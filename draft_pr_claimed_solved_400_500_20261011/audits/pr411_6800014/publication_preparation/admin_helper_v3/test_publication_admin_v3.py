"""Actual pinned administrative response replay; synthetic Sheet only. No API calls."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

sp = importlib.util.spec_from_file_location("v3", Path(__file__).with_name("publication_admin_v3.py"))
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)


class Replay:
    def __init__(self):
        self.calls = []; self.rows = {1: m.v1.HEADERS[:]}; self.changes = {}; self.fail_append = None

    def record(self, name):
        d = json.loads(m.g.read_regular(m.MAPPING_DIR / name, private=True)[0])
        if name in self.changes: self.changes[name](d)
        return d

    def zenodo(self, method, endpoint, *args, **kwargs):
        self.calls.append(("zenodo", method, endpoint)); assert method == "GET", "NO Zenodo mutation"
        name = "0002_response.json" if endpoint.endswith("/files") else "0001_response.json" if "/records/" in endpoint else "0000_response.json"
        return self.record(name)

    def public_json(self, record_id, native=False):
        self.calls.append(("public_json", "GET", record_id, native))
        return self.record("0004_response.json" if native else "0003_response.json")

    def public_hash(self, record_id, name):
        self.calls.append(("public_hash", "GET", record_id, name))
        mapping = json.loads(m.g.read_regular(m.MAPPING, private=True)[0])
        result = copy.deepcopy(next(x for x in mapping["public_downloads"] if x["name"] == name))
        if "hash" in self.changes: self.changes["hash"](result)
        return result

    def sheet(self, operation, params, payload=None):
        self.calls.append(("sheet", operation, copy.deepcopy(params), copy.deepcopy(payload)))
        if operation == "get":
            return {"spreadsheetId": m.v1.SHEET, "sheets": [{"properties": {"sheetId": m.v1.GID, "title": m.v1.TITLE}}]}
        if operation == "batchGet":
            values = []
            for rr in params["ranges"]:
                row = m.v1.canonical_range(rr)
                if row == "C2:C":
                    cells = [[self.rows[i][2]] if i in self.rows else [] for i in range(2, max(self.rows) + 1)]
                    rr = m.v1.TAB + "C2:C1000"
                else:
                    number = int(row.split(":")[0][1:]); cells = [self.rows[number]] if number in self.rows else []
                values.append({"range": rr, "majorDimension": "ROWS", "values": cells})
            return {"spreadsheetId": m.v1.SHEET, "valueRanges": values}
        assert operation == "append"
        if self.fail_append == "before": raise OSError("synthetic unknown append before response")
        n = max(self.rows) + 1; self.rows[n] = payload["values"][0][:]
        if self.fail_append == "after": raise OSError("synthetic applied append response lost")
        return {"spreadsheetId": m.v1.SHEET, "updates": {"spreadsheetId": m.v1.SHEET, "updatedRange": m.v1.TAB + f"A{n}:D{n}",
                "updatedRows": 1, "updatedColumns": 4, "updatedCells": 4}}


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="actual_admin_model_", dir=m.PRIVATE)
        self.tmp = Path(self.temp.name); self.state = self.tmp / "MODEL_STATE.json"; self.api = Replay(); self.counter = 0
        self.adoption = m.HERE / "PROPOSED_RECOVERY_ADOPTION.json"; self.digest = m.sha(m.g.read_regular(self.adoption)[0])
        self.original_v2_sha = m.sha(m.g.read_regular(m.V2_STATE, private=True)[0])

    def tearDown(self):
        self.assertEqual(m.sha(m.g.read_regular(m.V2_STATE, private=True)[0]), self.original_v2_sha)
        self.temp.cleanup()

    def engine(self):
        self.counter += 1; return m.Admin(self.api, self.tmp / str(self.counter), self.state)

    def recover(self): return self.engine().recover(self.adoption, self.digest, m.SPEC_SHA, m.NATIVE_SHA)

    def writes(self): return [x for x in self.api.calls if x[:2] == ("sheet", "append") or x[0] == "zenodo" and x[1] != "GET"]

    def test_actual_original_shape_recovery_and_one_tracker(self):
        result = self.recover(); self.assertEqual(result["status"], "known_publication_get_verified_adopted")
        self.assertEqual(len(self.api.calls), 8); self.assertFalse(self.writes())
        e = self.engine(); self.assertEqual(e.kind, "offline_model")
        self.assertEqual(e.tracker(m.SPEC_SHA, m.ID, m.NATIVE_SHA)["status"], "tracker_verified")
        self.assertEqual(len(self.writes()), 1)
        with self.assertRaises(m.Stop): self.engine().tracker(m.SPEC_SHA, m.ID, m.NATIVE_SHA)
        with self.assertRaises(m.Stop): self.recover()

    def test_no_zenodo_mutation_or_direct_append_under_either_flag(self):
        e = self.engine()
        for op in ("POST /api/deposit/depositions", f"POST /api/deposit/depositions/{m.ID}/actions/publish", f"PUT /api/deposit/depositions/{m.ID}", "PUT /api/files/a/file"):
            for flag in (False, True):
                with self.assertRaises(m.Stop): e.request("zenodo", op, write=flag)
        with self.assertRaises(m.Stop): e.publish(m.SPEC_SHA, m.ID, m.NATIVE_SHA)
        with self.assertRaises(m.Stop): e.stage()
        self.recover(); e = self.engine(); e.read_state(m.SPEC_SHA)
        with self.assertRaises(m.Stop): e.request("sheet", "append", {}, {}, write=True)
        self.assertFalse(self.writes())

    def test_exact_public_license_resource_doi_relations_and_no_extra_metadata(self):
        attacks = [lambda d:d["metadata"]["license"].update(title="extra"), lambda d:d["metadata"].update(license="cc-by-4.0"),
                   lambda d:d["metadata"]["resource_type"].update(subtype="article"), lambda d:d["metadata"].update(imprint_publisher="Zenodo"),
                   lambda d:d["metadata"].update(doi="10.5281/zenodo.1"), lambda d:d["metadata"]["relations"]["version"][0].update(is_last=1)]
        for attack in attacks:
            self.api.changes["0003_response.json"] = attack
            with self.assertRaises(m.Stop): self.recover()
            self.assertFalse(self.state.exists())
        self.assertFalse(self.writes())

    def test_private_parent_and_versions_have_only_observed_public_omissions(self):
        attacks = [lambda d:d["versions"].update(is_latest_draft=True), lambda d:d["versions"].update(index=1.0),
                   lambda d:d["parent"]["access"].update(grants=[]), lambda d:d["parent"]["pids"]["doi"].update(identifier="10.5281/zenodo.1"),
                   lambda d:d["metadata"].update(publisher="Other")]
        for attack in attacks:
            self.api.changes["0004_response.json"] = attack
            with self.assertRaises(m.Stop): self.recover()
            self.assertFalse(self.state.exists())
        self.assertFalse(self.writes())

    def test_auth_recid_type_and_native_completed_visible_assets(self):
        for name, attack in (("0000_response.json",lambda d:d["metadata"]["prereserve_doi"].update(recid=str(m.ID))),
                             ("0001_response.json",lambda d:d["parent"]["access"].update(grants=["nonempty"])),
                             ("0002_response.json",lambda d:d["entries"][0].update(status="pending")),
                             ("0004_response.json",lambda d:next(iter(d["files"]["entries"].values()))["access"].update(hidden=True)),
                             ("hash",lambda d:d.update(sha256="0"*64))):
            self.api.changes={name:attack}
            with self.assertRaises(m.Stop):self.recover()
            self.assertFalse(self.state.exists())
        self.assertFalse(self.writes())

    def test_unknown_append_after_application_get_only_exact_no_receipt_or_retry(self):
        self.recover(); self.api.fail_append="after"
        with self.assertRaises(m.Stop): self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.api.fail_append=None; before=len(self.writes());r=self.engine().reconcile(m.SPEC_SHA,native_approval=m.NATIVE_SHA)
        self.assertEqual(r["status"],"publication_and_tracker_observed_exact");self.assertFalse(r["append_response_available"])
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_unknown_append_before_response_absence_does_not_enable_retry(self):
        self.recover(); self.api.fail_append="before"
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.api.fail_append=None;before=len(self.writes())
        self.assertEqual(self.engine().reconcile(m.SPEC_SHA,native_approval=m.NATIVE_SHA)["status"],"publication_verified_tracker_absent_observed")
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.NATIVE_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_wrong_approvals_and_original_state_cannot_be_destination(self):
        with self.assertRaises(m.Stop):self.engine().recover(self.adoption,"0"*64,m.SPEC_SHA,m.NATIVE_SHA)
        with self.assertRaises(m.Stop):self.engine().recover(self.adoption,self.digest,m.SPEC_SHA,"0"*64)
        with self.assertRaises(m.Stop):m.Admin(self.api,self.tmp/"new",m.V2_STATE)
        self.assertFalse(self.api.calls)


if __name__ == "__main__":unittest.main(verbosity=2)
