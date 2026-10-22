#!/usr/bin/env python3
"""PR411 production Zenodo/DOI tracker administration. Explicit phases only.

No PR edits, math verdicts, credentials-file reads, or automatic write retries.
The caller supplies the final reviewed three assets and exact metadata schema.
Native APIs have no atomic publish/append lease; concurrent remote edits remain
possible. Unknown writes stop and can only be observed with GET reconciliation.
"""
import argparse
import base64
from contextlib import contextmanager, nullcontext
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import uuid
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
ROOT = CASE.parents[2]
PRIVATE = CASE / "private_sources/publication_admin_helper"
STATE = PRIVATE / "PRODUCTION_STATE.json"
SHEET = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
GID = 1254632077
TITLE = "Math Puzzles"
TAB = "'Math Puzzles'!"
HEADERS = ["Original Problem", "Solution Chat URL", "DOI", "Notes"]
GUARDS_PATH = CASE / "package_update_preparation/update_package.py"
GUARDS_SHA = "e32d5a12d08f6c7331070e2a5e7368aec5c1a44f6e1e8d2bef2623df9afb8ebf"
KIT_PATH = ROOT / "zenodo_deposit_tool/zenodo.py"
KIT_SHA = "a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca"


def module(name, path, expected):
    path = path.absolute()
    if ".." in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise RuntimeError("unsafe administration dependency path")
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise RuntimeError("nonregular administration dependency")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno()); raw = stream.read(1024 * 1024 + 1); after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if identity(before) != identity(opened) or identity(opened) != identity(after) or len(raw) > 1024 * 1024:
        raise RuntimeError("administration dependency changed during read")
    if hashlib.sha256(raw).hexdigest() != expected:
        raise RuntimeError("administration dependency seal changed")
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), "exec"), obj.__dict__)
    return obj


g = module("pr411_guards", GUARDS_PATH, GUARDS_SHA)
z = module("pr411_zenodo", KIT_PATH, KIT_SHA)
need, Stop, sha, encoded = g.need, g.Stop, g.sha, g.encoded
READ_ONLY_METADATA = {"doi", "prereserve_doi", "relations"}
METADATA_KEYS = {"title", "description", "upload_type", "publication_type", "publication_date", "creators",
                 "access_right", "license", "keywords", "related_identifiers", "references", "notes",
                 "version", "language", "method"}


def save(path, obj, exclusive=False):
    g.durable(path, obj, exclusive=exclusive, private=True)


def public_path(path):
    p = g.safe_path(path)
    need(p.is_relative_to(CASE) and not ({x.casefold() for x in p.parts} & {".secrets", ".zenodo-state"}),
         "spec/asset path outside public case")
    return p


def private_path(path):
    p = g.safe_path(path, private=True)
    need(p.is_relative_to(PRIVATE) and p != PRIVATE, "custody path outside own private directory")
    return p


