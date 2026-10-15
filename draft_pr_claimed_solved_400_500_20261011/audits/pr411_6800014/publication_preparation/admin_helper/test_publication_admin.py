"""Synthetic offline production-protocol models; no real stage/publish/append."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

loader = importlib.util.spec_from_file_location("admin", Path(__file__).with_name("publication_admin.py"))
m = importlib.util.module_from_spec(loader); loader.loader.exec_module(m)


class Model:
    def __init__(self):
        self.id = 22334488; self.metadata = None; self.assets = {}; self.submitted = False
        self.calls = []; self.fail = None; self.applied_before_error = False
        self.rows = {1: m.HEADERS[:]}; self.gid = m.GID; self.sheet_id = m.SHEET; self.title = m.TITLE
        self.native_change = False; self.public_change = False; self.hash_change = False; self.returned_range = None

    def files(self):
        return [{"filename": n, "checksum": "md5:" + hashlib.md5(data).hexdigest(), "filesize": len(data)}
                for n, data in self.assets.items()]

    def deposit(self):
        meta = copy.deepcopy(self.metadata)
        if self.submitted: meta["doi"] = f"10.5281/zenodo.{self.id}"
        return {"id": self.id, "metadata": meta, "submitted": self.submitted, "files": self.files(),
                "doi": f"10.5281/zenodo.{self.id}" if self.submitted else None,
                "links": {"bucket": "https://zenodo.org/api/files/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"}}

    def native_record(self):
        metadata = {"title": self.metadata["title"], "description": self.metadata["description"],
                    "fixture_projection": copy.deepcopy(self.metadata)}
        if self.native_change: metadata["title"] = "drifted native title"
        entries = {f["filename"]: {"key": f["filename"], "checksum": f["checksum"], "size": f["filesize"]} for f in self.files()}
        return {"id": str(self.id), "metadata": metadata, "custom_fields": {},
                "access": {"record": "public", "files": "public", "embargo": {"active": False}},
                "pids": {"doi": {"identifier": f"10.5281/zenodo.{self.id}", "provider": "datacite"}},
                "files": {"entries": entries}, "is_published": self.submitted}

    def maybe_fail(self, service, op, after=False):
        if self.fail == (service, op) and self.applied_before_error == after:
            raise OSError("synthetic response lost")

    def zenodo(self, method, ep, payload=None, file=None, **params):
        op = method + " " + ep; self.calls.append(("zenodo", op, copy.deepcopy(payload)))
        self.maybe_fail("zenodo", op)
        if method == "POST" and ep == "/api/deposit/depositions":
            self.metadata = copy.deepcopy(payload["metadata"]); response = self.deposit()
        elif method == "PUT" and ep.startswith("/api/files/"):
            name = ep.rsplit("/", 1)[1]; self.assets[name] = Path(file).read_bytes(); response = {"key": name}
        elif method == "PUT": self.metadata = copy.deepcopy(payload["metadata"]); response = self.deposit()
        elif method == "POST": self.submitted = True; response = self.deposit()
        elif "/api/records/" in ep: response = self.native_record()
        else: response = self.deposit()
        self.maybe_fail("zenodo", op, True)
        return copy.deepcopy(response)

    def sheet(self, op, params, payload=None):
        self.calls.append(("sheet", op, copy.deepcopy(params), copy.deepcopy(payload))); self.maybe_fail("sheet", op)
        if op == "get":
            response = {"spreadsheetId": self.sheet_id, "sheets": [{"properties": {"sheetId": self.gid, "title": self.title}}]}
        elif op == "batchGet":
            vr = []
            for rr in params["ranges"]:
                r = m.canonical_range(rr)
                if r == "C2:C":
                    values = [[self.rows[i][2]] if i in self.rows else [] for i in range(2, max(self.rows) + 1)]
                    rr = m.TAB + "C2:C1000"
                else:
                    row = int(r.split(":")[0][1:]); values = [self.rows[row]] if row in self.rows else []
                vr.append({"range": rr, "majorDimension": "ROWS", "values": values})
            response = {"spreadsheetId": self.sheet_id, "valueRanges": vr}
        elif op == "append":
            assert params["valueInputOption"] == "RAW" and params["insertDataOption"] == "INSERT_ROWS"
            assert len(payload["values"]) == 1 and len(payload["values"][0]) == 4
            n = max(self.rows) + 1; self.rows[n] = payload["values"][0][:]
            rr = self.returned_range or m.TAB + f"A{n}:D{n}"
            response = {"spreadsheetId": self.sheet_id, "updates": {"spreadsheetId": self.sheet_id,
                        "updatedRows": 1, "updatedColumns": 4, "updatedCells": 4, "updatedRange": rr}}
        else: raise AssertionError(op)
        self.maybe_fail("sheet", op, True)
        return copy.deepcopy(response)

    def public_json(self, record_id, native=False):
        self.calls.append(("public_json", "GET", record_id)); assert self.submitted
        response = self.native_record() if native else self.deposit()
        if self.public_change: response["metadata"]["description"] = "wrong public description"
        return copy.deepcopy(response)

    def public_hash(self, record_id, name):
        self.calls.append(("public_hash", "GET", name)); data = self.assets[name]
        if self.hash_change: data += b"corruption"
        return {"http_status": 200, "size": len(data), "sha256": m.sha(data), "md5": hashlib.md5(data).hexdigest()}


class AdminTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="offline_", dir=m.HERE)
        self.tmp = Path(self.temp.name); self.pkg = self.tmp / "assets"; self.pkg.mkdir()
        self.private = tempfile.TemporaryDirectory(prefix="models_", dir=m.PRIVATE)
        self.priv = Path(self.private.name); self.state = self.priv / "STATE.json"; self.counter = 0
        self.api = Model()
        assets = []
        for i, name in enumerate(("preprint.pdf", "source.zip", "verification.zip")):
            p = self.pkg / name; data = ("synthetic approved asset " + str(i)).encode(); p.write_bytes(data)
            assets.append({"local_path": str(p), "name": name, "sha256": m.sha(data), "md5": hashlib.md5(data).hexdigest(),
                           "size": len(data), "mode": "100644"})
        self.spec = {"schema": 1, "case": "pr411_6800014", "asset_root": str(self.pkg), "assets": assets,
                     "metadata": {"title": "Synthetic exact preprint", "description": "Synthetic complete disclosure",
                                  "upload_type": "publication", "publication_type": "preprint", "publication_date": "2026-10-13",
                                  "creators": [{"name": "Fixture, Test", "orcid": "0009-0001-9320-500X"}],
                                  "access_right": "open", "license": "cc-by-4.0"},
                     "tracker": {"original_problem": "https://example.invalid/problem", "solution_chat": "https://example.invalid/pr411", "notes": "Synthetic reviewed disclosure"}}
        self.spec_path = self.tmp / "spec.json"; self.write_spec()

    def tearDown(self): self.temp.cleanup(); self.private.cleanup()

    def write_spec(self): self.spec_path.write_bytes(m.encoded(self.spec))

    def engine(self):
        self.counter += 1; return m.Admin(self.api, self.priv / str(self.counter), self.state)

    def staged(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path); result = e.stage(s, digest, content)
        return digest, result["native_snapshot_sha256"]

    def published(self):
        digest, native = self.staged(); self.engine().publish(digest, self.api.id, native); return digest, native

    def writes(self):
        return [x for x in self.api.calls if (x[0] == "zenodo" and x[1].split()[0] != "GET") or (x[0] == "sheet" and x[1] == "append")]

    def test_inspect_and_exact_success_two_approvals_one_append(self):
        e = self.engine(); s, digest, _ = e.load_spec(self.spec_path); e.sheet_gate(); self.assertFalse(self.writes())
        digest, native = self.published()
        result = self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(result["status"], "tracker_verified")
        self.assertEqual(sum(x[0] == "sheet" for x in self.writes()), 1)
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        before = len(self.writes()); r = self.engine().reconcile(digest, native_approval=native)
        self.assertEqual(r["status"], "publication_and_tracker_observed_exact"); self.assertEqual(len(self.writes()), before)

    def test_spec_asset_hash_extra_private_symlink_fifo_pins(self):
        for key, wrong in (("sha256", "0" * 64), ("md5", "0" * 32), ("size", 1), ("mode", "100755")):
            old = self.spec["assets"][0][key]; self.spec["assets"][0][key] = wrong; self.write_spec()
            with self.assertRaises(m.Stop): self.engine().load_spec(self.spec_path)
            self.spec["assets"][0][key] = old
        self.write_spec(); extra = self.pkg / "extra"; extra.write_text("extra")
        with self.assertRaises(m.Stop): self.engine().load_spec(self.spec_path)
        extra.unlink(); extra.symlink_to(self.pkg / "preprint.pdf")
        with self.assertRaises(m.Stop): self.engine().load_spec(self.spec_path)
        extra.unlink(); os.mkfifo(extra)
        with self.assertRaises(m.Stop): self.engine().load_spec(self.spec_path)
        extra.unlink()
        with self.assertRaises(m.Stop): m.public_path(m.CASE / ".secrets/token")
        self.assertFalse(self.writes())

    def test_wrong_approval_native_snapshot_and_state_tampering(self):
        digest, native = self.staged()
        for d, n, ident in (("0" * 64, native, self.api.id), (digest, "0" * 64, self.api.id), (digest, native, 1)):
            before = len(self.writes())
            with self.assertRaises(m.Stop): self.engine().publish(d, ident, n)
            self.assertEqual(len(self.writes()), before)
        j = json.loads(self.state.read_text()); j["spec"]["metadata"]["title"] = "tampered"
        j["parsed_spec_sha256"] = m.sha(m.encoded(j["spec"])); m.save(self.state, j)
        with self.assertRaisesRegex(m.Stop, "raw spec"): self.engine().read_state(digest)

    def test_native_drift_before_publish_and_public_metadata_asset_drift(self):
        digest, native = self.staged(); self.api.native_change = True; before = len(self.writes())
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before); self.api.native_change = False
        self.engine().publish(digest, self.api.id, native)
        for field in ("public_change", "hash_change"):
            setattr(self.api, field, True); before = len(self.writes())
            with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
            self.assertEqual(len(self.writes()), before); setattr(self.api, field, False)

    def test_gid_title_header_identity_drift(self):
        for field, wrong in (("gid", 1), ("title", "Wrong tab"), ("sheet_id", "wrong")):
            old = getattr(self.api, field); setattr(self.api, field, wrong)
            with self.assertRaises(m.Stop): self.engine().sheet_gate()
            setattr(self.api, field, old)
        self.api.rows[1] = ["Original Problem", "DOI", "Solution Chat URL", "Notes"]
        with self.assertRaises(m.Stop): self.engine().sheet_gate()
        self.assertFalse(self.writes())

    def test_doi_only_dedup_bare_url_duplicate_and_conflicting_row(self):
        digest, native = self.published(); doi = f"10.5281/zenodo.{self.api.id}"
        row = [*self.spec["tracker"].values()]; expected = [row[0], row[1], "https://doi.org/" + doi, row[2]]
        self.api.rows[2] = expected
        before = len(self.writes()); self.assertEqual(self.engine().tracker(digest, self.api.id, native)["status"], "tracker_already_exact")
        self.assertEqual(len(self.writes()), before)
        self.api.rows[2][2] = doi.upper()
        self.assertEqual(self.engine().doi_rows(doi), [2])
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.api.rows[3] = expected
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertEqual(len(self.writes()), before)

    def test_unknown_create_stops_without_restaging(self):
        e = self.engine(); s, digest, content = e.load_spec(self.spec_path)
        self.api.fail = ("zenodo", "POST /api/deposit/depositions"); self.api.applied_before_error = True
        with self.assertRaises(m.Stop): e.stage(s, digest, content)
        before = len(self.writes()); self.api.fail = None
        with self.assertRaises(m.Stop): self.engine().stage(s, digest, content)
        with self.assertRaises(m.Stop): self.engine().reconcile(digest)
        r = self.engine().reconcile(digest, recover_id=self.api.id)
        self.assertEqual(r["status"], "draft_observed_publication_unconfirmed"); self.assertEqual(len(self.writes()), before)

    def test_unknown_publish_get_reconcile_no_repeat_post(self):
        digest, native = self.staged(); self.api.fail = ("zenodo", f"POST /api/deposit/depositions/{self.api.id}/actions/publish")
        self.api.applied_before_error = True
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        before = len(self.writes()); self.api.fail = None
        with self.assertRaises(m.Stop): self.engine().publish(digest, self.api.id, native)
        r = self.engine().reconcile(digest, native_approval=native)
        self.assertEqual(r["status"], "publication_verified_tracker_absent_observed"); self.assertEqual(len(self.writes()), before)

    def test_unknown_append_get_reconcile_no_repeat_append(self):
        digest, native = self.published(); self.api.fail = ("sheet", "append"); self.api.applied_before_error = True
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        before = len(self.writes()); self.api.fail = None
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        r = self.engine().reconcile(digest, native_approval=native)
        self.assertEqual(r["status"], "publication_and_tracker_observed_exact")
        self.assertFalse(r["append_response_available"]); self.assertEqual(len(self.writes()), before)

    def test_returned_row_boundary_other_tab_wrong_cells(self):
        digest, native = self.published(); self.api.returned_range = "'Other tab'!A2:D2"
        with self.assertRaises(m.Stop): self.engine().tracker(digest, self.api.id, native)
        self.assertTrue(json.loads(self.state.read_text())["append_intent"])
        self.assertEqual(sum(x[0] == "sheet" for x in self.writes()), 1)


if __name__ == "__main__": unittest.main(verbosity=2)
