#!/usr/bin/env python3
"""Small, dependency-free Zenodo draft and publication client."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / ".zenodo-state"
SECRETS = ROOT / ".secrets" / "zenodo.env"
BASES = {"production": "https://zenodo.org", "sandbox": "https://sandbox.zenodo.org"}
MAX_FILES = 100
MAX_BYTES = 50 * 1024**3
CHUNK = 1024 * 1024


class DepositError(Exception):
    pass


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DepositError(f"Cannot read JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DepositError(f"Expected a JSON object in {path}")
    return value


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def load_manifest(path: Path) -> tuple[dict, list[dict]]:
    manifest = read_json(path)
    if set(manifest) != {"metadata", "files"}:
        raise DepositError("Manifest must contain exactly 'metadata' and 'files'")
    metadata = manifest["metadata"]
    if not isinstance(metadata, dict):
        raise DepositError("metadata must be an object")
    required = ("title", "description", "upload_type", "creators")
    for key in required:
        if not metadata.get(key):
            raise DepositError(f"Missing metadata.{key}")
    if metadata["upload_type"] == "publication" and not metadata.get("publication_type"):
        raise DepositError("Publication metadata needs publication_type")
    if not isinstance(metadata["creators"], list) or any(
        not isinstance(c, dict) or not c.get("name") for c in metadata["creators"]
    ):
        raise DepositError("creators must be a nonempty list of named people")
    files = manifest["files"]
    if not isinstance(files, list) or not files or len(files) > MAX_FILES:
        raise DepositError(f"files must contain 1 to {MAX_FILES} entries")
    prepared = []
    names = set()
    for item in files:
        if not isinstance(item, dict) or set(item) - {"path", "name"} or not item.get("path"):
            raise DepositError("Each file needs path and optional name only")
        local = (path.parent / item["path"]).resolve()
        name = item.get("name", local.name)
        if not isinstance(name, str) or not name or name in {".", ".."} or "/" in name or "\\" in name:
            raise DepositError(f"Invalid Zenodo filename: {name!r}")
        if name in names:
            raise DepositError(f"Duplicate Zenodo filename: {name}")
        if not local.is_file():
            raise DepositError(f"Missing file: {local}")
        size = local.stat().st_size
        if size > MAX_BYTES:
            raise DepositError(f"File exceeds Zenodo's documented 50 GB limit: {local}")
        names.add(name)
        prepared.append({"path": local, "name": name, "size": size,
                         "md5": digest(local, "md5"), "sha256": digest(local, "sha256")})
    if sum(f["size"] for f in prepared) > MAX_BYTES:
        raise DepositError("Files exceed Zenodo's documented 50 GB record limit")
    return metadata, prepared


def state_path(manifest: Path, environment: str) -> Path:
    key = hashlib.sha256(str(manifest).encode()).hexdigest()[:24]
    return STATE_DIR / f"{key}-{environment}.json"


def save_state(path: Path, value: dict) -> None:
    path.parent.mkdir(mode=0o700, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".zenodo-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def token_for(environment: str) -> str:
    variable = "ZENODO_SANDBOX_TOKEN" if environment == "sandbox" else "ZENODO_TOKEN"
    token = os.environ.get(variable, "").strip()
    if token:
        if "\n" in token or "\r" in token:
            raise DepositError("Invalid token")
        return token
    if SECRETS.exists():
        if SECRETS.stat().st_mode & 0o077:
            raise DepositError(f"Private key file must have mode 600: {SECRETS}")
        for line in SECRETS.read_text(encoding="utf-8").splitlines():
            if line.startswith(variable + "="):
                token = line.partition("=")[2].strip().strip('"').strip("'")
                break
    if not token:
        raise DepositError(f"Set {variable} in the environment or {SECRETS}")
    if "\n" in token or "\r" in token:
        raise DepositError("Invalid token")
    return token


class ZenodoClient:
    def __init__(self, environment: str, token: str):
        self.base = BASES[environment]
        self.host = urlsplit(self.base).hostname
        self.token = token

    def request(self, method: str, url: str, payload: dict | None = None,
                file: Path | None = None) -> dict:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname != self.host or parsed.port not in (None, 443) or parsed.username:
            raise DepositError("Refusing an API URL outside the selected Zenodo environment")
        target = parsed.path + (("?" + parsed.query) if parsed.query else "")
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(data))
        elif file is not None:
            headers["Content-Type"] = "application/octet-stream"
            headers["Content-Length"] = str(file.stat().st_size)
        conn = http.client.HTTPSConnection(self.host, timeout=120)
        try:
            conn.putrequest(method, target)
            for key, value in headers.items():
                conn.putheader(key, value)
            conn.endheaders()
            if data is not None:
                conn.send(data)
            elif file is not None:
                with file.open("rb") as stream:
                    for block in iter(lambda: stream.read(CHUNK), b""):
                        conn.send(block)
            response = conn.getresponse()
            body = response.read(1024 * 1024)
            status = response.status
        except (OSError, http.client.HTTPException) as exc:
            raise DepositError(f"Zenodo connection failed: {str(exc).replace(self.token, '[redacted]')}") from exc
        finally:
            conn.close()
        try:
            result = json.loads(body) if body else {}
        except json.JSONDecodeError:
            result = {}
        if not 200 <= status < 300:
            detail = result.get("message", "Request failed") if isinstance(result, dict) else "Request failed"
            fields = result.get("errors", []) if isinstance(result, dict) else []
            raise DepositError(f"Zenodo HTTP {status}: {str(detail).replace(self.token, '[redacted]')} "
                               f"{str(fields).replace(self.token, '[redacted]')}")
        if not isinstance(result, dict):
            raise DepositError("Unexpected Zenodo response")
        return result

    def create(self, metadata: dict) -> dict:
        return self.request("POST", self.base + "/api/deposit/depositions", {"metadata": metadata})

    def get(self, deposit_id: int) -> dict:
        return self.request("GET", self.base + f"/api/deposit/depositions/{deposit_id}")

    def update(self, deposit_id: int, metadata: dict) -> dict:
        return self.request("PUT", self.base + f"/api/deposit/depositions/{deposit_id}", {"metadata": metadata})

    def upload(self, bucket: str, entry: dict) -> dict:
        return self.request("PUT", bucket.rstrip("/") + "/" + quote(entry["name"]), file=entry["path"])

    def publish(self, deposit_id: int) -> dict:
        return self.request("POST", self.base + f"/api/deposit/depositions/{deposit_id}/actions/publish")


def server_files(deposit: dict) -> dict:
    result = {}
    for item in deposit.get("files", []):
        name = item.get("filename") or item.get("key") or item.get("name")
        if not name or name in result:
            raise DepositError("Zenodo returned an invalid file list")
        result[name] = item
    return result


def matching_file(remote: dict, local: dict) -> bool:
    checksum = str(remote.get("checksum", "")).lower().removeprefix("md5:")
    size = remote.get("filesize", remote.get("size"))
    return checksum == local["md5"] and str(size) == str(local["size"])


def verify(deposit: dict, metadata: dict, files: list[dict]) -> None:
    remote_metadata = deposit.get("metadata", {})
    for key, value in metadata.items():
        if remote_metadata.get(key) != value:
            raise DepositError(f"Remote metadata differs at '{key}'; inspect the draft")
    remote_files = server_files(deposit)
    expected = {f["name"] for f in files}
    if set(remote_files) != expected:
        raise DepositError(f"Remote file list differs; expected {sorted(expected)}, found {sorted(remote_files)}")
    for entry in files:
        if not matching_file(remote_files[entry["name"]], entry):
            raise DepositError(f"Remote checksum/size differs for {entry['name']}")


def local_state(path: Path, environment: str) -> tuple[Path, dict | None]:
    place = state_path(path, environment)
    state = read_json(place) if place.exists() else None
    if state and (state.get("manifest") != str(path) or state.get("environment") != environment
                  or not isinstance(state.get("id"), int)):
        raise DepositError(f"Invalid local draft state: {place}")
    return place, state


def run(args: argparse.Namespace, client: ZenodoClient | None = None) -> dict:
    path = args.manifest.resolve()
    metadata, files = load_manifest(path)
    environment = "sandbox" if args.sandbox else "production"
    summary = {"environment": environment, "title": metadata["title"],
               "files": [{"name": f["name"], "size": f["size"], "sha256": f["sha256"]} for f in files]}
    if args.command == "check":
        return summary
    place, state = local_state(path, environment)
    if client is None:
        client = ZenodoClient(environment, token_for(environment))
    if args.command == "stage":
        if state:
            deposit = client.get(state["id"])
            if deposit.get("submitted"):
                raise DepositError("Local draft is already published")
        else:
            deposit = client.create(metadata)
            deposit_id = deposit.get("id")
            if not isinstance(deposit_id, int):
                raise DepositError("Zenodo did not return a deposition ID; inspect your account before retrying")
            state = {"manifest": str(path), "environment": environment, "id": deposit_id}
            save_state(place, state)
        deposit_id = state["id"]
        remote_files = server_files(deposit)
        expected = {f["name"] for f in files}
        extra = set(remote_files) - expected
        if extra:
            raise DepositError(f"Draft contains files absent from manifest: {sorted(extra)}")
        for entry in files:
            existing = remote_files.get(entry["name"])
            if existing:
                if not matching_file(existing, entry):
                    raise DepositError(f"Draft file differs: {entry['name']}. Resolve in Zenodo or use a new manifest.")
                continue
            bucket = deposit.get("links", {}).get("bucket")
            if not bucket:
                raise DepositError("Zenodo did not return a file bucket URL")
            client.upload(bucket, entry)
        client.update(deposit_id, metadata)
        deposit = client.get(deposit_id)
        verify(deposit, metadata, files)
        summary.update({"id": deposit_id, "draft_url": deposit.get("links", {}).get("html"), "state": "ready_to_publish"})
        return summary
    if not state:
        raise DepositError("No saved draft for this manifest/environment; run stage first")
    deposit = client.get(state["id"])
    if args.command == "inspect":
        verify(deposit, metadata, files)
        summary.update({"id": state["id"], "state": "published" if deposit.get("submitted") else "ready_to_publish",
                        "url": deposit.get("doi_url") or deposit.get("links", {}).get("html")})
        return summary
    if deposit.get("submitted"):
        raise DepositError("Deposit is already published")
    if args.confirm_id != state["id"]:
        raise DepositError(f"Publishing requires --confirm-id {state['id']}")
    verify(deposit, metadata, files)
    published = client.publish(state["id"])
    summary.update({"id": state["id"], "state": "published", "doi": published.get("doi"),
                    "url": published.get("doi_url") or published.get("links", {}).get("html")})
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "stage", "inspect", "publish"):
        sub = subcommands.add_parser(command)
        sub.add_argument("manifest", type=Path)
        sub.add_argument("--sandbox", action="store_true", help="Use sandbox.zenodo.org and its separate token")
        if command == "publish":
            sub.add_argument("--confirm-id", type=int, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args), indent=2))
    except DepositError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