@contextmanager
def mutation_lock():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    p = g.safe_path(PRIVATE / "PRODUCTION_LOCK", private=True)
    fd = os.open(p, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        need(stat.S_ISREG(os.fstat(fd).st_mode), "nonregular operation lock")
        try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc: raise Stop("another local publication operation holds the lock") from exc
        yield
    finally:
        os.close(fd)


def canonical_range(value):
    need(isinstance(value, str), "invalid returned range")
    for prefix in (TAB, TITLE + "!"):
        if value.startswith(prefix):
            return value[len(prefix):]
    raise Stop("returned range belongs to another tab")


def doi_key(value):
    if not isinstance(value, str):
        return None
    text = value.strip().casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/"):
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    return text if re.fullmatch(r"10\.5281/zenodo\.[1-9][0-9]*", text) else None


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise Stop("unexpected public Zenodo redirect; no credentials sent")


class Production:
    """Reuse audited transport/normalizations; every mutation is separately journaled."""
    def __init__(self):
        self.client = None; self.last_native = None

    def zenodo(self, method, endpoint, payload=None, file=None, accept="application/json"):
        if self.client is None:
            token = os.environ.get("ZENODO_TOKEN", "").strip()
            need(token and "\r" not in token and "\n" not in token, "ZENODO_TOKEN environment value required")
            self.client = z.ZenodoClient("production", token)
        self.last_native = None
        return self.client.request(method, "https://zenodo.org" + endpoint, payload=payload, file=file, accept=accept)

    def sheet(self, method, params, payload=None):
        resource = ["spreadsheets", "get"] if method == "get" else ["spreadsheets", "values", method]
        cmd = ["gws", "sheets", *resource, "--params", json.dumps(params)]
        if payload is not None:
            cmd += ["--json", json.dumps(payload)]
        self.last_native = {"service": "gws", "method": method, "params": params}
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=60)
        except subprocess.TimeoutExpired as exc:
            self.last_native.update({"returncode": None, "stdout_base64": base64.b64encode(exc.stdout or b"").decode(),
                                     "stderr_base64": base64.b64encode(exc.stderr or b"").decode()})
            raise
        self.last_native.update({"returncode": r.returncode, "stdout_base64": base64.b64encode(r.stdout).decode(),
                                 "stderr_base64": base64.b64encode(r.stderr).decode()})
        need(r.returncode == 0, "GWS request failed; raw output retained privately")
        return json.loads(r.stdout)

    def public_json(self, record_id, native=False):
        url = f"https://zenodo.org/api/records/{record_id}"
        accept = "application/vnd.inveniordm.v1+json" if native else "application/json"
        req = Request(url, headers={"User-Agent": z.USER_AGENT, "Accept": accept})
        self.last_native = None
        with build_opener(NoRedirect()).open(req, timeout=60) as response:
            raw = response.read(z.MAX_RESPONSE_BYTES + 1)
            need(len(raw) <= z.MAX_RESPONSE_BYTES, "oversized public JSON")
            self.last_native = {"url": url, "accept": accept, "status": response.status,
                                "body_base64": base64.b64encode(raw).decode()}
            return json.loads(raw)

    def public_hash(self, record_id, name):
        url = f"https://zenodo.org/api/records/{record_id}/files/{quote(name, safe='')}/content"
        req = Request(url, headers={"User-Agent": z.USER_AGENT})
        self.last_native = None
        h, md, size = hashlib.sha256(), hashlib.md5(), 0
        with build_opener(NoRedirect()).open(req, timeout=60) as response:
            while True:
                part = response.read(1024 * 1024)
                if not part: break
                size += len(part); need(size <= 128 * 1024**2, "public asset exceeds bounded limit")
                h.update(part); md.update(part)
            return {"url": url, "http_status": response.status, "sha256": h.hexdigest(), "md5": md.hexdigest(), "size": size}


