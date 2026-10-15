#!/usr/bin/env python3
"""PR411 known-publication GET recovery and one explicit tracker append only."""
import argparse
import base64
from contextlib import contextmanager, nullcontext
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import uuid

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
V2_PATH = CASE / "publication_preparation/admin_helper_v2/publication_admin_v2.py"
V2_SHA = "afe03699b252c4aff76f29ba71404dfbe3c9c6a8c924b7028cfa4141f0759f8a"
if any(p.is_symlink() for p in (V2_PATH, *V2_PATH.parents)) or not stat.S_ISREG(V2_PATH.lstat().st_mode):
    raise RuntimeError("unsafe sealed V2 source")
fd = os.open(V2_PATH, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
with os.fdopen(fd, "rb") as f:
    before = os.fstat(f.fileno()); source = f.read(1024 * 1024); after = os.fstat(f.fileno())
import hashlib
identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
if identity(before) != identity(after) or hashlib.sha256(source).hexdigest() != V2_SHA:
    raise RuntimeError("sealed V2 source changed")
sp = importlib.util.spec_from_file_location("publication_admin_v2", V2_PATH)
v2 = importlib.util.module_from_spec(sp); exec(compile(source, str(V2_PATH), "exec"), v2.__dict__)
v1, g, z = v2.v1, v2.g, v2.z
need, Stop, sha, encoded = g.need, g.Stop, g.sha, g.encoded
ID, HEAD, SPEC_SHA, NATIVE_SHA = v2.ID, v2.HEAD, v2.SPEC_SHA, v2.ROOT_SNAPSHOT_SHA
PRIVATE = CASE / "private_sources/publication_admin_helper_v3"
STATE = PRIVATE / "PRODUCTION_STATE.json"
V2_STATE = v2.STATE
V2_STATE_SHA = "46e1b481e5291520fd1d2fb2ca9403b9e8184e097b8d240a9b1d4cc0ea4db66c"
PUB_DIR = v2.PRIVATE / "20261013T045244Z_27e7ee6d662443a5a797474b490ea039"
ACK_SHA = "f416880a93426aa4a01b9370a0fa7b0fa0a913cff869d1209802513796031b8a"
MAPPING = CASE / "publication_preparation/ROOT_ACTUAL_PUBLICATION_MAPPING_ACCEPTANCE.json"
MAPPING_SHA = "ff8e97f7e9c4f88efcaa2fc88bfa41ddf7777e036e668da81c785a2b1c964dad"
MAPPING_DIR = v2.PRIVATE / "ROOT_READONLY_PUBLIC_MAPPING_20261013T0510"
V2_COPY = MAPPING_DIR / "ORIGINAL_V2_PRODUCTION_STATE.json"
NINE = {"access_right", "creators", "description", "keywords", "language", "notes", "publication_date", "title", "version"}
DOI = f"10.5281/zenodo.{ID}"


def own(path):
    p = g.safe_path(path, private=True)
    need(p.is_relative_to(PRIVATE) and p != PRIVATE, "outside V3 private custody")
    return p


@contextmanager
def local_lock():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    fd = os.open(own(PRIVATE / "PRODUCTION_LOCK"), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        need(stat.S_ISREG(os.fstat(fd).st_mode), "nonregular operation lock")
        try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc: raise Stop("another V3 operator holds lock") from exc
        yield
    finally: os.close(fd)


class BoundTransport:
    """One backend call per V3 dispatch; inherited dispatch cannot mint a grant."""
    def __init__(self, owner, backend):
        self.owner, self.backend, self.last_native = owner, backend, None
    def send(self, service, operation, params, payload=None, file=None):
        self.last_native = None
        actual = encoded([service, operation, params, payload, str(file) if file else None])
        need(self.owner._dispatch_grant == actual, "backend lacks exact V3 dispatch grant")
        self.owner._dispatch_grant = None
        if hasattr(self.backend, "last_native"): self.backend.last_native = None
        try:
            if service == "zenodo":
                method, endpoint = operation.split(" ", 1)
                need(method == "GET" and payload is None and file is None, "transport is Zenodo GET-only")
                return self.backend.zenodo(method, endpoint, payload, file, **(params or {}))
            if service == "sheet": return self.backend.sheet(operation, params, payload)
            if service == "public_json": return self.backend.public_json(params["id"], params["native"])
            return self.backend.public_hash(params["id"], params["name"])
        finally: self.last_native = getattr(self.backend, "last_native", None)
    def zenodo(self, method, endpoint, payload=None, file=None, **params):
        return self.send("zenodo", method + " " + endpoint, params or None, payload, file)
    def sheet(self, method, params, payload=None): return self.send("sheet", method, params, payload)
    def public_json(self, record_id, native=False): return self.send("public_json", "GET", {"id": record_id, "native": native})
    def public_hash(self, record_id, name): return self.send("public_hash", "GET", {"id": record_id, "name": name})


class Admin(v2.Admin):
    def __init__(self, api, evidence, state_path=STATE):
        self.api, self.state_path = api, own(state_path)
        self.evidence = own(evidence); self.evidence.mkdir(parents=True, exist_ok=False)
        self.kind = "native_production_api" if isinstance(api, v1.Production) else "offline_model"
        self.count, self.state, self.contract, self._active_phase = 0, None, None, None
        self.mapping, self._dispatch_grant = None, None
        self.api = BoundTransport(self, api)

    def publish(self, *args, **kwargs):
        raise Stop("V3 publication/create/upload/metadata operations unavailable")

    def request(self, service, operation, params=None, payload=None, file=None, write=False):
        need(service != "zenodo" or operation.startswith("GET "), "V3 has no Zenodo mutation path")
        need(not write or service == "sheet" and operation == "append", "V3 permits only guarded tracker append")
        need(self._dispatch_grant is None, "nested V3 dispatch unavailable")
        self._dispatch_grant = encoded([service, operation, params, payload, str(file) if file else None])
        try: return super().request(service, operation, params, payload, file, write)
        finally: self._dispatch_grant = None

    def check_original(self):
        raw, _ = v2.pinned(V2_STATE, V2_STATE_SHA); copy, _ = v2.pinned(V2_COPY, V2_STATE_SHA)
        need(raw == copy, "V2 STOP state/copy differs")
        reader = v2.Admin.__new__(v2.Admin); reader.state_path = V2_STATE
        j = reader.read_state(SPEC_SHA)
        need(j["phase"] == "intent_recorded" and j["publish_intent"] is True and j["append_intent"] is False
             and len(j["intents"]) == 1, "known-publication/never-attempted append history differs")
        intent = j["intents"][0]
        need(intent == j["last_intent"] and intent["service"] == "zenodo"
             and intent["operation"] == f"POST /api/deposit/depositions/{ID}/actions/publish"
             and intent["payload_sha256"] == sha(encoded(None)) and intent["file_sha256"] is None
             and intent["evidence_kind"] == "native_production_api", "known publish intent differs")
        reader.accepted_native(NATIVE_SHA)
        return j

    def load_adoption(self, path, approved):
        raw, _ = g.read_regular(v1.public_path(path)); a = json.loads(raw)
        need(sha(raw) == approved, "root-approved V3 adoption digest differs")
        g.fields(a, ["schema", "case", "id", "science_head", "spec_sha256", "v2_stop_state", "v2_state_copy",
                     "known_publish_directory", "known_publish_files_sha256", "root_mapping"])
        need(type(a["schema"]) is int and a["schema"] == 3 and a["case"] == "pr411_6800014"
             and type(a["id"]) is int and a["id"] == ID and a["science_head"] == HEAD and a["spec_sha256"] == SPEC_SHA,
             "V3 adoption scope differs")
        for key, p, h in (("v2_stop_state", V2_STATE, V2_STATE_SHA), ("v2_state_copy", V2_COPY, V2_STATE_SHA), ("root_mapping", MAPPING, MAPPING_SHA)):
            need(a[key] == {"path": str(p), "sha256": h}, "V3 original pointer differs")
        names = {f"{i:04d}_{kind}.json" for i in range(3, 8) for kind in ("intent", "response")} | {"0007_native.json"}
        need(a["known_publish_directory"] == str(PUB_DIR) and set(a["known_publish_files_sha256"]) == names, "known-publish positive map differs")
        receipts = {name: v2.pinned(PUB_DIR / name, digest)[1] for name, digest in a["known_publish_files_sha256"].items()}
        j = self.check_original()
        need(receipts["0003_intent.json"] == {"intent": j["intents"][0], "payload": None}
             and sha(encoded(receipts["0003_response.json"])) == ACK_SHA, "confirmed publish ACK/intent differs")
        _, mapping = v2.pinned(MAPPING, MAPPING_SHA)
        need(mapping["result"] == "ROOT_ACTUAL_PUBLICATION_PUBLIC_MAPPING_ACCEPTED" and mapping["id"] == ID
             and mapping["spec_sha256"] == SPEC_SHA and mapping["scientific_head"] == HEAD
             and mapping["approved_native_snapshot_sha256"] == NATIVE_SHA
             and mapping["original_v2_stop_state_sha256"] == V2_STATE_SHA and mapping["original_v1_state_sha256"] == v2.ORIGINAL_STATE_SHA
             and mapping["authenticated_requested_metadata12_exact"] is True and mapping["public_legacy_exact13keys"] is True
             and mapping["public_native_full_metadata_access_custom_fields_equal_approved"] is True
             and mapping["sheet_append_attempted"] is False and mapping["remote_mutations"] == 0
             and mapping["doi"] == DOI and mapping["concept_id"] == j["adoption"]["concept_id"], "root actual mapping acceptance differs")
        self.mapping = mapping
        self.contract = {"path": str(path), "sha256": approved, "publisher": "Zenodo", "concept_id": mapping["concept_id"],
                         "v2_stop_state_sha256": V2_STATE_SHA, "public_mapping_sha256": MAPPING_SHA}
        self.legacy(receipts["0003_response.json"], j["spec"], ID)
        self.legacy(receipts["0004_response.json"], j["spec"], ID)
        actual_public = receipts["0007_response.json"]; self.public_legacy(actual_public, receipts["0004_response.json"], j["spec"])
        native_http = receipts["0007_native.json"]
        need(native_http["status"] == 200 and native_http["accept"] == "application/json"
             and native_http["url"] == f"https://zenodo.org/api/records/{ID}"
             and json.loads(base64.b64decode(native_http["body_base64"], validate=True)) == actual_public, "actual public HTTP body join differs")
        for relative, pin in mapping["positive_private_originals"].items():
            q = g.safe_path(CASE / relative, private=True)
            need(q.is_relative_to(MAPPING_DIR), "root mapping source outside positive directory")
            body, _ = g.read_regular(q, private=True); need(len(body) == pin["bytes"] and sha(body) == pin["sha256"], "root mapping original changed")
        self.check_original()
        return j

    def legacy(self, d, s, record_id, complete=True):
        need(record_id == ID and set(d.get("metadata", {})) == v2.METADATA12 | {"doi", "prereserve_doi", "imprint_publisher"}, "authenticated exact15 metadata keys differ")
        need(encoded({k: d["metadata"][k] for k in v2.METADATA12}) == encoded(s["metadata"]) and d["submitted"] is True
             and d["doi"] == d["metadata"]["doi"] == DOI
             and encoded(d["metadata"]["prereserve_doi"]) == encoded({"doi": DOI, "recid": ID}),
             "authenticated requested12/submitted DOI/integer reservation differs")
        return super().legacy(d, s, record_id, complete)

    def public_legacy(self, p, auth, s):
        z.validate_record(p, ID)
        expected = {k: auth["metadata"][k] for k in NINE}
        expected.update(doi=DOI, license=self.mapping["explicit_license_projection"], resource_type=self.mapping["explicit_resource_type_projection"],
                        relations=self.mapping["actual_first_version_relation"])
        need(self.mapping["explicit_license_projection"] == {"id": s["metadata"]["license"]}
             and self.mapping["explicit_resource_type_projection"] == {"type": "publication", "subtype": "preprint", "title": "Preprint"}
             and self.mapping["actual_first_version_relation"] == {"version": [{"index": 0, "is_last": True,
                 "parent": {"pid_type": "recid", "pid_value": self.contract["concept_id"]}}]}, "observed public mapping identity differs")
        need(p["submitted"] is True and p["doi"] == DOI and encoded(p["metadata"]) == encoded(expected), "exact actual public13 metadata projection differs")
        z.verify({"metadata": s["metadata"], "files": p["files"]}, s["metadata"], s["assets"])

    def native(self, record_id, s, draft, expected=None):
        snapshot, native = super().native(record_id, s, draft, expected)
        need(expected is not None and encoded(snapshot) == encoded(expected), "exact authenticated native snapshot types differ")
        return snapshot, native

    def published(self, s, record_id, expected_native):
        need(self.mapping and record_id == ID, "accepted known-publication mapping required")
        auth = self.request("zenodo", f"GET /api/deposit/depositions/{ID}"); self.legacy(auth, s, ID)
        snapshot, native = self.native(ID, s, False, expected_native)
        public = self.request("public_json", "GET", {"id": ID, "native": False}); self.public_legacy(public, auth, s)
        pn = self.request("public_json", "GET", {"id": ID, "native": True})
        need(str(pn.get("id")) == str(ID) and pn.get("is_published") is True and pn.get("is_draft") is False
             and encoded({k: pn.get(k) for k in snapshot}) == encoded(snapshot)
             and encoded(pn.get("pids")) == encoded(native.get("pids")), "public native snapshot/pids/publication differs")
        parent = json.loads(json.dumps(native["parent"]))
        need(parent["access"].get("grants") == [] and parent["access"].get("links") == [], "nonempty parent ACL decoration")
        del parent["access"]["grants"]; del parent["access"]["links"]
        versions = native.get("versions", {})
        need(set(versions) == {"index", "is_latest", "is_latest_draft"} and type(versions["index"]) is int
             and versions["index"] == 1 and versions["is_latest"] is True and versions["is_latest_draft"] is True,
             "actual authenticated first-version flags differ")
        need(encoded(pn.get("parent")) == encoded(parent) and encoded(pn.get("versions")) == encoded({"index": 1, "is_latest": True})
             and str(parent["id"]) == self.contract["concept_id"] and parent["pids"]["doi"]["identifier"] == "10.5281/zenodo." + self.contract["concept_id"]
             and native["pids"]["doi"]["identifier"] == DOI, "exact observed public parent/version identity differs")
        files = pn.get("files", {}); entries = files.get("entries", {})
        need(files.get("enabled") is True and files.get("count") == 3 and isinstance(entries, dict)
             and all(k == v.get("key") and v.get("access", {}).get("hidden") is False for k, v in entries.items()), "public native file mapping/visibility differs")
        z.verify({"metadata": s["metadata"], "files": list(entries.values())}, s["metadata"], s["assets"])
        hashes = []
        for f in s["assets"]:
            h = self.request("public_hash", "GET", {"id": ID, "name": f["name"]})
            need(h.get("http_status") == 200 and h.get("url") == f"https://zenodo.org/api/records/{ID}/files/{v1.quote(f['name'], safe='')}/content"
                 and all(h[k] == f[k] for k in ("sha256", "md5", "size")), "public exact asset bytes/status/url differ")
            hashes.append({"name": f["name"], "sha256": h["sha256"], "size": h["size"]})
        return {"id": ID, "doi": DOI, "doi_url": "https://doi.org/" + DOI, "record_url": f"https://zenodo.org/records/{ID}", "asset_hashes": hashes}

    def read_state(self, approved):
        j = v1.Admin.read_state(self, approved)
        need(j.get("revision") == 3 and j.get("v2_helper_sha256") == V2_SHA, "wrong tracker-only revision")
        self.load_adoption(j["adoption"]["path"], j["adoption"]["sha256"])
        need(j["adoption"] == self.contract, "V3 adoption binding differs")
        return j

    def accepted_native(self, approved):
        need(approved == NATIVE_SHA == self.state.get("native_snapshot_sha256"), "root actual native digest required")
        raw, _ = g.read_regular(own(self.state["native_snapshot_path"]), private=True)
        need(sha(raw) == approved and encoded(json.loads(raw)) == encoded(self.state["native_staged"]), "V3 copied native bytes differ")
        return self.state["native_staged"]

    def recover(self, path, adoption_digest, spec_digest, native_digest):
        need(not self.state_path.exists() and spec_digest == SPEC_SHA and native_digest == NATIVE_SHA, "V3 recovery already claimed/wrong approvals")
        original = self.load_adoption(path, adoption_digest)
        _, snapshot = v2.pinned(v2.ROOT_SNAPSHOT, NATIVE_SHA)
        self.state = {**original, "revision": 3, "v2_helper_sha256": V2_SHA, "adoption": self.contract, "phase": "get_recovery_only",
                      "intents": [], "publish_intent": True, "append_intent": False, "evidence_kind": self.kind}
        self.state.pop("last_intent", None)
        result = self.published(original["spec"], ID, snapshot)
        copied = self.evidence / "NATIVE_METADATA_ACCESS_SNAPSHOT.json"; v1.save(copied, snapshot, True)
        need(sha(g.read_regular(copied, private=True)[0]) == NATIVE_SHA, "exact native copy changed")
        self.state.update(phase="published_verified", publication=result, approved_native_sha256=NATIVE_SHA, native_staged=snapshot,
                          native_snapshot_path=str(copied), native_snapshot_sha256=NATIVE_SHA)
        self.check_original(); v1.save(self.state_path, self.state, True); self.check_original()
        return {"status": "known_publication_get_verified_adopted", "read_only_remote": True, "adoption_sha256": adoption_digest, **result}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("inspect", "recover", "tracker", "reconcile"))
    p.add_argument("--adoption"); p.add_argument("--approved-adoption-sha256", required=True)
    p.add_argument("--approved-spec-sha256", required=True); p.add_argument("--approved-native-sha256", required=True)
    p.add_argument("--confirm-id", type=int, required=True); a = p.parse_args()
    need(a.confirm_id == ID and a.approved_spec_sha256 == SPEC_SHA and a.approved_native_sha256 == NATIVE_SHA, "exact root known-publication pins required")
    with local_lock() if a.mode in ("recover", "tracker") else nullcontext():
        e = Admin(v1.Production(), PRIVATE / (g.dt.datetime.now(g.dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex))
        if a.mode in ("inspect", "recover"):
            need(a.adoption, "approved V3 positive source map required")
            if a.mode == "inspect":
                e.load_adoption(a.adoption, a.approved_adoption_sha256); result = {"status": "known_ack_mapping_locally_verified", "id": ID, "remote_requests": 0}
            else: result = e.recover(a.adoption, a.approved_adoption_sha256, a.approved_spec_sha256, a.approved_native_sha256)
        else:
            j = e.read_state(a.approved_spec_sha256); need(j["adoption"]["sha256"] == a.approved_adoption_sha256, "explicit V3 adoption digest differs")
            result = e.tracker(SPEC_SHA, ID, NATIVE_SHA) if a.mode == "tracker" else e.reconcile(SPEC_SHA, native_approval=NATIVE_SHA)
        result["evidence_kind"] = e.kind; result["revision"] = 3
        v1.save(e.evidence / "RESULT.json", result, True); print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print("STOP: " + (str(exc) if isinstance(exc, Stop) else type(exc).__name__ + "; inspect private custody"), file=sys.stderr); sys.exit(2)
