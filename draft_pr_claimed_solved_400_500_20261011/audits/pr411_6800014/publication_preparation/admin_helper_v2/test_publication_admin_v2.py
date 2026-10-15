"""Synthetic V2 protocol tests plus GET-only replay of actual administrative custody.

No Production transport is instantiated; no actual assets are read or uploaded.
Synthetic source receipts model native shapes and are not native success receipts.
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

sp = importlib.util.spec_from_file_location("v2", Path(__file__).with_name("publication_admin_v2.py"))
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
b = m.v1.module("baseline_test_models", m.V1_PATH.with_name("test_publication_admin.py"),
                "793a81dbfe964d7740d52dbd403b4290ff679f2b3d1c906bb573713ac179e4d3")


class Model(b.Model):
    def __init__(self):
        super().__init__(); self.id = m.ID; self.publisher = "Zenodo"

    def deposit(self):
        d = super().deposit(); d["conceptrecid"] = str(self.id - 1)
        d["metadata"]["imprint_publisher"] = self.publisher
        d["metadata"]["prereserve_doi"] = {"doi": f"10.5281/zenodo.{self.id}", "recid": str(self.id)}
        return d

    def native_record(self):
        n = super().native_record(); n["is_draft"] = not self.submitted
        n["parent"] = {"id": str(self.id - 1)}; n["metadata"]["publisher"] = self.publisher
        n["files"].update(enabled=True, count=3)
        for f in n["files"]["entries"].values(): f["access"] = {"hidden": False}
        return n

    def zenodo(self, method, ep, payload=None, file=None, **params):
        if method == "GET" and ep.endswith("/files"):
            op = method + " " + ep; self.calls.append(("zenodo", op, None)); self.maybe_fail("zenodo", op)
            return {"enabled": True, "entries": [{"key": f["filename"], "checksum": f["checksum"], "size": f["filesize"],
                    "status": "completed", "access": {"hidden": False}} for f in self.files()]}
        return super().zenodo(method, ep, payload, file, **params)


class V2Tests(unittest.TestCase):
    def setUp(self):
        m.PRIVATE.mkdir(parents=True, exist_ok=True)
        self.pub = tempfile.TemporaryDirectory(prefix="synthetic_", dir=m.HERE)
        self.private = tempfile.TemporaryDirectory(prefix="synthetic_", dir=m.PRIVATE)
        self.tmp, self.priv = Path(self.pub.name), Path(self.private.name); self.context = ExitStack(); self.counter = 0
        self.api = Model(); assets = []
        for i, name in enumerate(("preprint.pdf", "source.zip", "verification.zip")):
            data = ("synthetic opaque asset " + str(i)).encode(); self.api.assets[name] = data
            assets.append({"name": name, "local_path": str(self.tmp / name), "sha256": m.sha(data), "md5": hashlib.md5(data).hexdigest(),
                           "size": len(data), "mode": "100644"})
        self.spec = {"schema": 1, "case": "pr411_6800014", "asset_root": str(self.tmp), "assets": assets,
                     "metadata": {"title": "Synthetic", "description": "Synthetic complete disclosure", "keywords": ["synthetic"],
                                  "language": "eng", "license": "cc-by-4.0", "notes": "Synthetic notes", "publication_date": "2026-10-13",
                                  "publication_type": "preprint", "upload_type": "publication", "version": "1", "access_right": "open",
                                  "creators": [{"name": "Fixture, Test", "orcid": "0009-0001-9320-500X"}]},
                     "tracker": {"original_problem": "https://example.invalid/problem", "solution_chat": "https://example.invalid/pr411", "notes": "Synthetic notes"}}
        self.state = self.priv / "V2_STATE.json"; self.source = self.priv / "original_state.json"; self.source_copy = self.priv / "state_copy.json"
        self.stage_dir = self.priv / "stage"; self.stage_dir.mkdir(); self.acceptance = self.priv / "acceptance.json"
        self.root_snapshot = self.priv / "root_snapshot.json"; self.adoption_path = self.tmp / "adoption.json"
        self.install_sources()

    def tearDown(self):
        self.context.close(); self.pub.cleanup(); self.private.cleanup()

    def install_sources(self):
        self.context.close(); self.context = ExitStack()
        self.api.metadata = copy.deepcopy(self.spec["metadata"]); self.api.submitted = False
        snapshot = {k: self.api.native_record()[k] for k in ("metadata", "access", "custom_fields")}
        snapshot_raw = m.encoded(snapshot); self.root_snapshot.write_bytes(snapshot_raw)
        original = m.encoded(self.spec); spec_sha = m.sha(original)
        bucket = self.api.deposit()["links"]["bucket"]
        ops = ["POST /api/deposit/depositions", *["PUT " + bucket.removeprefix("https://zenodo.org") + "/" + f["name"] for f in self.spec["assets"]],
               f"PUT /api/deposit/depositions/{m.ID}", f"GET /api/deposit/depositions/{m.ID}"]
        intents = []
        for i, op in enumerate(ops, 2):
            payload = {"metadata": self.spec["metadata"]} if i in (2, 6) else None
            intent = {"service": "zenodo", "operation": op, "params": None, "payload_sha256": m.sha(m.encoded(payload)),
                      "file_sha256": self.spec["assets"][i-3]["sha256"] if i in (3, 4, 5) else None,
                      "evidence_kind": "native_production_api", "utc": "2026-10-13T00:00:00+00:00"}
            (self.stage_dir / f"{i:04d}_intent.json").write_bytes(m.encoded({"intent": intent, "payload": payload}))
            if i in (3, 4, 5):
                f = self.spec["assets"][i-3]; response = {"key": f["name"], "size": f["size"], "checksum": "md5:" + f["md5"]}
            else:
                response = self.api.deposit()
                if i == 2: response["files"] = []
            (self.stage_dir / f"{i:04d}_response.json").write_bytes(m.encoded(response))
            if i < 7: intents.append(intent)
        j = {"case": "pr411_6800014", "evidence_kind": "native_production_api", "id": m.ID, "phase": "intent_recorded", "publish_intent": False,
             "append_intent": False, "spec": self.spec, "spec_sha256": spec_sha, "spec_bytes_base64": base64.b64encode(original).decode(),
             "parsed_spec_sha256": m.sha(m.encoded(self.spec)), "dependencies": {"guards": m.v1.GUARDS_SHA, "zenodo": m.v1.KIT_SHA},
             "intents": intents, "last_intent": intents[-1]}
        state_raw = m.encoded(j); self.source.write_bytes(state_raw); self.source_copy.write_bytes(state_raw)
        acceptance = {"result": "ROOT_ACTUAL_DRAFT_NATIVE_METADATA_ACCEPTED", "id": m.ID, "all12_requested_legacy_fields_exact": True,
                      "publication_confirmed": False, "publisher_is_read_only": False, "generated_editable_default_publisher": "Zenodo",
                      "approved_native_snapshot_sha256": m.sha(snapshot_raw), "original_stage_state_sha256": m.sha(state_raw),
                      "native_files_exact3_completed_MD5_size_matched": True,
                      "native_full12field_representation_and_author_orcid_access_license_checked": True}
        acceptance_raw = m.encoded(acceptance); self.acceptance.write_bytes(acceptance_raw)
        constants = {"SPEC_SHA": spec_sha, "ORIGINAL_STATE": self.source, "STATE_COPY": self.source_copy, "ORIGINAL_STATE_SHA": m.sha(state_raw),
                     "STAGE_DIR": self.stage_dir, "ROOT_ACCEPTANCE": self.acceptance, "ROOT_ACCEPTANCE_SHA": m.sha(acceptance_raw),
                     "ROOT_SNAPSHOT": self.root_snapshot, "ROOT_SNAPSHOT_SHA": m.sha(snapshot_raw)}
        for key, value in constants.items(): self.context.enter_context(patch.object(m, key, value))
        self.adoption = {"schema": 2, "case": "pr411_6800014", "id": m.ID, "science_head": m.HEAD, "spec_sha256": spec_sha,
                         "whole_acceptance_sha256": m.WHOLE_ACCEPTANCE_SHA, "publisher": "Zenodo", "source_state": {"path": str(self.source), "sha256": m.ORIGINAL_STATE_SHA},
                         "source_state_copy": {"path": str(self.source_copy), "sha256": m.ORIGINAL_STATE_SHA}, "stage_directory": str(self.stage_dir),
                         "stage_files_sha256": {name: m.sha((self.stage_dir/name).read_bytes()) for name in m.STAGE_FILES},
                         "root_acceptance": {"path": str(self.acceptance), "sha256": m.ROOT_ACCEPTANCE_SHA},
                         "root_snapshot": {"path": str(self.root_snapshot), "sha256": m.ROOT_SNAPSHOT_SHA}}
        self.write_adoption()

    def write_adoption(self):
        self.adoption_path.write_bytes(m.encoded(self.adoption)); self.adoption_sha = m.sha(self.adoption_path.read_bytes())

    def engine(self):
        self.counter += 1; return m.Admin(self.api, self.priv / ("evidence_" + str(self.counter)), self.state)

    def recover(self):
        return self.engine().recover(self.adoption_path, self.adoption_sha, m.SPEC_SHA, m.ROOT_SNAPSHOT_SHA)

    def publish(self):
        self.recover(); return self.engine().publish(m.SPEC_SHA, m.ID, m.ROOT_SNAPSHOT_SHA)

    def writes(self):
        return [x for x in self.api.calls if x[0] == "zenodo" and not x[1].startswith("GET ") or x[0] == "sheet" and x[1] == "append"]

    def test_exact_existing_stage_recovery_publish_tracker_and_original_immutable(self):
        e = self.engine(); e.load_adoption(self.adoption_path, self.adoption_sha); self.assertFalse(self.api.calls)
        self.assertEqual(self.recover()["status"], "existing_stage_get_verified_adopted"); self.assertEqual(len(self.api.calls), 3)
        self.assertFalse(self.writes()); j=json.loads(self.state.read_bytes())
        self.assertEqual(m.sha(Path(j["native_snapshot_path"]).read_bytes()), m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(self.engine().publish(m.SPEC_SHA, m.ID, m.ROOT_SNAPSHOT_SHA)["status"], "published_verified")
        self.assertEqual(self.engine().tracker(m.SPEC_SHA, m.ID, m.ROOT_SNAPSHOT_SHA)["status"], "tracker_verified")
        self.assertEqual(len(self.writes()), 2); self.assertEqual(m.sha(self.source.read_bytes()), m.ORIGINAL_STATE_SHA)
        with self.assertRaises(m.Stop): self.engine().recover(self.adoption_path, self.adoption_sha, m.SPEC_SHA, m.ROOT_SNAPSHOT_SHA)

    def test_stage_and_low_level_create_upload_metadata_unavailable(self):
        e = self.engine()
        with self.assertRaises(m.Stop): e.stage()
        e.state = {"phase": "staged_pending_native_acceptance"}
        for op in ("POST /api/deposit/depositions", "PUT /api/files/anything/file", f"PUT /api/deposit/depositions/{m.ID}", "POST /api/deposit/depositions/1/actions/publish"):
            with self.assertRaises(m.Stop): e.request("zenodo", op, write=True)
        self.assertFalse(self.api.calls)

    def test_wrong_approvals_adoption_history_source_and_native_no_writes(self):
        for key, wrong in (("publisher", "Other"), ("science_head", "0"*40), ("schema", True), ("id", True), ("whole_acceptance_sha256", "0"*64)):
            old=self.adoption[key]; self.adoption[key]=wrong; self.write_adoption()
            with self.assertRaises(m.Stop): self.engine().load_adoption(self.adoption_path, self.adoption_sha)
            self.adoption[key]=old
        self.write_adoption()
        with self.assertRaises(m.Stop): self.engine().load_adoption(self.adoption_path, "0"*64)
        self.adoption["stage_files_sha256"].pop("0004_response.json"); self.write_adoption()
        with self.assertRaises(m.Stop): self.engine().load_adoption(self.adoption_path, self.adoption_sha)
        self.assertFalse(self.api.calls)

    def test_evil_requested_metadata_readonly_keys_and_types_rejected(self):
        for key in ("imprint_publisher", "doi", "prereserve_doi", "relations", "unexpected"):
            self.spec["metadata"][key]="evil"; self.install_sources()
            with self.assertRaises(m.Stop): self.engine().load_adoption(self.adoption_path, self.adoption_sha)
            del self.spec["metadata"][key]
        self.spec["schema"]=True; self.install_sources()
        with self.assertRaises(m.Stop): self.engine().load_adoption(self.adoption_path, self.adoption_sha)
        self.assertFalse(self.api.calls)

    def test_fresh_publisher_native_projection_and_incomplete_files_stop(self):
        self.api.publisher="Other"
        with self.assertRaises(m.Stop): self.recover()
        self.api.publisher="Zenodo"; self.api.native_change=True
        with self.assertRaises(m.Stop): self.recover()
        self.api.native_change=False; original=self.api.zenodo
        def incomplete(method, ep, *args, **kwargs):
            r=original(method, ep, *args, **kwargs)
            if ep.endswith('/files'):r['entries'][0]['status']='pending'
            return r
        with patch.object(self.api,'zenodo',incomplete):
            with self.assertRaises(m.Stop): self.recover()
        self.assertFalse(self.state.exists()); self.assertFalse(self.writes())

    def test_original_state_drift_blocks_publish_and_no_overwrite(self):
        self.recover(); self.source.write_bytes(b'changed original state')
        with self.assertRaises(m.Stop): self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertFalse(self.writes()); self.assertEqual(self.source.read_bytes(),b'changed original state')

    def test_unknown_publish_get_only_reconcile_no_new_append_or_retry(self):
        self.recover(); self.api.fail=('zenodo',f'POST /api/deposit/depositions/{m.ID}/actions/publish'); self.api.applied_before_error=True
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.api.fail=None; before=len(self.writes()); result=self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(result['status'],'publication_verified_tracker_absent_observed')
        with self.assertRaises(m.Stop):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_unknown_append_observed_exact_without_fabricated_response(self):
        self.publish();self.api.fail=('sheet','append');self.api.applied_before_error=True
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.api.fail=None;before=len(self.writes());r=self.engine().reconcile(m.SPEC_SHA,native_approval=m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(r['status'],'publication_and_tracker_observed_exact');self.assertFalse(r['append_response_available'])
        with self.assertRaises(m.Stop):self.engine().tracker(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertEqual(len(self.writes()),before)

    def test_durable_publish_intent_error_before_network_and_native_scope(self):
        self.recover();original=m.v1.save
        def failed(path,obj,exclusive=False):
            if Path(path)==self.state and obj.get('phase')=='intent_recorded':raise OSError('synthetic storage error')
            return original(path,obj,exclusive)
        with patch.object(m.v1,'save',failed):
            with self.assertRaises(OSError):self.engine().publish(m.SPEC_SHA,m.ID,m.ROOT_SNAPSHOT_SHA)
        self.assertFalse(self.writes())
        with self.assertRaises(m.Stop):m.Admin(self.api,self.priv/'new',self.tmp/'outside_state.json')


class ActualAdministrativeReplay(unittest.TestCase):
    def test_actual_root_custody_publisher_projection_get_only_replay(self):
        class Replay:
            def __init__(self):self.calls=[]
            def zenodo(self,method,endpoint,*args,**kwargs):
                self.calls.append((method,endpoint));assert method=='GET'
                root=m.ROOT_SNAPSHOT.parent
                name='0002_response.json' if endpoint.endswith('/files') else '0001_response.json' if '/records/' in endpoint else '0000_response.json'
                return json.loads(m.g.read_regular(root/name,private=True)[0])
        with tempfile.TemporaryDirectory(prefix='actual_replay_',dir=m.PRIVATE) as directory:
            p=Path(directory);api=Replay();e=m.Admin(api,p/'evidence',p/'ephemeral_state.json')
            adoption=m.HERE/'PROPOSED_RECOVERY_ADOPTION.json';digest=m.sha(adoption.read_bytes())
            before=m.sha(m.g.read_regular(m.ORIGINAL_STATE,private=True)[0])
            result=e.recover(adoption,digest,m.SPEC_SHA,m.ROOT_SNAPSHOT_SHA)
            self.assertEqual(result['status'],'existing_stage_get_verified_adopted');self.assertEqual(len(api.calls),3)
            self.assertEqual(e.kind,'offline_model');self.assertEqual(m.sha(m.g.read_regular(m.ORIGINAL_STATE,private=True)[0]),before)


if __name__ == '__main__':unittest.main(verbosity=2)