class Admin:
    def __init__(self, api, evidence, state_path=STATE):
        self.api, self.state_path = api, private_path(state_path)
        self.evidence = private_path(evidence); self.evidence.mkdir(parents=True, exist_ok=False)
        self.kind = "native_production_api" if isinstance(api, Production) else "offline_model"
        self.count, self.state = 0, None

    def request(self, service, operation, params=None, payload=None, file=None, write=False):
        i = self.count; self.count += 1
        intent = {"service": service, "operation": operation, "params": params, "payload_sha256": sha(encoded(payload)),
                  "file_sha256": sha(g.read_regular(file, private=True)[0]) if file else None,
                  "evidence_kind": self.kind, "utc": g.dt.datetime.now(g.dt.timezone.utc).isoformat()}
        if write:
            need(self.state is not None, "mutation lacks state")
            self.state["phase"] = "intent_recorded"; self.state["last_intent"] = intent
            self.state["intents"].append(intent); save(self.state_path, self.state)
        save(self.evidence / f"{i:04d}_intent.json", {"intent": intent, "payload": payload}, True)
        try:
            if service == "zenodo":
                method, endpoint = operation.split(" ", 1)
                response = self.api.zenodo(method, endpoint, payload, file, **(params or {}))
            elif service == "sheet": response = self.api.sheet(operation, params, payload)
            elif service == "public_json": response = self.api.public_json(params["id"], params["native"])
            elif service == "public_hash": response = self.api.public_hash(params["id"], params["name"])
            else: raise Stop("unsupported service")
            if getattr(self.api, "last_native", None) is not None:
                save(self.evidence / f"{i:04d}_native.json", self.api.last_native, True)
            save(self.evidence / f"{i:04d}_response.json", response, True)
            return response
        except Exception as exc:
            native = getattr(self.api, "last_native", None)
            if native is not None and not (self.evidence / f"{i:04d}_native.json").exists():
                save(self.evidence / f"{i:04d}_native.json", native, True)
            save(self.evidence / f"{i:04d}_error.json", {"kind": type(exc).__name__, "uncertain": write}, True)
            if write:
                self.state["phase"] = "unknown_write"; save(self.state_path, self.state)
            raise Stop("STOP: response failed/uncertain; GET-only reconcile, no write retry") from exc

    def load_spec(self, path):
        raw, _ = g.read_regular(public_path(path)); s = json.loads(raw); self.spec_bytes = raw
        g.fields(s, ["schema", "case", "asset_root", "assets", "metadata", "tracker"])
        need(s["schema"] == 1 and s["case"] == "pr411_6800014", "wrong case/schema")
        metadata = s["metadata"]
        required = {"title", "description", "upload_type", "publication_type", "publication_date", "creators", "access_right", "license"}
        need(isinstance(metadata, dict) and required <= set(metadata) <= METADATA_KEYS, "unsupported/incomplete metadata")
        need(metadata["upload_type"] == "publication" and metadata["publication_type"] == "preprint"
             and metadata["access_right"] == "open", "production preprint must be open")
        need(all(isinstance(metadata[k], str) and metadata[k] for k in required - {"creators"}), "metadata text invalid")
        need(isinstance(metadata["creators"], list) and metadata["creators"] and
             all(isinstance(c, dict) and c.get("name") for c in metadata["creators"]), "invalid creators")
        g.fields(s["tracker"], ["original_problem", "solution_chat", "notes"])
        need(all(isinstance(x, str) and x for x in s["tracker"].values()), "four complete tracker cells required")
        root = public_path(s["asset_root"])
        need(root.is_dir() and root.is_relative_to(CASE) and root != CASE, "asset root outside case")
        need(isinstance(s["assets"], list) and len(s["assets"]) == 3, "exactly three reviewed assets required")
        inventory = set()
        for parent, dirs, files in os.walk(root, followlinks=False):
            for name in dirs + files:
                p = public_path(Path(parent) / name)
                need(p.is_dir() or p.is_file() and not p.is_symlink(), "nonregular extra asset")
                if name in files: inventory.add(str(p))
        paths, names, content = set(), set(), {}
        for f in s["assets"]:
            g.fields(f, ["local_path", "name", "sha256", "md5", "size", "mode"])
            p = public_path(f["local_path"]); name = f["name"]
            need(p.is_relative_to(root) and str(p) not in paths and isinstance(name, str) and name not in names
                 and name not in ("", ".", "..") and not re.search(r"[/\\\x00]", name), "bad/duplicate asset path/name")
            data, mode = g.read_regular(p)
            need(0 < len(data) <= 128 * 1024**2 and len(data) == f["size"] and mode == f["mode"]
                 and sha(data) == f["sha256"] and hashlib.md5(data).hexdigest() == f["md5"], "asset pin mismatch")
            paths.add(str(p)); names.add(name); content[name] = data
        need(paths == inventory, "unlisted asset extras")
        return s, sha(raw), content

    def sheet_gate(self, row_range=None):
        p = {"spreadsheetId": SHEET, "fields": "spreadsheetId,sheets.properties"}
        meta = self.request("sheet", "get", p)
        need(meta.get("spreadsheetId") == SHEET, "spreadsheet identity drift")
        matches = [x["properties"] for x in meta["sheets"] if x["properties"].get("sheetId") == GID]
        need(len(matches) == 1 and matches[0].get("title") == TITLE, "target gid/title drift")
        ranges = [TAB + "A1:D1"] + ([row_range] if row_range else [])
        r = self.request("sheet", "batchGet", {"spreadsheetId": SHEET, "ranges": ranges,
                         "majorDimension": "ROWS", "valueRenderOption": "UNFORMATTED_VALUE"})
        need(r.get("spreadsheetId") == SHEET and len(r.get("valueRanges", [])) == len(ranges), "batchGet identity/count drift")
        for actual, requested in zip(r["valueRanges"], ranges):
            need(canonical_range(actual["range"]) == canonical_range(requested) and actual.get("majorDimension") == "ROWS",
                 "batchGet range/dimension drift")
        need(r["valueRanges"][0].get("values") == [HEADERS], "target header drift")
        return r["valueRanges"][1].get("values", []) if row_range else None

    def doi_rows(self, doi):
        r = self.request("sheet", "batchGet", {"spreadsheetId": SHEET, "ranges": [TAB + "C2:C"],
                         "majorDimension": "ROWS", "valueRenderOption": "UNFORMATTED_VALUE"})
        need(r.get("spreadsheetId") == SHEET and len(r.get("valueRanges", [])) == 1, "DOI column identity drift")
        v = r["valueRanges"][0]
        need(re.fullmatch(r"C2:C[2-9][0-9]*|C2:C1[0-9]+|C2:C", canonical_range(v["range"])) and v.get("majorDimension") == "ROWS",
             "DOI column range drift")
        rows = v.get("values", [])
        need(isinstance(rows, list) and all(isinstance(x, list) and len(x) <= 1 for x in rows), "malformed DOI column")
        return [i + 2 for i, x in enumerate(rows) if x and doi_key(x[0]) == doi_key(doi)]

    def legacy(self, deposit, s, record_id, complete=True):
        z.validate_record(deposit, record_id)
        actual = deposit.get("metadata", {})
        need(set(actual) - READ_ONLY_METADATA == set(s["metadata"]), "extra/missing submitted metadata")
        for value in (deposit.get("doi"), actual.get("doi")):
            need(value is None or doi_key(value) == f"10.5281/zenodo.{record_id}", "generated deposition DOI differs")
        reserved = actual.get("prereserve_doi")
        if reserved is not None:
            need(isinstance(reserved, dict) and doi_key(reserved.get("doi")) == f"10.5281/zenodo.{record_id}"
                 and str(reserved.get("recid")) == str(record_id), "reserved DOI/record ID differs")
        files = [{**f, "path": Path(f["local_path"])} for f in s["assets"]]
        if complete: return z.verify(deposit, s["metadata"], files)
        wanted = {f["name"]: f for f in files}; present = z.server_files(deposit)
        need(set(present) <= set(wanted), "unexpected partial draft assets")
        for name, f in present.items(): need(z.matching_file(f, wanted[name]), "partial draft asset differs")
        z.verify({**deposit, "files": []}, s["metadata"], [])

    def native(self, record_id, s, draft, expected=None):
        suffix = "/draft" if draft else ""
        n = self.request("zenodo", f"GET /api/records/{record_id}{suffix}",
                         {"accept": "application/vnd.inveniordm.v1+json"})
        need(str(n.get("id")) == str(record_id) and isinstance(n.get("metadata"), dict) and n["metadata"]
             and isinstance(n.get("access"), dict) and n.get("custom_fields") == {}, "native snapshot shape/ID/custom fields differ")
        access = n["access"]
        if "is_published" in n:
            need(type(n["is_published"]) is bool and n["is_published"] is (not draft), "native publication flag differs")
        pid = n.get("pids", {}).get("doi", {}).get("identifier")
        need(pid is None or doi_key(pid) == f"10.5281/zenodo.{record_id}", "native generated DOI differs")
        times = {}
        for key in ("created", "updated"):
            if key in n:
                need(isinstance(n[key], str), "native timestamp shape differs")
                times[key] = g.dt.datetime.fromisoformat(n[key].replace("Z", "+00:00"))
                need(times[key].tzinfo is not None, "native timestamp lacks timezone")
        need(len(times) < 2 or times["created"] <= times["updated"], "native timestamp chronology differs")
        need(access.get("record") == "public" and access.get("files") == "public"
             and access.get("embargo", {}).get("active", False) is False, "native access is not public")
        snapshot = {k: n[k] for k in ("metadata", "access", "custom_fields")}
        need(expected is None or snapshot == expected, "root-approved native metadata/access snapshot drift")
        files = n.get("files", {}).get("entries")
        if files is None:
            f = self.request("zenodo", f"GET /api/records/{record_id}{suffix}/files")
            files = f.get("entries")
        if isinstance(files, dict):
            files = [{"key": key, **value} for key, value in files.items()]
        need(isinstance(files, list), "native file snapshot unavailable")
        z.verify({"metadata": s["metadata"], "files": files}, s["metadata"], s["assets"])
        return snapshot, n

    def published(self, s, record_id, expected_native):
        deposit = self.request("zenodo", f"GET /api/deposit/depositions/{record_id}")
        self.legacy(deposit, s, record_id); need(deposit["submitted"] is True, "publication not confirmed")
        doi = doi_key(deposit.get("doi") or deposit["metadata"].get("doi"))
        need(doi == f"10.5281/zenodo.{record_id}", "specific production DOI differs")
        snapshot, native = self.native(record_id, s, False, expected_native)
        need(doi_key(native.get("pids", {}).get("doi", {}).get("identifier")) == doi, "native DOI differs")
        public = self.request("public_json", "GET", {"id": record_id, "native": False})
        need(str(public.get("id")) == str(record_id) and isinstance(public.get("metadata"), dict), "public identity/metadata differs")
        need({k: v for k, v in public["metadata"].items() if k not in READ_ONLY_METADATA} ==
             {k: v for k, v in deposit["metadata"].items() if k not in READ_ONLY_METADATA}, "public submitted metadata differs")
        need(doi_key(public.get("doi") or public["metadata"].get("doi")) == doi_key(doi), "public DOI differs")
        self.legacy({**public, "id": record_id, "submitted": True}, s, record_id)
        pn = self.request("public_json", "GET", {"id": record_id, "native": True})
        need(str(pn.get("id")) == str(record_id) and all(pn.get(k) == v for k, v in snapshot.items())
             and pn.get("pids") == native.get("pids"), "public native metadata differs")
        hashes = []
        for f in s["assets"]:
            actual = self.request("public_hash", "GET", {"id": record_id, "name": f["name"]})
            need(actual.get("http_status") == 200 and all(actual[k] == f[k] for k in ("sha256", "md5", "size")), "public asset byte hash differs")
            hashes.append({"name": f["name"], "sha256": actual["sha256"], "size": actual["size"]})
        return {"id": record_id, "doi": doi, "doi_url": "https://doi.org/" + doi,
                "record_url": f"https://zenodo.org/records/{record_id}", "asset_hashes": hashes}

    def read_state(self, approved):
        raw, _ = g.read_regular(self.state_path, private=True); state = json.loads(raw)
        need(state.get("spec_sha256") == approved and state.get("case") == "pr411_6800014"
             and state.get("dependencies") == {"guards": GUARDS_SHA, "zenodo": KIT_SHA}, "state/spec/dependency binding drift")
        need(sha(encoded(state["spec"])) == state["parsed_spec_sha256"], "state spec changed")
        original = base64.b64decode(state["spec_bytes_base64"], validate=True)
        need(sha(original) == approved and json.loads(original) == state["spec"], "approved raw spec differs from state")
        self.state = state
        return state

    def accepted_native(self, approved):
        j = self.state
        need(approved and approved == j.get("native_snapshot_sha256"), "root-approved native snapshot digest required")
        raw, _ = g.read_regular(private_path(j["native_snapshot_path"]), private=True)
        need(sha(raw) == approved and json.loads(raw) == j["native_staged"], "native snapshot bytes changed")
        return j["native_staged"]

    def stage(self, s, digest, content):
        need(not self.state_path.exists(), "case publication state exists; reconcile only")
        need(hasattr(self, "spec_bytes") and sha(self.spec_bytes) == digest and json.loads(self.spec_bytes) == s,
             "stage must use this engine's exact inspected spec bytes")
        need(set(content) == {f["name"] for f in s["assets"]} and all(
             sha(content[f["name"]]) == f["sha256"] and len(content[f["name"]]) == f["size"]
             and hashlib.md5(content[f["name"]]).hexdigest() == f["md5"] for f in s["assets"]), "staging bytes differ from approved pins")
        self.sheet_gate()
        self.state = {"case": "pr411_6800014", "spec": s, "spec_sha256": digest, "parsed_spec_sha256": sha(encoded(s)),
                      "spec_bytes_base64": base64.b64encode(self.spec_bytes).decode(),
                      "dependencies": {"guards": GUARDS_SHA, "zenodo": KIT_SHA}, "phase": "prepared", "intents": [], "id": None,
                      "evidence_kind": self.kind, "publish_intent": False, "append_intent": False}
        save(self.state_path, self.state, True)
        deposit = self.request("zenodo", "POST /api/deposit/depositions", payload={"metadata": s["metadata"]}, write=True)
        record_id = deposit.get("id"); need(type(record_id) is int and record_id > 0, "created ID unknown; reconcile account, no restage")
        self.state["id"] = record_id; save(self.state_path, self.state)
        z.validate_record(deposit, record_id); need(deposit["submitted"] is False and not z.server_files(deposit), "new draft state/files differ")
        bucket = deposit.get("links", {}).get("bucket")
        need(isinstance(bucket, str) and re.fullmatch(r"https://zenodo\.org/api/files/[0-9a-f-]+", bucket), "unexpected upload bucket")
        for f in s["assets"]:
            snapshot = self.evidence / ("asset_" + uuid.uuid4().hex)
            fd = os.open(snapshot, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
            with os.fdopen(fd, "wb") as stream:
                stream.write(content[f["name"]]); stream.flush(); os.fsync(stream.fileno())
            self.request("zenodo", "PUT " + bucket.removeprefix("https://zenodo.org") + "/" + quote(f["name"], safe=""), file=snapshot, write=True)
        self.request("zenodo", f"PUT /api/deposit/depositions/{record_id}", payload={"metadata": s["metadata"]}, write=True)
        final = self.request("zenodo", f"GET /api/deposit/depositions/{record_id}")
        self.legacy(final, s, record_id); need(final["submitted"] is False, "draft submitted unexpectedly")
        snapshot, _ = self.native(record_id, s, True)
        snapshot_path = self.evidence / "NATIVE_METADATA_ACCESS_SNAPSHOT.json"
        save(snapshot_path, snapshot, True)
        self.state.update(native_staged=snapshot, native_snapshot_path=str(snapshot_path), native_snapshot_sha256=sha(encoded(snapshot)),
                          phase="staged_pending_native_acceptance")
        save(self.state_path, self.state)
        return {"status": "staged_pending_native_acceptance", "id": record_id, "spec_sha256": digest,
                "native_snapshot_path": str(snapshot_path), "native_snapshot_sha256": self.state["native_snapshot_sha256"]}

    def publish(self, approved, confirm_id, native_approval):
        j = self.read_state(approved); record_id, s = j["id"], j["spec"]
        need(confirm_id == record_id and j["phase"] == "staged_pending_native_acceptance" and not j["publish_intent"], "publication phase/id differs; reconcile only")
        expected = self.accepted_native(native_approval)
        deposit = self.request("zenodo", f"GET /api/deposit/depositions/{record_id}")
        self.legacy(deposit, s, record_id); need(deposit["submitted"] is False, "already submitted; reconcile, no publish retry")
        self.native(record_id, s, True, expected)
        j["publish_intent"] = True; j["approved_native_sha256"] = native_approval; save(self.state_path, j)
        self.request("zenodo", f"POST /api/deposit/depositions/{record_id}/actions/publish", write=True)
        result = self.published(s, record_id, expected)
        j["phase"] = "published_verified"; j["publication"] = result; save(self.state_path, j)
        return {"status": "published_verified", **result}

    def tracker(self, approved, confirm_id, native_approval):
        j = self.read_state(approved); record_id, s = j["id"], j["spec"]
        need(type(record_id) is int and confirm_id == record_id and j["phase"] == "published_verified"
             and not j["append_intent"], "tracker verified-publication/ID/one-append guard; reconcile only")
        expected = self.accepted_native(native_approval)
        result = self.published(s, record_id, expected)
        row = [s["tracker"]["original_problem"], s["tracker"]["solution_chat"], result["doi_url"], s["tracker"]["notes"]]
        self.sheet_gate(); matches = self.doi_rows(result["doi"])
        need(len(matches) <= 1, "duplicate DOI rows; do not append")
        if matches:
            row_range = TAB + f"A{matches[0]}:D{matches[0]}"
            need(self.sheet_gate(row_range) == [row], "existing DOI row differs; do not append")
            return {"status": "tracker_already_exact", "tracker_range": row_range, **result}
        # Fresh header/identity/DOI-only absence check immediately before ONE
        # RAW INSERT_ROWS append. API lacks atomic dedup; final duplicate scan
        # detects a concurrent append but cannot prevent it or remove rows.
        self.sheet_gate(); need(not self.doi_rows(result["doi"]), "DOI appeared before append")
        j["append_intent"] = True; save(self.state_path, j)
        params = {"spreadsheetId": SHEET, "range": TAB + "A:D", "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS",
                  "includeValuesInResponse": True, "responseValueRenderOption": "UNFORMATTED_VALUE"}
        response = self.request("sheet", "append", params, {"majorDimension": "ROWS", "values": [row]}, write=True)
        updates = response.get("updates", {}); rr = updates.get("updatedRange")
        need(response.get("spreadsheetId") == SHEET and updates.get("spreadsheetId") == SHEET
             and (updates.get("updatedRows"), updates.get("updatedColumns"), updates.get("updatedCells")) == (1, 4, 4), "append identity/count mismatch")
        match = re.fullmatch(r"A([1-9][0-9]*):D\1", canonical_range(rr)); need(match and int(match[1]) >= 2, "returned row range invalid")
        j["append_range"] = rr; save(self.state_path, j)
        need(self.sheet_gate(rr) == [row], "exact returned row/header/values mismatch")
        need(self.doi_rows(result["doi"]) == [int(match[1])], "DOI duplication/drift after append")
        j["phase"] = "tracker_verified"; save(self.state_path, j)
        return {"status": "tracker_verified", "tracker_range": rr, **result}

    def reconcile(self, approved, recover_id=None, native_approval=None):
        j = self.read_state(approved); s = j["spec"]; record_id = j["id"]
        if record_id is None:
            need(type(recover_id) is int and recover_id > 0, "unknown created ID requires operator-supplied ID; no account search/restage")
            record_id = recover_id
        need(recover_id is None or recover_id == record_id, "recovery ID differs")
        d = self.request("zenodo", f"GET /api/deposit/depositions/{record_id}")
        z.validate_record(d, record_id)
        if not d["submitted"]:
            self.legacy(d, s, record_id, complete=False)
            return {"status": "draft_observed_publication_unconfirmed", "id": record_id, "read_only": True,
                    "note": "GET observations do not authorize stage/publish retries; partial draft may remain."}
        expected = self.accepted_native(native_approval)
        result = self.published(s, record_id, expected)
        self.sheet_gate(); rows = self.doi_rows(result["doi"])
        need(len(rows) <= 1, "duplicate DOI rows during reconcile")
        if rows:
            rr = TAB + f"A{rows[0]}:D{rows[0]}"
            wanted = [s["tracker"]["original_problem"], s["tracker"]["solution_chat"], result["doi_url"], s["tracker"]["notes"]]
            need(self.sheet_gate(rr) == [wanted], "DOI row values differ during reconcile")
            if j.get("append_range"):
                need(canonical_range(rr) == canonical_range(j["append_range"]), "row moved from returned append range")
            return {"status": "publication_and_tracker_observed_exact", "read_only": True,
                    "append_response_available": bool(j.get("append_range")), "tracker_range": rr, **result}
        return {"status": "publication_verified_tracker_absent_observed", "read_only": True,
                "note": "A stale GET cannot prove an unknown append did not occur; never append again automatically.", **result}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("inspect", "stage", "publish", "tracker", "reconcile"))
    p.add_argument("--spec"); p.add_argument("--approved-spec-sha256")
    p.add_argument("--approved-native-sha256")
    p.add_argument("--confirm-id", type=int); p.add_argument("--recover-id", type=int)
    a = p.parse_args()
    need(a.mode == "inspect" or a.approved_spec_sha256, "write/reconcile requires explicit exact spec digest")
    need(a.mode not in ("publish", "tracker") or a.confirm_id, "publish/tracker require exact ID confirmation")
    with mutation_lock() if a.mode in ("stage", "publish", "tracker") else nullcontext():
        e = Admin(Production(), PRIVATE / (g.dt.datetime.now(g.dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex))
        if a.mode in ("inspect", "stage"):
            need(a.spec, "inspect/stage require parent spec")
            s, digest, content = e.load_spec(a.spec)
            if a.mode == "inspect":
                e.sheet_gate()
                result = {"status": "read_only_spec_inspected", "spec_sha256": digest, "metadata_sha256": sha(encoded(s["metadata"])),
                          "assets": [{k: f[k] for k in ("name", "sha256", "size")} for f in s["assets"]]}
            else:
                need(digest == a.approved_spec_sha256, "approved spec differs")
                result = e.stage(s, digest, content)
        elif a.mode == "publish": result = e.publish(a.approved_spec_sha256, a.confirm_id, a.approved_native_sha256)
        elif a.mode == "tracker": result = e.tracker(a.approved_spec_sha256, a.confirm_id, a.approved_native_sha256)
        else: result = e.reconcile(a.approved_spec_sha256, a.recover_id, a.approved_native_sha256)
    result["evidence_kind"] = e.kind
    save(e.evidence / "RESULT.json", result, True)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try: main()
    except Exception as exc:
        # Never expose authentication, HTTP response bodies, or unrelated sheet
        # contents through exception text from the underlying clients.
        print("STOP: " + (str(exc) if isinstance(exc, Stop) else type(exc).__name__ + "; inspect private custody"), file=sys.stderr)
        sys.exit(2)
